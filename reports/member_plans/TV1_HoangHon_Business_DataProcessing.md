# KẾ HOẠCH CHI TIẾT - THÀNH VIÊN 1: HOÀNG HÔN (TRƯỞNG NHÓM)
**Phân công:** `Business & Data Processing`  
**Thời gian thực hiện:** 3 Ngày cốt lõi (Tuần 1) & Điều phối suốt 3 tuần  
**Mục tiêu chính:** Xác định bài toán nghiệp vụ, xây dựng pipeline tiền xử lý văn bản tiếng Việt chuẩn mực, gán nhãn và tạo bộ dữ liệu sạch.

---

## 📌 I. DANH SÁCH NHIỆM VỤ CHI TIẾT (DAY-BY-DAY CHECKLIST)

### 🟢 Ngày 1: Business Objective & Quản lý Tổng thể
- [ ] **Xác định mục tiêu bài toán (Business Understanding):**
  - Làm rõ bài toán phân loại cảm xúc 3 lớp: `Positive`, `Negative`, `Neutral` trên dữ liệu đánh giá ITviec.
  - Thiết kế luồng xử lý tổng thể của hệ thống (Pipeline Architecture).
- [ ] **Khởi tạo và chuẩn hóa môi trường dự án:**
  - Thiết lập repo Git, kiểm tra file `requirements.txt` và phân quyền cho các thành viên.
  - Phân phát kế hoạch chi tiết cho TV2, TV3, TV4.

### 🟢 Ngày 2: Xây dựng Pipeline Tiền xử lý Dữ liệu Text (Data Processing)
- [ ] **Hoàn thiện module `src/preprocessing.py`:**
  - Chuẩn hóa bảng mã Unicode sang chuẩn **NFC** (`unicodedata.normalize`).
  - Xử lý biểu tượng cảm xúc: Ánh xạ emoji/emojicon sang từ ngữ mang cảm xúc tích cực/tiêu cực từ [emojicon.txt](file:///d:/Trí tuệ nhân tạo/HK2/Xử lý ngôn ngữ tự nhiên/Do_An_Sentiment_Analysis/data/dictionaries/emojicon.txt), [positive_emoji.txt](file:///d:/Trí tuệ nhân tạo/HK2/Xử lý ngôn ngữ tự nhiên/Do_An_Sentiment_Analysis/data/dictionaries/positive_emoji.txt), [negative_emoji.txt](file:///d:/Trí tuệ nhân tạo/HK2/Xử lý ngôn ngữ tự nhiên/Do_An_Sentiment_Analysis/data/dictionaries/negative_emoji.txt).
  - Chuẩn hóa teencode / từ viết tắt IT (`cty`, `ot`, `dev`, `pm`,...) bằng [teencode.txt](file:///d:/Trí tuệ nhân tạo/HK2/Xử lý ngôn ngữ tự nhiên/Do_An_Sentiment_Analysis/data/dictionaries/teencode.txt).
  - Chuẩn hóa lỗi chính tả và tiếng Anh bằng [wrong-word.txt](file:///d:/Trí tuệ nhân tạo/HK2/Xử lý ngôn ngữ tự nhiên/Do_An_Sentiment_Analysis/data/dictionaries/wrong-word.txt) và [english-vnmese.txt](file:///d:/Trí tuệ nhân tạo/HK2/Xử lý ngôn ngữ tự nhiên/Do_An_Sentiment_Analysis/data/dictionaries/english-vnmese.txt).
  - Tách từ tiếng Việt (Word Segmentation) bằng `underthesea.word_tokenize`.
  - Lọc bỏ stopwords bằng [vietnamese-stopwords.txt](file:///d:/Trí tuệ nhân tạo/HK2/Xử lý ngôn ngữ tự nhiên/Do_An_Sentiment_Analysis/data/dictionaries/vietnamese-stopwords.txt).
- [ ] **Tạo 2 trường văn bản chuẩn hóa trong DataFrame:**
  - `clean_basic_text`: Chỉ làm sạch ký tự lạ, emoji và teencode (giữ nguyên cấu trúc câu).
  - `clean_advance_text`: Đã tách từ và loại bỏ stopwords.

### 🟢 Ngày 3: Trích xuất đặc trưng Lexicon, Gán nhãn & Xuất dữ liệu
- [ ] **Trích xuất đặc trưng Lexicon:**
  - Đếm số từ tích cực (`pos_w`) và tiêu cực (`neg_w`) dựa trên [positive_words.txt](file:///d:/Trí tuệ nhân tạo/HK2/Xử lý ngôn ngữ tự nhiên/Do_An_Sentiment_Analysis/data/dictionaries/positive_words.txt) và [negative_words.txt](file:///d:/Trí tuệ nhân tạo/HK2/Xử lý ngôn ngữ tự nhiên/Do_An_Sentiment_Analysis/data/dictionaries/negative_words.txt).
  - Đếm số icon tích cực (`pos_e`) và tiêu cực (`neg_e`).
  - Tính toán tỷ lệ cảm xúc: `sentiment_ratio = (pos_w + pos_e - neg_w - neg_e) / (pos_w + pos_e + neg_w + neg_e + 1)`.
- [ ] **Gán nhãn & Kiểm thử chất lượng nhãn:**
  - Gán nhãn cảm xúc 3 lớp (`Positive`, `Neutral`, `Negative`).
  - Xuất file kết quả sạch: `data/processed/reviews_cleaned.xlsx`.
- [ ] **Bàn giao:** Chuyển giao file `reviews_cleaned.xlsx` cho **TV2 (Văn Duy)** và **TV3 (Duy Khang)**.

### 🟢 Giai đoạn Nước rút: Kiểm soát Chất lượng, Giám sát Kỹ thuật & Nghiệm thu (QA Lead)
- [x] Hoàn thiện pipeline tiền xử lý 2 tầng (`clean_basic_text` & `clean_advance_text`).
- [x] Mở rộng bộ từ điển, đối sánh cụm từ tham lam (Greedy Matching 99.75%) và thuật toán nhận diện phạm vi phủ định (**Negation Scope Detection**).
- [x] Tích hợp bộ máy **Hybrid Decision Gate** (`src/app_services.py`) xử lý trường hợp phủ định biên.
- [ ] Giám sát triển khai **Phương án 2** (Mô hình `Text + Lexicon` 5.005 đặc trưng song song) và duy trì 39 unit tests pass 100%.
- [ ] **Kiểm tra Báo cáo toàn văn**: Đọc soát, bắt lỗi số liệu và duyệt cuốn Báo cáo (Word/PDF 6 chương) do Văn Duy nộp.
- [ ] **Kiểm tra Bộ Slide**: Duyệt bộ Slide trình chiếu (18-20 slides) do Duy Khang nộp.
- [ ] **Kiểm tra Video & Kịch bản**: Duyệt Video Clip Demo Full HD (3-5 phút) và kịch bản thuyết trình do Thành Trung nộp.
- [ ] **Duyệt xuất xưởng (Final Sign-off)**: Bấm nút nộp bài chính thức đại diện cho nhóm.

---

## 📦 II. ĐẦU VÀO & ĐẦU RA (INPUTS & OUTPUTS)

* **Đầu vào (Inputs):**
  - Dữ liệu thô: [Reviews.xlsx](file:///d:/Trí tuệ nhân tạo/HK2/Xử lý ngôn ngữ tự nhiên/Do_An_Sentiment_Analysis/data/raw/Reviews.xlsx) (8,417 mẫu).
  - Bộ từ điển: `data/dictionaries/` (teencode, stopwords, emoji, wrong-words).
* **Đầu ra (Outputs bàn giao):**
  - Code module hoàn chỉnh: [src/preprocessing.py](file:///d:/Trí tuệ nhân tạo/HK2/Xử lý ngôn ngữ tự nhiên/Do_An_Sentiment_Analysis/src/preprocessing.py).
  - Notebook hoàn chỉnh: [notebooks/02_text_preprocessing.ipynb](file:///d:/Trí tuệ nhân tạo/HK2/Xử lý ngôn ngữ tự nhiên/Do_An_Sentiment_Analysis/notebooks/02_text_preprocessing.ipynb).
  - File dữ liệu sạch: `data/processed/reviews_cleaned.xlsx` (có đủ cột `clean_basic_text`, `clean_advance_text`, `pos_w`, `neg_w`, `sentiment_ratio`, `sentiment`).
  - Kho mã nguồn Git chuẩn mực, sạch sẽ, đạt 39/39 tests pass.
  - Biên bản nghiệm thu và phê duyệt chất lượng cho 3 sản phẩm: Báo cáo Word/PDF, Slide PPTX và Video Demo.
