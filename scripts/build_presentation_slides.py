# -*- coding: utf-8 -*-
"""Generate the 15-slide dark-tech PPTX used for the graduation defense.

Regenerates reports/slides/NLP_ITviec_Sentiment_Slides.pptx from scratch —
palette matches src/app_theme.py, figures are pulled from reports/figures/,
and the metric numbers embedded in the slide text are the ones documented in
reports/modeling_hyperparameter_tuning.md and
reports/model_evaluation_error_analysis.md (update both places together if a
number changes).

Usage:
    pip install python-pptx pillow   # pillow is already a project dependency
    python scripts/build_presentation_slides.py

Requires reports/figures/*.png to already exist (see
reports/modeling_hyperparameter_tuning.md / notebooks for how they're built).
"""
import os
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR

REPO_ROOT = Path(__file__).resolve().parent.parent
FIG = str(REPO_ROOT / "reports" / "figures") + "/"
OUT_PATH = REPO_ROOT / "reports" / "slides" / "NLP_ITviec_Sentiment_Slides.pptx"

# ---- Coerce any float EMU lengths (from true division, e.g. w/2) to int ----
# python-pptx Length is an int subclass; `/` produces a plain float, which
# lxml then serializes as "123.0" -> invalid XML. Patch the shape-creation
# entry points so this class of bug can never leak into the saved file.
import pptx.shapes.shapetree as _st
def _coerce_lengths(fn):
    def wrapper(self, *args, **kwargs):
        args = tuple(int(round(a)) if isinstance(a, float) else a for a in args)
        kwargs = {k: (int(round(v)) if isinstance(v, float) else v) for k, v in kwargs.items()}
        return fn(self, *args, **kwargs)
    return wrapper
for _cls in (_st._BaseGroupShapes, _st.SlideShapes):
    for _m in ("add_shape", "add_textbox", "add_picture", "add_table", "add_connector"):
        if hasattr(_cls, _m):
            setattr(_cls, _m, _coerce_lengths(getattr(_cls, _m)))

# ---- Real font-metric text measurement -------------------------------------
# There's no PowerPoint/LibreOffice on the build machine to render a real
# preview, so a couple of overlap bugs only showed up once the user opened the
# file (title wrapped to more lines than expected; a stat value silently
# wrapped to 2 lines and ran into its label below). Measuring against the
# actual TTF glyph widths lets a long value auto-shrink to fit one line
# instead of guessing a size and hoping it's short enough.
from PIL import ImageFont
def _find_font(bold):
    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    return next((c for c in candidates if os.path.exists(c)), None)
_FONT_PATH = {False: _find_font(False), True: _find_font(True)}
_FONT_AVAILABLE = all(_FONT_PATH.values())
if not _FONT_AVAILABLE:
    print("WARNING: no usable TTF found for text-width measurement; "
          "stat-chip values will use their default size without the "
          "auto-shrink-to-fit safety net.")
_font_cache = {}
def _get_measure_font(size_pt, bold):
    key = (round(size_pt, 1), bold)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(_FONT_PATH[bool(bold)], max(1, int(round(size_pt * 4))))
    return _font_cache[key]
def text_width_in(text, size_pt, bold=False):
    if not _FONT_AVAILABLE:
        return 0.0
    f = _get_measure_font(size_pt, bold)
    return (f.getlength(text) / 4) / 72.0
def shrink_to_fit(text, avail_w_in, size_pt, bold=True, floor=13):
    """Return the largest font size <= size_pt (down to floor) at which text
    fits on one line within avail_w_in, so a stat value never silently wraps."""
    if not _FONT_AVAILABLE:
        return size_pt
    s = size_pt
    while s > floor and text_width_in(text, s, bold) > avail_w_in:
        s -= 1
    return s

# ---------- Palette (matches src/app_theme.py dark-tech theme) ----------
BG        = RGBColor(0x08, 0x0B, 0x10)
BG2       = RGBColor(0x0B, 0x10, 0x18)
CARD      = RGBColor(0x14, 0x1A, 0x24)
CARD2     = RGBColor(0x11, 0x16, 0x1F)
STROKE    = RGBColor(0x24, 0x2C, 0x3A)
TXT       = RGBColor(0xF1, 0xF5, 0xF9)
TXT_SUB   = RGBColor(0xA0, 0xAD, 0xBF)
TXT_DIM   = RGBColor(0x6B, 0x76, 0x88)
BLUE      = RGBColor(0x7A, 0xA7, 0xFF)
BLUE_D    = RGBColor(0x52, 0x7B, 0xD1)
GREEN     = RGBColor(0x50, 0xE3, 0xA4)   # positive
YELLOW    = RGBColor(0xF4, 0xD3, 0x5E)   # neutral
ORANGE    = RGBColor(0xFF, 0x99, 0x4F)
RED       = RGBColor(0xFF, 0x66, 0x77)   # negative
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)

FONT = "Segoe UI"
FONT_SB = "Segoe UI Semibold"

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
MARGIN = Inches(0.55)

prs = Presentation()
prs.slide_width = SLIDE_W
prs.slide_height = SLIDE_H
BLANK = prs.slide_layouts[6]

SLIDE_NO = {"n": 0}

# ---------------------------------------------------------------- helpers
def no_line(shape):
    shape.line.fill.background()

def no_shadow(shape):
    shape.shadow.inherit = False

def solid(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color

def set_radius(shape, r=0.08):
    try:
        shape.adjustments[0] = r
    except Exception:
        pass

def add_rect(slide, x, y, w, h, color, line=None, radius=None, shape_type=MSO_SHAPE.RECTANGLE):
    sp = slide.shapes.add_shape(shape_type, x, y, w, h)
    no_shadow(sp)
    if color is not None:
        solid(sp, color)
    else:
        sp.fill.background()
    if line is None:
        no_line(sp)
    else:
        sp.line.color.rgb = line
        sp.line.width = Pt(1)
    if radius is not None:
        set_radius(sp, radius)
    return sp

def add_text(slide, x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
             line_spacing=1.0, wrap=True, space_after=None):
    """runs: list of paragraphs; each paragraph is list of (text, size, color, bold, font) tuples."""
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        if space_after is not None:
            p.space_after = space_after
        for (text, size, color, bold, font) in para:
            r = p.add_run()
            r.text = text
            r.font.size = Pt(size)
            r.font.color.rgb = color
            r.font.bold = bold
            r.font.name = font
    return tb

def simple_text(slide, x, y, w, h, text, size, color, bold=False, align=PP_ALIGN.LEFT,
                 anchor=MSO_ANCHOR.TOP, font=FONT, line_spacing=1.0, wrap=True):
    return add_text(slide, x, y, w, h, [[(text, size, color, bold, font)]],
                     align=align, anchor=anchor, line_spacing=line_spacing, wrap=wrap)

def base_slide(kicker, title, page_note=""):
    """Standard dark slide with header bar + footer. Returns (slide, content_top)."""
    slide = prs.slides.add_slide(BLANK)
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, BG)
    # subtle top accent line
    add_rect(slide, 0, 0, SLIDE_W, Pt(3), BLUE)
    # brand mark (mini speech-bubble logo) top-right
    brand_mark(slide, SLIDE_W - Inches(0.85), Inches(0.28))
    # kicker
    simple_text(slide, MARGIN, Inches(0.42), Inches(9), Inches(0.32), kicker.upper(),
                11, BLUE, bold=True)
    # title
    simple_text(slide, MARGIN, Inches(0.72), Inches(11.6), Inches(0.7), title,
                27, TXT, bold=True)
    # divider
    add_rect(slide, MARGIN, Inches(1.42), Inches(0.55), Pt(3.2), GREEN)
    # footer
    SLIDE_NO["n"] += 1
    simple_text(slide, MARGIN, SLIDE_H - Inches(0.42), Inches(7), Inches(0.3),
                "Phân tích Cảm xúc Đánh giá ITviec  ·  Nhóm 4", 9.5, TXT_DIM)
    simple_text(slide, SLIDE_W - Inches(1.4), SLIDE_H - Inches(0.42), Inches(0.85), Inches(0.3),
                f"{SLIDE_NO['n']:02d} / 15", 9.5, TXT_DIM, align=PP_ALIGN.RIGHT)
    return slide, Inches(1.65)

def brand_mark(slide, x, y, s=0.4):
    size = Inches(s)
    box = add_rect(slide, x, y, size, size, CARD, line=RGBColor(0x2A,0x33,0x44), radius=0.32)
    # speech bubble path approximated with rounded rect + tail dot
    bub = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Emu(int(size*0.22)), y + Emu(int(size*0.22)),
                                  Emu(int(size*0.56)), Emu(int(size*0.4)))
    no_shadow(bub); bub.fill.background()
    bub.line.color.rgb = BLUE; bub.line.width = Pt(1.1)
    set_radius(bub, 0.45)
    for i, c in enumerate([GREEN, BLUE, YELLOW]):
        d = Emu(int(size*0.075))
        dx = x + Emu(int(size*0.34)) + Emu(int(size*0.16))*i
        dy = y + Emu(int(size*0.38))
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, dx, dy, d, d)
        no_shadow(dot); solid(dot, c); no_line(dot)

def bullet_list(slide, x, y, w, items, size=14.5, gap=0.14, color=TXT, dot_color=BLUE,
                 bold_lead=False, line_h=None):
    """items: list of strings OR (lead, rest) tuples for bold-lead bullets."""
    cy = y
    for it in items:
        row_h = line_h or Inches(0.5)
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, x, cy + Inches(0.075), Inches(0.09), Inches(0.09))
        no_shadow(dot); solid(dot, dot_color); no_line(dot)
        if isinstance(it, tuple):
            lead, rest = it
            add_text(slide, x + Inches(0.24), cy, w - Inches(0.24), row_h,
                      [[(lead, size, TXT, True, FONT), (rest, size, color, False, FONT)]],
                      line_spacing=1.08)
        else:
            add_text(slide, x + Inches(0.24), cy, w - Inches(0.24), row_h,
                      [[(it, size, color, False, FONT)]], line_spacing=1.08)
        # estimate advance (rough char-based wrap heuristic)
        text_len = len(it if isinstance(it, str) else it[0] + it[1])
        chars_per_line = max(1, int((w - Inches(0.24)) / Inches(0.082)))
        lines = max(1, -(-text_len // chars_per_line))
        cy += Inches(0.30) * lines + Inches(gap)
    return cy

def stat_chip(slide, x, y, w, h, value, label, value_color=GREEN, value_size=None, label_size=None):
    """Fixed (not proportional) vertical rhythm so the label text can never be
    clipped by the value line above it, regardless of chip height. The value
    font auto-shrinks so it never silently wraps to a 2nd line."""
    card = add_rect(slide, x, y, w, h, CARD, line=STROKE, radius=0.12)
    h_in = h / Inches(1)
    if value_size is None:
        value_size = 24 if h_in >= 0.95 else (20 if h_in >= 0.7 else 17)
    if label_size is None:
        label_size = 10.5 if h_in >= 0.95 else 9
    pad = Inches(0.15)
    avail_w_in = (w - 2*pad) / Inches(1)
    value_size = shrink_to_fit(value, avail_w_in, value_size, bold=True, floor=13)
    value_line_h = Inches(value_size * 1.25 / 72)
    add_text(slide, x + pad, y + Inches(0.08), w - 2*pad, value_line_h,
             [[(value, value_size, value_color, True, FONT)]], align=PP_ALIGN.LEFT, wrap=False)
    label_top = y + Inches(0.08) + value_line_h + Inches(0.04)
    label_lines = label.split("\n")
    add_text(slide, x + pad, label_top, w - 2*pad, max(h - (label_top - y) - Inches(0.06), Inches(0.15)),
             [[(ln, label_size, TXT_SUB, False, FONT)] for ln in label_lines],
             align=PP_ALIGN.LEFT, line_spacing=1.05)
    return card

def img_card(slide, path, x, y, w, h, caption=None, pad=0.14):
    from PIL import Image
    card = add_rect(slide, x, y, w, h, RGBColor(0xFF,0xFF,0xFF), line=STROKE, radius=0.05)
    iw, ih = Image.open(path).size
    ar = iw/ih
    avail_w = w - Inches(pad*2)
    avail_h = h - Inches(pad*2) - (Inches(0.3) if caption else 0)
    box_ar = avail_w/avail_h
    if ar > box_ar:
        pic_w = avail_w; pic_h = Emu(int(pic_w/ar))
    else:
        pic_h = avail_h; pic_w = Emu(int(pic_h*ar))
    px = x + (w - pic_w)/2
    py = y + Inches(pad) + (avail_h - pic_h)/2
    slide.shapes.add_picture(path, px, py, width=pic_w, height=pic_h)
    if caption:
        simple_text(slide, x + Inches(pad), y + h - Inches(0.32), w - Inches(pad*2), Inches(0.28),
                    caption, 10.5, RGBColor(0x33,0x3A,0x44), align=PP_ALIGN.CENTER)
    return card

def pipeline_box(slide, x, y, w, h, label, sub, color=BLUE):
    card = add_rect(slide, x, y, w, h, CARD, line=STROKE, radius=0.14)
    add_rect(slide, x, y, Inches(0.06), h, color, radius=0)
    simple_text(slide, x + Inches(0.16), y + Inches(0.1), w - Inches(0.28), h*0.5,
                label, 12.5, TXT, bold=True, line_spacing=1.0)
    simple_text(slide, x + Inches(0.16), y + h*0.52, w - Inches(0.28), h*0.46,
                sub, 9.5, TXT_SUB, line_spacing=1.05)
    return card

def arrow_between(slide, x, y, w, h, color=TXT_DIM):
    ar = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, x, y, w, h)
    no_shadow(ar); solid(ar, color); no_line(ar)
    try:
        ar.adjustments[0] = 0.6
        ar.adjustments[1] = 0.55
    except Exception:
        pass
    return ar

def section_card(slide, x, y, w, h, title, color=BLUE):
    card = add_rect(slide, x, y, w, h, CARD, line=STROKE, radius=0.06)
    add_rect(slide, x, y, w, Inches(0.05), color)
    simple_text(slide, x + Inches(0.2), y + Inches(0.16), w - Inches(0.4), Inches(0.35),
                title, 13.5, TXT, bold=True)
    return card

def style_table(table, header_bg=CARD2, header_fg=TXT, body_fg=TXT_SUB, font_size=11,
                 highlight_rows=None, zebra=True):
    highlight_rows = highlight_rows or {}
    n_rows = len(table.rows)
    n_cols = len(table.columns)
    for r in range(n_rows):
        for c in range(n_cols):
            cell = table.cell(r, c)
            cell.margin_left = Inches(0.08)
            cell.margin_right = Inches(0.08)
            cell.margin_top = Inches(0.04)
            cell.margin_bottom = Inches(0.04)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            for p in tf.paragraphs:
                p.alignment = PP_ALIGN.LEFT if c == 0 else PP_ALIGN.CENTER
                for run in p.runs:
                    run.font.size = Pt(font_size)
                    run.font.name = FONT
            if r == 0:
                cell.fill.solid(); cell.fill.fore_color.rgb = header_bg
                for p in tf.paragraphs:
                    for run in p.runs:
                        run.font.bold = True
                        run.font.color.rgb = header_fg
            else:
                bg = highlight_rows.get(r)
                if bg:
                    cell.fill.solid(); cell.fill.fore_color.rgb = bg
                else:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = CARD if (zebra and r % 2 == 0) else BG2
                for p in tf.paragraphs:
                    for run in p.runs:
                        run.font.color.rgb = body_fg if r not in highlight_rows else TXT
                        if r in highlight_rows:
                            run.font.bold = True

def set_cell(table, r, c, text, size=11):
    cell = table.cell(r, c)
    cell.text = text
    for p in cell.text_frame.paragraphs:
        for run in p.runs:
            run.font.size = Pt(size)
            run.font.name = FONT

print("helpers ready")

# =====================================================================
# SLIDE 1 — TRANG BÌA
# =====================================================================
s1 = prs.slides.add_slide(BLANK)
add_rect(s1, 0, 0, SLIDE_W, SLIDE_H, BG)
add_rect(s1, 0, 0, SLIDE_W, SLIDE_H, BG2)  # base
# decorative dot grid (top-right)
import random
random.seed(7)
for i in range(60):
    gx = Inches(9.6) + Inches(random.uniform(0, 3.4))
    gy = Inches(0.3) + Inches(random.uniform(0, 3.6))
    dsize = Inches(0.018 + random.uniform(0, 0.02))
    dot = s1.shapes.add_shape(MSO_SHAPE.OVAL, gx, gy, dsize, dsize)
    no_shadow(dot); no_line(dot)
    dot.fill.solid(); dot.fill.fore_color.rgb = BLUE_D
    dot.fill.fore_color.brightness = 0
# accent glow bar
add_rect(s1, 0, Inches(6.55), SLIDE_W, Pt(3), BLUE)
add_rect(s1, MARGIN, Inches(1.42), Inches(0.7), Pt(4), GREEN)

brand_mark(s1, MARGIN, Inches(0.55), s=0.5)
simple_text(s1, MARGIN + Inches(0.62), Inches(0.6), Inches(6), Inches(0.4),
            "SENTIMENT LAB  ·  NLP CAPSTONE 2026", 12, TXT_SUB, bold=True)

simple_text(s1, MARGIN, Inches(1.6), Inches(11.8), Inches(0.4),
            "ĐỒ ÁN TỐT NGHIỆP — MÔN XỬ LÝ NGÔN NGỮ TỰ NHIÊN", 14, BLUE, bold=True)
add_text(s1, MARGIN, Inches(2.05), Inches(12.2), Inches(1.35),
         [[("PHÂN TÍCH CẢM XÚC ĐÁNH GIÁ NHÂN VIÊN", 33, TXT, True, FONT)],
          [("NGÀNH CÔNG NGHỆ THÔNG TIN TRÊN ITVIEC", 33, TXT, True, FONT)]],
         line_spacing=1.12, space_after=Pt(2))
simple_text(s1, MARGIN, Inches(3.5), Inches(11.5), Inches(0.4),
            "Machine Learning truyền thống · Stacking Ensemble · Deep Learning ViSoBERT · Explainable AI",
            14, TXT_SUB)

# info cards row
info_y = Inches(4.15)
card_w = Inches(3.85); card_h = Inches(1.55); gap = Inches(0.22)
gv_card = add_rect(s1, MARGIN, info_y, Inches(7.92), card_h, CARD, line=STROKE, radius=0.1)
simple_text(s1, MARGIN+Inches(0.25), info_y+Inches(0.16), Inches(3.4), Inches(0.3), "GIẢNG VIÊN HƯỚNG DẪN", 10.5, BLUE, bold=True)
simple_text(s1, MARGIN+Inches(0.25), info_y+Inches(0.52), Inches(3.4), Inches(0.5), "Thầy Đặng Văn Thìn", 18, TXT, bold=True)
simple_text(s1, MARGIN+Inches(0.25), info_y+Inches(0.98), Inches(3.4), Inches(0.4), "Khoa Công nghệ Thông tin", 11, TXT_SUB)

simple_text(s1, MARGIN+Inches(4.1), info_y+Inches(0.16), Inches(3.6), Inches(0.3), "NHÓM THỰC HIỆN — NHÓM 4", 10.5, GREEN, bold=True)
members = ["Hoàng Hôn  ·  Trưởng nhóm / Tech Lead", "Văn Duy  ·  Data & Research Specialist",
           "Duy Khang  ·  Machine Learning Specialist", "Thành Trung  ·  UI/UX & Deployment Specialist"]
my = info_y+Inches(0.52)
for m in members:
    simple_text(s1, MARGIN+Inches(4.1), my, Inches(3.7), Inches(0.26), m, 10.8, TXT_SUB)
    my += Inches(0.245)

stat_chip(s1, Inches(9.15), info_y, Inches(1.55), card_h/2 - Inches(0.05), "8.417", "review", BLUE)
stat_chip(s1, Inches(10.85), info_y, Inches(1.55), card_h/2 - Inches(0.05), "7", "mô hình", GREEN)
stat_chip(s1, Inches(9.15), info_y+card_h/2+Inches(0.1), Inches(1.55), card_h/2 - Inches(0.05), "0.5619", "CV Macro F1", YELLOW)
stat_chip(s1, Inches(10.85), info_y+card_h/2+Inches(0.1), Inches(1.55), card_h/2 - Inches(0.05), "43/43", "unit test", ORANGE)

# =====================================================================
# SLIDE 2 — ĐẶT VẤN ĐỀ & THÁCH THỨC DỮ LIỆU
# =====================================================================
s2, top = base_slide("Chương 1 · Đặt vấn đề", "Bối cảnh & Thách thức dữ liệu đánh giá ITviec")

section_card(s2, MARGIN, top, Inches(6.1), Inches(4.75), "Bối cảnh & Mục tiêu nghiên cứu", BLUE)
bullet_list(s2, MARGIN+Inches(0.25), top+Inches(0.65), Inches(5.6), [
    ("Review ứng viên/nhân viên trên ITviec ", "là nguồn tín hiệu quan trọng phản ánh văn hoá, đãi ngộ và môi trường làm việc thực tế của doanh nghiệp IT."),
    ("Mục tiêu: ", "tự động phân loại cảm xúc 3 lớp (Tích cực / Trung tính / Tiêu cực) từ văn bản đánh giá tiếng Việt."),
    ("So sánh có hệ thống ", "giữa ML cổ điển, Stacking Ensemble và Deep Learning Transformer (ViSoBERT)."),
    ("Khai thác insight ", "theo từng doanh nghiệp để hỗ trợ phòng Nhân sự & Ban quản lý ra quyết định."),
], size=13.5, gap=0.2, line_h=Inches(0.62))

section_card(s2, Inches(6.85), top, Inches(5.9), Inches(4.75), "4 Thách thức kỹ thuật cốt lõi", RED)
challenges = [
    ("Mất cân bằng nghiêm trọng 11:1", "73.8% Tích cực vs 6.8% Tiêu cực — mô hình dễ \"lười\" đoán về lớp đa số.", RED),
    ("Teencode & thuật ngữ IT Anh-Việt", "\"ko\", \"cty\", \"OT\", \"leader\", \"benefit\" xen lẫn trong cùng một câu.", ORANGE),
    ("Khen/chê đan xen trong 1 review", "Một đoạn văn vừa khen môi trường vừa chê lương — dễ gây nhiễu nhãn.", YELLOW),
    ("Câu phủ định phức tạp", "\"không được thân thiện\", \"ít cơ hội học hỏi\" — phủ định đảo cực tính từ vựng.", BLUE),
]
cy = top + Inches(0.62)
ch_h = Inches(0.92)
for label, desc, c in challenges:
    add_rect(s2, Inches(6.85)+Inches(0.22), cy, Inches(0.08), ch_h-Inches(0.14), c)
    simple_text(s2, Inches(6.85)+Inches(0.42), cy, Inches(5.2), Inches(0.32), label, 13, TXT, bold=True)
    simple_text(s2, Inches(6.85)+Inches(0.42), cy+Inches(0.34), Inches(5.2), Inches(0.5), desc, 11, TXT_SUB, line_spacing=1.05)
    cy += ch_h

# =====================================================================
# SLIDE 3 — SƠ ĐỒ KIẾN TRÚC TỔNG THỂ (END-TO-END PIPELINE)
# =====================================================================
s3, top = base_slide("Kiến trúc hệ thống", "Sơ đồ pipeline tổng thể End-to-End")

stages = [
    ("1. Thu thập dữ liệu", "8.417 review ITviec đa công ty, kèm rating & khía cạnh", BLUE),
    ("2. Tiền xử lý 2 tầng", "Chuẩn hoá, Negation Scope, tách từ tiếng Việt", GREEN),
    ("3. Trích xuất đặc trưng", "TF-IDF 5.000 chiều + Lexicon cảm xúc", YELLOW),
    ("4. Mô hình hoá ML/DL", "4 baseline · Stacking Ensemble · ViSoBERT", ORANGE),
    ("5. Hybrid Decision Gate", "Kết hợp xác suất ML + tri thức từ điển miền", RED),
    ("6. Web App & XAI", "Streamlit demo, dự đoán realtime, giải thích", BLUE),
]
n = len(stages)
box_w = Inches(1.72); box_h = Inches(1.85)
arrow_w = Inches(0.42)
total_w = n*box_w + (n-1)*arrow_w
start_x = MARGIN + (Inches(12.23) - total_w)/2
by = top + Inches(1.3)
x = start_x
for i, (label, sub, c) in enumerate(stages):
    pipeline_box(s3, x, by, box_w, box_h, label, sub, c)
    x += box_w
    if i < n-1:
        arrow_between(s3, x, by + box_h/2 - Inches(0.14), arrow_w, Inches(0.28))
        x += arrow_w

simple_text(s3, MARGIN, top+Inches(0.05), Inches(12.2), Inches(0.5),
            "Toàn bộ pipeline được đóng gói dạng module tái sử dụng, kiểm chứng bằng 43/43 unit test — bảo đảm nhất quán giữa notebook nghiên cứu và ứng dụng Web.",
            13, TXT_SUB, line_spacing=1.1)

feat_y = by + box_h + Inches(0.45)
feats = [("Tách biệt Train/CV/Final-Test", "Final test chỉ mở khoá đúng 1 lần, chống rò rỉ dữ liệu."),
         ("2 pipeline tiền xử lý song song", "clean_advance_text (ML) vs clean_text_for_transformer (DL)."),
         ("Song song 2 mô hình trên UI", "Radio chọn Text-only (5.000) hoặc Text+Lexicon (5.005) chiều.")]
fw = Inches(3.95)
for i, (t, d) in enumerate(feats):
    fx = MARGIN + i*(fw+Inches(0.19))
    card = add_rect(s3, fx, feat_y, fw, Inches(1.05), CARD, line=STROKE, radius=0.12)
    simple_text(s3, fx+Inches(0.18), feat_y+Inches(0.12), fw-Inches(0.36), Inches(0.32), t, 12.5, GREEN, bold=True)
    simple_text(s3, fx+Inches(0.18), feat_y+Inches(0.46), fw-Inches(0.36), Inches(0.5), d, 10.5, TXT_SUB, line_spacing=1.05)

print("slides 1-3 done")

# =====================================================================
# SLIDE 4 — TIỀN XỬ LÝ CHUYÊN SÂU & NEGATION SCOPE
# =====================================================================
s4, top = base_slide("Chương 2 · Tiền xử lý dữ liệu", "Pipeline tiền xử lý 2 tầng & Negation Scope Detection")

section_card(s4, MARGIN, top, Inches(6.0), Inches(4.75), "Hai pipeline tiền xử lý độc lập", BLUE)
steps_ml = ["Chuẩn hoá Unicode NFC", "Emoji → từ ngữ sắc thái", "Chuẩn hoá teencode & thuật ngữ IT",
            "Tách từ (underthesea) + Greedy Matching 99.75%", "Loại stopword (giữ từ phủ định: chưa, thiếu, ít)"]
mly = top+Inches(0.62)
simple_text(s4, MARGIN+Inches(0.22), mly, Inches(5.5), Inches(0.3), "clean_advance_text()  →  dùng cho ML cổ điển", 12, GREEN, bold=True)
mly += Inches(0.36)
for st in steps_ml:
    dot = s4.shapes.add_shape(MSO_SHAPE.OVAL, MARGIN+Inches(0.24), mly+Inches(0.06), Inches(0.07), Inches(0.07))
    no_shadow(dot); solid(dot, GREEN); no_line(dot)
    simple_text(s4, MARGIN+Inches(0.42), mly, Inches(5.3), Inches(0.3), st, 11.5, TXT_SUB)
    mly += Inches(0.34)

mly += Inches(0.18)
add_rect(s4, MARGIN+Inches(0.22), mly, Inches(5.55), Pt(1), STROKE)
mly += Inches(0.18)
simple_text(s4, MARGIN+Inches(0.22), mly, Inches(5.5), Inches(0.3), "clean_text_for_transformer()  →  dùng cho ViSoBERT", 12, BLUE, bold=True)
mly += Inches(0.36)
for st in ["Chỉ chuẩn hoá Unicode & khoảng trắng", "Giữ nguyên cấu trúc câu, dấu câu, ngữ cảnh",
           "Không tách từ / không lọc stopword — để tokenizer BPE tự xử lý"]:
    dot = s4.shapes.add_shape(MSO_SHAPE.OVAL, MARGIN+Inches(0.24), mly+Inches(0.06), Inches(0.07), Inches(0.07))
    no_shadow(dot); solid(dot, BLUE); no_line(dot)
    simple_text(s4, MARGIN+Inches(0.42), mly, Inches(5.3), Inches(0.3), st, 11.5, TXT_SUB)
    mly += Inches(0.34)

section_card(s4, Inches(6.75), top, Inches(6.0), Inches(4.75), "Negation Scope Detection", RED)
ny = top+Inches(0.62)
simple_text(s4, Inches(6.75)+Inches(0.22), ny, Inches(5.55), Inches(0.55),
            "Thuật toán quét cửa sổ phủ định (không, chưa, chẳng...) và đảo cực tính các từ cảm xúc nằm trong phạm vi ảnh hưởng.",
            12, TXT_SUB, line_spacing=1.15)
ny += Inches(0.75)
ex_card = add_rect(s4, Inches(6.75)+Inches(0.22), ny, Inches(5.55), Inches(1.55), CARD2, line=STROKE, radius=0.1)
simple_text(s4, Inches(6.75)+Inches(0.42), ny+Inches(0.14), Inches(5.15), Inches(0.3), "VÍ DỤ THỰC TẾ", 9.5, TXT_DIM, bold=True)
add_text(s4, Inches(6.75)+Inches(0.42), ny+Inches(0.44), Inches(5.15), Inches(0.5),
         [[("“... môi trường làm việc ", 13, TXT_SUB, False, FONT),
           ("không được ", 13, RED, True, FONT),
           ("thân thiện ...”", 13, TXT_SUB, False, FONT)]])
add_text(s4, Inches(6.75)+Inches(0.42), ny+Inches(0.92), Inches(5.15), Inches(0.5),
         [[("“thân thiện” (tích cực)  ", 12, TXT_SUB, False, FONT),
           ("→ trong cửa sổ phủ định →  ", 12, TXT_DIM, False, FONT),
           ("cực tính đảo ngược (tiêu cực)", 12, RED, True, FONT)]])
ny += Inches(1.75)
for label, val, c in [("Không có Negation Scope", "Nhận diện sai → gán nhãn Tích cực/Trung tính", ORANGE),
                       ("Có Negation Scope + Hybrid Gate", "Nhận diện đúng → Tiêu cực (71.1%)", GREEN)]:
    add_rect(s4, Inches(6.75)+Inches(0.22), ny, Inches(0.08), Inches(0.5), c)
    simple_text(s4, Inches(6.75)+Inches(0.42), ny, Inches(5.2), Inches(0.28), label, 11.5, TXT, bold=True)
    simple_text(s4, Inches(6.75)+Inches(0.42), ny+Inches(0.27), Inches(5.2), Inches(0.26), val, 10.5, TXT_SUB)
    ny += Inches(0.62)

# =====================================================================
# SLIDE 5 — EDA
# =====================================================================
s5, top = base_slide("Chương 2 · Khám phá dữ liệu", "EDA — 8.417 review ITviec")

cap_w = Inches(3.95)
img_card(s5, FIG+"eda_sentiment_counts.png", MARGIN, top, cap_w, Inches(4.75),
         caption="Phân bố nhãn: 73.8% Tích cực · 19.5% Trung tính · 6.8% Tiêu cực")
img_card(s5, FIG+"eda_text_length_distribution.png", MARGIN+cap_w+Inches(0.18), top, cap_w, Inches(4.75),
         caption="Phân bố độ dài văn bản đánh giá theo nhãn cảm xúc")
img_card(s5, FIG+"eda_aspect_correlation.png", MARGIN+2*(cap_w+Inches(0.18)), top, cap_w, Inches(4.75),
         caption="Tương quan giữa các khía cạnh đánh giá (Lương, Đào tạo, Quản lý...)")

print("slides 4-5 done")

# =====================================================================
# SLIDE 6 — ABLATION STUDY
# =====================================================================
s6, top = base_slide("Chương 3 · Thí nghiệm đối chứng", "Feature Ablation Study — Text vs. Text + Lexicon")

img_card(s6, FIG+"eda_feature_ablation_cv.png", MARGIN, top, Inches(7.1), Inches(4.75),
         caption="So sánh 5-fold Stratified CV Macro F1 giữa các nhóm đặc trưng")

rx = MARGIN+Inches(7.3)
rw = Inches(5.0)
stat_chip(s6, rx, top, rw/2-Inches(0.09), Inches(1.15), "0.5579 → 0.5664", "CV Macro F1\nText-only → Text+Lexicon", GREEN)
stat_chip(s6, rx+rw/2+Inches(0.09), top, rw/2-Inches(0.09), Inches(1.15), "45.6% → 48.0%", "Recall lớp Tiêu cực", ORANGE)

note = add_rect(s6, rx, top+Inches(1.35), rw, Inches(1.85), CARD, line=STROKE, radius=0.08)
simple_text(s6, rx+Inches(0.2), top+Inches(1.5), rw-Inches(0.4), Inches(0.3), "5.005 CHIỀU ĐẶC TRƯNG", 10.5, BLUE, bold=True)
simple_text(s6, rx+Inches(0.2), top+Inches(1.82), rw-Inches(0.4), Inches(1.3),
            "TF-IDF (5.000 chiều n-gram 1-2) song song với 5 đặc trưng Lexicon cảm xúc domain IT, chuẩn hoá MinMaxScaler — cải thiện ổn định trên cả Macro F1 và Recall lớp thiểu số.",
            11.5, TXT_SUB, line_spacing=1.2)

warn = add_rect(s6, rx, top+Inches(3.35), rw, Inches(1.4), CARD2, line=RED, radius=0.08)
simple_text(s6, rx+Inches(0.2), top+Inches(3.5), rw-Inches(0.4), Inches(0.3), "⚠ VÌ SAO LOẠI BỎ ASPECT RATINGS?", 10.8, RED, bold=True)
simple_text(s6, rx+Inches(0.2), top+Inches(3.82), rw-Inches(0.4), Inches(0.9),
            "Dù Text+Aspect đạt Macro F1 0.7369, đặc trưng này gần trùng nhãn mục tiêu → rủi ro Data Shortcut, không phản ánh khả năng hiểu ngôn ngữ thật của mô hình.",
            10.8, TXT_SUB, line_spacing=1.15)

# =====================================================================
# SLIDE 7 — 4 MÔ HÌNH ML CƠ SỞ & STACKING ENSEMBLE
# =====================================================================
s7, top = base_slide("Chương 3 · Mô hình hoá", "4 Mô hình ML cơ sở & Kỹ thuật Stacking Ensemble")

section_card(s7, MARGIN, top, Inches(5.6), Inches(4.75), "4 mô hình nền tảng (class_weight='balanced')", BLUE)
models4 = [("Logistic Regression", "0.5567", BLUE),
           ("Linear SVM (Platt scaling)", "0.5561", GREEN),
           ("Random Forest", "0.5515", YELLOW),
           ("Multinomial Naive Bayes", "0.4890", ORANGE)]
my = top+Inches(0.68)
for name, f1, c in models4:
    add_rect(s7, MARGIN+Inches(0.22), my, Inches(5.16), Inches(0.78), CARD2, line=STROKE, radius=0.14)
    add_rect(s7, MARGIN+Inches(0.22), my, Inches(0.07), Inches(0.78), c)
    simple_text(s7, MARGIN+Inches(0.45), my+Inches(0.12), Inches(3.3), Inches(0.3), name, 13, TXT, bold=True)
    simple_text(s7, MARGIN+Inches(0.45), my+Inches(0.44), Inches(3.3), Inches(0.28), "CV Macro F1 (GridSearchCV, 5-fold)", 9.5, TXT_SUB)
    simple_text(s7, MARGIN+Inches(3.7), my+Inches(0.12), Inches(1.55), Inches(0.55), f1, 20, c, bold=True, align=PP_ALIGN.RIGHT)
    my += Inches(0.94)

section_card(s7, Inches(6.9), top, Inches(5.85), Inches(4.75), "Stacking Ensemble Classifier", GREEN)
sy = top+Inches(0.65)
simple_text(s7, Inches(6.9)+Inches(0.22), sy, Inches(5.4), Inches(0.55),
            "Kết hợp 3 base estimator tốt nhất (NB + LR + SVM); meta-classifier Logistic Regression tổng hợp dự đoán (StackingClassifier, cv=5).",
            11.5, TXT_SUB, line_spacing=1.15)
sy += Inches(0.85)
# mini architecture: 3 base -> meta
bw = Inches(1.55); bh = Inches(0.6)
bx0 = Inches(6.9)+Inches(0.35)
for i, nm in enumerate(["Naive\nBayes", "Logistic\nRegression", "Linear\nSVM"]):
    bx = bx0 + i*(bw+Inches(0.15))
    b = add_rect(s7, bx, sy, bw, bh, CARD2, line=STROKE, radius=0.16)
    simple_text(s7, bx, sy+Inches(0.08), bw, Inches(0.45), nm.replace("\n"," "), 10, TXT, bold=True, align=PP_ALIGN.CENTER, line_spacing=1.0)
sy += bh+Inches(0.25)
# convergent lines to meta box
meta_w = Inches(2.6); meta_x = Inches(6.9)+Inches(0.35)+ (3*bw+2*Inches(0.15))/2 - meta_w/2
for i in range(3):
    bx = bx0 + i*(bw+Inches(0.15)) + bw/2
    ln = s7.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, bx, sy-Inches(0.25), meta_x+meta_w/2, sy)
    ln.line.color.rgb = STROKE; ln.line.width = Pt(1.2)
meta = add_rect(s7, meta_x, sy, meta_w, bh, GREEN, radius=0.16)
simple_text(s7, meta_x, sy+Inches(0.08), meta_w, Inches(0.45), "Meta: Logistic Regression", 10.5, BG, bold=True, align=PP_ALIGN.CENTER, line_spacing=1.0)
sy += bh+Inches(0.35)
stat_chip(s7, Inches(6.9)+Inches(0.35), sy, Inches(2.6), Inches(1.0), "0.5619", "CV Macro F1 — tốt nhất trong 5 mô hình ML", GREEN)
stat_chip(s7, Inches(6.9)+Inches(3.1), sy, Inches(2.6), Inches(1.0), "0.7766", "Accuracy trên Final Test khoá", BLUE)

print("slides 6-7 done")

# =====================================================================
# SLIDE 8 — VISOBERT GPU
# =====================================================================
s8, top = base_slide("Chương 3 · Deep Learning", "Thử nghiệm ViSoBERT (Transformer) trên GPU Runpod")

section_card(s8, MARGIN, top, Inches(5.7), Inches(4.75), "Kết quả Zero-shot trên Final Test", ORANGE)
sy = top+Inches(0.65)
stat_chip(s8, MARGIN+Inches(0.22), sy, Inches(2.55), Inches(1.05), "0.4036", "Macro F1 (ViSoBERT)", ORANGE)
stat_chip(s8, MARGIN+Inches(2.9), sy, Inches(2.55), Inches(1.05), "65.36%", "Accuracy tổng thể", BLUE)
sy += Inches(1.25)
stat_chip(s8, MARGIN+Inches(0.22), sy, Inches(2.55), Inches(1.05), "75.44%", "Recall lớp Tiêu cực (vượt Stacking)", GREEN)
stat_chip(s8, MARGIN+Inches(2.9), sy, Inches(2.55), Inches(1.05), "4.88%", "Recall lớp Trung tính (gần như không nhận ra)", RED)
sy += Inches(1.3)
simple_text(s8, MARGIN+Inches(0.22), sy, Inches(5.2), Inches(0.8),
            "So với Stacking (Acc 0.7766, Macro F1 0.5475): ViSoBERT zero-shot yếu hơn tổng thể nhưng vượt trội ở khả năng phát hiện Tiêu cực — đánh đổi bằng việc bỏ sót gần hết lớp Trung tính.",
            11, TXT_SUB, line_spacing=1.2)

section_card(s8, Inches(6.9), top, Inches(5.85), Inches(4.75), "Vì sao Tiền xử lý cổ điển \"xung đột\" với Transformer?", RED)
ny = top+Inches(0.65)
for lead, rest in [("Over-cleaning: ", "loại stopword/tách từ làm mất ngữ cảnh câu mà Self-Attention cần để học quan hệ giữa các từ."),
                    ("Tokenizer BPE riêng biệt: ", "ViSoBERT đã có subword tokenizer huấn luyện trên dữ liệu mạng xã hội — tiền xử lý thêm gây méo phân phối token."),
                    ("Zero-shot, chưa fine-tune: ", "mô hình chưa được huấn luyện lại trên domain review IT nên chưa tối ưu cho bài toán 3 lớp."),
                    ("Hạ tầng GPU Runpod: ", "phù hợp huấn luyện DL nhưng công đoạn fine-tune đầy đủ nằm ở hướng phát triển tiếp theo.")]:
    dot = s8.shapes.add_shape(MSO_SHAPE.OVAL, Inches(6.9)+Inches(0.24), ny+Inches(0.06), Inches(0.09), Inches(0.09))
    no_shadow(dot); solid(dot, RED); no_line(dot)
    add_text(s8, Inches(6.9)+Inches(0.44), ny, Inches(5.2), Inches(0.85),
             [[(lead, 12, TXT, True, FONT), (rest, 12, TXT_SUB, False, FONT)]], line_spacing=1.15)
    ny += Inches(0.98)

# =====================================================================
# SLIDE 9 — LEADERBOARD & CONFUSION MATRIX
# =====================================================================
s9, top = base_slide("Chương 4 · Kết quả thực nghiệm", "Bảng Leaderboard tổng hợp & Ma trận nhầm lẫn")

lb_w = Inches(6.5)
rows = 7
tbl_shape = s9.shapes.add_table(rows, 3, MARGIN, top, lb_w, Inches(3.15))
table = tbl_shape.table
table.columns[0].width = Inches(3.5); table.columns[1].width = Inches(1.5); table.columns[2].width = Inches(1.5)
headers = ["Mô hình", "CV Macro F1", "Final Test F1"]
data = [
    ("Stacking (NB+LR+SVM)", "0.5619", "0.5475"),
    ("Logistic Regression", "0.5567", "—"),
    ("Linear SVM", "0.5561", "—"),
    ("Random Forest", "0.5515", "—"),
    ("ViSoBERT (zero-shot DL)", "—", "0.4036"),
    ("Multinomial Naive Bayes", "0.4890", "—"),
]
for c, h in enumerate(headers):
    set_cell(table, 0, c, h, 11.5)
for r, row in enumerate(data, start=1):
    for c, v in enumerate(row):
        set_cell(table, r, c, v, 11)
style_table(table, highlight_rows={1: RGBColor(0x14,0x33,0x28)})
simple_text(s9, MARGIN, top+Inches(3.28), lb_w, Inches(0.3),
            "Final Test chỉ được mở khoá 1 lần cho mô hình đã chọn (Stacking) và benchmark ViSoBERT — tránh rò rỉ dữ liệu.",
            10, TXT_DIM, line_spacing=1.1)

warn2 = add_rect(s9, MARGIN, top+Inches(3.7), lb_w, Inches(1.0), CARD2, line=ORANGE, radius=0.1)
simple_text(s9, MARGIN+Inches(0.2), top+Inches(3.82), lb_w-Inches(0.4), Inches(0.3), "⚠ BẪY ACCURACY", 11, ORANGE, bold=True)
simple_text(s9, MARGIN+Inches(0.2), top+Inches(4.12), lb_w-Inches(0.4), Inches(0.5),
            "Accuracy 77.66% có vẻ cao, nhưng Macro F1 chỉ 0.5475 — do mô hình nghiêng mạnh về lớp Positive đa số (1.241/1.683 mẫu).",
            10.5, TXT_SUB, line_spacing=1.1)

img_card(s9, FIG+"best_model_confusion_matrix.png", MARGIN+lb_w+Inches(0.25), top, Inches(5.5), Inches(4.75),
         caption="Confusion Matrix — Stacking Classifier trên Final Test (1.683 mẫu)")

print("slides 8-9 done")

# =====================================================================
# SLIDE 10 — ERROR ANALYSIS & HYBRID DECISION GATE
# =====================================================================
s10, top = base_slide("Chương 4 · Phân tích lỗi", "Phân tích lỗi sai định tính & Hybrid Decision Gate")

section_card(s10, MARGIN, top, Inches(6.0), Inches(4.75), "Case study: câu phủ định phức tạp", RED)
cy = top+Inches(0.62)
ex = add_rect(s10, MARGIN+Inches(0.22), cy, Inches(5.55), Inches(1.15), CARD2, line=STROKE, radius=0.1)
add_text(s10, MARGIN+Inches(0.42), cy+Inches(0.14), Inches(5.15), Inches(0.9),
         [[("“Môi trường làm việc không được thân thiện, đồng nghiệp không hỗ trợ và ít cơ hội học hỏi.”", 12.5, TXT, False, FONT)]],
         line_spacing=1.2)
cy += Inches(1.35)
for label, val, c in [("Không có Hybrid Gate", "Dự đoán sai → Trung tính / Tích cực", RED),
                       ("Có Hybrid Decision Gate", "Tiêu cực (71.1%) — bóc tách 3 cụm từ XAI", GREEN)]:
    add_rect(s10, MARGIN+Inches(0.22), cy, Inches(0.08), Inches(0.55), c)
    simple_text(s10, MARGIN+Inches(0.42), cy, Inches(5.2), Inches(0.28), label, 12, TXT, bold=True)
    simple_text(s10, MARGIN+Inches(0.42), cy+Inches(0.29), Inches(5.2), Inches(0.28), val, 11, TXT_SUB)
    cy += Inches(0.7)
cy += Inches(0.1)
simple_text(s10, MARGIN+Inches(0.22), cy, Inches(5.6), Inches(0.6),
            "Các lỗi khác thường gặp: câu châm biếm, khen/chê đan xen trong cùng review, đánh giá Trung tính mập mờ giữa 2 cực.",
            10.8, TXT_SUB, line_spacing=1.15)

section_card(s10, Inches(7.0), top, Inches(5.75), Inches(4.75), "Cơ chế Hybrid Decision Gate", GREEN)
img_card(s10, FIG+"negative_threshold_sensitivity.png", Inches(7.0)+Inches(0.22), top+Inches(0.6), Inches(5.3), Inches(2.55),
         caption="Độ nhạy ngưỡng xác suất P(Negative) trên Recall/Precision")
gy = top+Inches(3.35)
simple_text(s10, Inches(7.0)+Inches(0.22), gy, Inches(5.3), Inches(0.9),
            "Nếu P(Tiêu cực) ≥ 0.30 theo mô hình ML → ưu tiên gán nhãn Tiêu cực, kết hợp tri thức từ điển miền IT (negation, từ khoá nhạy cảm) để hiệu chỉnh các trường hợp mô hình còn lưỡng lự.",
            11, TXT_SUB, line_spacing=1.2)
stat_chip(s10, Inches(7.0)+Inches(0.22), gy+Inches(0.95), Inches(2.55), Inches(0.75), "26.3%→35.1%", "Recall Negative khi áp ngưỡng 0.30", GREEN)
stat_chip(s10, Inches(7.0)+Inches(2.95), gy+Inches(0.95), Inches(2.55), Inches(0.75), "+0.0032", "Macro F1 cải thiện", BLUE)

# =====================================================================
# SLIDE 11 — INSIGHT CẢM XÚC NGÀNH CNTT
# =====================================================================
s11, top = base_slide("Chương 5 · Insight doanh nghiệp", "Khám phá Insight cảm xúc ngành Công nghệ Thông tin")

wc_w = Inches(3.0)
img_card(s11, FIG+"wordcloud_positive_all.png", MARGIN, top, wc_w, Inches(2.25), caption="WordCloud — Tích cực")
img_card(s11, FIG+"wordcloud_negative_all.png", MARGIN, top+Inches(2.4), wc_w, Inches(2.25), caption="WordCloud — Tiêu cực")

img_card(s11, FIG+"company_fpt_software_sentiment_distribution.png", MARGIN+wc_w+Inches(0.2), top, Inches(4.55), Inches(2.25),
         caption="Phân bố cảm xúc — FPT Software")
img_card(s11, FIG+"company_nashtech_sentiment_distribution.png", MARGIN+wc_w+Inches(0.2), top+Inches(2.4), Inches(4.55), Inches(2.25),
         caption="Phân bố cảm xúc — NashTech")

rx = MARGIN+wc_w+Inches(4.55)+Inches(0.4)
section_card(s11, rx, top, Inches(4.35), Inches(4.75), "Chủ đề nổi bật theo sắc thái", YELLOW)
ry = top+Inches(0.65)
for lead, rest, c in [("Được khen nhiều nhất: ", "môi trường trẻ, đồng nghiệp thân thiện, công nghệ mới, lộ trình rõ ràng.", GREEN),
                       ("Bị phàn nàn nhiều nhất: ", "chế độ OT, tốc độ tăng lương, quy trình quản lý cứng nhắc.", RED),
                       ("So sánh giữa doanh nghiệp: ", "FPT Software và NashTech có tỷ lệ hài lòng khác biệt rõ theo từng khía cạnh.", BLUE)]:
    dot = s11.shapes.add_shape(MSO_SHAPE.OVAL, rx+Inches(0.24), ry+Inches(0.06), Inches(0.09), Inches(0.09))
    no_shadow(dot); solid(dot, c); no_line(dot)
    add_text(s11, rx+Inches(0.44), ry, Inches(3.75), Inches(1.05),
             [[(lead, 12, TXT, True, FONT), (rest, 12, TXT_SUB, False, FONT)]], line_spacing=1.15)
    ry += Inches(1.15)

print("slides 10-11 done")

# =====================================================================
# SLIDE 12 — WEB DEMO STREAMLIT
# =====================================================================
s12, top = base_slide("Chương 5 · Triển khai", "Ứng dụng Web Demo — Streamlit Dashboard")

mock_x, mock_y = MARGIN, top
mock_w, mock_h = Inches(7.6), Inches(4.75)
mock = add_rect(s12, mock_x, mock_y, mock_w, mock_h, RGBColor(0x0C,0x11,0x19), line=STROKE, radius=0.03)
# top tab bar
tab_labels = ["Tổng quan", "Khám phá dữ liệu", "Company Insights", "Dự đoán Realtime"]
tab_colors = [BLUE, GREEN, YELLOW, ORANGE]
tw = mock_w/4
for i, (lab, c) in enumerate(zip(tab_labels, tab_colors)):
    tx = mock_x + i*tw
    active = (i == 3)
    tab = add_rect(s12, tx+Inches(0.05), mock_y+Inches(0.12), tw-Inches(0.1), Inches(0.5),
                    CARD2 if active else None, radius=0.25)
    if active:
        add_rect(s12, tx+Inches(0.05), mock_y+Inches(0.56), tw-Inches(0.1), Pt(2.2), c)
    simple_text(s12, tx, mock_y+Inches(0.24), tw, Inches(0.3), lab, 10.5,
                TXT if active else TXT_DIM, bold=active, align=PP_ALIGN.CENTER)
# body: fake input + prediction result card
body_y = mock_y+Inches(0.85)
inp = add_rect(s12, mock_x+Inches(0.3), body_y, mock_w-Inches(0.6), Inches(0.95), CARD, line=STROKE, radius=0.1)
simple_text(s12, mock_x+Inches(0.5), body_y+Inches(0.1), mock_w-Inches(1.0), Inches(0.25), "NHẬP REVIEW CẦN PHÂN TÍCH", 9, TXT_DIM, bold=True)
simple_text(s12, mock_x+Inches(0.5), body_y+Inches(0.38), mock_w-Inches(1.0), Inches(0.5),
            "“Môi trường làm việc không được thân thiện, đồng nghiệp không hỗ trợ...”", 11.5, TXT_SUB)
res_y = body_y+Inches(1.15)
res = add_rect(s12, mock_x+Inches(0.3), res_y, mock_w-Inches(0.6), Inches(1.15), CARD2, line=RED, radius=0.12)
simple_text(s12, mock_x+Inches(0.5), res_y+Inches(0.12), Inches(3), Inches(0.3), "KẾT QUẢ DỰ ĐOÁN", 9, TXT_DIM, bold=True)
simple_text(s12, mock_x+Inches(0.5), res_y+Inches(0.42), Inches(3), Inches(0.6), "TIÊU CỰC", 22, RED, bold=True)
simple_text(s12, mock_x+mock_w-Inches(2.6), res_y+Inches(0.12), Inches(2.1), Inches(0.9), "71.1%", 30, TXT, bold=True, align=PP_ALIGN.RIGHT)
simple_text(s12, mock_x+mock_w-Inches(2.6), res_y+Inches(0.82), Inches(2.1), Inches(0.28), "độ tin cậy", 10, TXT_DIM, align=PP_ALIGN.RIGHT)
# model switch chip
sw_y = res_y+Inches(1.3)
add_rect(s12, mock_x+Inches(0.3), sw_y, mock_w-Inches(0.6), Inches(0.55), CARD, line=STROKE, radius=0.3)
simple_text(s12, mock_x+Inches(0.5), sw_y+Inches(0.13), mock_w-Inches(1.0), Inches(0.3),
            "○ Mô hình 1: Text-only (5.000)      ● Mô hình 2: Text + Lexicon (5.005)", 10.5, TXT_SUB)

rx = mock_x+mock_w+Inches(0.25)
section_card(s12, rx, top, Inches(4.5), Inches(4.75), "4 phân hệ chức năng", BLUE)
ry = top+Inches(0.62)
for lab, desc, c in [("Tổng quan dự án", "Giới thiệu pipeline, số liệu tổng hợp toàn hệ thống.", BLUE),
                      ("Khám phá dữ liệu", "EDA tương tác: phân bố nhãn, độ dài văn bản, khía cạnh.", GREEN),
                      ("Phân tích doanh nghiệp", "WordCloud & thống kê cảm xúc theo từng công ty IT.", YELLOW),
                      ("Dự đoán thời gian thực", "Nhập review, chọn mô hình, xem kết quả kèm giải thích XAI.", ORANGE)]:
    add_rect(s12, rx+Inches(0.22), ry, Inches(0.08), Inches(0.85), c)
    simple_text(s12, rx+Inches(0.42), ry, Inches(3.7), Inches(0.28), lab, 12, TXT, bold=True)
    simple_text(s12, rx+Inches(0.42), ry+Inches(0.3), Inches(3.7), Inches(0.5), desc, 10.3, TXT_SUB, line_spacing=1.1)
    ry += Inches(1.0)

# =====================================================================
# SLIDE 13 — XAI (EXPLAINABLE AI)
# =====================================================================
s13, top = base_slide("Chương 5 · Explainable AI", "Kiến trúc XAI thời gian thực — Giải thích quyết định mô hình")

section_card(s13, MARGIN, top, Inches(6.0), Inches(4.75), "Feature Importance — trọng số TF-IDF", GREEN)
words = [("không hỗ trợ", -0.82, RED), ("không thân thiện", -0.76, RED), ("ít cơ hội", -0.58, RED),
         ("học hỏi", 0.22, GREEN), ("đồng nghiệp", 0.12, GREEN)]
content_left = MARGIN + Inches(0.22)
content_right = MARGIN + Inches(6.0) - Inches(0.22)
label_w = Inches(1.55)
gap1 = Inches(0.15)
neg_track = Inches(2.3)               # bar length budget for the largest |value|
zero_x = content_left + label_w + gap1 + neg_track
val_x = content_right - Inches(0.65)  # fixed column so +/- labels line up
max_val = max(abs(v) for _, v, _ in words)
scale = neg_track / max_val           # in-EMU-per-unit-value (float)
wy = top+Inches(0.65)
for w, val, c in words:
    simple_text(s13, content_left, wy, label_w, Inches(0.3), w, 11.5, TXT, align=PP_ALIGN.RIGHT)
    bw = Emu(int(scale*abs(val)))
    bx = zero_x if val >= 0 else zero_x - bw
    add_rect(s13, bx, wy+Inches(0.02), bw, Inches(0.24), c, radius=0.5)
    simple_text(s13, val_x, wy-Inches(0.02), Inches(0.65), Inches(0.3), f"{val:+.2f}", 10.5, TXT_SUB)
    wy += Inches(0.46)
add_rect(s13, zero_x, top+Inches(0.65), Pt(1.2), wy-top-Inches(0.65), STROKE)
simple_text(s13, MARGIN+Inches(0.25), wy+Inches(0.15), Inches(5.5), Inches(0.6),
            "Mỗi thanh thể hiện mức đóng góp của từ/cụm từ vào quyết định cuối cùng — âm (đỏ) kéo về Tiêu cực, dương (xanh) kéo về Tích cực.",
            10.8, TXT_SUB, line_spacing=1.15)

section_card(s13, Inches(6.9), top, Inches(5.85), Inches(4.75), "Vì sao cần XAI trong bài toán này?", BLUE)
xy = top+Inches(0.65)
for lead, rest, c in [("Minh bạch quyết định: ", "người dùng (ứng viên, HR) hiểu vì sao một review bị gán Tiêu cực/Tích cực.", BLUE),
                       ("Bóc tách 3 cụm từ ảnh hưởng nhất: ", "hiển thị trực tiếp trên UI mỗi lần dự đoán realtime.", GREEN),
                       ("Kiểm chứng Negation Scope: ", "XAI cho thấy rõ cụm phủ định đã đảo cực tính đúng theo kỳ vọng.", YELLOW),
                       ("Hỗ trợ debug mô hình: ", "phát hiện các từ khoá gây nhiễu, phục vụ cải tiến pipeline sau này.", ORANGE)]:
    dot = s13.shapes.add_shape(MSO_SHAPE.OVAL, Inches(6.9)+Inches(0.24), xy+Inches(0.06), Inches(0.09), Inches(0.09))
    no_shadow(dot); solid(dot, c); no_line(dot)
    add_text(s13, Inches(6.9)+Inches(0.44), xy, Inches(5.2), Inches(0.85),
             [[(lead, 12, TXT, True, FONT), (rest, 12, TXT_SUB, False, FONT)]], line_spacing=1.15)
    xy += Inches(0.98)

print("slides 12-13 done")

# =====================================================================
# SLIDE 14 — ĐÁNH GIÁ, BÀI HỌC & HẠN CHẾ
# =====================================================================
s14, top = base_slide("Chương 6 · Tổng kết", "Đánh giá thực nghiệm, Bài học kinh nghiệm & Hạn chế")

cols = [
    ("THÀNH TỰU ĐẠT ĐƯỢC", GREEN, [
        "Pipeline tiền xử lý tiếng Việt chuyên sâu, Negation Scope Detection, Greedy Matching 99.75%.",
        "Stacking Ensemble đạt CV Macro F1 0.5619, benchmark chéo với ViSoBERT trên GPU.",
        "Ablation Study khoa học: Text+Lexicon vượt Text-only, có kiểm soát Data Shortcut.",
        "Web App Streamlit realtime tích hợp XAI, 43/43 unit test pass.",
    ]),
    ("BÀI HỌC KINH NGHIỆM", YELLOW, [
        "Mất cân bằng dữ liệu cần xử lý ở cả tầng đặc trưng và tầng đánh giá (Macro F1, không chỉ Accuracy).",
        "Tiền xử lý cho ML cổ điển và cho Transformer cần thiết kế khác nhau, không dùng chung 1 pipeline.",
        "Final Test chỉ nên mở khoá 1 lần — kỷ luật này giúp kết quả đáng tin cậy hơn.",
    ]),
    ("HẠN CHẾ HIỆN TẠI", RED, [
        "Recall lớp Tiêu cực còn thấp (26–35%) do dữ liệu thiểu số nghiêm trọng (6.8%).",
        "ViSoBERT mới ở zero-shot, chưa fine-tune đầy đủ trên domain review IT.",
        "Chưa phân tích cảm xúc ở mức khía cạnh chi tiết (Aspect-Based).",
    ]),
]
cw = Inches(3.98); gap = Inches(0.15)
for i, (title, c, items) in enumerate(cols):
    cx = MARGIN + i*(cw+gap)
    section_card(s14, cx, top, cw, Inches(4.75), title, c)
    bullet_list(s14, cx+Inches(0.22), top+Inches(0.65), cw-Inches(0.4), items, size=11.5, gap=0.16,
                dot_color=c, line_h=Inches(0.5))

# =====================================================================
# SLIDE 15 — KẾT LUẬN, HƯỚNG PHÁT TRIỂN & LỜI CẢM ƠN
# =====================================================================
s15, top = base_slide("Chương 6 · Kết luận", "Hướng phát triển tương lai & Lời cảm ơn")

section_card(s15, MARGIN, top, Inches(7.0), Inches(4.75), "Hướng phát triển tương lai", BLUE)
fy = top+Inches(0.65)
future = [
    ("Aspect-Based Sentiment Analysis (ABSA)", "Phân tích cảm xúc chi tiết theo từng khía cạnh (Lương, OT, Quản lý...) thay vì chỉ cảm xúc tổng thể.", BLUE),
    ("Fine-tuning toàn phần ViSoBERT", "Huấn luyện lại trên domain review IT tiếng Việt để khai thác tối đa năng lực Transformer.", GREEN),
    ("Ứng dụng LLM Agent", "Tự động tổng hợp báo cáo insight nhân sự theo thời gian thực cho từng doanh nghiệp.", YELLOW),
    ("Mở rộng dữ liệu đa nguồn", "Thu thập thêm review từ các nền tảng tuyển dụng khác để tăng độ bao phủ & cân bằng lớp.", ORANGE),
]
for lead, rest, c in future:
    dot = s15.shapes.add_shape(MSO_SHAPE.OVAL, MARGIN+Inches(0.24), fy+Inches(0.06), Inches(0.1), Inches(0.1))
    no_shadow(dot); solid(dot, c); no_line(dot)
    add_text(s15, MARGIN+Inches(0.46), fy, Inches(6.3), Inches(0.9),
             [[(lead, 13, TXT, True, FONT)], [(rest, 11.3, TXT_SUB, False, FONT)]], line_spacing=1.15, space_after=Pt(2))
    fy += Inches(1.02)

thanks = add_rect(s15, Inches(7.75), top, Inches(4.85), Inches(4.75), CARD, line=BLUE, radius=0.08)
add_rect(s15, Inches(7.75), top, Inches(4.85), Inches(0.06), BLUE)
brand_mark(s15, Inches(7.75)+Inches(0.3), top+Inches(0.3), s=0.55)
simple_text(s15, Inches(7.75)+Inches(0.3), top+Inches(1.05), Inches(4.25), Inches(0.4), "LỜI CẢM ƠN", 15, BLUE, bold=True)
simple_text(s15, Inches(7.75)+Inches(0.3), top+Inches(1.5), Inches(4.25), Inches(1.1),
            "Nhóm 4 xin chân thành cảm ơn Thầy Đặng Văn Thìn đã tận tình hướng dẫn, cùng Hội đồng đánh giá đã dành thời gian theo dõi phần trình bày của nhóm.",
            12.5, TXT_SUB, line_spacing=1.25)
add_rect(s15, Inches(7.75)+Inches(0.3), top+Inches(2.85), Inches(4.25), Pt(1), STROKE)
simple_text(s15, Inches(7.75)+Inches(0.3), top+Inches(3.05), Inches(4.25), Inches(0.4), "NHÓM 4 SẴN SÀNG BƯỚC VÀO", 11, TXT_DIM, bold=True)
simple_text(s15, Inches(7.75)+Inches(0.3), top+Inches(3.42), Inches(4.25), Inches(0.8), "PHẦN HỎI ĐÁP (Q&A)", 24, TXT, bold=True)
simple_text(s15, Inches(7.75)+Inches(0.3), top+Inches(4.15), Inches(4.25), Inches(0.4), "Trân trọng cảm ơn!", 13, GREEN, bold=True)

# =====================================================================
os.makedirs(OUT_PATH.parent, exist_ok=True)
prs.save(str(OUT_PATH))
print("SAVED:", OUT_PATH.name, "| slides:", len(prs.slides))
