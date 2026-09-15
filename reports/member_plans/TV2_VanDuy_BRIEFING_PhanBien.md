# TV2 — Văn Duy — Briefing trình bày & phản biện

Phần việc: **Feature Engineering & EDA**. Bản này để tra nhanh trước khi báo cáo, không phải báo cáo.

---

## 1. Chốt phần việc trong 3 câu

Nhận dữ liệu sạch từ TV1, trả về **ma trận đặc trưng + phép chia dữ liệu** cho TV3 huấn luyện.

Ở giữa hai đầu đó là 4 quyết định có bằng chứng thực nghiệm: chọn chỉ số đánh giá, chọn cách vector hóa, chọn nhóm đặc trưng, chọn cách xử lý mất cân bằng.

Toàn bộ so sánh chạy trên **5-fold Stratified CV, cùng fold, cùng seed 2026, cùng Logistic Regression** — cố định bộ phân loại để mọi chênh lệch quy về khác biệt đặc trưng.

---

## 2. Sáu con số phải thuộc

| Số | Ý nghĩa |
|---|---|
| **8.417 → 8.413** | Review sau tiền xử lý → sau khi loại text trùng và nhóm bất đồng nhãn |
| **73,76 / 19,47 / 6,77 %** | Tỷ lệ Positive / Neutral / Negative. Positive gấp **10,9 lần** Negative |
| **0,5579** | Macro F1 text-only (TF-IDF 1-2 gram + class_weight balanced) |
| **0,7433** | Macro F1 cấu hình đầy đủ text + lexicon + aspect |
| **0,7676 / 0,0921** | Accuracy / Recall Negative khi KHÔNG xử lý mất cân bằng |
| **6.730 × 5.000** | Kích thước ma trận development text-only (final test 1.683 × 5.000) |

---

## 3. Bốn quyết định — mỗi cái một dòng lý do

**① Chỉ số chính là Macro F1, không phải Accuracy.**
Bộ phân loại luôn đoán Positive đã đạt ~73,8% Accuracy mà vô dụng. Bằng chứng mạnh nhất: cấu hình không xử lý mất cân bằng đạt Accuracy **cao nhất** trong 3 chiến lược (0,7676) nhưng Recall Negative chỉ 0,0921 — bỏ sót hơn 90% review tiêu cực.

**② TF-IDF (1,2) sublinear, không phải BoW, không phải unigram.**
- (1,2) hơn (1,1): +0,0183 Macro F1 (0,5579 vs 0,5396)
- TF-IDF hơn BoW: +0,0161 Macro F1, cải thiện ở 4/5 fold
- BoW có Accuracy **cao hơn** (0,7177 vs 0,7158) nhưng Recall Negative thấp hơn hẳn (0,3773 vs 0,4563). BoW đếm tần suất tuyệt đối nên bị lớp đa số lấn át, IDF của TF-IDF triệt tiêu ảnh hưởng đó.
- Cấu hình: `max_features=5000`, `min_df=2`, `sublinear_tf=True`

**③ Bàn giao SONG SONG hai bộ đặc trưng, không phải một.**
- `text-only` (5.000 chiều) → dùng cho kịch bản deploy, người dùng chỉ nhập văn bản tự do
- `text + lexicon + aspect` (5.010 chiều) → dùng cho bảng so sánh mô hình trong báo cáo
- Hai bộ dùng **chung phép chia và chung seed** nên số liệu đặt cạnh nhau so sánh được

**④ `class_weight='balanced'`, không phải SMOTE.**
SMOTE chỉ hơn 0,0020 Macro F1 và **chỉ cải thiện ở 2/5 fold** — không phân biệt được với nhiễu. Đổi lại class_weight cho Recall Negative cao hơn (0,4563 vs 0,4410), không sinh mẫu giả, không đổi kích thước ma trận. Trên TF-IDF thưa và nhiều chiều, vector do SMOTE nội suy không ứng với văn bản có thật nên không diễn giải được. SMOTE vẫn giữ trong `src/features.py` làm phương án dự phòng cho model không hỗ trợ trọng số lớp.

---

## 4. Bảng tra nhanh

**Ablation nhóm đặc trưng (5-fold CV, development)**

| Nhóm | Macro F1 | Neutral F1 | Recall Neg | Acc | Fold cải thiện |
|---|---:|---:|---:|---:|:---:|
| Text-only | 0,5579 | 0,4456 | 0,4563 | 0,7158 | — |
| Text + lexicon | 0,5664 | 0,4578 | 0,4803 | 0,7211 | 4/5 |
| Text + aspect | 0,7369 | 0,6441 | 0,6952 | 0,8373 | 5/5 |
| **Text + lexicon + aspect** | **0,7433** | **0,6497** | 0,7061 | **0,8409** | 5/5 |
| Aspect ratings only | 0,7388 | 0,6353 | **0,7676** | 0,8337 | 5/5 |

**Xử lý mất cân bằng**

| Chiến lược | Macro F1 | Recall Neg | Acc |
|---|---:|---:|---:|
| Không xử lý | 0,4622 | 0,0921 | **0,7676** |
| `class_weight='balanced'` | 0,5579 | **0,4563** | 0,7158 |
| SMOTE | **0,5600** | 0,4410 | 0,7263 |

**Tương quan Spearman aspect với Rating:** Management 0,7368 · Salary 0,7343 · Culture 0,6566 · Training 0,6398 · Office 0,5423

---

## 5. Câu hỏi phản biện — trả lời sẵn

**"Macro F1 0,5579 thấp quá, sao không cải thiện?"**
Đó là con số của cấu hình chỉ dùng văn bản, cố tình giữ thấp để phản ánh đúng kịch bản deploy. Cấu hình đầy đủ đạt 0,7433. Trần của text-only bị chặn bởi chất lượng nhãn: nhãn là weak label suy từ Rating, không phải nhãn người đọc nội dung gán, nên văn bản và nhãn không khớp hoàn toàn.

**"Thêm aspect tăng 0,1853 Macro F1 — sao không lấy luôn làm kết quả chính?"**
Vì phần tăng đó phần lớn không phải do hiểu ngôn ngữ tốt hơn. Nhãn `sentiment` suy trực tiếp từ `Rating`, mà 5 điểm aspect tương quan Spearman 0,54–0,74 với chính `Rating`. Bằng chứng trực tiếp: **cấu hình Aspect-only đạt Macro F1 0,7388 mà không đọc một từ nào trong review**. Mô hình đang khôi phục lại thang điểm đã sinh ra nhãn. Thêm nữa, deploy thực tế người dùng chỉ nhập văn bản, không có đủ 5 điểm aspect.

**"Sao không đưa Rating vào đặc trưng, tương quan cao nhất mà?"**
Rò rỉ nhãn. Nhãn `sentiment` được tạo trực tiếp từ `Rating` theo quy tắc ≥4 sao Positive, 3 sao Neutral, ≤2 sao Negative. Đưa vào là mô hình học thuộc quy tắc, không học gì cả.

**"Lexicon chỉ tăng 0,0084, có ý nghĩa thống kê không?"**
Không đủ bằng chứng để khẳng định. Cải thiện ở 4/5 fold, fold xấu nhất giảm 0,0038, biên độ này nằm trong dao động giữa các fold (std 0,007–0,015). Vẫn giữ lexicon vì đây là **đặc trưng duy nhất ngoài TF-IDF tính được trực tiếp từ văn bản người dùng nhập**, nên dùng được ở kịch bản deploy. Muốn khẳng định thì phải lặp CV với nhiều seed.

**"Làm sao chắc không rò rỉ dữ liệu?"**
Ba lớp chặn: chia 80/20 stratified **trước** khi fit bất cứ thứ gì, final test khóa lại không dùng để chọn đặc trưng. Vectorizer và MinMaxScaler fit lại độc lập **bên trong từng fold**. SMOTE chỉ áp trên phần train của fold, không bao giờ trên phần validation.

**"Từ điển cảm xúc bao phủ được bao nhiêu?"**
Ban đầu đối sánh từ đơn chỉ phủ 12,26% review. Sau khi đổi sang đối sánh cụm từ dài nhất (Greedy Longest Phrase Matching) và mở rộng từ điển thì lên **99,75%**. Đáng chú ý là việc này **đảo chiều kết luận**: phiên bản cũ Text+lexicon đạt 0,5556 (thấp hơn text-only), phiên bản mới đạt 0,5664 (cao hơn).

**"Có bằng chứng gì nhãn yếu không đáng tin?"**
Trường `Recommend?` bất đồng với nhãn ở tỷ lệ đáng kể: 41 review Negative vẫn được khuyến nghị, 411 Neutral và 87 Positive thì không. Không chứng minh nhãn sai, nhưng đủ để không mô tả Rating như ground truth tuyệt đối.

---

## 6. Ba chỗ yếu — biết trước để không bị động

**① Bộ audit 300 review chưa gán nhãn.**
`data/annotation/sentiment_audit_blind.csv` đã chuẩn bị 300 mẫu nhưng ba cột `annotator_1_label`, `annotator_2_label`, `adjudicated_label` **còn trống hoàn toàn**. Nghĩa là chưa có số đo agreement giữa nhãn người và nhãn yếu. Nếu bị hỏi "đã kiểm chứng nhãn yếu bằng người chưa" thì trả lời thẳng: đã thiết kế quy trình audit mù và chuẩn bị mẫu, chưa kịp chạy vòng gán nhãn, đây là việc đầu tiên nếu có thêm thời gian. Đừng nói đã làm.

**② Chỉ chạy một seed.**
Mọi kết luận dựa trên 5-fold với `random_state=2026`. Chênh lệch nhỏ (lexicon +0,0084, SMOTE +0,0020) không thể khẳng định với một seed. Chính báo cáo đã nêu điều này — nhắc trước thì thành điểm cộng về tính cẩn trọng, để hội đồng nêu thì thành lỗ hổng.

**③ TỒN TẠI HAI PHIÊN BẢN SỐ LIỆU — bắt buộc chốt trước khi lên bảng.**

Commit `7c12557` (08/09, chạy lại toàn bộ thí nghiệm trên từ điển 99,75%) mới chỉ nằm trên `origin/feature/aspect-hybrid-features`, **chưa merge vào master của nhóm** (`mrkiss-it/master`). Bộ slide phản biện 15 trang do NDK dựng ngày 13-14/09 lấy số từ master, tức là số TRƯỚC lần chạy lại.

| Chỉ số | Local của anh (sau rerun 08/09) | Master nhóm + slide + `ke_hoach_hoan_thien_do_an.md` |
|---|---:|---:|
| Text + lexicon Macro F1 | 0,5664 | **0,5658** |
| Text + lexicon + aspect Macro F1 | 0,7433 | **0,7389** |
| Delta lexicon so text-only | +0,0084, **4/5 fold**, xấu nhất −0,0038 | +0,0079, **3/5 fold**, xấu nhất −0,0021 |
| `sentiment_ratio` mean lớp Negative | 0,063 | 0,090 |
| `pos_e` / `neg_e` | khác 0 trên 20 review | mô tả là hằng số 0 |

Chênh lệch Macro F1 chỉ 0,0006 nên không đổi bất kỳ kết luận nào. Nhưng **con số fold đổi từ 3/5 sang 4/5** — đây là chỗ lộ nếu phản biện cầm báo cáo của nhóm mà anh nói theo bản local.

Hai lựa chọn, chọn một rồi nói với nhóm:
- **An toàn**: nói theo số của master (0,5658 · 3/5 fold) vì slide, trang benchmark và checklist nghiệm thu đều đang dùng số này.
- **Đúng hơn**: mở PR đẩy `7c12557` lên master và nhờ NDK chạy lại `scripts/build_presentation_slides.py`. Chỉ làm nếu còn đủ thời gian trước buổi báo cáo.

Số `0.5619` trên slide 1 và slide 7 là CV Macro F1 của Stacking (phần TV3), không phải số của anh — đừng nhận nhầm.

---

## 7. Việc còn treo

Ô chưa tick duy nhất trong kế hoạch TV2: **viết báo cáo toàn văn 6 chương (Word + PDF), 35–45 trang**, theo khung `reports/final_report_outline.md`, tích hợp số liệu của cả 4 thành viên, nộp Hoàng Hôn duyệt.

---

## 8. Đường dẫn cần mở nhanh khi bị hỏi

| Cần chứng minh | Mở file |
|---|---|
| Toàn bộ số liệu và lập luận | `reports/eda_feature_engineering.md` |
| Bảng ablation gốc | `reports/aspect_hybrid_ablation.csv` (+ `_per_fold.csv`) |
| TF-IDF vs BoW | `reports/tv2_vectorizer_comparison.csv` |
| Chiến lược cân bằng lớp | `reports/tv2_balancing_comparison.csv` |
| Code chia tập, chống rò rỉ, SMOTE | `src/features.py` (362 dòng) |
| Script chạy lại thí nghiệm | `scripts/run_aspect_hybrid_ablation.py`, `scripts/run_tv2_feature_experiments.py` |
| Hash dữ liệu, Git SHA, checksum | `models/artifact_manifest.json` |
| 10 biểu đồ 300 DPI | `reports/figures/` |
