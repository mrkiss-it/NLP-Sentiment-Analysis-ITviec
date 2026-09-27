# KẾ HOẠCH & PHÂN CHIA CÔNG VIỆC ĐỒ ÁN NLP: PHÂN TÍCH CẢM XÚC ĐÁNH GIÁ ITVIEC
*(Chuyên sâu 100% về Sentiment Analysis - Theo bình chọn của nhóm)*

- **Thời gian thực hiện:** 3 tuần (21 ngày)
- **Danh sách thành viên:**
  1. **TV1: Hoàng Hôn** (Trưởng nhóm) - `Business & Data Processing`
  2. **TV2: Văn Duy** - `Feature Engineering & EDA`
  3. **TV3: Duy Khang** - `Modeling & Hyperparameter Tuning`
  4. **TV4: Thành Trung** - `Evaluation, Sentiment Insights & Deployment`

---

## 👥 I. BẢNG PHÂN CHIA NHIỆM VỤ THEO BÌNH CHỌN (RACI MATRIX)

| Thành viên | Phân công | Nhiệm vụ kỹ thuật chi tiết (Tập trung Sentiment Analysis) | Phần Báo cáo phụ trách |
| :--- | :--- | :--- | :--- |
| **👑 TV1: Hoàng Hôn**<br>*(Trưởng nhóm)* | **Business & Data Processing**<br>*(3 Ngày)* | - **Business Understanding:** Xác định mục tiêu bài toán phân loại cảm xúc đa lớp (Positive, Neutral, Negative), thiết kế luồng pipeline NLP tổng thể.<br>- **Data Preprocessing:** Xây dựng module `src/preprocessing.py`: chuẩn hóa Unicode NFC, xử lý emoji/emojicon mang cảm xúc, dịch teencode, sửa từ sai chính tả, lọc stopwords, tách từ `underthesea`.<br>- **Tạo tập dữ liệu sạch:** Gán nhãn cảm xúc và xuất `data/processed/reviews_cleaned.xlsx` bàn giao cho TV2 & TV3.<br>- **Quản lý chung:** Quản lý Repo Git, điều phối tiến độ, tổng hợp toàn văn Báo cáo & thiết kế Slide thuyết trình. | - **Chương 1:** Tổng quan & Đặt vấn đề<br>- **Mục 2.3:** Quy trình tiền xử lý văn bản tiếng Việt<br>- **Tổng hợp toàn bộ Báo cáo & Slide** |
| **👨‍💻 TV2: Văn Duy** | **Feature Engineering & EDA**<br>*(4 Ngày)* | - **Exploratory Data Analysis (EDA):** Chạy `01_data_exploration_eda.ipynb`, phân tích phân bố số sao rating, độ dài review, thống kê từ rỗng, phân tích tương quan điểm số các khía cạnh (Lương, Đào tạo, Quản lý, OT) với cảm xúc chung.<br>- **Feature Engineering:** Xây dựng `src/features.py`: trích xuất đặc trưng TF-IDF (N-gram 1-2, sublinear TF), BoW, trích xuất đặc trưng điểm số từ điển cảm xúc Lexicon tích cực/tiêu cực.<br>- **Data Preparation:** Chia tập Train/Test (Stratified 80/20) và áp dụng kỹ thuật cân bằng lớp (SMOTE / Class Weighting). | - **Mục 2.1 - 2.2:** Giới thiệu dữ liệu & Phân tích khám phá (EDA)<br>- **Mục 3.1:** Phương pháp trích xuất đặc trưng văn bản |
| **👨‍💻 TV3: Duy Khang** | **Modeling & Hyperparameter Tuning**<br>*(4 Ngày)* | - **Mô hình hóa (Modeling):** Xây dựng `src/models.py`, chạy `03_sentiment_modeling_ml.ipynb` với ít nhất **4 mô hình ML**: Multinomial Naive Bayes, Logistic Regression, Linear SVM, Random Forest.<br>- **Mô hình nâng cao:** Xây dựng mô hình kết hợp **Stacking Ensemble Classifier** và thử nghiệm **Pretrained ViSoBERT / PhoBERT** (`04_sentiment_modeling_deeplearning.ipynb`).<br>- **Hyperparameter Tuning:** Sử dụng `GridSearchCV` / `RandomizedSearchCV` với K-Fold CV để tìm bộ siêu tham số tối ưu.<br>- **Lưu trữ:** Lưu model tốt nhất vào `models/best_sentiment_model.joblib`. | - **Mục 3.2 - 3.3:** Thiết kế mô hình học máy, Ensemble & Tinh chỉnh siêu tham số |
| **👨‍💻 TV4: Thành Trung** | **Evaluation, Sentiment Insights & Deployment**<br>*(4 Ngày)* | - **Model Evaluation & Error Analysis:** Tính toán bảng so sánh số liệu (Accuracy, Macro F1, Precision, Recall), vẽ **Confusion Matrix**, phân tích các trường hợp mô hình đoán sai (Error Analysis).<br>- **Company Sentiment Insights & WordCloud:** Chạy `05_company_sentiment_insights.ipynb`, tạo WordCloud từ khóa tích cực/tiêu cực theo từng công ty (Case study 2-3 công ty IT tiêu biểu).<br>- **Deployment / Demo Web:** Xây dựng giao diện Demo tương tác bằng **Streamlit / Gradio** (nhập review -> dự đoán nhãn cảm xúc và độ tin cậy theo thời gian thực). | - **Chương 4:** Kết quả thực nghiệm & Đánh giá mô hình<br>- **Chương 5:** Phân tích Insight cảm xúc doanh nghiệp & Demo<br>- **Chương 6:** Kết luận & Hướng phát triển |

---

## 📅 II. TIMELINE CHI TIẾT 3 TUẦN (21 NGÀY)

```mermaid
gantt
    title Lịch trình thực hiện Đồ án Phân tích Cảm xúc NLP
    dateFormat  YYYY-MM-DD
    section Tuần 1: Dữ liệu, EDA & Tiền xử lý
    TV1: Thiết lập Repo, Pipeline & Làm sạch text (Hoàng Hôn) :a1, 2026-08-28, 4d
    TV1: Gán nhãn & Xuất reviews_cleaned.xlsx (Hoàng Hôn)     :a2, after a1, 2d
    TV2: Thực hiện phân tích EDA & Trực quan (Văn Duy)         :a3, 2026-08-28, 4d
    TV2: Xây dựng Module TF-IDF & Features (Văn Duy)          :a4, 2026-09-01, 3d
    TV3: Chuẩn bị khung huấn luyện & Baseline NB (Duy Khang)  :a5, 2026-08-31, 4d
    TV4: Khảo sát Error Analysis & Giao diện Demo (Thành Trung):a6, 2026-08-31, 4d

    section Tuần 2: Huấn luyện, Tối ưu & Trích xuất Insight
    TV3: Huấn luyện 4 mô hình ML & Tuning K-Fold (Duy Khang)  :b1, 2026-09-04, 5d
    TV3: Xây dựng Stacking & Thử nghiệm ViSoBERT (Duy Khang)  :b2, 2026-09-07, 4d
    TV4: Tính toán Confusion Matrix & Phân tích lỗi (Trung)   :b3, 2026-09-04, 5d
    TV4: Trích xuất Insight cảm xúc công ty & WordCloud (Trung):b4, 2026-09-08, 4d
    TV1 & TV2: Viết nháp Chương 1, 2, 3 Báo cáo               :b5, 2026-09-07, 4d

    section Tuần 3: Demo, Báo cáo & Slide
    TV4: Hoàn thiện Web Demo Streamlit/Gradio (Thành Trung)   :c1, 2026-09-11, 4d
    TV3: Hoàn tất bảng số liệu & Bàn giao checkpoint model    :c2, 2026-09-11, 3d
    TV1: Tổng hợp toàn văn Báo cáo (Word/PDF) (Hoàng Hôn)     :c3, 2026-09-13, 5d
    TV1: Thiết kế Slide & Họp tập dượt thuyết trình           :c4, 2026-09-15, 3d
```

---

## 🎯 BẢNG GIAO HẸN SẢN PHẨM CUỐI CÙNG (DELIVERABLES)

| STT | Sản phẩm bàn giao | Người phụ trách chính | Hạn chót | Trạng thái |
| :---: | :--- | :--- | :---: | :---: |
| 1 | File dữ liệu sạch `data/processed/reviews_cleaned.xlsx` | **TV1 (Hoàng Hôn)** | Hết Ngày 6 | ✅ **100% (Hoàn thành)** |
| 2 | Báo cáo EDA + Module trích xuất đặc trưng `src/features.py` | **TV2 (Văn Duy)** | Hết Ngày 7 | ✅ **100% (Hoàn thành)** |
| 3 | Bảng so sánh 4+ mô hình ML, Stacking, ViSoBERT + File model `.joblib` | **TV3 (Duy Khang)** | Hết Ngày 12 | ✅ **100% (Hoàn thành)** |
| 4 | Bộ WordCloud cảm xúc theo công ty + Confusion Matrix + Web Demo | **TV4 (Thành Trung)** | Hết Ngày 14 | ✅ **100% (Hoàn thành)** |
| 5 | Báo cáo toàn văn đầy đủ 6 chương (Word/PDF) | **TV2 (Văn Duy)** & Nhóm | Ngày 18 | ✅ **100% (Hoàn thành)** |
| 6 | Bộ Slide trình chiếu 15 trang chuẩn hóa (PPTX/PDF) | **TV3 (Duy Khang)** & Nhóm | Ngày 20 | ✅ **100% (Hoàn thành)** |
