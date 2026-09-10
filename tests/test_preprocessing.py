import os
import sys
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocessing import TextPreprocessor

DICT_DIR = PROJECT_ROOT / "data" / "dictionaries"



@pytest.fixture(scope="module")
def preprocessor():
    return TextPreprocessor(dict_dir=str(DICT_DIR))


def test_phrase_matching_che_do_bao_hiem_tot(preprocessor):
    """Kiểm tra cụm từ 'chế độ bảo hiểm tốt' được match chính xác theo góp ý của Văn Duy."""
    text = "Công ty có chế độ bảo hiểm tốt và phúc lợi đầy đủ."
    feats = preprocessor.calc_sentiment_features(text)
    
    assert feats["pos_w"] >= 1, f"Cần match ít nhất 1 cụm từ tích cực, thực tế: {feats}"
    assert feats["neg_w"] == 0, f"Không được có từ tiêu cực, thực tế: {feats}"
    assert feats["total_we"] >= 1
    assert feats["sentiment_ratio"] > 0.0


def test_phrase_matching_common_positive_phrases(preprocessor):
    """Kiểm tra nhận diện nhiều cụm từ tích cực trong một đánh giá."""
    text = "Môi trường làm việc thoải mái vui vẻ, đồng nghiệp thân thiện, sếp tốt."
    feats = preprocessor.calc_sentiment_features(text)
    
    # Các cụm: thoải mái, vui vẻ, thân thiện, sếp tốt
    assert feats["pos_w"] >= 3, f"Kỳ vọng ít nhất 3 cụm từ tích cực, thực tế: {feats}"
    assert feats["neg_w"] == 0
    assert feats["sentiment_ratio"] == 1.0


def test_phrase_matching_negation_handling(preprocessor):
    """
    Kiểm tra thuật toán Greedy Longest Matching xử lý chính xác ngữ cảnh phủ định:
    - 'lương không tăng', 'sếp không lắng nghe' -> NEG (không bị bắt nhầm POS 'tăng lương', 'lắng nghe')
    - 'không toxic' -> POS (không bị bắt nhầm NEG 'toxic')
    """
    neg_text = "Lương không tăng mà sếp không lắng nghe nhân viên."
    neg_feats = preprocessor.calc_sentiment_features(neg_text)
    assert neg_feats["neg_w"] >= 2, f"Kỳ vọng ít nhất 2 cụm tiêu cực, thực tế: {neg_feats}"
    assert neg_feats["pos_w"] == 0, f"Không được bắt nhầm từ tích cực trong cụm phủ định, thực tế: {neg_feats}"
    assert neg_feats["sentiment_ratio"] == -1.0

    pos_text = "Môi trường làm việc năng động và không toxic."
    pos_feats = preprocessor.calc_sentiment_features(pos_text)
    assert pos_feats["pos_w"] >= 2, f"Kỳ vọng bắt được 'năng động' và 'không toxic', thực tế: {pos_feats}"
    assert pos_feats["neg_w"] == 0, f"'không toxic' không được tính là tiêu cực, thực tế: {pos_feats}"


def test_phrase_matching_with_underscores_from_tokenizer(preprocessor):
    """Kiểm tra văn bản sau khi tách từ (có dấu gạch dưới _) vẫn match trọn vẹn cụm từ."""
    segmented_text = "chế_độ bảo_hiểm tốt môi_trường thoải_mái thân_thiện"
    feats = preprocessor.calc_sentiment_features(segmented_text)
    
    assert feats["pos_w"] >= 3, f"Kỳ vọng match ít nhất 3 cụm từ, thực tế: {feats}"
    assert feats["neg_w"] == 0
    assert feats["sentiment_ratio"] == 1.0


def test_empty_and_invalid_inputs(preprocessor):
    """Kiểm tra giá trị mặc định an toàn cho văn bản rỗng hoặc không hợp lệ."""
    for empty_val in ["", "   ", None, 123]:
        feats = preprocessor.calc_sentiment_features(empty_val)
        assert feats["pos_w"] == 0
        assert feats["neg_w"] == 0
        assert feats["pos_e"] == 0
        assert feats["neg_e"] == 0
        assert feats["total_we"] == 0
        assert feats["sentiment_ratio"] == 0.0


def test_emoji_detection(preprocessor):
    """Kiểm tra nhận diện emoji cả dạng Unicode gốc lẫn dạng đã chuẩn hóa."""
    # Unicode emoji
    feats_unicode = preprocessor.calc_sentiment_features("Tuyệt vời 😊 👍")
    assert feats_unicode["pos_e"] >= 1

    # Dạng text thay thế từ clean_basic_text
    feats_cleaned = preprocessor.calc_sentiment_features("Công ty tốt tích_cực")
    assert feats_cleaned["pos_e"] >= 1


def test_core_unigrams_and_negations(preprocessor):
    """
    Kiểm tra nhận diện các từ đơn cảm xúc cốt lõi (tốt, đẹp, ổn, xịn) 
    và các cụm phủ định tương ứng (không tốt, chưa ổn, không đẹp, lương không cao).
    """
    # 1. Từ đơn tích cực độc lập hoặc đi kèm tiếng Anh
    pos_sample = "Công ty tốt, văn phòng đẹp, trang thiết bị xịn và pantry rất ổn."
    pos_res = preprocessor.calc_sentiment_features(pos_sample)
    assert pos_res["pos_w"] >= 4, f"Kỳ vọng ít nhất 4 từ tích cực (tốt, đẹp, xịn, ổn), thực tế: {pos_res}"
    assert pos_res["neg_w"] == 0
    assert pos_res["sentiment_ratio"] == 1.0

    # 2. Cụm phủ định của từ đơn không được bắt nhầm thành tích cực
    neg_sample = "Môi trường không tốt, sếp chưa chuyên nghiệp và lương không cao."
    neg_res = preprocessor.calc_sentiment_features(neg_sample)
    assert neg_res["neg_w"] >= 3, f"Kỳ vọng 3 cụm tiêu cực (không tốt, chưa chuyên nghiệp, không cao), thực tế: {neg_res}"
    assert neg_res["pos_w"] == 0, f"Không được bắt nhầm 'tốt' hay 'cao' thành pos_w, thực tế: {neg_res}"
    assert neg_res["sentiment_ratio"] == -1.0
def test_dataset_high_coverage(preprocessor):
    """Kiểm tra độ bao phủ trên mẫu 200 đánh giá thực tế từ reviews_cleaned.csv đạt trên 95%."""
    data_file = PROJECT_ROOT / "data" / "processed" / "reviews_cleaned.csv"
    if not data_file.exists():
        pytest.skip("Tệp reviews_cleaned.csv không tồn tại.")
    import pandas as pd
    df = pd.read_csv(data_file, nrows=200)
    texts = df["clean_basic_text"].fillna("")
    matched_count = 0
    for text in texts:
        res = preprocessor.calc_sentiment_features(text)
        if res["total_we"] > 0:
            matched_count += 1
    coverage = matched_count / len(df)
    assert coverage >= 0.95, f"Độ bao phủ thực tế chỉ đạt {coverage * 100:.2f}%, yêu cầu >= 95%"


def test_negation_scope_handling_complex_review(preprocessor):
    """Kiểm tra câu phủ định phức tạp nhiều vế được nhận diện chính xác là tiêu cực."""
    text = "Môi trường làm việc không được thân thiện, đồng nghiệp không hỗ trợ và ít cơ hội học hỏi."
    res = preprocessor.calc_sentiment_features(text)
    assert res["neg_w"] >= 2, f"Cần phát hiện ít nhất 2 cụm tiêu cực, thực tế: {res}"
    assert res["pos_w"] == 0, f"Không được nhận nhầm từ tích cực sau phủ định, thực tế: {res}"
    assert res["sentiment_ratio"] <= -0.8, f"Sentiment ratio phải tiêu cực rõ rệt, thực tế: {res['sentiment_ratio']}"


def test_clean_text_for_transformer_preserves_context(preprocessor):
    """
    Kiểm tra tiền xử lý chuyên biệt cho Transformer:
    - Bảo tồn dấu câu và ngữ pháp (. , !) cho cơ chế Self-Attention.
    - Giữ nguyên Emoji tự nhiên cho bộ từ vựng BPE.
    - Rút gọn ký tự lặp kéo dài về tối đa 2 ký tự.
    - Xóa URL và Email gây nhiễu.
    - Giữ nguyên teencode và thuật ngữ IT (không dịch thô).
    """
    raw_text = (
        "Công ty IT service này vuiiiii quáaaa! Sếp tốt, ko bắt OT nhiều 😡. "
        "Chi tiết xem tại https://itviec.com hoặc liên hệ hr@company.com nhé."
    )
    cleaned = preprocessor.clean_text_for_transformer(raw_text)

    # 1. Bảo tồn dấu câu
    assert "." in cleaned and "!" in cleaned, "Dấu câu phải được giữ lại cho Transformer"
    # 2. Giữ nguyên Emoji
    assert "😡" in cleaned, "Emoji phải được giữ nguyên cho BPE tokenizer của ViSoBERT"
    # 3. Rút gọn ký tự lặp
    assert "vuii" in cleaned and "quáa" in cleaned, "Ký tự lặp kéo dài phải được rút gọn về 2 ký tự"
    assert "vuiiiii" not in cleaned and "quáaaa" not in cleaned
    # 4. Xóa link và email
    assert "https://" not in cleaned and "itviec.com" not in cleaned
    assert "hr@company.com" not in cleaned
    # 5. Giữ nguyên teencode và tiếng Anh IT (không dịch 'IT' thành 'nó', không dịch 'OT')
    assert "IT service" in cleaned
    assert "ko" in cleaned
    assert "OT" in cleaned


