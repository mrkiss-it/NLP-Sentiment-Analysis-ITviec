# ĐỀ CƯƠNG BÁO CÁO ĐỒ ÁN NLP: PHÂN TÍCH CẢM XÚC ĐÁNH GIÁ ITVIEC
*(Chuyên sâu: Sentiment Analysis & Employee Feedback Analytics)*

---

## CHƯƠNG 1: TỔNG QUAN VÀ ĐẶT VẤN ĐỀ
1.1. Bối cảnh đề tài và tầm quan trọng của việc phân tích ý kiến đánh giá nhân sự trong ngành CNTT.  
1.2. Mục tiêu nghiên cứu:
   - Xây dựng hệ thống tự động phân loại cảm xúc đánh giá (Tích cực, Tiêu cực, Trung tính).
   - So sánh hiệu năng giữa các thuật toán Machine Learning truyền thống, mô hình Ensemble và mô hình Pretrained Transformer.
   - Khám phá các chủ đề/từ khóa then chốt tác động đến cảm xúc nhân viên theo từng công ty.  
1.3. Bố cục của báo cáo.

---

## CHƯƠNG 2: TỔNG QUAN DỮ LIỆU & TIỀN XỬ LÝ (DATA & PREPROCESSING)
2.1. Giới thiệu bộ dữ liệu ITviec Reviews (Cấu trúc bảng, các trường nội dung review, điểm đánh giá thành phần).  
2.2. Khám phá dữ liệu (EDA):
   - Phân tích phân bố số sao rating và mức độ mất cân bằng lớp.
   - Thống kê độ dài văn bản đánh giá, phân bố từ ngữ.
   - Phân tích tương quan giữa điểm các khía cạnh (Lương thưởng, Đào tạo, Quản lý, Môi trường, OT) với cảm xúc chung.  
2.3. Quy trình tiền xử lý văn bản tiếng Việt chuyên sâu:
   - Chuẩn hóa mã Unicode NFC.
   - Xử lý biểu tượng cảm xúc (Emoji/Emojicon) thành từ ngữ mang sắc thái.
   - Chuẩn hóa viết tắt (teencode), thuật ngữ IT và sửa lỗi chính tả.
   - Tách từ tiếng Việt (Word Segmentation) bằng `underthesea` và đối sánh cụm từ tham lam (Greedy Matching).
   - Lọc bỏ stopwords tiếng Việt (tối ưu hóa bảo lưu từ phủ định và định lượng: `chưa`, `thiếu`, `ít`).
   - Thuật toán nhận diện cửa sổ phạm vi phủ định (Negation Scope Detection).
2.4. Chiến lược gán nhãn cảm xúc và tạo tập dữ liệu huấn luyện (Rating-derived Weak Labels và audit độc lập).

---

## CHƯƠNG 3: BIỂU DIỄN VĂN BẢN VÀ MÔ HÌNH HỌC MÁY (MODELING)
3.1. Phương pháp trích xuất đặc trưng văn bản:
   - TF-IDF Vectorizer (N-gram 1-2, sublinear TF, phân tích tham số tối ưu 5.000 chiều).
   - Trích xuất đặc trưng Lexicon cảm xúc (độ bao phủ 99.75%, xử lý phủ định).
   - Biểu diễn ngữ cảnh với Pretrained Language Model (ViSoBERT / PhoBERT).
3.2. Thí nghiệm đối chứng nhóm đặc trưng (Feature Ablation Study):
   - So sánh 5-fold Stratified CV: Text-only (0.5579) vs. Text + Lexicon (0.5658) vs. Text + Aspect (0.7369) vs. Full Hybrid (0.7389).
   - Phân tích rủi ro data shortcut của điểm khía cạnh và lý do duy trì pipeline Text-only.
3.3. Thiết kế các mô hình học máy:
   - Mô hình 1: Multinomial Naive Bayes (Baseline).
   - Mô hình 2: Logistic Regression (với trọng số lớp cân bằng).
   - Mô hình 3: Support Vector Machine (Linear SVM với Platt scaling / Calibrated proba).
   - Mô hình 4: Random Forest Classifier.
   - Mô hình 5: Stacking Ensemble Classifier (NB + LR + SVM).
   - Mô hình 6: Zero-shot / Fine-tuned ViSoBERT (Deep Learning trên GPU).
3.4. Kỹ thuật xử lý mất cân bằng dữ liệu (`class_weight='balanced'` vs. SMOTE) và tinh chỉnh siêu tham số (GridSearchCV với 5-Fold Stratified CV).
3.5. Kiến trúc suy luận thực tế: Bộ máy ra quyết định lai (Hybrid Decision Gate) kết hợp xác suất ML và tri thức ngữ nghĩa tiên nghiệm.

---

## CHƯƠNG 4: KẾT QUẢ THỰC NGHIỆM VÀ ĐÁNH GIÁ (EVALUATION)
4.1. Môi trường thực nghiệm và các thang đo đánh giá (Accuracy, Macro F1, Weighted F1, Precision, Recall).  
4.2. Bảng tổng hợp so sánh hiệu năng giữa các mô hình trên tập Cross-validation và tập Final Test độc lập đã khóa.  
4.3. Phân tích ma trận nhầm lẫn (Confusion Matrix) và hiện tượng bẫy Accuracy trên dữ liệu mất cân bằng.  
4.4. Phân tích lỗi sai chuyên sâu (Qualitative Error Analysis):
   - Phân tích các trường hợp mô hình đoán sai (câu châm biếm, phủ định ghép nhiều vế, câu chứa cả ý khen và chê).
   - Case study câu phủ định phức tạp: *"Môi trường làm việc không được thân thiện, đồng nghiệp không hỗ trợ và ít cơ hội học hỏi."* — So sánh trước và sau khi có Negation Scope & Hybrid Gate.
   - Đánh giá ảnh hưởng của bước tiền xử lý đối với độ chính xác của mô hình.

---

## CHƯƠNG 5: PHÂN TÍCH INSIGHT CẢM XÚC DOANH NGHIỆP & TRIỂN KHAI (BUSINESS INSIGHTS & DEMO)
5.1. Trực quan hóa đám mây từ khóa (WordCloud) cảm xúc Tích cực và Tiêu cực.  
5.2. Phân tích cảm xúc theo từng doanh nghiệp (Case Study các công ty IT tiêu biểu):
   - Tỷ lệ hài lòng / không hài lòng của nhân viên.
   - Các chủ đề được khen ngợi nhiều nhất (Điểm mạnh của công ty).
   - Các vấn đề bị phàn nàn nhiều nhất (Chế độ OT, Lương thưởng, Quy trình quản lý).  
5.3. Xây dựng ứng dụng Demo trực quan (Streamlit Dashboard):
   - Giao diện Dark mode tối ưu hóa cho màn hình ultrawide.
   - Dự đoán thời gian thực tích hợp Explainable AI (XAI) bóc tách từ ngữ sắc thái.
5.4. Đề xuất giải pháp thực tế cho ban quản lý doanh nghiệp và phòng nhân sự (HR).

---

## CHƯƠNG 6: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
6.1. Những kết quả chính đạt được của đề tài.  
6.2. Những điểm hạn chế còn tồn tại.  
6.3. Hướng phát triển trong tương lai (Phân tích cảm xúc theo từng khía cạnh chi tiết - Aspect-Based Sentiment Analysis ABSA, ứng dụng LLM Agent).
