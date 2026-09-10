# KẾ HOẠCH CHI TIẾT - THÀNH VIÊN 4: THÀNH TRUNG
**Phân công:** `Evaluation, Sentiment Insights & Deployment`
**Thời gian thực hiện:** 4 Ngày cốt lõi (Tuần 2 & Tuần 3) & Giai đoạn Nước rút
**Mục tiêu chính:** Đánh giá toàn diện các mô hình (Confusion Matrix, Error Analysis), trích xuất Insight cảm xúc doanh nghiệp (WordCloud), xây dựng ứng dụng Web Demo (Streamlit), quay Video Demo và điều phối kịch bản thuyết trình.

---

## 📌 I. DANH SÁCH NHIỆM VỤ CHI TIẾT (DAY-BY-DAY CHECKLIST)

### 🟢 Ngày 1: Đánh giá Mô hình & Phân tích Lỗi sai (Evaluation & Error Analysis)
- [x] Nhận model Stacking và artifact final test từ **TV3 (Duy Khang)**.
- [x] **Tính toán đầy đủ các thang đo đánh giá trên tập Test cho model được chọn:**
  - **Accuracy** (Độ chính xác toàn diện).
  - **Precision, Recall, F1-score** theo từng lớp: `Positive`, `Neutral`, `Negative`.
  - **Macro F1-score** (Đánh giá công bằng giữa các lớp) & **Weighted F1-score**.
- [x] **Vẽ ma trận nhầm lẫn (Confusion Matrix) cho Stacking model được triển khai:**
  - So sánh baseline với policy Negative threshold 0,30 bằng `seaborn.heatmap`.
  - Lưu ảnh 300 DPI tại `reports/figures/stacking_confusion_matrix_threshold_comparison.png`.
- [ ] Vẽ lại Confusion Matrix cho từng model ứng viên nếu báo cáo cuối yêu cầu so sánh NB/LR/SVM/Stacking/ViSoBERT trên cùng một split và cùng prediction artifact.
- [x] **Phân tích lỗi sai chuyên sâu (Error Analysis) cho model được chọn:**
  - Trích xuất 10-15 câu mẫu mà mô hình đoán sai (ví dụ: Nhãn thật là Negative nhưng mô hình đoán Positive).
  - Phân tích nguyên nhân: Do câu châm biếm ("Công ty tuyệt vời, suốt ngày được OT xuyên đêm không lương!"), câu phủ định ("Không thể không khen"), hoặc do câu ngắn thiếu ngữ cảnh.

### 🟢 Ngày 2: Trích xuất Insight Cảm xúc Doanh nghiệp & WordCloud
- [x] Mở và chạy notebook `notebooks/05_company_sentiment_insights.ipynb`.
- [x] **Tạo WordCloud cảm xúc toàn diện:**
  - Tạo WordCloud cho toàn bộ tập đánh giá Tích cực (`wordcloud_positive_all.png`).
  - Tạo WordCloud cho toàn bộ tập đánh giá Tiêu cực (`wordcloud_negative_all.png`).
- [x] **Phân tích Case Study theo từng Doanh nghiệp cụ thể:**
  - Chỉ phân tích công ty đạt ngưỡng mẫu tối thiểu; luôn hiển thị số review và không xếp hạng công ty có mẫu quá nhỏ.
  - Thống kê tỷ lệ phần trăm đánh giá Tích cực / Tiêu cực tại công ty đó.
  - Tạo WordCloud riêng về các vấn đề bị phàn nàn nhiều nhất (Điểm yếu cần cải thiện) và các điểm được khen ngợi nhiều nhất (Điểm mạnh) của công ty.
  - Đưa ra đề xuất cải tiến thiết thực cho Ban lãnh đạo & HR của doanh nghiệp.

### 🟢 Ngày 3: Xây dựng Ứng dụng Web Demo Phân loại Cảm xúc (Deployment)
- [x] **Xây dựng ứng dụng Web tương tác bằng Streamlit:**
  - Tạo file `app.py` và cấu trúc các trang trong `app_pages/`.
  - Tải các artifact Text-only và Text + Lexicon; kiểm tra feature contract tương ứng trước khi inference.
  - Giao diện gồm:
    - **Ô nhập văn bản:** Cho phép người dùng nhập 1 câu review bất kỳ.
    - **Nút "Phân tích cảm xúc":** Tự động tiền xử lý $\rightarrow$ TF-IDF/Text + Lexicon $\rightarrow$ Stacking $\rightarrow$ threshold/Hybrid Decision Gate.
    - **Hiển thị kết quả:** Nhãn, xác suất ba lớp, token, đặc trưng TF-IDF và giải thích quy tắc quyết định.
  - Giao diện dark mode gồm:
    - **Trang Tổng quan (Overview):** Khái quát bài toán, cấu trúc dữ liệu, sơ đồ luồng pipeline.
    - **Trang Dashboard Insight:** Biểu đồ phân tích cảm xúc và WordCloud của các công ty IT.
    - **Trang Benchmark:** So sánh các hướng mô hình và chỉ số từng lớp.
    - **Trang Dự đoán thời gian thực:** Chọn Text-only hoặc Text + Lexicon, xem xác suất và chẩn đoán đầu vào.
    - **Trang Evaluation:** Confusion Matrix, sensitivity analysis và 15 mẫu lỗi thật.
- [x] Chạy thử nghiệm cục bộ và kiểm tra giao diện bằng Playwright trên desktop.

### 🟢 Giai đoạn Nước rút: Chuyên trách Live Demo, Quay Video & Soạn Kịch bản
- [x] Hoàn thiện notebook phân tích insight 180 công ty IT (`05_company_sentiment_insights.ipynb`) và các ảnh WordCloud 300 DPI.
- [x] Xây dựng hoàn chỉnh ứng dụng Web Demo Streamlit giao diện Dark mode chuyên nghiệp (`app.py`, `app_pages/`).
- [ ] **CHUYÊN TRÁCH 100% LIVE DEMO, QUAY VIDEO VÀ SOẠN KỊCH BẢN**:
  - **Quay 01 Video Clip Demo Full HD (3 – 5 phút)**: Giới thiệu trọn vẹn 3 phân hệ (Overview, Company Insights WordCloud, Real-time Prediction), thuyết minh rõ ràng và test đúng case study câu phủ định khó có giải thích XAI.
  - **Trực tiếp thao tác Live Demo** trên máy chiếu khi Hội đồng bảo vệ đồ án yêu cầu.
  - **Soạn 01 File Kịch bản Thuyết trình chi tiết (Presentation Script)**: Phân vai lời thoại từng phút cho cả nhóm (căn chuẩn thời gian 15-18 phút).
  - **Soạn 01 Bộ tài liệu Câu hỏi Phản biện & Câu trả lời mẫu (Q&A Guide)**: Chuẩn bị 10 câu hỏi hóc búa của Hội đồng để Khang, Duy, Trung học thuộc và tự tin đối đáp.
  - Nộp video và kịch bản cho **Trưởng nhóm (Hoàng Hôn)** duyệt nghiệm thu.

---

## 📦 II. ĐẦU VÀO & ĐẦU RA (INPUTS & OUTPUTS)

* **Đầu vào (Inputs):**
  - File mô hình từ TV3 và pipeline từ TV1 & TV2.
  - Toàn bộ kết quả insight từ `05_company_sentiment_insights.ipynb`.
* **Đầu ra (Outputs bàn giao):**
  - Notebook hoàn chỉnh: [notebooks/05_company_sentiment_insights.ipynb](../../notebooks/05_company_sentiment_insights.ipynb).
  - Ứng dụng Web Demo Streamlit hoàn chỉnh (`app.py`).
  - **01 Video Clip Demo Full HD (3–5 phút)** sẵn sàng nộp kèm đồ án hoặc chiếu dự phòng.
  - **01 File Kịch bản Thuyết trình phân vai chi tiết** (15–18 phút).
  - **01 Bộ tài liệu Hỏi - Đáp Phản biện (Q&A Defense Guide)**.
