import re
import os
import unicodedata
from typing import Dict, Set

class TextPreprocessor:
    """
    Class xử lý tiền xử lý văn bản tiếng Việt & trích xuất đặc trưng Lexicon cho Sentiment Analysis.
    """
    def __init__(self, dict_dir: str = None):
        if dict_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            dict_dir = os.path.join(os.path.dirname(current_dir), 'data', 'dictionaries')
        
        self.dict_dir = dict_dir
        self.it_terms_dict = self._load_dict_from_file(os.path.join(dict_dir, 'it_terms.txt'))
        self.stopwords = self._load_set_from_file(os.path.join(dict_dir, 'vietnamese-stopwords.txt'))
        self.teencode_dict = self._load_dict_from_file(os.path.join(dict_dir, 'teencode.txt'))
        self.wrong_words_dict = self._load_dict_from_file(os.path.join(dict_dir, 'wrong-word.txt'))
        self.english_vnmese_dict = self._load_dict_from_file(os.path.join(dict_dir, 'english-vnmese.txt'))
        self.emoji_dict = self._load_dict_from_file(os.path.join(dict_dir, 'emojicon.txt'))
        self.emoji_dict = dict(sorted(self.emoji_dict.items(), key=lambda x: len(x[0]), reverse=True))

        # Load lexicon cảm xúc
        self.positive_words = self._load_set_from_file(os.path.join(dict_dir, 'positive_words.txt'))
        self.negative_words = self._load_set_from_file(os.path.join(dict_dir, 'negative_words.txt'))
        self.positive_emojis = self._load_set_from_file(os.path.join(dict_dir, 'positive_emoji.txt'))
        self.negative_emojis = self._load_set_from_file(os.path.join(dict_dir, 'negative_emoji.txt'))

        # Xác định độ dài cụm từ tối đa (theo số từ phân tách bằng khoảng trắng)
        all_phrases = self.positive_words | self.negative_words
        self.max_phrase_len = max((len(p.split()) for p in all_phrases), default=1)

    def _load_set_from_file(self, filepath: str) -> Set[str]:
        if not os.path.exists(filepath):
            return set()
        with open(filepath, 'r', encoding='utf-8') as f:
            result = set()
            for line in f:
                line_clean = line.strip().lower()
                if line_clean and not line_clean.startswith('#'):
                    # Chuẩn hóa khoảng trắng và gạch dưới
                    normalized = " ".join(line_clean.replace('_', ' ').split())
                    result.add(normalized)
            return result

    def _load_dict_from_file(self, filepath: str) -> Dict[str, str]:
        if not os.path.exists(filepath):
            return {}
        result = {}
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line_clean = line.strip()
                if not line_clean or line_clean.startswith('#'):
                    continue
                parts = line_clean.split('\t') if '\t' in line_clean else line_clean.split(' ', 1)
                if len(parts) >= 2:
                    result[parts[0].lower()] = parts[1].lower()
        return result

    def normalize_unicode(self, text: str) -> str:
        """Chuẩn hóa bảng mã Unicode sang chuẩn NFC."""
        if not isinstance(text, str):
            return ""
        return unicodedata.normalize('NFC', text)

    def process_emojis(self, text: str) -> str:
        """Thay thế emoji/emojicon bằng từ ngữ mang sắc thái cảm xúc."""
        for emo, replacement in self.emoji_dict.items():
            if any(c.isalpha() for c in emo):
                text = re.sub(re.escape(emo), f" {replacement} ", text, flags=re.IGNORECASE)
            else:
                text = text.replace(emo, f" {replacement} ")
        for emo in self.positive_emojis:
            text = text.replace(emo, " tích_cực ")
        for emo in self.negative_emojis:
            text = text.replace(emo, " tiêu_cực ")
        return text

    def replace_teencode_and_typos(self, text: str) -> str:
        """Thay thế viết tắt, teencode, thuật ngữ IT và lỗi chính tả."""
        # Xử lý các cụm teencode nhiều từ trước (nếu có trong từ điển teencode)
        for k, v in self.teencode_dict.items():
            if ' ' in k:
                text = re.sub(r'\b' + re.escape(k) + r'\b', v, text, flags=re.IGNORECASE)

        # Đệm khoảng trắng quanh ký tự đặc biệt để tách từ không bị dính dấu câu
        padded_text = re.sub(r'([^\w\s])', r' \1 ', text)
        words = padded_text.split()
        normalized_words = []
        for word in words:
            w_lower = word.lower()
            if w_lower in self.it_terms_dict:
                normalized_words.append(self.it_terms_dict[w_lower])
            elif w_lower in self.teencode_dict:
                normalized_words.append(self.teencode_dict[w_lower])
            elif w_lower in self.wrong_words_dict:
                normalized_words.append(self.wrong_words_dict[w_lower])
            elif w_lower in self.english_vnmese_dict:
                normalized_words.append(self.english_vnmese_dict[w_lower])
            else:
                normalized_words.append(word)
        return " ".join(normalized_words)

    def clean_basic_text(self, text: str) -> str:
        """
        Bước 1: Làm sạch cơ bản (Clean Basic Text)
        - Chuẩn hóa Unicode NFC
        - Xử lý emoji & biểu tượng cảm xúc
        - Chuẩn hóa teencode, từ tiếng Anh, từ sai chính tả
        - Xóa liên kết URL, email, ký tự đặc biệt vô nghĩa
        """
        if not isinstance(text, str) or not text.strip():
            return ""
        
        text = self.normalize_unicode(text)
        text = self.process_emojis(text)
        
        # Xóa URL và email
        text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
        text = re.sub(r'\S+@\S+', ' ', text)
        
        # Chuyển về chữ thường
        text = text.lower()
        
        # Thay thế teencode & từ sai
        text = self.replace_teencode_and_typos(text)
        
        # Giữ lại các chữ cái tiếng Việt, số và khoảng trắng
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def clean_advance_text(self, text: str, remove_stopwords: bool = True) -> str:
        """
        Bước 2: Làm sạch nâng cao (Clean Advance Text)
        - Thực hiện tách từ tiếng Việt (Word Segmentation)
          Ưu tiên: underthesea → pyvi (fallback nếu underthesea không load được)
        - Loại bỏ từ dừng (Stopwords) nếu yêu cầu
        """
        basic = self.clean_basic_text(text)
        if not basic:
            return ""

        # Lazy-load tokenizer: thử underthesea trước, fallback pyvi
        tokenized = basic  # default: không tách từ
        try:
            from underthesea import word_tokenize as _wt
            tokenized = _wt(basic, format="text")
        except Exception:
            try:
                from pyvi import ViTokenizer
                tokenized = ViTokenizer.tokenize(basic)
            except Exception:
                tokenized = basic  # fallback cuối: giữ nguyên

        if remove_stopwords:
            words = tokenized.split()
            words = [w for w in words if w not in self.stopwords]
            return " ".join(words)

        return tokenized

    def clean_text_for_transformer(self, text: str) -> str:
        """
        Bước tiền xử lý tối ưu cho các mô hình Pretrained Transformer (ViSoBERT, PhoBERT):
        - Chuẩn hóa Unicode NFC
        - Xóa liên kết URL và địa chỉ Email gây nhiễu
        - Chuẩn hóa ký tự lặp kéo dài về tối đa 2 ký tự (vd: 'vuiiiii' -> 'vuii')
        - GIỮ NGUYÊN cấu trúc ngữ pháp và dấu câu (., !?) để bảo toàn cơ chế Self-Attention
        - GIỮ NGUYÊN Emoji tự nhiên vì ViSoBERT có sẵn token embedding cho emoji
        - GIỮ NGUYÊN teencode, từ lóng và thuật ngữ tiếng Anh IT (không dịch thô làm sai nghĩa)
        """
        if not isinstance(text, str) or not text.strip():
            return ""

        # 1. Chuẩn hóa Unicode NFC
        text = self.normalize_unicode(text)

        # 2. Xóa liên kết URL và Email
        text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
        text = re.sub(r'\S+@\S+', ' ', text)

        # 3. Rút gọn ký tự lặp quá đà về tối đa 2 ký tự (giữ sắc thái nhấn mạnh)
        text = re.sub(r'([a-zA-ZÀ-ỹ])\1{2,}', r'\1\1', text)

        # 4. Chuẩn hóa khoảng trắng nhưng giữ nguyên dấu câu và emoji
        text = re.sub(r'\s+([.,!?:;])', r'\1', text)
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def calc_sentiment_features(self, text: str, raw_text: str = None) -> Dict[str, float]:
        """
        Trích xuất các thuộc tính thống kê Lexicon bằng thuật toán Greedy Longest Phrase Matching:
        - pos_w, neg_w: Số cụm từ tích cực / tiêu cực khớp trong từ điển
        - pos_e, neg_e: Số emoji tích cực / tiêu cực
        - total_we: Tổng số cụm từ & emoji mang cảm xúc
        - sentiment_ratio: Tỷ lệ cân bằng giữa tích cực và tiêu cực (-1.0 đến +1.0)
        """
        if not isinstance(text, str) or not text.strip():
            return {
                'pos_w': 0, 'neg_w': 0, 'pos_e': 0, 'neg_e': 0,
                'total_we': 0, 'sentiment_ratio': 0.0
            }
        
        # 1. Đếm emoji: ưu tiên chuỗi thô (raw_text hoặc text)
        emoji_source = raw_text if (isinstance(raw_text, str) and raw_text.strip()) else text
        pos_e = sum(emoji_source.count(e) for e in self.positive_emojis)
        neg_e = sum(emoji_source.count(e) for e in self.negative_emojis)
        
        # Nếu văn bản đã qua clean_basic_text (emoji đã thay bằng text "tích_cực" / "tiêu_cực")
        if pos_e == 0 and neg_e == 0:
            pos_e = text.count('tích_cực')
            neg_e = text.count('tiêu_cực')

        # 2. Chuẩn hóa văn bản cho việc đối sánh cụm từ:
        # Thay thế '_' thành ' ' (hỗ trợ cả text sau tách từ ViTokenizer lẫn clean_basic_text)
        clean_text = self.normalize_unicode(text).lower()
        clean_text = clean_text.replace('_', ' ')
        clean_text = re.sub(r'[^\w\s]', ' ', clean_text)
        tokens = clean_text.split()
        n_tokens = len(tokens)

        # 3. Quét cụm từ tham lam (Greedy Longest Matching) kết hợp xử lý phạm vi phủ định (Negation Scope):
        # - Ưu tiên cụm tiêu cực dài nhất
        # - Nếu gặp từ tích cực nhưng có tiền tố phủ định đi trước (vd: "không được thân thiện"), tự động đảo chiều sang tiêu cực
        NEGATION_WORDS = {
            'không', 'chưa', 'chẳng', 'chả', 'ít', 'thiếu', 'kém', 'hạn chế',
            'không hề', 'chưa hề', 'không được', 'chưa được', 'không có'
        }

        pos_w = 0
        neg_w = 0
        matched_pos = []
        matched_neg = []
        i = 0
        max_k = self.max_phrase_len

        while i < n_tokens:
            matched = False
            for k in range(min(max_k, n_tokens - i), 0, -1):
                phrase = " ".join(tokens[i : i + k])
                if phrase in self.negative_words:
                    neg_w += 1
                    matched_neg.append(phrase)
                    i += k
                    matched = True
                    break
                elif phrase in self.positive_words:
                    # Kiểm tra xem ngay trước cụm từ tích cực có từ/cụm phủ định không (khoảng cách 1-2 từ)
                    is_negated = False
                    neg_prefix = ''
                    if i > 0 and tokens[i - 1] in NEGATION_WORDS:
                        is_negated = True
                        neg_prefix = tokens[i - 1]
                    elif i > 1 and f"{tokens[i - 2]} {tokens[i - 1]}" in NEGATION_WORDS:
                        is_negated = True
                        neg_prefix = f"{tokens[i - 2]} {tokens[i - 1]}"
                    elif i > 1 and tokens[i - 2] in NEGATION_WORDS and tokens[i - 1] in {'được', 'hề', 'quá', 'rất', 'thực sự'}:
                        is_negated = True
                        neg_prefix = f"{tokens[i - 2]} {tokens[i - 1]}"

                    if is_negated:
                        neg_w += 1
                        matched_neg.append(f"{neg_prefix} {phrase}")
                    else:
                        pos_w += 1
                        matched_pos.append(phrase)

                    i += k
                    matched = True
                    break

            if not matched:
                i += 1

        total_w = pos_w + neg_w
        total_e = pos_e + neg_e
        total_we = total_w + total_e

        # Tỷ lệ cảm xúc chuẩn hóa từ -1 (tiêu cực) đến +1 (tích cực)
        if total_we > 0:
            sentiment_ratio = (pos_w + pos_e - neg_w - neg_e) / float(total_we)
        else:
            sentiment_ratio = 0.0

        return {
            'pos_w': pos_w,
            'neg_w': neg_w,
            'pos_e': pos_e,
            'neg_e': neg_e,
            'total_we': total_we,
            'sentiment_ratio': round(sentiment_ratio, 4),
            'pos_phrases': matched_pos,
            'neg_phrases': matched_neg
        }


    @staticmethod
    def map_sentiment_label(rating: int) -> str:
        """
        Gán nhãn cảm xúc dựa trên số sao đánh giá (Rating):
        - 4 hoặc 5 sao -> 'Positive' (Tích cực)
        - 3 sao        -> 'Neutral'  (Trung tính)
        - 1 hoặc 2 sao -> 'Negative' (Tiêu cực)
        """
        if rating >= 4:
            return 'Positive'
        elif rating == 3:
            return 'Neutral'
        else:
            return 'Negative'
