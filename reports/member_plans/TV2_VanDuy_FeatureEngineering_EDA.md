# KẾ HOẠCH CHI TIẾT - THÀNH VIÊN 2: VĂN DUY
**Phân công:** `Feature Engineering & EDA`  
**Thời gian thực hiện:** 4 Ngày cốt lõi (Tuần 1 & Đầu Tuần 2)  
**Mục tiêu chính:** Phân tích khám phá dữ liệu (EDA), xây dựng pipeline NLP text-only bằng TF-IDF, khảo sát lexicon/aspect bằng ablation, xử lý mất cân bằng và bàn giao development/final-test có contract tái lập được.

---

## 📌 I. DANH SÁCH NHIỆM VỤ CHI TIẾT (DAY-BY-DAY CHECKLIST)

### 🟢 Ngày 1: Khám phá Dữ liệu Toàn diện (EDA)
- [x] Mở và chạy notebook [notebooks/01_data_exploration_eda.ipynb](../../notebooks/01_data_exploration_eda.ipynb).
- [x] **Thực hiện các phân tích thống kê:**
  - Thống kê phân bố số sao đánh giá (1 sao - 5 sao).
  - Phân tích phân bố các nhãn cảm xúc: Tỷ lệ % của `Positive`, `Neutral`, `Negative`.
  - Phân tích độ dài câu (số lượng từ trong `What I liked`, `Suggestions for improvement`).
  - Kiểm tra mức độ tương quan giữa năm điểm khía cạnh thực có trong dữ liệu với weak label; không suy diễn quan hệ nhân quả và không báo cáo khía cạnh OT vì schema không có trường này.
  - Phân tích phân bố theo công ty/thời gian, text trùng, lexicon coverage và bất nhất giữa `Recommend?` với weak label.
- [x] Xuất và lưu các biểu đồ EDA chất lượng cao vào `reports/figures/` (ví dụ: `eda_rating_distribution.png`, `eda_sentiment_counts.png`).

### 🟢 Ngày 2: Xây dựng Module Trích xuất Đặc trưng (Feature Engineering)
- [x] Hoàn thiện module [src/features.py](../../src/features.py).
- [x] **Cấu hình trích xuất đặc trưng văn bản (Text Features):**
  - Sử dụng `TfidfVectorizer` trên trường `clean_advance_text`:
    - Thử nghiệm `ngram_range=(1, 1)` và `ngram_range=(1, 2)`.
    - Thiết lập `max_features` tối ưu (3000 - 5000 từ).
    - Sử dụng `sublinear_tf=True` và lọc bỏ các từ xuất hiện quá ít (`min_df=2`).
  - Chọn cấu hình bằng 5-fold CV trên development và lưu vectorizer text-only vào `models/text_tfidf_vectorizer.joblib`.

### 🟢 Ngày 3: Ghép đặc trưng số & Xử lý Mất cân bằng dữ liệu (Imbalanced Data)
- [x] **Ablation đặc trưng số (Numerical Features):**
  - Lấy các thuộc tính số do TV1 tạo ra: `pos_w`, `neg_w`, `sentiment_ratio` và điểm rating thành phần (nếu có).
  - Fit `MinMaxScaler` bên trong từng fold development.
  - So sánh text-only, text + lexicon, aspect-only và structured hybrid. Chỉ text-only được bàn giao làm pipeline NLP chính.
- [x] **Chiến lược chia tập & Xử lý mất cân bằng:**
  - Loại text trùng/bất đồng rồi chia **80% development - 20% final test** với `stratify=y`; final test không được dùng để chọn feature.
  - Khảo sát và thử nghiệm kỹ thuật cân bằng lớp:
    - Cách 1: Áp dụng `SMOTE` từ thư viện `imbalanced-learn` trên tập Train.
    - Cách 2: Thiết lập `class_weight='balanced'` cho các mô hình.
- [x] **Bàn giao:** Chuyển giao ma trận đặc trưng $X_{train}, X_{test}, y_{train}, y_{test}$ và file dữ liệu cho **TV3 (Duy Khang)**.

### 🟢 Giai đoạn Nước rút: Chuyên trách Viết Báo cáo Toàn văn (Lead Report Writer)
- [x] Soạn thảo báo cáo EDA & Feature Engineering khoa học tại `reports/eda_feature_engineering.md`.
- [x] Hoàn thành thí nghiệm Ablation 5-fold CV: chứng minh `Text + Lexicon` đạt **Macro F1 0.5658** (tăng so với Text-only 0.5579), tăng Recall Negative lên 48.24%.
- [x] Xuất 10 biểu đồ chuẩn 300 DPI tại `reports/figures/` phục vụ báo cáo và slide.
- [ ] **CHUYÊN TRÁCH 100% VIẾT BÁO CÁO TOÀN VĂN (Word / PDF)**:
  - Soạn thảo đầy đủ 6 Chương theo khung đề cương chuẩn `reports/final_report_outline.md`.
  - Tích hợp số liệu thực nghiệm của TV1 (tiền xử lý, từ điển), TV2 (EDA, ablation), TV3 (modeling, Stacking, ViSoBERT) và TV4 (insights, XAI, web demo).
  - Định dạng chuẩn học thuật (Times New Roman 13, dãn dòng 1.3-1.5, lề chuẩn), xuất file Word `.docx` và file PDF hoàn chỉnh.
  - Nộp bản thảo cho **Trưởng nhóm (Hoàng Hôn)** duyệt nghiệm thu trước khi xuất xưởng.

---

## 📦 II. ĐẦU VÀO & ĐẦU RA (INPUTS & OUTPUTS)

* **Đầu vào (Inputs):**
  - File dữ liệu sạch từ TV1: `data/processed/reviews_cleaned.xlsx`.
  - Kết quả mô hình từ TV3: `reports/modeling_hyperparameter_tuning.md`, `best_sentiment_model.joblib`.
  - Kết quả insight từ TV4: `05_company_sentiment_insights.ipynb`, biểu đồ WordCloud.
* **Đầu ra (Outputs bàn giao):**
  - Notebook hoàn chỉnh: [notebooks/01_data_exploration_eda.ipynb](../../notebooks/01_data_exploration_eda.ipynb).
  - Module code: [src/features.py](../../src/features.py) và các scripts thực nghiệm trong `scripts/`.
  - File ma trận đặc trưng: `models/train_test_features.joblib`, `models/hybrid_train_test_features.joblib`.
  - Toàn bộ hình ảnh biểu đồ EDA 300 DPI trong `reports/figures/`.
  - **01 Cuốn Báo cáo Đồ án Toàn văn Hoàn chỉnh (File Word & File PDF)** 6 Chương (35–45 trang).
