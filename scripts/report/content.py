# -*- coding: utf-8 -*-
"""Nội dung Báo cáo đồ án toàn văn 6 chương.

Mọi con số trong tài liệu này lấy từ các artifact đã chạy thật trong repo:
  reports/aspect_hybrid_ablation.csv, reports/tv2_vectorizer_comparison.csv,
  reports/tv2_balancing_comparison.csv, reports/evaluation/*.csv|json,
  reports/modeling_hyperparameter_tuning.md, models/*_manifest.json.
Không điền số ước lượng.
"""

META = {
    "org": "Đại học Quốc gia Thành phố Hồ Chí Minh",
    "school": "Trường Đại học Công nghệ Thông tin",
    "faculty": "Khoa Khoa học Máy tính",
    "logo": "assets/uit-logo.png",
    "doc_kind": "Báo cáo đồ án môn học",
    "course": "Môn học: Xử lý ngôn ngữ tự nhiên",
    "topic_label": "Đề tài:",
    "title": "Phân tích cảm xúc đánh giá nhân sự ngành Công nghệ thông tin "
             "trên nền tảng ITviec",
    "advisor_label": "Giảng viên hướng dẫn:",
    "advisor": "Thầy Đặng Văn Thìn",
    "team_label": "Nhóm sinh viên thực hiện:",
    "team_name": "Nhóm 9",
    "members": [
        ("1. Trần Hoàng Hôn - 26410046 (Trưởng nhóm)", True),
        ("2. Nguyễn Duy Khang - 26410055", False),
        ("3. Vũ Văn Duy - 26410031", False),
        ("4. Phạm Thành Trung - 26410141", False),
    ],
    "author": "Trần Hoàng Hôn, Nguyễn Duy Khang, Vũ Văn Duy, Phạm Thành Trung",
    "place_date": "TP. Hồ Chí Minh - Tháng 09/2026",
}

BLOCKS = []
B = BLOCKS.append

# ==========================================================================
# PHẦN MỞ ĐẦU
# ==========================================================================
B(("h1", "MỤC LỤC"))
B(("toc",))
B(("pagebreak",))

B(("h1", "DANH MỤC TỪ VIẾT TẮT VÀ THUẬT NGỮ"))
B(("table", "Bảng 0.1. Danh mục từ viết tắt và thuật ngữ sử dụng trong báo cáo",
   ["Từ viết tắt", "Dạng đầy đủ", "Giải thích ngắn gọn"],
   [
       ["NLP", "Natural Language Processing", "Xử lý ngôn ngữ tự nhiên"],
       ["TF-IDF", "Term Frequency – Inverse Document Frequency",
        "Trọng số từ theo tần suất trong tài liệu và độ hiếm trên toàn tập"],
       ["BoW", "Bag-of-Words", "Biểu diễn văn bản bằng số lần xuất hiện của từ"],
       ["CV", "Cross-Validation", "Kiểm định chéo"],
       ["OOF", "Out-of-Fold", "Dự đoán trên phần dữ liệu không tham gia huấn luyện của fold"],
       ["NB", "Multinomial Naive Bayes", "Bộ phân loại Bayes ngây thơ đa thức"],
       ["LR", "Logistic Regression", "Hồi quy logistic"],
       ["SVM", "Support Vector Machine", "Máy vector hỗ trợ"],
       ["RF", "Random Forest", "Rừng ngẫu nhiên"],
       ["SMOTE", "Synthetic Minority Over-sampling Technique",
        "Sinh mẫu tổng hợp cho lớp thiểu số"],
       ["XAI", "Explainable Artificial Intelligence", "Trí tuệ nhân tạo giải thích được"],
       ["ABSA", "Aspect-Based Sentiment Analysis", "Phân tích cảm xúc theo khía cạnh"],
       ["BPE", "Byte-Pair Encoding", "Thuật toán tách token theo cặp byte của Transformer"],
       ["NFC", "Normalization Form Canonical Composition",
        "Dạng chuẩn hóa Unicode dựng sẵn"],
       ["OT", "Overtime", "Làm thêm giờ"],
       ["HR", "Human Resources", "Bộ phận nhân sự"],
   ],
   ["c", "l", "l"]))
B(("pagebreak",))

B(("h1", "DANH MỤC BẢNG"))
B(("lines", [
   "Bảng 0.1. Danh mục từ viết tắt và thuật ngữ sử dụng trong báo cáo",
   "Bảng 2.1. Sáu nhóm trường của bộ dữ liệu sau tiền xử lý",
   "Bảng 2.2. Quy tắc ánh xạ điểm đánh giá sang nhãn cảm xúc yếu",
   "Bảng 2.3. Thống kê giá trị khuyết thiếu và kết quả audit trùng lặp",
   "Bảng 2.4. Phân bố số sao đánh giá",
   "Bảng 2.5. Phân bố nhãn cảm xúc",
   "Bảng 2.6. Thống kê độ dài hai trường nội dung chính (đơn vị: từ)",
   "Bảng 2.7. Thống kê token rỗng và review quá ngắn sau tiền xử lý",
   "Bảng 2.8. Tương quan Spearman giữa điểm khía cạnh và điểm tổng thể",
   "Bảng 2.9. Chẩn đoán chất lượng nhãn yếu qua trường Recommend?",
   "Bảng 2.10. Quy mô các bộ từ điển tiếng Việt sử dụng trong pipeline",
   "Bảng 3.1. So sánh cấu hình n-gram của TF-IDF trên 5-fold CV",
   "Bảng 3.2. So sánh TF-IDF và Bag-of-Words trên cùng bộ fold",
   "Bảng 3.3. Kết quả thí nghiệm đối chứng năm nhóm đặc trưng",
   "Bảng 3.4. Kiểm định chênh lệch theo từng cặp fold so với Text-only",
   "Bảng 3.5. Kích thước ma trận đặc trưng của hai cấu hình bàn giao",
   "Bảng 3.6. So sánh ba chiến lược xử lý mất cân bằng lớp",
   "Bảng 3.7. Cấu hình bốn mô hình học máy cơ sở",
   "Bảng 3.8. Kết quả 5-fold CV với tham số mặc định",
   "Bảng 3.9. Lưới siêu tham số và kết quả GridSearchCV",
   "Bảng 3.10. Xếp hạng CV Macro F1 sau tinh chỉnh",
   "Bảng 4.1. Kết quả tổng hợp của Stacking Ensemble trên tập kiểm tra cuối",
   "Bảng 4.2. Chỉ số theo từng lớp của Stacking Ensemble trên tập kiểm tra cuối",
   "Bảng 4.3. Ma trận nhầm lẫn của phương án argmax mặc định",
   "Bảng 4.4. So sánh Stacking Ensemble và ViSoBERT zero-shot",
   "Bảng 4.5. Chỉ số theo từng lớp của ViSoBERT zero-shot",
   "Bảng 4.6. So sánh phương án argmax và chính sách ngưỡng 0,30",
   "Bảng 4.7. Ma trận nhầm lẫn khi áp dụng chính sách ngưỡng 0,30",
   "Bảng 4.8. Phân tích độ nhạy theo ngưỡng quyết định lớp Negative",
   "Bảng 5.1. Phân bố cảm xúc trên toàn bộ dữ liệu",
   "Bảng 5.2. Kết quả phân tích hai doanh nghiệp có nhiều review nhất",
   "Bảng 5.3. Bốn phân hệ của ứng dụng web demo",
   "Bảng 6.1. Đối chiếu mục tiêu đề ra và kết quả đạt được",
   "Bảng A.1. Notebook và script thực nghiệm",
   "Bảng A.2. Module mã nguồn",
   "Bảng A.3. Artifact mô hình và tệp kết quả"]))
B(("pagebreak",))

B(("h1", "DANH MỤC HÌNH VẼ"))
B(("lines", [
   "Hình 2.1. Phân bố số sao đánh giá",
   "Hình 2.2. Phân bố ba nhãn cảm xúc",
   "Hình 2.3. Phân bố độ dài nội dung review",
   "Hình 2.4. Ma trận tương quan giữa các điểm đánh giá",
   "Hình 2.5. Điểm khía cạnh phân tách theo nhãn cảm xúc",
   "Hình 2.6. Phân bố review theo doanh nghiệp và theo thời gian",
   "Hình 2.7. Chẩn đoán chất lượng nhãn yếu và độ bao phủ từ điển",
   "Hình 3.1. So sánh cấu hình n-gram của TF-IDF",
   "Hình 3.2. Thí nghiệm đối chứng năm nhóm đặc trưng trên tập phát triển",
   "Hình 3.3. Chỉ số theo lớp thiểu số của từng nhóm đặc trưng",
   "Hình 3.4. So sánh CV Macro F1 giữa các mô hình sau tinh chỉnh",
   "Hình 4.1. Ma trận nhầm lẫn của mô hình Stacking Ensemble",
   "Hình 4.2. So sánh ma trận nhầm lẫn trước và sau chính sách ngưỡng",
   "Hình 4.3. Độ nhạy của các chỉ số theo ngưỡng quyết định lớp Negative",
   "Hình 5.1. Đám mây từ khóa của nhóm review tích cực",
   "Hình 5.2. Đám mây từ khóa của nhóm review tiêu cực",
   "Hình 5.3. Phân bố cảm xúc tại FPT Software",
   "Hình 5.4. Từ khóa tích cực tại FPT Software",
   "Hình 5.5. Từ khóa tiêu cực tại FPT Software",
   "Hình 5.6. Phân bố cảm xúc tại NashTech",
   "Hình 5.7. Từ khóa tích cực tại NashTech",
   "Hình 5.8. Từ khóa tiêu cực tại NashTech"]))
B(("pagebreak",))

# ==========================================================================
# CHƯƠNG 1
# ==========================================================================
B(("h1", "CHƯƠNG 1. TỔNG QUAN VÀ ĐẶT VẤN ĐỀ"))

B(("h2", "1.1. Bối cảnh đề tài"))
B(("p", "Thị trường lao động công nghệ thông tin tại Việt Nam có đặc điểm khác biệt so với "
       "nhiều ngành khác: tỷ lệ dịch chuyển nhân sự cao, thông tin về môi trường làm việc "
       "lan truyền nhanh trong cộng đồng, và ứng viên thường tham khảo đánh giá của nhân "
       "viên cũ trước khi quyết định ứng tuyển. ITviec là một trong những nền tảng tuyển "
       "dụng công nghệ lớn nhất trong nước, nơi nhân viên và cựu nhân viên để lại đánh giá "
       "công khai về công ty họ từng làm việc, kèm theo điểm số tổng thể và điểm cho từng "
       "khía cạnh như lương thưởng, đào tạo, quản lý, văn hóa và cơ sở vật chất."))
B(("p", "Khối lượng đánh giá tích lũy trên nền tảng này đã đủ lớn để không thể đọc thủ công. "
       "Một doanh nghiệp muốn biết nhân viên đang phàn nàn điều gì phải đọc hàng nghìn đoạn "
       "văn bản tự do; một ứng viên muốn đánh giá một công ty phải tự tổng hợp cảm nhận từ "
       "hàng trăm ý kiến trái chiều. Đây chính là bài toán mà phân tích cảm xúc tự động "
       "(sentiment analysis) có thể giải quyết: quy các đoạn văn bản tự do về một nhãn cảm "
       "xúc có thể thống kê được, rồi tổng hợp thành bức tranh ở cấp doanh nghiệp."))
B(("p", "Tuy nhiên, việc áp dụng phân tích cảm xúc lên dữ liệu đánh giá nhân sự tiếng Việt "
       "không phải một bài toán chuẩn mực có thể giải bằng cách lắp ghép thư viện có sẵn. "
       "Văn bản đánh giá trên ITviec chêm xen dày đặc thuật ngữ tiếng Anh ngành công nghệ "
       "(*OT*, *fresher*, *probation*, *outsourcing*, *layoff*, *micromanage*), sử dụng "
       "teencode và từ viết tắt tiếng Việt không chuẩn (*cty*, *mn*, *k*, *lm*, *cx*), đồng "
       "thời thường mang cấu trúc hai mặt — vừa khen môi trường và đồng nghiệp, vừa chê gay "
       "gắt chế độ đãi ngộ. Ba đặc điểm này khiến các pipeline NLP tiếng Anh phổ thông hoạt "
       "động kém, và đòi hỏi một quy trình tiền xử lý được thiết kế riêng cho miền dữ liệu."))

B(("h2", "1.2. Mục tiêu nghiên cứu"))
B(("p", "Đồ án đặt ra bốn mục tiêu cụ thể, có thể kiểm chứng bằng số liệu thực nghiệm:"))
B(("num", [
    "**Xây dựng hệ thống phân loại cảm xúc ba lớp** (Tích cực – Trung tính – Tiêu cực) cho "
    "văn bản đánh giá nhân sự tiếng Việt, từ khâu làm sạch dữ liệu thô đến khâu suy luận "
    "trên văn bản người dùng nhập tự do.",
    "**So sánh có kiểm chứng hiệu năng** giữa ba nhóm phương pháp: các thuật toán học máy "
    "cổ điển trên biểu diễn TF-IDF, mô hình kết hợp Stacking Ensemble, và mô hình ngôn ngữ "
    "tiền huấn luyện tiếng Việt ViSoBERT ở chế độ zero-shot.",
    "**Định lượng đóng góp của từng nhóm đặc trưng** bằng thí nghiệm đối chứng (ablation "
    "study) trên cùng bộ fold và cùng seed, đồng thời phân tích rủi ro rò rỉ nhãn khi đưa "
    "các trường điểm số có quan hệ trực tiếp với nhãn mục tiêu vào ma trận đặc trưng.",
    "**Khai thác thông tin nghiệp vụ và triển khai ứng dụng**: trích xuất từ khóa đặc trưng "
    "cho nhóm đánh giá tích cực và tiêu cực theo từng doanh nghiệp, đồng thời đóng gói mô "
    "hình thành ứng dụng web cho phép dự đoán thời gian thực kèm giải thích quyết định.",
]))
B(("p", "Một mục tiêu ngầm định nhưng xuyên suốt toàn bộ đồ án là **tính trung thực về mặt "
       "phương pháp**. Bộ dữ liệu sử dụng nhãn yếu suy ra từ điểm đánh giá, chứ không phải "
       "nhãn vàng do con người đọc nội dung và gán. Đặc điểm này chi phối cách diễn giải "
       "mọi kết quả và được nêu lại ở từng chương có liên quan, thay vì chỉ nhắc một lần "
       "trong phần giới hạn ở cuối báo cáo."))

B(("h2", "1.3. Đối tượng và phạm vi nghiên cứu"))
B(("p", "**Đối tượng nghiên cứu** là văn bản đánh giá công ty do nhân viên ngành công nghệ "
       "thông tin viết bằng tiếng Việt, cùng các trường siêu dữ liệu đi kèm: tên công ty, "
       "thời điểm đánh giá, điểm tổng thể và năm điểm khía cạnh."))
B(("p", "**Phạm vi nghiên cứu** được giới hạn như sau. Bài toán được đặt là phân loại cảm "
       "xúc ở mức toàn văn bản (document-level), phân thành ba lớp rời rạc. Đồ án không giải "
       "bài toán phân tích cảm xúc theo khía cạnh (ABSA), không thực hiện phát hiện chủ đề "
       "tự động, và không xây dựng hệ thống xếp hạng doanh nghiệp. Về mô hình, đồ án tập "
       "trung vào các thuật toán học máy cổ điển trên biểu diễn thưa; mô hình Transformer "
       "chỉ được đưa vào ở chế độ zero-shot làm mốc đối chiếu, không fine-tune, do giới hạn "
       "tài nguyên GPU trong khung thời gian ba tuần."))
B(("p", "Về dữ liệu, đồ án sử dụng một ảnh chụp tĩnh gồm 8.417 đánh giá đã thu thập sẵn, "
       "không thực hiện thu thập bổ sung trong quá trình làm bài, nhằm bảo đảm mọi thí "
       "nghiệm đều tái lập được trên cùng một tập dữ liệu có giá trị băm SHA-256 cố định."))

B(("h2", "1.4. Phương pháp tiếp cận tổng quát"))
B(("p", "Đồ án được triển khai theo quy trình tuần tự sáu giai đoạn, mỗi giai đoạn sinh ra "
       "artifact có thể kiểm chứng độc lập và được bàn giao cho giai đoạn kế tiếp:"))
B(("num", [
    "**Chuẩn bị dữ liệu**: ghép ba trường nội dung thành một đoạn văn bản thống nhất, ánh "
    "xạ điểm đánh giá sang nhãn cảm xúc yếu, kiểm tra giá trị khuyết thiếu và trùng lặp.",
    "**Tiền xử lý văn bản tiếng Việt**: pipeline hai tầng, sinh ra hai phiên bản văn bản "
    "sạch phục vụ hai nhóm mô hình có yêu cầu khác nhau.",
    "**Trích xuất đặc trưng**: vector hóa TF-IDF, tính đặc trưng từ điển cảm xúc, thí nghiệm "
    "đối chứng để quyết định nhóm đặc trưng nào được đưa vào pipeline chính thức.",
    "**Mô hình hóa và tinh chỉnh**: huấn luyện bốn mô hình cơ sở, tinh chỉnh siêu tham số "
    "bằng GridSearchCV, xây dựng mô hình Stacking Ensemble.",
    "**Đánh giá và phân tích lỗi**: đánh giá đúng một lần trên tập kiểm tra cuối đã khóa, "
    "phân tích ma trận nhầm lẫn và các nhóm lỗi điển hình.",
    "**Khai thác thông tin và triển khai**: phân tích cảm xúc theo doanh nghiệp, đóng gói "
    "ứng dụng web tương tác.",
]))
B(("p", "Nguyên tắc chi phối toàn bộ quy trình là **tách bạch tập lựa chọn và tập đánh giá**. "
       "Dữ liệu được chia thành tập phát triển 80% và tập kiểm tra cuối 20% ngay từ đầu. Mọi "
       "quyết định về đặc trưng, siêu tham số và mô hình đều dựa trên kiểm định chéo bên "
       "trong tập phát triển. Tập kiểm tra cuối chỉ được mở đúng một lần, sau khi mô hình đã "
       "được khóa hoàn toàn."))

B(("h2", "1.5. Đóng góp của đồ án"))
B(("p", "Ngoài việc hoàn thành các mục tiêu đã nêu, nhóm xác định bốn đóng góp có giá trị "
       "riêng của đồ án:"))
B(("bullet", [
    "**Thuật toán nhận diện phạm vi phủ định kết hợp đối sánh cụm từ tham lam** cho từ điển "
    "cảm xúc tiếng Việt, nâng độ bao phủ từ điển từ 12,26% lên 99,75% số review.",
    "**Bằng chứng định lượng về hiện tượng data shortcut**: cấu hình chỉ dùng năm điểm khía "
    "cạnh, không đọc một từ nào trong review, vẫn đạt Macro F1 0,7388 — cao hơn cấu hình "
    "văn bản đầy đủ tới 0,18 điểm. Đây là căn cứ để loại nhóm đặc trưng này khỏi pipeline "
    "triển khai thay vì tận dụng nó để làm đẹp số liệu.",
    "**Phân tích đầy đủ về bẫy Accuracy**: ba thí nghiệm độc lập trong báo cáo đều cho thấy "
    "cấu hình có Accuracy cao nhất lại là cấu hình có Recall lớp Negative thấp nhất.",
    "**Bộ artifact có ràng buộc tái lập**: mỗi tệp mô hình đi kèm manifest ghi phiên bản "
    "Python, giá trị băm dữ liệu nguồn, Git SHA và checksum, cho phép kiểm chứng rằng kết "
    "quả báo cáo được sinh từ đúng phiên bản dữ liệu và mã nguồn nào.",
]))

B(("h2", "1.6. Bố cục báo cáo"))
B(("p", "Báo cáo gồm sáu chương. **Chương 1** trình bày bối cảnh, mục tiêu và phạm vi. "
       "**Chương 2** mô tả bộ dữ liệu, kết quả phân tích khám phá và quy trình tiền xử lý "
       "văn bản tiếng Việt. **Chương 3** trình bày phương pháp biểu diễn văn bản, thí nghiệm "
       "đối chứng nhóm đặc trưng và thiết kế các mô hình học máy. **Chương 4** báo cáo kết "
       "quả thực nghiệm trên tập kiểm tra cuối, phân tích ma trận nhầm lẫn và phân tích lỗi "
       "định tính. **Chương 5** trình bày kết quả khai thác thông tin ở cấp doanh nghiệp và "
       "ứng dụng web triển khai. **Chương 6** tổng kết đóng góp, nêu hạn chế và hướng phát "
       "triển."))
B(("pagebreak",))

# ==========================================================================
# CHƯƠNG 2
# ==========================================================================
B(("h1", "CHƯƠNG 2. TỔNG QUAN DỮ LIỆU VÀ TIỀN XỬ LÝ"))

B(("h2", "2.1. Giới thiệu bộ dữ liệu ITviec Reviews"))
B(("h3", "2.1.1. Nguồn dữ liệu và cấu trúc"))
B(("p", "Bộ dữ liệu sau tiền xử lý được lưu tại `data/processed/reviews_cleaned.xlsx`, gồm "
       "**8.417 review** và **23 trường**, không có dòng trùng lặp hoàn toàn. Dữ liệu bao "
       "phủ **180 công ty** công nghệ trong giai đoạn từ tháng 07/2016 đến tháng 05/2025. "
       "Các trường được tổ chức thành sáu nhóm chức năng."))
B(("table", "Bảng 2.1. Sáu nhóm trường của bộ dữ liệu sau tiền xử lý",
   ["Nhóm trường", "Các trường thành phần", "Vai trò trong pipeline"],
   [
       ["Định danh và doanh nghiệp", "`id`, `Company Name`, `Cmt_day`",
        "Phân nhóm phân tích theo công ty và theo thời gian"],
       ["Nội dung review",
        "`Title`, `What I liked`, `Suggestions for improvement`",
        "Nguồn văn bản thô để ghép thành đoạn đánh giá hoàn chỉnh"],
       ["Điểm tổng thể", "`Rating` (thang 1–5 sao)",
        "Nguồn sinh nhãn yếu; **không** đưa vào ma trận đặc trưng"],
       ["Điểm khía cạnh",
        "Lương và phúc lợi, đào tạo, quản lý, văn hóa, văn phòng",
        "Chỉ dùng trong thí nghiệm đối chứng, loại khỏi pipeline triển khai"],
       ["Nội dung đã xử lý",
        "`raw_review_text`, `clean_basic_text`, `clean_advance_text`",
        "Đầu vào của hai nhóm mô hình khác nhau"],
       ["Đặc trưng từ điển",
        "`pos_w`, `neg_w`, `pos_e`, `neg_e`, `total_we`, `sentiment_ratio`",
        "Đặc trưng số bổ trợ cho biểu diễn TF-IDF"],
   ],
   ["l", "l", "l"]))
B(("p", "Văn bản đánh giá hoàn chỉnh được tạo bằng cách nối ba trường nội dung theo thứ tự "
       "tiêu đề, phần khen và phần góp ý, ngăn cách bằng dấu chấm. Cách ghép này giữ lại "
       "được cả hai mặt của một đánh giá trong cùng một chuỗi, phù hợp với bài toán phân "
       "loại ở mức toàn văn bản."))

B(("h3", "2.1.2. Chiến lược gán nhãn yếu từ điểm đánh giá"))
B(("p", "Bộ dữ liệu gốc không có nhãn cảm xúc do con người đọc nội dung và gán. Nhóm sử dụng "
       "**nhãn yếu suy ra từ điểm đánh giá** (rating-derived weak label) theo quy tắc ánh xạ "
       "cố định dưới đây."))
B(("table", "Bảng 2.2. Quy tắc ánh xạ điểm đánh giá sang nhãn cảm xúc yếu",
   ["Điểm `Rating`", "Nhãn `sentiment`", "Số mẫu", "Tỷ lệ", "Diễn giải nghiệp vụ"],
   [
       ["4 – 5 sao", "Positive", "6.208", "73,76%",
        "Hài lòng về chế độ, môi trường, văn hóa hoặc đồng nghiệp"],
       ["3 sao", "Neutral", "1.639", "19,47%",
        "Trung hòa, thường có cả điểm khen và điểm chê cân bằng"],
       ["1 – 2 sao", "Negative", "570", "6,77%",
        "Thất vọng về làm thêm giờ, áp lực, đãi ngộ hoặc quản lý"],
   ],
   ["c", "c", "r", "r", "l"]))
B(("p", "Cần nhấn mạnh rằng đây **không phải nhãn vàng**. Người viết review chấm điểm dựa "
       "trên tổng thể trải nghiệm của họ, trong đó có những yếu tố không được viết ra trong "
       "phần văn bản. Vì vậy tồn tại những review 3 sao có nội dung chê rất nặng, và những "
       "review 5 sao vẫn kèm góp ý tiêu cực dài. Hệ quả là **trần hiệu năng lý thuyết** của "
       "mọi mô hình học trên bộ dữ liệu này bị chặn bởi mức độ nhất quán giữa điểm số và nội "
       "dung, chứ không phải bởi năng lực của thuật toán. Nhận định này được kiểm chứng bằng "
       "số liệu ở mục 2.2.6 và được dùng lại khi diễn giải kết quả ở Chương 4."))

B(("h3", "2.1.3. Giá trị khuyết thiếu và audit trùng lặp"))
B(("p", "Dữ liệu khuyết thiếu chỉ xuất hiện ở hai trường nội dung và ở mức không đáng kể. "
       "Các cột đã tiền xử lý và cột nhãn không có giá trị khuyết thiếu. Đáng chú ý hơn là "
       "kết quả audit văn bản trùng: tồn tại 6 dòng thuộc ba nhóm (mỗi nhóm 2 dòng) có "
       "`clean_advance_text` giống hệt nhau, trong đó **một nhóm có cùng nội dung văn bản nhưng khác nhãn yếu** (một dòng Neutral, một dòng Positive)."))
B(("table", "Bảng 2.3. Thống kê giá trị khuyết thiếu và kết quả audit trùng lặp",
   ["Hạng mục", "Số dòng", "Tỷ lệ", "Xử lý"],
   [
       ["Khuyết `What I liked`", "1", "0,01%", "Giữ lại, phần nội dung còn lại vẫn đủ"],
       ["Khuyết `Suggestions for improvement`", "5", "0,06%", "Giữ lại"],
       ["Khuyết cột đã xử lý và cột nhãn", "0", "0,00%", "Không cần xử lý"],
       ["Trùng văn bản, cùng nhãn (2 nhóm × 2 dòng)", "2 dòng dư", "0,02%",
        "Giữ lại một dòng đại diện mỗi nhóm"],
       ["Trùng văn bản, **khác nhãn** (1 nhóm × 2 dòng)", "2 dòng", "0,02%",
        "**Loại toàn bộ nhóm**"],
       ["Tổng số dòng bị loại", "**4**", "0,05%", "8.417 − 4 = 8.413"],
       ["Tổng dòng đưa vào mô hình", "**8.413**", "99,95%", "Khớp `models/artifact_manifest.json`"],
   ],
   ["l", "r", "r", "l"]))
B(("p", "Việc loại toàn bộ nhóm bất đồng nhãn, thay vì giữ lại một dòng bất kỳ, là quyết "
       "định có chủ đích: nếu giữ lại, cùng một chuỗi văn bản có thể rơi vào tập huấn luyện "
       "với một nhãn và rơi vào tập kiểm định với nhãn khác, tạo ra một giới hạn trên giả "
       "tạo cho chính mô hình. Bước audit này được thực hiện **trước** khi chia dữ liệu, "
       "nên không có văn bản nào xuất hiện đồng thời ở cả hai phía của phép chia."))

B(("h2", "2.2. Phân tích khám phá dữ liệu"))
B(("h3", "2.2.1. Phân bố số sao và mức độ mất cân bằng lớp"))
B(("p", "Phân bố điểm đánh giá lệch mạnh về phía điểm cao. Riêng hai mức 4 và 5 sao đã chiếm "
       "gần ba phần tư toàn bộ dữ liệu, trong khi mức 1 sao chỉ có 124 review."))
B(("table", "Bảng 2.4. Phân bố số sao đánh giá",
   ["Số sao", "1 sao", "2 sao", "3 sao", "4 sao", "5 sao"],
   [["Số review", "124", "446", "1.639", "2.698", "3.510"],
    ["Tỷ lệ", "1,47%", "5,30%", "19,47%", "32,05%", "41,70%"]],
   ["l", "r", "r", "r", "r", "r"]))
B(("figure", "Hình 2.1. Phân bố số sao đánh giá", "reports/figures/eda_rating_distribution.png"))
B(("table", "Bảng 2.5. Phân bố nhãn cảm xúc",
   ["Nhãn", "Số review", "Tỷ lệ", "Tỷ số so với lớp Negative"],
   [["Positive", "6.208", "73,76%", "10,9 : 1"],
    ["Neutral", "1.639", "19,47%", "2,9 : 1"],
    ["Negative", "570", "6,77%", "1 : 1"]],
   ["l", "r", "r", "c"]))
B(("figure", "Hình 2.2. Phân bố ba nhãn cảm xúc", "reports/figures/eda_sentiment_counts.png"))
B(("p", "Lớp Positive lớn gấp khoảng **10,9 lần** lớp Negative. Mức mất cân bằng này có một "
       "hệ quả trực tiếp về mặt đánh giá: một bộ phân loại tầm thường luôn dự đoán Positive "
       "cho mọi đầu vào đã đạt xấp xỉ **73,8% Accuracy** mà không mang lại bất kỳ giá trị sử "
       "dụng nào. Do đó toàn bộ báo cáo lấy **Macro F1** làm chỉ số quyết định, đồng thời "
       "theo dõi riêng **Recall của lớp Negative** như chỉ số nghiệp vụ quan trọng nhất — vì "
       "trong bài toán quản trị nhân sự, bỏ sót một phản hồi tiêu cực gây thiệt hại lớn hơn "
       "nhiều so với cảnh báo nhầm một phản hồi tích cực."))

B(("h3", "2.2.2. Độ dài nội dung đánh giá"))
B(("p", "Độ dài hai trường nội dung chính được đo theo số từ. Phân bố lệch phải rõ rệt ở cả "
       "hai trường: phần lớn review ngắn, nhưng tồn tại một số ngoại lệ rất dài."))
B(("table", "Bảng 2.6. Thống kê độ dài hai trường nội dung chính (đơn vị: từ)",
   ["Trường", "Trung bình", "Trung vị", "Phân vị 95", "Phân vị 99", "Lớn nhất"],
   [["What I liked", "50,29", "36", "131", "237,36", "1.400"],
    ["Suggestions for improvement", "29,97", "20", "78", "184", "876"]],
   ["l", "r", "r", "r", "r", "r"]))
B(("figure", "Hình 2.3. Phân bố độ dài nội dung review",
   "reports/figures/eda_text_length_distribution.png"))
B(("p", "Khoảng cách giữa trung vị (36 từ) và giá trị lớn nhất (1.400 từ) lên tới gần 40 "
       "lần. Đặc điểm này ủng hộ việc chọn TF-IDF thay vì Bag-of-Words làm biểu diễn chính: "
       "TF-IDF sử dụng trọng số đã chuẩn hóa theo độ dài tài liệu, nên một review dài không "
       "tự động có vector với chuẩn lớn hơn và không chi phối quá mức quá trình huấn luyện. "
       "Kết quả thực nghiệm ở mục 3.1.3 xác nhận dự đoán này."))

B(("h3", "2.2.3. Thống kê token rỗng và review quá ngắn"))
B(("p", "Chuỗi `clean_advance_text` sau tiền xử lý được kiểm tra nhằm xác định có review nào "
       "bị mất toàn bộ nội dung hay không. Đây là bước kiểm tra bắt buộc, vì một tài liệu "
       "rỗng sẽ tạo ra vector TF-IDF toàn số 0 và trở thành nhiễu thuần túy trong huấn luyện."))
B(("table", "Bảng 2.7. Thống kê token rỗng và review quá ngắn sau tiền xử lý",
   ["Nhóm", "Số review", "Tỷ lệ"],
   [["Chuỗi rỗng hoàn toàn", "0", "0,00%"],
    ["Dưới 3 token", "0", "0,00%"],
    ["Dưới 5 token", "0", "0,00%"],
    ["Dưới 10 token", "35", "0,42%"]],
   ["l", "r", "r"]))
B(("p", "Trên 8.413 review dùng cho mô hình, số token trung bình là **35,95**, trung vị 28, "
       "nhỏ nhất 5 và lớn nhất 511. Không tồn tại tài liệu rỗng hay ngắn tới mức vô nghĩa, "
       "nên pipeline không cần thêm bước lọc theo độ dài trước khi vector hóa. Kết quả này "
       "cũng gián tiếp xác nhận rằng bước lọc từ dừng ở tầng tiền xử lý thứ hai không xóa "
       "quá tay nội dung của bất kỳ review nào."))

B(("h3", "2.2.4. Quan hệ giữa điểm khía cạnh và cảm xúc tổng thể"))
B(("p", "Năm điểm khía cạnh được đối chiếu với điểm tổng thể bằng hệ số tương quan hạng "
       "Spearman. Tương quan hạng được chọn thay cho Pearson vì các điểm số là biến thứ bậc "
       "trên thang 1–5, không phải biến liên tục."))
B(("table", "Bảng 2.8. Tương quan Spearman giữa điểm khía cạnh và điểm tổng thể",
   ["Khía cạnh", "Tương quan Spearman với `Rating`"],
   [["Management cares about me (Quản lý quan tâm)", "0,7368"],
    ["Salary & benefits (Lương và phúc lợi)", "0,7343"],
    ["Culture & fun (Văn hóa)", "0,6566"],
    ["Training & learning (Đào tạo)", "0,6398"],
    ["Office & workspace (Văn phòng)", "0,5423"]],
   ["l", "r"]))
B(("figure", "Hình 2.4. Ma trận tương quan giữa các điểm đánh giá",
   "reports/figures/eda_aspect_correlation.png"))
B(("p", "Điểm trung bình của mọi khía cạnh đều giảm đều theo thứ tự Positive, Neutral, "
       "Negative, với chênh lệch lớn nhất tập trung ở quản lý, lương và phúc lợi, văn hóa. "
       "Xét thuần túy về mặt thống kê, đây là những tín hiệu dự báo rất mạnh."))
B(("figure", "Hình 2.5. Điểm khía cạnh phân tách theo nhãn cảm xúc",
   "reports/figures/eda_aspect_by_sentiment.png"))
B(("p", "Tuy nhiên chính sức mạnh dự báo này lại là vấn đề. Nhãn `sentiment` được sinh trực "
       "tiếp từ `Rating`; năm điểm khía cạnh lại tương quan với `Rating` ở mức 0,54 đến "
       "0,74. Nếu đưa chúng vào ma trận đặc trưng, mô hình sẽ học cách khôi phục lại thang "
       "điểm đã sinh ra nhãn, thay vì học cách hiểu ngôn ngữ. Điểm `Rating` tổng thể vì lý "
       "do hiển nhiên hơn nữa mà **không bao giờ** được đưa vào đặc trưng. Toàn bộ lập luận "
       "này được kiểm chứng bằng thí nghiệm đối chứng ở mục 3.2."))

B(("h3", "2.2.5. Phân bố theo doanh nghiệp và theo thời gian"))
B(("p", "Dữ liệu bao phủ 180 công ty nhưng phân bố rất không đồng đều. FPT Software một mình "
       "chiếm **2.014 review, tương đương 23,93%** toàn bộ dữ liệu, trong khi **110 trên 180 "
       "công ty có dưới 20 review**."))
B(("figure", "Hình 2.6. Phân bố review theo doanh nghiệp và theo thời gian",
   "reports/figures/eda_company_time_distribution.png"))
B(("p", "Hệ quả trực tiếp của phân bố này là mọi kết quả ở cấp công ty đều phải hiển thị kèm "
       "số mẫu và chỉ nên diễn giải khi đạt ngưỡng tối thiểu. Trong ứng dụng web trình bày "
       "ở Chương 5, dashboard áp dụng ngưỡng tối thiểu trước khi so sánh giữa các doanh "
       "nghiệp, và phần phân tích case study ở mục 5.2 chỉ chọn doanh nghiệp có từ 50 review "
       "trở lên. Một tỷ lệ tiêu cực tính trên 8 review không có ý nghĩa thống kê, dù con số "
       "phần trăm trông rất ấn tượng."))

B(("h3", "2.2.6. Chẩn đoán chất lượng nhãn yếu và độ bao phủ từ điển"))
B(("p", "Mục này trình bày ba chẩn đoán cho thấy vì sao nhãn yếu không thể được mô tả như "
       "ground truth tuyệt đối, đồng thời ghi lại quá trình sửa lỗi bộ từ điển cảm xúc."))
B(("p", "**Thứ nhất, về độ bao phủ từ điển.** Ở phiên bản đối sánh theo từ đơn, từ điển cảm "
       "xúc chỉ khớp được ít nhất một từ trên **12,26%** số review — nghĩa là gần 88% review "
       "có giá trị đặc trưng từ điển bằng 0 và hoàn toàn vô dụng. Sau khi chuyển sang thuật "
       "toán **đối sánh cụm từ dài nhất (Greedy Longest Phrase Matching)** và mở rộng từ "
       "điển, độ bao phủ đạt **99,75%**; giá trị trung bình của `total_we` tăng từ 0,16 lên "
       "**6,74** và `pos_w` tăng từ 0,08 lên **5,31**."))
B(("p", "**Thứ hai, về đặc trưng emoji.** Hai đặc trưng `pos_e` và `neg_e` từng bằng 0 trên "
       "toàn bộ 8.417 dòng ở các phiên bản trước do lỗi ở khâu đếm. Sau khi sửa, chúng nhận "
       "giá trị khác 0 nhưng chỉ trên **20 review (0,24%)**, gồm 19 dòng có emoji tích cực "
       "và 1 dòng có emoji tiêu cực. Đóng góp thực tế của hai đặc trưng này vào mô hình vì "
       "vậy vẫn không đáng kể, và báo cáo không trình bày chúng như một thành phần có ý "
       "nghĩa."))
B(("p", "**Thứ ba, về tính nhất quán của nhãn yếu.** Trường `Recommend?` — nơi người viết "
       "trả lời trực tiếp câu hỏi có giới thiệu công ty cho người khác hay không — bất đồng "
       "với nhãn yếu ở một tỷ lệ đáng kể."))
B(("table", "Bảng 2.9. Chẩn đoán chất lượng nhãn yếu qua trường Recommend?",
   ["Nhóm bất đồng", "Số review", "Ý nghĩa"],
   [["Nhãn Negative nhưng **vẫn** khuyến nghị công ty", "41",
     "Điểm thấp có thể phản ánh một khía cạnh cụ thể, không phải cảm xúc tổng thể"],
    ["Nhãn Neutral nhưng **không** khuyến nghị", "411",
     "Nhóm 3 sao chứa nhiều đánh giá thực chất tiêu cực"],
    ["Nhãn Positive nhưng **không** khuyến nghị", "87",
     "Điểm cao không đồng nghĩa với việc sẵn sàng giới thiệu"]],
   ["l", "r", "l"]))
B(("figure", "Hình 2.7. Chẩn đoán chất lượng nhãn yếu và độ bao phủ từ điển",
   "reports/figures/eda_label_quality_diagnostics.png"))
B(("p", "Ba chẩn đoán trên không chứng minh rằng nhãn yếu sai. Chúng cho thấy `Rating` chỉ "
       "là một xấp xỉ có nhiễu của cảm xúc thực sự chứa trong văn bản. Con số 411 review "
       "Neutral không được khuyến nghị đặc biệt đáng chú ý, vì nó giải thích trước một phần "
       "hiện tượng sẽ quan sát được ở Chương 4: lớp Neutral là lớp mà mọi mô hình đều phân "
       "loại kém nhất."))

B(("h2", "2.3. Quy trình tiền xử lý văn bản tiếng Việt"))
B(("p", "Toàn bộ quy trình tiền xử lý được cài đặt trong module `src/preprocessing.py`. "
       "Thiết kế cốt lõi là **pipeline hai tầng**: cùng một văn bản thô sinh ra hai phiên bản "
       "sạch khác nhau, phục vụ hai nhóm mô hình có yêu cầu trái ngược nhau về cấu trúc câu."))

B(("h3", "2.3.1. Lý do thiết kế pipeline hai tầng"))
B(("p", "Mô hình học máy cổ điển trên biểu diễn TF-IDF hưởng lợi từ việc làm sạch triệt để: "
       "tách từ ghép tiếng Việt thành đơn vị có nghĩa, loại bỏ từ dừng để giảm nhiễu, chuẩn "
       "hóa mọi biến thể chính tả về một dạng duy nhất. Càng ít biến thể, từ vựng càng gọn "
       "và trọng số càng tập trung."))
B(("p", "Mô hình Transformer tiền huấn luyện thì ngược lại. Tokenizer Byte-Pair Encoding của "
       "ViSoBERT đã được huấn luyện trên văn bản tiếng Việt có dấu câu và trật tự từ tự "
       "nhiên. Nếu đưa vào một chuỗi đã bị tách từ bằng gạch dưới và bị xóa hết từ dừng, "
       "phân phối token đầu vào sẽ lệch hoàn toàn so với phân phối mà mô hình từng thấy khi "
       "tiền huấn luyện — hiện tượng thường được gọi là **over-cleaning**."))
B(("p", "Vì vậy pipeline sinh ra hai cột: `clean_basic_text` giữ nguyên cấu trúc câu tự "
       "nhiên, dành cho ViSoBERT; và `clean_advance_text` đã tách từ và lọc từ dừng, dành "
       "cho TF-IDF. Việc hai nhóm mô hình dùng hai phiên bản văn bản khác nhau nhưng **cùng "
       "một phép chia dữ liệu và cùng một tập kiểm tra cuối** cho phép so sánh kết quả của "
       "chúng một cách công bằng ở Chương 4."))

B(("h3", "2.3.2. Tầng 1 — Chuẩn hóa cơ bản"))
B(("p", "Hàm `clean_basic_text` thực hiện tuần tự sáu bước:"))
B(("num", [
    "**Chuẩn hóa Unicode NFC.** Tiếng Việt có thể được mã hóa ở dạng tổ hợp (ký tự cơ sở "
    "cộng dấu rời) hoặc dạng dựng sẵn. Hai dạng này trông giống hệt nhau trên màn hình "
    "nhưng là hai chuỗi byte khác nhau, khiến cùng một từ bị đếm thành hai từ vựng riêng "
    "biệt. Chuẩn hóa NFC quy mọi biến thể về dạng dựng sẵn.",
    "**Giải mã emoji và emojicon thành từ mang sắc thái.** Ký hiệu `:)` và ký tự 😡 được "
    "thay bằng các từ `tích_cực` và `tiêu_cực`, nhờ đó tín hiệu cảm xúc của chúng được giữ "
    "lại thay vì bị bước lọc ký tự đặc biệt xóa mất.",
    "**Xóa URL và địa chỉ thư điện tử**, vốn không mang thông tin cảm xúc nhưng lại tạo ra "
    "rất nhiều token hiếm làm loãng từ vựng.",
    "**Chuyển về chữ thường** để hợp nhất các biến thể viết hoa.",
    "**Chuẩn hóa teencode, thuật ngữ tiếng Anh và lỗi chính tả** bằng cách tra ba bộ từ "
    "điển ánh xạ. Đây là bước có tác động lớn nhất trên miền dữ liệu này.",
    "**Lọc ký tự đặc biệt và chuẩn hóa khoảng trắng**, chỉ giữ lại chữ cái tiếng Việt, chữ "
    "số và khoảng trắng.",
]))
B(("table", "Bảng 2.10. Quy mô các bộ từ điển tiếng Việt sử dụng trong pipeline",
   ["Tệp từ điển", "Số mục", "Vai trò"],
   [["`wrong-word.txt`", "11.850", "Sửa lỗi chính tả và biến thể gõ sai"],
    ["`english-vnmese.txt`", "4.252", "Ánh xạ thuật ngữ tiếng Anh sang tiếng Việt"],
    ["`vietnamese-stopwords.txt`", "1.947", "Danh sách từ dừng tiếng Việt"],
    ["`teencode.txt`", "413", "Chuẩn hóa từ viết tắt và teencode"],
    ["`negative_words.txt`", "344", "Từ và cụm từ mang sắc thái tiêu cực"],
    ["`positive_words.txt`", "299", "Từ và cụm từ mang sắc thái tích cực"],
    ["`neutral_keywords.txt`", "201", "Từ khóa trung tính"],
    ["`emojicon.txt`", "118", "Ánh xạ emojicon dạng ký tự sang từ"],
    ["`positive_emoji.txt` / `negative_emoji.txt`", "24 / 19", "Emoji mang cực tính"],
    ["`it_terms.txt`", "11", "Thuật ngữ đặc thù ngành công nghệ thông tin"]],
   ["l", "r", "l"]))

B(("h3", "2.3.3. Tầng 2 — Tách từ và lọc từ dừng"))
B(("p", "Hàm `clean_advance_text` nhận đầu ra của tầng 1 và thực hiện thêm hai bước."))
B(("p", "**Tách từ tiếng Việt.** Tiếng Việt viết rời từng âm tiết, nên ranh giới từ không "
       "trùng với ranh giới khoảng trắng. Chuỗi *môi trường làm việc* là ba từ có nghĩa "
       "(*môi_trường*, *làm_việc*) chứ không phải bốn âm tiết độc lập. Pipeline sử dụng "
       "`underthesea.word_tokenize`, và cài đặt cơ chế dự phòng hai lớp: nếu `underthesea` "
       "không nạp được thì chuyển sang `pyvi.ViTokenizer`, nếu cả hai đều lỗi thì giữ "
       "nguyên chuỗi chưa tách. Cơ chế này bảo đảm pipeline không bao giờ sinh ra chuỗi "
       "rỗng do lỗi môi trường — điều đã được xác nhận bằng số liệu ở mục 2.2.3."))
B(("p", "**Lọc từ dừng có chọn lọc.** Danh sách từ dừng chuẩn của tiếng Việt chứa nhiều từ "
       "phủ định và định lượng như *chưa*, *thiếu*, *ít*. Nếu lọc máy móc theo danh sách "
       "này, cụm *ít cơ hội học hỏi* sẽ bị rút gọn thành *cơ_hội học_hỏi* — đảo ngược hoàn "
       "toàn sắc thái. Nhóm vì vậy đã bảo lưu nhóm từ phủ định và định lượng khỏi danh sách "
       "lọc."))

B(("h3", "2.3.4. Thuật toán đối sánh cụm từ tham lam và nhận diện phạm vi phủ định"))
B(("p", "Hàm `calc_sentiment_features` tính sáu đặc trưng từ điển cảm xúc. Điểm kỹ thuật "
       "đáng chú ý nhất của đồ án nằm ở đây, và được cài đặt trong cùng một vòng quét duy "
       "nhất trên chuỗi token."))
B(("p", "**Đối sánh cụm từ dài nhất (Greedy Longest Phrase Matching).** Thay vì tra từ điển "
       "theo từng từ đơn, thuật toán thử khớp cụm dài nhất trước rồi mới giảm dần độ dài. "
       "Nhờ vậy cụm *môi trường làm việc tốt* được khớp nguyên cụm thay vì bị tách thành "
       "các từ rời rạc không có trong từ điển. Chính thay đổi này nâng độ bao phủ từ điển "
       "từ 12,26% lên 99,75% như đã nêu ở mục 2.2.6."))
B(("p", "**Nhận diện phạm vi phủ định (Negation Scope Detection).** Khi thuật toán khớp được "
       "một cụm từ *tích cực*, nó kiểm tra ngược lại một đến hai token liền trước để tìm "
       "dấu hiệu phủ định. Tập từ phủ định gồm *không*, *chưa*, *chẳng*, *chả*, *ít*, "
       "*thiếu*, *kém*, *hạn chế* cùng các tổ hợp *không hề*, *chưa hề*, *không được*, "
       "*chưa được*, *không có*. Thuật toán xét ba mẫu:"))
B(("num", [
    "Token liền trước nằm trong tập từ phủ định — ví dụ *không thân_thiện*.",
    "Hai token liền trước ghép lại tạo thành một cụm phủ định — ví dụ *không được hỗ_trợ*.",
    "Token cách hai vị trí là từ phủ định và token liền trước là một trong các trạng từ "
    "trung gian *được*, *hề*, *quá*, *rất*, *thực sự* — ví dụ *không hề rõ ràng*.",
]))
B(("p", "Khi một trong ba mẫu khớp, cụm từ vốn tích cực được tính vào bộ đếm **tiêu cực** "
       "`neg_w` thay vì `pos_w`, và cụm đã đảo chiều được ghi lại kèm tiền tố phủ định phục "
       "vụ tính năng giải thích quyết định ở ứng dụng web. Đây là điểm khác biệt cốt lõi so "
       "với cách đếm từ điển thông thường, vốn sẽ tính *không thân thiện* thành một tín hiệu "
       "tích cực."))
B(("p", "Sáu đặc trưng đầu ra gồm `pos_w`, `neg_w` (số cụm từ tích cực và tiêu cực đã khớp), "
       "`pos_e`, `neg_e` (số emoji theo cực tính), `total_we` (tổng tín hiệu cảm xúc) và "
       "`sentiment_ratio` — tỷ lệ chuẩn hóa về khoảng từ −1 đến +1 theo công thức: tổng tín "
       "hiệu tích cực trừ tổng tín hiệu tiêu cực, chia cho tổng toàn bộ tín hiệu. Hiệu quả "
       "thực nghiệm của nhóm đặc trưng này được đo ở mục 3.2.4."))

B(("h2", "2.4. Chiến lược chia dữ liệu"))
B(("p", "Sau khi loại văn bản trùng theo kết quả audit ở mục 2.1.3, **8.413 dòng** còn lại "
       "được chia phân tầng thành tập phát triển 80% và tập kiểm tra cuối 20%, với "
       "`random_state=2026` và tham số `stratify` đặt theo nhãn để giữ nguyên tỷ lệ ba lớp "
       "ở cả hai phía."))
B(("p", "Kết quả là **6.730 mẫu** ở tập phát triển và **1.683 mẫu** ở tập kiểm tra cuối. "
       "Phân bố nhãn trên tập phát triển gồm 4.964 Positive, 1.310 Neutral và 456 Negative; "
       "trên tập kiểm tra cuối gồm 1.241 Positive, 328 Neutral và 114 Negative."))
B(("p", "Hai ràng buộc được áp dụng nghiêm ngặt trên phép chia này. **Thứ nhất**, tập kiểm "
       "tra cuối bị khóa: không một chỉ số nào tính trên tập này được dùng để chọn đặc "
       "trưng, chọn siêu tham số hay chọn mô hình. **Thứ hai**, vectorizer và bộ chuẩn hóa "
       "được fit lại độc lập bên trong từng fold của kiểm định chéo, chứ không fit một lần "
       "trên toàn tập phát triển — nếu fit một lần, thông tin về phân phối từ vựng của phần "
       "kiểm định đã rò rỉ vào phần huấn luyện và kết quả CV sẽ lạc quan giả tạo."))
B(("p", "Tất cả artifact sinh ra từ phép chia này đều kèm một tệp manifest ghi phiên bản "
       "Python, giá trị băm SHA-256 của tệp dữ liệu nguồn, Git SHA của mã nguồn tại thời "
       "điểm sinh, và checksum của chính artifact. Nhờ vậy có thể kiểm chứng rằng mọi con số "
       "trong Chương 3 và Chương 4 đều được sinh từ cùng một phép chia dữ liệu."))
B(("pagebreak",))

# ==========================================================================
# CHƯƠNG 3
# ==========================================================================
B(("h1", "CHƯƠNG 3. BIỂU DIỄN VĂN BẢN VÀ MÔ HÌNH HỌC MÁY"))

B(("h2", "3.1. Phương pháp trích xuất đặc trưng văn bản"))
B(("h3", "3.1.1. Giao thức thí nghiệm chung"))
B(("p", "Mọi so sánh trong chương này đều tuân theo một giao thức thống nhất, nhằm bảo đảm "
       "chênh lệch quan sát được phản ánh đúng yếu tố đang khảo sát chứ không phải nhiễu "
       "ngẫu nhiên hoặc khác biệt về điều kiện thí nghiệm."))
B(("bullet", [
    "**Dữ liệu**: tập phát triển 6.730 mẫu; tập kiểm tra cuối 1.683 mẫu bị khóa hoàn toàn "
    "trong suốt giai đoạn chọn đặc trưng.",
    "**Giao thức đánh giá**: 5-fold Stratified Cross-Validation trên tập phát triển, dùng "
    "chung một bộ fold và một seed cho mọi cấu hình.",
    "**Bộ phân loại cố định**: Logistic Regression với `class_weight='balanced'`, "
    "`max_iter=1000`, `random_state=2026`. Việc cố định bộ phân loại cho phép quy mọi "
    "chênh lệch quan sát được về khác biệt giữa các nhóm đặc trưng.",
    "**Chống rò rỉ**: vectorizer và bộ chuẩn hóa `MinMaxScaler` được fit lại độc lập bên "
    "trong từng fold, chỉ trên phần huấn luyện của fold đó.",
    "**Chỉ số**: Macro F1 là chỉ số quyết định; Neutral F1, Negative F1, Recall Negative "
    "và Accuracy được báo cáo kèm để lộ rõ các đánh đổi.",
]))

B(("h3", "3.1.2. Lựa chọn cấu hình TF-IDF"))
B(("p", "TF-IDF được fit trên cột `clean_advance_text` với `max_features=5000`, `min_df=2` "
       "và `sublinear_tf=True`. Tham số `min_df=2` loại các token chỉ xuất hiện một lần "
       "trên toàn tập — thường là lỗi gõ hoặc tên riêng — vốn không thể khái quát hóa. "
       "Tham số `sublinear_tf=True` thay tần suất thô bằng dạng logarit, giúp một từ lặp "
       "mười lần trong một review không có trọng số gấp mười lần so với khi xuất hiện một "
       "lần; điều này đặc biệt phù hợp với dữ liệu có độ dài biến thiên lớn đã quan sát ở "
       "mục 2.2.2."))
B(("p", "Cấu hình n-gram được chọn bằng thực nghiệm thay vì theo mặc định."))
B(("table", "Bảng 3.1. So sánh cấu hình n-gram của TF-IDF trên 5-fold CV",
   ["Cấu hình", "Macro F1 trung bình", "Độ lệch chuẩn"],
   [["Unigram `(1, 1)`", "0,5396", "0,0073"],
    ["**Unigram + bigram `(1, 2)`**", "**0,5579**", "0,0127"]],
   ["l", "r", "r"]))
B(("figure", "Hình 3.1. So sánh cấu hình n-gram của TF-IDF",
   "reports/figures/eda_tfidf_ngram_comparison.png"))
B(("p", "Cấu hình unigram kết hợp bigram cao hơn **0,0183 Macro F1** và được chọn cho toàn "
       "bộ thí nghiệm phía sau. Mức cải thiện này có lý giải ngôn ngữ học rõ ràng: bigram "
       "cho phép biểu diễn giữ lại các tổ hợp mang nghĩa đảo chiều như *không_tốt*, "
       "*ít_cơ_hội*, *lương_thấp* — những cặp mà biểu diễn unigram sẽ tách rời và làm mất "
       "quan hệ."))

B(("h3", "3.1.3. So sánh TF-IDF với Bag-of-Words"))
B(("p", "Hai phương pháp biểu diễn văn bản được so sánh trên cùng bộ fold, cùng cấu hình từ "
       "vựng và cùng bộ phân loại."))
B(("table", "Bảng 3.2. So sánh TF-IDF và Bag-of-Words trên cùng bộ fold",
   ["Phương pháp", "Macro F1", "Neutral F1", "Recall Negative", "Negative F1", "Accuracy"],
   [["**TF-IDF, sublinear TF**", "**0,5579**", "**0,4456**", "**0,4563**", "**0,3894**", "0,7158"],
    ["Bag-of-Words", "0,5418", "0,4147", "0,3773", "0,3706", "**0,7177**"]],
   ["l", "r", "r", "r", "r", "r"]))
B(("p", "TF-IDF cao hơn **0,0161 Macro F1** và cải thiện ở 4 trên 5 fold. Kết quả này là "
       "**lần thứ nhất trong ba lần** báo cáo quan sát được bẫy Accuracy: Bag-of-Words đạt "
       "Accuracy cao hơn (0,7177 so với 0,7158) nhưng Recall lớp Negative thấp hơn đáng kể "
       "(0,3773 so với 0,4563). Bag-of-Words đếm số lần xuất hiện tuyệt đối nên chịu ảnh "
       "hưởng mạnh từ các từ phổ biến của lớp đa số; trọng số nghịch đảo tần suất tài liệu "
       "của TF-IDF làm giảm ảnh hưởng đó. Nếu chọn theo Accuracy, nhóm đã chọn sai biểu "
       "diễn. Toàn bộ thí nghiệm phía sau dùng TF-IDF."))

B(("h2", "3.2. Thí nghiệm đối chứng nhóm đặc trưng"))
B(("h3", "3.2.1. Ba câu hỏi cần trả lời"))
B(("p", "Thí nghiệm đối chứng (ablation study) được thiết kế để trả lời ba câu hỏi cụ thể. "
       "**Thứ nhất**, mô hình học được bao nhiêu từ nội dung văn bản so với từ các điểm số "
       "có sẵn trong dữ liệu. **Thứ hai**, nhóm đặc trưng từ điển cảm xúc sau khi nâng độ "
       "bao phủ lên gần 100% có thực sự cải thiện kết quả hay không. **Thứ ba**, việc bổ "
       "sung năm điểm khía cạnh có cải thiện riêng hai lớp thiểu số Neutral và Negative hay "
       "không, và nếu có thì mức cải thiện đó phản ánh điều gì."))
B(("table", "Bảng 3.3. Kết quả thí nghiệm đối chứng năm nhóm đặc trưng",
   ["Nhóm đặc trưng", "Macro F1", "Neutral F1", "Recall Negative", "Negative F1", "Accuracy"],
   [["Text-only", "0,5579", "0,4456", "0,4563", "0,3894", "0,7158"],
    ["Text + lexicon", "0,5664", "0,4578", "0,4803", "0,3999", "0,7211"],
    ["Text + aspect", "0,7369", "0,6441", "0,6952", "0,6485", "0,8373"],
    ["**Text + lexicon + aspect**", "**0,7433**", "**0,6497**", "0,7061", "0,6606", "**0,8409**"],
    ["Aspect ratings only", "0,7388", "0,6353", "**0,7676**", "**0,6649**", "0,8337"]],
   ["l", "r", "r", "r", "r", "r"]))
B(("figure", "Hình 3.2. Thí nghiệm đối chứng năm nhóm đặc trưng trên tập phát triển",
   "reports/figures/eda_feature_ablation_cv.png"))
B(("figure", "Hình 3.3. Chỉ số theo lớp thiểu số của từng nhóm đặc trưng",
   "reports/figures/eda_ablation_per_class.png"))
B(("p", "Một chi tiết kỹ thuật bảo đảm tính so sánh được của hai bảng 3.1 và 3.3: cột "
       "`clean_advance_text` không thay đổi sau khi cập nhật thuật toán từ điển, giống hệt "
       "trên toàn bộ 8.417 dòng. Nhờ vậy cấu hình Text-only tái lập đúng giá trị 0,5579 của "
       "thí nghiệm n-gram."))

B(("h3", "3.2.2. Kiểm định chênh lệch theo từng cặp fold"))
B(("p", "Chênh lệch giữa các giá trị trung bình trong Bảng 3.3 chưa đủ để kết luận, vì độ "
       "lệch chuẩn giữa các fold nằm trong khoảng 0,007 đến 0,015 — có thể lớn hơn chính "
       "chênh lệch cần đo. Do các nhóm đặc trưng dùng chung fold và chung seed, chênh lệch "
       "được tính lại theo **từng cặp fold tương ứng**, một cách kiểm định chặt chẽ hơn "
       "nhiều so với so sánh hai giá trị trung bình."))
B(("table", "Bảng 3.4. Kiểm định chênh lệch theo từng cặp fold so với Text-only",
   ["So với Text-only", "Delta Macro F1", "Số fold cải thiện", "Delta nhỏ nhất"],
   [["Text + lexicon", "+0,0084", "4/5", "−0,0038"],
    ["Text + aspect", "+0,1789", "5/5", "+0,1635"],
    ["Text + lexicon + aspect", "+0,1853", "5/5", "+0,1647"],
    ["Aspect ratings only", "+0,1808", "5/5", "+0,1640"]],
   ["l", "r", "c", "r"]))
B(("p", "Bảng này làm lộ ra một khác biệt về chất mà bảng giá trị trung bình che giấu. "
       "Nhóm đặc trưng khía cạnh cải thiện ở **toàn bộ 5 trên 5 fold** với fold kém nhất "
       "vẫn tăng trên 0,16 — một tín hiệu cực mạnh và nhất quán. Nhóm đặc trưng từ điển thì "
       "ngược lại: cải thiện ở 4 trên 5 fold nhưng fold xấu nhất **giảm** 0,0038."))

B(("h3", "3.2.3. Kết quả đối với đặc trưng từ điển cảm xúc"))
B(("p", "Việc nâng độ bao phủ từ điển đã đảo chiều đóng góp của nhóm đặc trưng này. Ở phiên "
       "bản đối sánh từ đơn, cấu hình Text + lexicon đạt 0,5556 Macro F1 — **thấp hơn** "
       "Text-only, tức là nhóm đặc trưng này khi đó là nhiễu thuần túy. Ở phiên bản đối sánh "
       "cụm từ tham lam mô tả ở mục 2.3.4, cấu hình này đạt 0,5664, **cao hơn** Text-only."))
B(("p", "Cần trung thực về mức độ chắc chắn của kết luận này. Mức cải thiện chỉ đạt "
       "**+0,0084 Macro F1**, xuất hiện ở 4 trên 5 fold, với fold xấu nhất giảm 0,0038. "
       "Biên độ này vẫn nằm trong dao động giữa các fold, nên **chưa đủ bằng chứng thống kê "
       "để khẳng định chắc chắn** — dù bằng chứng đã mạnh hơn phiên bản từ điển trước, khi "
       "đó chỉ cải thiện ở 3 trên 5 fold. Việc khẳng định mức tăng này đòi hỏi lặp lại kiểm "
       "định chéo với nhiều seed khác nhau, một thí nghiệm nhóm chưa thực hiện được trong "
       "khung thời gian của đồ án."))
B(("p", "Ở mức đặc trưng đơn lẻ, tín hiệu rõ ràng hơn. Đặc trưng `sentiment_ratio` sau khi "
       "cập nhật đã phân tách ba lớp đúng theo thứ tự kỳ vọng, với giá trị trung bình "
       "**0,063** ở lớp Negative, **0,429** ở lớp Neutral và **0,677** ở lớp Positive. Ở "
       "phiên bản trước, đặc trưng này gần như phẳng giữa ba lớp — bằng chứng cho thấy vấn "
       "đề nằm ở độ bao phủ từ điển chứ không ở ý tưởng thiết kế đặc trưng."))

B(("h3", "3.2.4. Kết quả đối với điểm khía cạnh và rủi ro data shortcut"))
B(("p", "Việc bổ sung năm điểm khía cạnh cải thiện cả ba chỉ số quan tâm, ở toàn bộ 5 trên "
       "5 fold: Neutral F1 tăng từ 0,4456 lên 0,6497 (**+0,2041**), Recall lớp Negative "
       "tăng từ 0,4563 lên 0,7061 (**+0,2498**) và Macro F1 tăng từ 0,5579 lên 0,7433 "
       "(**+0,1853**). Nếu chỉ nhìn bảng số, đây là cấu hình nên được chọn."))
B(("p", "Nhóm quyết định **không** đưa nhóm đặc trưng này vào pipeline triển khai, vì hai "
       "lý do được trình bày dưới đây."))
B(("p", "**Lý do thứ nhất — rò rỉ nhãn.** Nhãn `sentiment` được suy ra trực tiếp từ "
       "`Rating`, trong khi năm điểm khía cạnh có tương quan Spearman từ 0,5423 đến 0,7368 "
       "với chính `Rating` (Bảng 2.8). Phần lớn mức tăng do đó phản ánh việc mô hình khôi "
       "phục lại thang điểm đã sinh ra nhãn, chứ không phản ánh năng lực hiểu ngôn ngữ tốt "
       "hơn. Bằng chứng trực tiếp nhất cho nhận định này nằm ngay trong Bảng 3.3: cấu hình "
       "**Aspect ratings only đạt Macro F1 0,7388 mà không đọc một từ nào** trong review. "
       "Một mô hình phân tích cảm xúc văn bản không đọc văn bản mà vẫn vượt xa mô hình đọc "
       "văn bản thì thứ nó học được không phải là cảm xúc trong ngôn ngữ."))
B(("p", "**Lý do thứ hai — không khả dụng tại thời điểm suy luận.** Cấu hình chứa điểm khía "
       "cạnh đòi hỏi đủ năm điểm số tại thời điểm dự đoán. Kịch bản sử dụng thực tế của ứng "
       "dụng, trong đó người dùng chỉ nhập một đoạn văn bản tự do, không đáp ứng được điều "
       "kiện này. Một mô hình đạt Macro F1 0,74 trên giấy nhưng không chạy được trong sản "
       "phẩm thì không có giá trị triển khai."))
B(("p", "Một quan sát bổ sung đáng chú ý: cấu hình Aspect ratings only đạt Recall Negative "
       "cao nhất (0,7676) nhưng Neutral F1 lại **thấp hơn** cấu hình có văn bản (0,6353 so "
       "với 0,6497). Điều này cho thấy biểu diễn văn bản vẫn đóng góp thông tin riêng cho "
       "việc phân tách lớp Neutral, và mô hình đầy đủ không đơn thuần đọc lại thang điểm "
       "khía cạnh."))
B(("quote", "Kết luận của mục này: báo cáo giữ song song hai bộ đặc trưng. Cấu hình chứa "
            "điểm khía cạnh chỉ phục vụ phần thí nghiệm đối chứng và luôn được trình bày "
            "kèm giới hạn vừa nêu. Cấu hình chỉ dùng văn bản — và biến thể văn bản kết hợp "
            "từ điển — phục vụ toàn bộ phần mô hình hóa, đánh giá và triển khai ở Chương 4 "
            "và Chương 5."))

B(("h3", "3.2.5. Ma trận đặc trưng bàn giao"))
B(("table", "Bảng 3.5. Kích thước ma trận đặc trưng của hai cấu hình bàn giao",
   ["Cấu hình", "Tập phát triển", "Tập kiểm tra cuối", "Sử dụng"],
   [["Chỉ văn bản", "6.730 × 5.000", "1.683 × 5.000", "Pipeline chính thức, mô hình triển khai"],
    ["Văn bản + từ điển", "6.730 × 5.005", "1.683 × 5.005", "Mô hình thứ hai trong ứng dụng web"],
    ["Văn bản + từ điển + khía cạnh", "6.730 × 5.010", "1.683 × 5.010",
     "Chỉ dùng cho thí nghiệm đối chứng"]],
   ["l", "c", "c", "l"]))
B(("p", "Năm cột khía cạnh không có giá trị khuyết thiếu trên toàn bộ dữ liệu, nên bước thay "
       "giá trị khuyết bằng 0 trong `FeatureExtractor._prepare_numeric` không kích hoạt và "
       "không tạo ra giá trị nằm ngoài thang 1–5. Hai cột `pos_e` và `neg_e` chỉ khác 0 trên "
       "20 review như đã nêu ở mục 2.2.6, nên trong 10 cột số của cấu hình đầy đủ chỉ có 8 "
       "cột đóng góp đáng kể."))

B(("h2", "3.3. Xử lý mất cân bằng dữ liệu"))
B(("p", "Với tỷ lệ lớp Positive gấp 10,9 lần lớp Negative, ba chiến lược được so sánh thực "
       "nghiệm trên cùng giao thức. SMOTE chỉ được áp dụng trên phần huấn luyện của từng "
       "fold, không bao giờ trên phần kiểm định — nếu sinh mẫu tổng hợp trước khi chia fold, "
       "các mẫu nội suy từ dữ liệu kiểm định sẽ rò rỉ vào dữ liệu huấn luyện và kết quả trở "
       "nên vô nghĩa."))
B(("table", "Bảng 3.6. So sánh ba chiến lược xử lý mất cân bằng lớp",
   ["Chiến lược", "Macro F1", "Neutral F1", "Recall Negative", "Negative F1", "Accuracy"],
   [["Không xử lý", "0,4622", "0,3508", "0,0921", "0,1646", "**0,7676**"],
    ["`class_weight='balanced'`", "0,5579", "**0,4456**", "**0,4563**", "0,3894", "0,7158"],
    ["SMOTE", "**0,5600**", "0,4340", "0,4410", "**0,3989**", "0,7263"]],
   ["l", "r", "r", "r", "r", "r"]))
B(("p", "Dòng đầu tiên của bảng này là kết quả có ý nghĩa phương pháp luận quan trọng nhất "
       "trong toàn bộ Chương 3, và là **lần thứ hai** báo cáo quan sát bẫy Accuracy. Cấu "
       "hình không xử lý mất cân bằng đạt **Accuracy cao nhất trong cả ba** (0,7676) nhưng "
       "Recall lớp Negative chỉ **0,0921** — tức là bỏ sót hơn 90% số review tiêu cực. Với "
       "bài toán mà mục đích nghiệp vụ chính là phát hiện phản hồi tiêu cực, đây là một mô "
       "hình vô dụng có điểm Accuracy đẹp nhất."))
B(("p", "Giữa hai chiến lược còn lại, SMOTE cao hơn 0,0020 Macro F1 nhưng chỉ cải thiện ở "
       "**2 trên 5 fold** — tức là không phân biệt được với `class_weight='balanced'` ở mức "
       "nhiễu hiện tại. Trong khi đó `class_weight='balanced'` cho Recall lớp Negative cao "
       "hơn (0,4563 so với 0,4410), không sinh thêm mẫu tổng hợp, và giữ nguyên kích thước "
       "ma trận huấn luyện. Với biểu diễn TF-IDF thưa và số chiều cao, các vector do SMOTE "
       "nội suy cũng khó diễn giải về mặt ngữ nghĩa vì chúng không tương ứng với văn bản có "
       "thật nào."))
B(("p", "Từ các căn cứ trên, `class_weight='balanced'` được chọn làm chiến lược mặc định cho "
       "mọi thí nghiệm trong báo cáo. SMOTE được giữ lại trong `src/features.py` như một "
       "lựa chọn thay thế cho các mô hình không hỗ trợ trọng số lớp."))

B(("h2", "3.4. Thiết kế các mô hình học máy"))
B(("h3", "3.4.1. Đầu vào thống nhất"))
B(("p", "Toàn bộ mô hình trong chương này dùng lại đúng artifact text-only đã bàn giao ở mục "
       "3.2.5, tệp `models/train_test_features.joblib`: ma trận huấn luyện 6.730 × 5.000 và "
       "ma trận kiểm tra cuối 1.683 × 5.000, vector hóa bằng TF-IDF unigram kết hợp bigram "
       "với `sublinear_tf=True`. Notebook mô hình hóa chỉ nạp artifact qua hàm "
       "`load_feature_split`, **không fit lại TF-IDF**. Ràng buộc này bảo đảm mọi mô hình "
       "được so sánh trên đúng cùng một không gian đặc trưng."))

B(("h3", "3.4.2. Bốn mô hình cơ sở"))
B(("table", "Bảng 3.7. Cấu hình bốn mô hình học máy cơ sở",
   ["Mô hình", "Cấu hình chính", "Vai trò trong thiết kế"],
   [["Multinomial Naive Bayes", "`alpha` được tinh chỉnh",
     "Đường cơ sở cổ điển cho phân loại văn bản"],
    ["Logistic Regression", "`class_weight='balanced'`; `C`, `solver`, `penalty` tinh chỉnh",
     "Mô hình tuyến tính chính, chịu được dữ liệu mất cân bằng"],
    ["Linear SVM", "`class_weight='balanced'`, `probability=True`, `C` tinh chỉnh",
     "Tối ưu cho không gian TF-IDF nhiều chiều; xuất xác suất để dùng trong Stacking"],
    ["Random Forest", "`class_weight='balanced'`; `n_estimators`, `max_depth` tinh chỉnh",
     "Mô hình cây kết hợp, bắt được tương tác phi tuyến giữa các đặc trưng"]],
   ["l", "l", "l"]))
B(("p", "Cả bốn mô hình đều dùng `class_weight='balanced'`, ngoại trừ Naive Bayes vốn không "
       "hỗ trợ tham số này do bản chất sinh của thuật toán. Lựa chọn Linear SVM thay vì "
       "kernel phi tuyến xuất phát từ đặc điểm dữ liệu: trong không gian 5.000 chiều thưa, "
       "các lớp gần như đã tách tuyến tính, và kernel phi tuyến chỉ làm tăng chi phí tính "
       "toán mà không cải thiện kết quả."))

B(("h3", "3.4.3. Mô hình Stacking Ensemble"))
B(("p", "Mô hình thứ năm kết hợp ba mô hình cơ sở tốt nhất — **Naive Bayes, Logistic "
       "Regression và Linear SVM** — làm bộ ước lượng tầng nền, với một Logistic Regression "
       "khác đóng vai trò meta-classifier ở tầng kết hợp, cấu hình `StackingClassifier(cv=5)`."))
B(("p", "Ý tưởng của Stacking là các mô hình cơ sở mắc lỗi theo những cách khác nhau: Naive "
       "Bayes có xu hướng thiên về lớp đa số nhưng rất ổn định; Logistic Regression cân bằng "
       "giữa các lớp; Linear SVM nhạy hơn với các mẫu nằm gần biên quyết định. Meta-classifier "
       "học cách đặt trọng số cho dự đoán của từng mô hình tùy theo vùng không gian đặc "
       "trưng, thay vì lấy trung bình cứng. Random Forest được loại khỏi tầng nền vì kết quả "
       "kiểm định chéo cho thấy nó không bổ sung thông tin độc lập so với ba mô hình còn lại."))
B(("p", "Một chi tiết quan trọng về tính đúng đắn: Stacking sử dụng đúng bộ siêu tham số đã "
       "tinh chỉnh ở mục 3.5 cho từng mô hình nền, **không khởi tạo lại tham số mặc định**. "
       "Nếu dùng tham số mặc định, so sánh giữa Stacking và các mô hình đã tinh chỉnh sẽ "
       "không công bằng."))

B(("h3", "3.4.4. Mô hình ViSoBERT"))
B(("p", "Mô hình thứ sáu là checkpoint tiền huấn luyện `5CD-AI/Vietnamese-Sentiment-visobert`, "
       "được benchmark ở **chế độ zero-shot, không fine-tune**, trên đúng tập kiểm tra cuối "
       "1.683 mẫu mà Stacking sử dụng. Thí nghiệm được chạy thật trên GPU đám mây."))
B(("p", "Đầu vào của ViSoBERT là cột `clean_basic_text` chứ không phải `clean_advance_text`, "
       "đúng theo thiết kế pipeline hai tầng đã trình bày ở mục 2.3.1. Việc đưa văn bản đã "
       "tách từ và lọc từ dừng vào một tokenizer BPE sẽ tạo ra phân phối token lệch hoàn "
       "toàn so với dữ liệu tiền huấn luyện. Kết quả và phân tích chi tiết được trình bày ở "
       "mục 4.4."))

B(("h2", "3.5. Tinh chỉnh siêu tham số"))
B(("h3", "3.5.1. Đường cơ sở với tham số mặc định"))
B(("p", "Trước khi tinh chỉnh, bốn mô hình được chạy với tham số mặc định của thư viện để "
       "thiết lập mốc so sánh."))
B(("table", "Bảng 3.8. Kết quả 5-fold CV với tham số mặc định",
   ["Mô hình", "CV Macro F1 trung bình", "Độ lệch chuẩn"],
   [["Logistic Regression", "0,5567", "0,0155"],
    ["Linear SVM", "0,5448", "0,0114"],
    ["Random Forest", "0,5286", "0,0370"],
    ["Multinomial Naive Bayes", "0,3460", "0,0054"]],
   ["l", "r", "r"]))
B(("p", "Hai quan sát đáng chú ý. Naive Bayes ở mức 0,3460 gần như vô dụng với tham số mặc "
       "định — `alpha=1.0` làm mượt quá mạnh trên từ vựng 5.000 chiều thưa. Random Forest có "
       "độ lệch chuẩn 0,0370, cao gấp đôi đến gấp ba các mô hình còn lại, cho thấy kết quả "
       "của nó phụ thuộc nhiều vào cách chia fold."))

B(("h3", "3.5.2. Lưới siêu tham số và kết quả tìm kiếm"))
B(("p", "Quá trình tinh chỉnh sử dụng `GridSearchCV` với 5-fold Stratified CV, hàm mục tiêu "
       "tối ưu là **Macro F1** — không phải Accuracy, theo đúng lập luận ở mục 2.2.1."))
B(("table", "Bảng 3.9. Lưới siêu tham số và kết quả GridSearchCV",
   ["Mô hình", "Lưới tham số", "CV Macro F1 sau tinh chỉnh", "Tham số tối ưu"],
   [["Multinomial Naive Bayes", "`alpha ∈ [0.01, 0.1, 0.5, 1.0, 2.0]`", "0,4890", "`alpha=0.1`"],
    ["Logistic Regression",
     "`C ∈ [0.1, 1, 5, 10]`; `solver ∈ [lbfgs, saga]`; `penalty ∈ [l1, l2]`",
     "0,5567", "`C=1.0, penalty=l2, solver=lbfgs`"],
    ["Linear SVM", "`C ∈ [0.1, 0.5, 1, 2, 5]`", "0,5561", "`C=0.1`"],
    ["Random Forest", "`n_estimators ∈ [100, 200]`; `max_depth ∈ [10, 20, None]`",
     "0,5515", "`n_estimators=200, max_depth=20`"]],
   ["l", "l", "r", "l"]))
B(("p", "Lưới của Logistic Regression phải tách thành hai nhánh (`lbfgs` kết hợp `l2`, và "
       "`saga` kết hợp cả `l1` lẫn `l2`) vì solver `lbfgs` không hỗ trợ chuẩn hóa `l1`."))
B(("p", "So với đường cơ sở, tinh chỉnh cải thiện rõ rệt Naive Bayes (**+0,1430**, từ 0,3460 "
       "lên 0,4890) nhờ giảm hệ số làm mượt từ 1,0 xuống 0,1. Random Forest tăng **+0,0229** "
       "và quan trọng hơn là ổn định hơn hẳn khi giới hạn độ sâu ở 20. Linear SVM tăng "
       "**+0,0113** với giá trị `C=0.1` — tham số phạt nhỏ, tức là mô hình chọn biên rộng "
       "và chấp nhận nhiều lỗi huấn luyện hơn, phù hợp với dữ liệu nhiều nhiễu nhãn như đã "
       "phân tích ở mục 2.2.6. Logistic Regression giữ nguyên 0,5567 vì cấu hình mặc định "
       "vốn đã là điểm tối ưu trong lưới tìm kiếm."))

B(("h3", "3.5.3. Xếp hạng cuối cùng trên tập phát triển"))
B(("table", "Bảng 3.10. Xếp hạng CV Macro F1 sau tinh chỉnh",
   ["Hạng", "Mô hình", "Cấu hình", "CV Macro F1"],
   [["1", "**Stacking Ensemble**", "NB + LR + Linear SVM đã tinh chỉnh", "**0,5619**"],
    ["2", "Logistic Regression", "`C=1.0`, L2, balanced", "0,5567"],
    ["3", "Linear SVM", "`C=0.1`, balanced", "0,5561"],
    ["4", "Random Forest", "200 cây, độ sâu 20", "0,5515"],
    ["5", "Multinomial Naive Bayes", "`alpha=0.1`", "0,4890"]],
   ["c", "l", "l", "r"]))
B(("figure", "Hình 3.4. So sánh CV Macro F1 giữa các mô hình sau tinh chỉnh",
   "reports/figures/model_comparison_f1_macro.png"))
B(("p", "Stacking Ensemble đạt CV Macro F1 cao nhất và được **khóa làm mô hình cuối cùng**, "
       "lưu tại `models/best_sentiment_model.joblib`. Cần lưu ý rằng khoảng cách giữa "
       "Stacking (0,5619) và Logistic Regression (0,5567) chỉ là 0,0052 — nhỏ hơn độ lệch "
       "chuẩn giữa các fold của hầu hết mô hình. Vì vậy phát biểu trung thực là *Stacking "
       "đạt điểm cao nhất trên giao thức này*, chứ không phải *Stacking vượt trội hơn hẳn "
       "Logistic Regression*. Nhóm vẫn chọn Stacking vì nó không kém hơn ở bất kỳ chỉ số "
       "nào, nhưng không xem chênh lệch này là bằng chứng mạnh."))
B(("p", "Sau bước này, lựa chọn mô hình được khóa hoàn toàn. Tập kiểm tra cuối được mở ở "
       "Chương 4 và chỉ được đánh giá đúng một lần."))

B(("h2", "3.6. Kiến trúc suy luận thực tế: bộ máy ra quyết định lai"))
B(("p", "Mô hình đã khóa ở mục 3.5 là kết quả nghiên cứu. Khi đưa vào ứng dụng thực tế, nhóm "
       "bổ sung thêm một tầng ra quyết định đặt **sau** đầu ra xác suất của mô hình, gọi là "
       "**Hybrid Decision Gate**. Tầng này kết hợp xác suất do mô hình học máy sinh ra với "
       "tri thức ngữ nghĩa tiên nghiệm lấy từ bộ đặc trưng từ điển ở mục 2.3.4."))
B(("p", "Lý do tồn tại của tầng này bắt nguồn trực tiếp từ hai kết quả đã trình bày. Thứ "
       "nhất, mô hình bỏ sót gần ba phần tư review tiêu cực (Bảng 4.2). Thứ hai, thuật toán "
       "nhận diện phạm vi phủ định tính được những tín hiệu mà biểu diễn TF-IDF không thể "
       "biểu diễn — cụ thể là cụm *không được thân thiện* đã bị đảo chiều thành tín hiệu "
       "tiêu cực trước khi vào mô hình. Hybrid Decision Gate cho phép tín hiệu này can thiệp "
       "vào kết luận cuối khi nó đủ mạnh và mô hình đang phân vân."))
B(("p", "Trình tự ra quyết định trong ứng dụng gồm ba tầng xếp chồng:"))
B(("num", [
    "**Tầng mô hình học máy**: mô hình đã khóa sinh ra phân phối xác suất trên ba lớp.",
    "**Tầng chính sách ngưỡng**: nếu xác suất lớp Negative đạt từ 0,30 trở lên thì kết luận "
    "Negative, đúng theo chính sách ở mục 4.5.",
    "**Tầng cổng lai**: ba luật dựa trên đặc trưng từ điển có thể ghi đè kết luận của hai "
    "tầng trên.",
]))
B(("p", "Ba luật của tầng cổng lai được cài đặt như sau, trong đó `neg_w` và `pos_w` là số "
       "cụm từ tiêu cực và tích cực đã khớp, còn `ratio` là giá trị `sentiment_ratio`:"))
B(("bullet", [
    "**Luật A — tín hiệu tiêu cực rất rõ.** Khi `neg_w >= 2` và `ratio <= -0,4` mà mô hình "
    "không kết luận Negative, hệ thống ghi đè thành Negative. Đây là trường hợp văn bản "
    "chứa nhiều cụm phàn nàn hoặc cụm đã bị phủ định đảo chiều, nhưng mô hình vẫn thiên về "
    "lớp đa số.",
    "**Luật B — mô hình phân vân ở vùng ranh giới.** Khi `neg_w > pos_w`, `ratio <= -0,2` "
    "và mô hình hoặc kết luận Neutral hoặc có khoảng cách giữa xác suất Neutral và Negative "
    "nhỏ hơn 0,15, hệ thống kết luận Negative. Luật này nhắm đúng đường lỗi lớn nhất của "
    "lớp Negative đã phân tích ở mục 4.3.",
    "**Luật C — tín hiệu tích cực áp đảo.** Khi `pos_w >= 2`, `ratio >= 0,5` mà mô hình kết "
    "luận Neutral, hệ thống nâng lên Positive.",
]))
B(("p", "Mỗi lần can thiệp, hệ thống ghi lại loại quyết định (`ml`, `threshold` hay "
       "`hybrid`) và một câu giải thích nêu rõ những cụm từ nào đã kích hoạt luật. Nhờ vậy "
       "người dùng luôn nhìn thấy vì sao kết luận cuối khác với dự đoán gốc của mô hình, "
       "thay vì đối diện một hộp đen."))
B(("quote", "Giới hạn cần nêu rõ: các ngưỡng 2, −0,4, −0,2, 0,5 và 0,15 của ba luật trên "
            "được chọn bằng quan sát thủ công trên các ví dụ khó, **không** được tối ưu "
            "bằng kiểm định chéo. Hybrid Decision Gate vì vậy chỉ hoạt động trong ứng dụng "
            "demo và **không tham gia vào bất kỳ con số nào ở Chương 4** — toàn bộ kết quả "
            "đánh giá trong chương đó được tính trên đầu ra thuần của mô hình và chính sách "
            "ngưỡng. Việc đưa tầng này vào báo cáo hiệu năng sẽ đòi hỏi tinh chỉnh ngưỡng "
            "trên tập phát triển rồi đánh giá lại một lần trên tập test mới."))
B(("pagebreak",))

# ==========================================================================
# CHƯƠNG 4
# ==========================================================================
B(("h1", "CHƯƠNG 4. KẾT QUẢ THỰC NGHIỆM VÀ ĐÁNH GIÁ"))

B(("h2", "4.1. Môi trường thực nghiệm và thang đo"))
B(("p", "Toàn bộ thí nghiệm học máy cổ điển được chạy trên Python 3.11 với môi trường khóa "
       "phiên bản trong tệp `requirements.lock`. Thí nghiệm ViSoBERT được chạy trên GPU đám "
       "mây. Mỗi artifact mô hình đi kèm một manifest ghi phiên bản Python, giá trị băm "
       "SHA-256 của dữ liệu nguồn, Git SHA của mã nguồn và checksum của artifact."))
B(("p", "Bốn thang đo được sử dụng, với vai trò phân biệt rõ ràng:"))
B(("bullet", [
    "**Macro F1** — trung bình cộng không trọng số của F1 ba lớp. Đây là chỉ số quyết định "
    "của toàn bộ báo cáo, vì nó cho lớp Negative với 114 mẫu cùng trọng số như lớp Positive "
    "với 1.241 mẫu.",
    "**Recall lớp Negative** — tỷ lệ review tiêu cực được phát hiện. Đây là chỉ số nghiệp "
    "vụ quan trọng nhất: bỏ sót một phản hồi tiêu cực gây thiệt hại lớn hơn cảnh báo nhầm.",
    "**Precision lớp Negative** — độ tin cậy của cảnh báo tiêu cực. Luôn được báo cáo kèm "
    "Recall, vì có thể nâng Recall lên rất cao bằng cách dự đoán Negative tràn lan.",
    "**Accuracy** — được báo cáo để đối chiếu và để minh họa bẫy Accuracy, **không** dùng "
    "làm căn cứ lựa chọn ở bất kỳ bước nào.",
]))

B(("h2", "4.2. Kết quả trên tập kiểm tra cuối"))
B(("p", "Mô hình Stacking Ensemble đã khóa được đánh giá **đúng một lần** trên 1.683 mẫu của "
       "tập kiểm tra cuối, gồm 114 Negative, 328 Neutral và 1.241 Positive."))
B(("table", "Bảng 4.1. Kết quả tổng hợp của Stacking Ensemble trên tập kiểm tra cuối",
   ["Chỉ số", "Giá trị trên tập kiểm tra cuối", "Ước lượng CV trên tập phát triển"],
   [["Accuracy", "0,7766", "—"],
    ["Macro F1", "0,5475", "0,5619"]],
   ["l", "r", "r"]))
B(("table", "Bảng 4.2. Chỉ số theo từng lớp của Stacking Ensemble trên tập kiểm tra cuối",
   ["Lớp", "Precision", "Recall", "F1", "Số mẫu"],
   [["Negative", "0,5357", "0,2632", "0,3529", "114"],
    ["Neutral", "0,4914", "0,3476", "0,4071", "328"],
    ["Positive", "0,8337", "0,9371", "0,8824", "1.241"]],
   ["l", "r", "r", "r", "r"]))
B(("p", "Macro F1 trên tập kiểm tra cuối (0,5475) thấp hơn ước lượng CV (0,5619) khoảng "
       "0,0144. Đây là khoảng chênh hợp lý phản ánh phương sai giữa các fold, **không phải "
       "dấu hiệu rò rỉ dữ liệu**: tập kiểm tra cuối chỉ được dùng đúng một lần, sau khi mô "
       "hình đã khóa bằng kiểm định chéo. Nếu có rò rỉ, chênh lệch sẽ theo chiều ngược lại."))
B(("p", "Bảng 4.2 cho thấy rõ cấu trúc năng lực của mô hình. Lớp Positive được nhận diện rất "
       "tốt với F1 0,8824 và Recall 0,9371. Lớp Neutral kém hơn nhiều với F1 0,4071. Lớp "
       "Negative có Precision chấp nhận được (0,5357) nhưng **Recall chỉ 0,2632** — mô hình "
       "bỏ sót gần ba phần tư số review tiêu cực. Đây chính là điểm yếu đã được dự báo từ "
       "phân tích EDA ở mục 2.2.1, và là lý do trực tiếp dẫn đến chính sách hiệu chỉnh ngưỡng "
       "trình bày ở mục 4.5."))

B(("h2", "4.3. Phân tích ma trận nhầm lẫn"))
B(("figure", "Hình 4.1. Ma trận nhầm lẫn của mô hình Stacking Ensemble",
   "reports/figures/best_model_confusion_matrix.png"))
B(("table", "Bảng 4.3. Ma trận nhầm lẫn của phương án argmax mặc định",
   ["Nhãn thật \\\\ Dự đoán", "Negative", "Neutral", "Positive", "Tổng"],
   [["Negative", "**30**", "49", "35", "114"],
    ["Neutral", "17", "**114**", "197", "328"],
    ["Positive", "9", "69", "**1.163**", "1.241"],
    ["Tổng dự đoán", "56", "232", "1.395", "1.683"]],
   ["l", "r", "r", "r", "r"]))
B(("p", "Ba đường lỗi chính có thể đọc trực tiếp từ ma trận."))
B(("p", "**Lỗi Negative bị đẩy sang Neutral (49 trên 114 mẫu).** Đây là đường lỗi lớn nhất "
       "của lớp Negative. Các review 2 sao thường có giọng văn tiết chế hơn review 1 sao, "
       "nêu vấn đề dưới dạng góp ý thay vì phàn nàn gay gắt, nên phân phối từ vựng của chúng "
       "nằm gần lớp Neutral. Nhóm lỗi này chính là mục tiêu mà chính sách ngưỡng ở mục 4.5 "
       "nhắm vào."))
B(("p", "**Lỗi Negative bị đẩy sang Positive (35 trên 114 mẫu).** Đây là nhóm lỗi nghiêm "
       "trọng hơn về mặt nghiệp vụ, vì mô hình không chỉ bỏ sót mà còn đảo chiều hoàn toàn "
       "kết luận. Phân tích định tính ở mục 4.6 cho thấy phần lớn thuộc nhóm review vừa "
       "khen vừa chê, trong đó phần khen đứng trước và chiếm nhiều từ hơn."))
B(("p", "**Lỗi Neutral bị đẩy sang Positive (197 trên 328 mẫu).** Đây là đường lỗi lớn nhất "
       "toàn ma trận xét theo số tuyệt đối. Kết quả này phù hợp với hai quan sát độc lập từ "
       "Chương 2: phân phối dữ liệu lệch mạnh về Positive, và 411 review Neutral thực chất "
       "không được người viết khuyến nghị (Bảng 2.9). Ranh giới giữa 3 sao và 4 sao vốn đã "
       "mờ ngay trong dữ liệu gốc."))
B(("p", "Xét tổng thể, mô hình đạt Accuracy 77,66% chủ yếu nhờ phân loại đúng 1.163 trên "
       "1.241 mẫu Positive. Nếu bỏ lớp Positive ra khỏi phép tính, mô hình chỉ đúng 144 "
       "trên 442 mẫu thuộc hai lớp thiểu số. Đây là **lần thứ ba** báo cáo chỉ ra bẫy "
       "Accuracy, lần này trên chính mô hình cuối cùng."))

B(("h2", "4.4. So sánh với mô hình ViSoBERT"))
B(("p", "Checkpoint ViSoBERT được benchmark ở chế độ zero-shot trên **đúng cùng 1.683 dòng** "
       "mà Stacking sử dụng, bảo đảm so sánh công bằng."))
B(("table", "Bảng 4.4. So sánh Stacking Ensemble và ViSoBERT zero-shot",
   ["Mô hình", "Accuracy", "Macro F1"],
   [["**Stacking Ensemble (NB + LR + SVM, đã tinh chỉnh)**", "**0,7766**", "**0,5475**"],
    ["ViSoBERT (zero-shot, không fine-tune)", "0,6536", "0,4036"]],
   ["l", "r", "r"]))
B(("table", "Bảng 4.5. Chỉ số theo từng lớp của ViSoBERT zero-shot",
   ["Lớp", "Precision", "Recall", "F1", "Số mẫu"],
   [["Negative", "0,1882", "**0,7544**", "0,3012", "114"],
    ["Neutral", "0,3902", "0,0488", "0,0867", "328"],
    ["Positive", "0,8422", "0,8042", "0,8228", "1.241"]],
   ["l", "r", "r", "r", "r"]))
B(("p", "Kết quả này thú vị hơn nhiều so với một kết luận đơn giản kiểu *Stacking thắng*. "
       "Đúng là Stacking vượt ViSoBERT 0,1439 Macro F1 về tổng thể, nhưng hai mô hình mắc "
       "lỗi theo hai cách hoàn toàn trái ngược."))
B(("p", "**ViSoBERT nhạy hơn hẳn với tín hiệu tiêu cực.** Recall lớp Negative đạt 0,7544 so "
       "với 0,2632 của Stacking — cao gần gấp ba. Là mô hình tiền huấn luyện trên khối lượng "
       "văn bản tiếng Việt lớn, nó nhận ra sắc thái phàn nàn tốt hơn nhiều so với mô hình "
       "học trên 6.730 mẫu. Cái giá phải trả là Precision chỉ 0,1882: cứ năm lần cảnh báo "
       "tiêu cực thì hơn bốn lần sai."))
B(("p", "**Điểm yếu chí mạng của ViSoBERT nằm ở lớp Neutral**, với Recall chỉ 0,0488 — mô "
       "hình gần như không nhận ra lớp này, đẩy hầu hết mẫu Neutral sang Positive hoặc "
       "Negative. Nguyên nhân có thể lý giải: checkpoint này được huấn luyện với một định "
       "nghĩa *trung tính* khác hẳn định nghĩa trong đồ án. Ở đây, Neutral không phải là "
       "*không có cảm xúc* mà là *chấm 3 sao* — một trạng thái thường chứa cả khen lẫn chê "
       "ở cường độ cao. Mô hình tổng quát không có cách nào biết được quy ước này."))
B(("p", "Bài học phương pháp rút ra: **một mô hình đơn giản được huấn luyện đúng trên phân "
       "phối dữ liệu mục tiêu vẫn có thể vượt một mô hình tiền huấn luyện mạnh nhưng chưa "
       "fine-tune.** Điều này không chứng minh Transformer kém hơn học máy cổ điển; nó chỉ "
       "cho thấy zero-shot không phải một cách dùng Transformer đúng cho bài toán có quy ước "
       "nhãn riêng. Hướng cải thiện hợp lý là fine-tune ViSoBERT trên chính tập huấn luyện "
       "này, nội dung được nêu lại ở mục 6.3."))

B(("h2", "4.5. Chính sách ngưỡng quyết định lớp Negative"))
B(("h3", "4.5.1. Cơ sở nghiệp vụ"))
B(("p", "Phương án argmax mặc định gán nhãn theo lớp có xác suất cao nhất, ngầm giả định "
       "rằng chi phí của mọi loại lỗi là như nhau. Giả định này không đúng trong bài toán "
       "quản trị nhân sự: bỏ sót một phản hồi tiêu cực khiến vấn đề tiếp tục tồn tại mà "
       "không ai biết, trong khi cảnh báo nhầm một phản hồi tích cực chỉ tốn thời gian của "
       "người đọc duyệt."))
B(("p", "Nhóm vì vậy áp dụng một chính sách hiệu chỉnh **sau suy luận**: nếu xác suất mô "
       "hình gán cho lớp Negative đạt từ **0,30** trở lên thì kết luận Negative, các trường "
       "hợp còn lại giữ nguyên dự đoán mặc định. Chính sách này không huấn luyện lại và "
       "không thay đổi trọng số mô hình; nó chỉ dịch chuyển ranh giới quyết định."))

B(("h3", "4.5.2. Kết quả áp dụng"))
B(("table", "Bảng 4.6. So sánh phương án argmax và chính sách ngưỡng 0,30",
   ["Tiêu chí", "Argmax mặc định", "Ngưỡng 0,30", "Thay đổi"],
   [["Accuracy", "77,66%", "77,30%", "−0,36 điểm %"],
    ["Macro F1", "0,5475", "**0,5507**", "**+0,0032**"],
    ["Recall Negative", "26,32% (30/114)", "**35,09% (40/114)**", "**+8,77 điểm %**"],
    ["Precision Negative", "53,57%", "44,44%", "−9,13 điểm %"],
    ["F1 Negative", "0,3529", "**0,3922**", "+0,0393"],
    ["Số dự đoán Negative", "56", "90", "+34"]],
   ["l", "r", "r", "r"]))
B(("table", "Bảng 4.7. Ma trận nhầm lẫn khi áp dụng chính sách ngưỡng 0,30",
   ["Nhãn thật \\\\ Dự đoán", "Negative", "Neutral", "Positive", "Tổng"],
   [["Negative", "**40**", "40", "34", "114"],
    ["Neutral", "31", "**100**", "197", "328"],
    ["Positive", "19", "61", "**1.161**", "1.241"],
    ["Tổng dự đoán", "90", "201", "1.392", "1.683"]],
   ["l", "r", "r", "r", "r"]))
B(("figure", "Hình 4.2. So sánh ma trận nhầm lẫn trước và sau chính sách ngưỡng",
   "reports/figures/stacking_confusion_matrix_threshold_comparison.png"))
B(("p", "Đọc hai ma trận cạnh nhau cho thấy chính xác chính sách này làm gì. Nó cứu thêm 10 "
       "mẫu Negative, **chủ yếu từ nhóm trước đó bị dự đoán Neutral** (49 giảm còn 40), đúng "
       "như thiết kế. Đổi lại, số cảnh báo sai tăng 24 mẫu: thêm 14 Neutral và 10 Positive "
       "bị chuyển thành Negative. Số mẫu Neutral bị đẩy sang Positive không đổi (197), vì "
       "chính sách chỉ tác động lên ranh giới của lớp Negative."))

B(("h3", "4.5.3. Phân tích độ nhạy theo ngưỡng"))
B(("p", "Nhóm khảo sát toàn dải ngưỡng để hiểu rõ đánh đổi, thay vì chỉ báo cáo một giá trị."))
B(("table", "Bảng 4.8. Phân tích độ nhạy theo ngưỡng quyết định lớp Negative",
   ["Ngưỡng", "Accuracy", "Macro F1", "Precision Neg.", "Recall Neg.", "Số dự đoán Neg."],
   [["0,10", "0,7267", "0,4561", "25,21%", "77,19%", "349"],
    ["0,14", "0,7570", "0,5240", "32,50%", "68,42%", "240"],
    ["**0,18**", "0,7683", "**0,5545**", "37,93%", "**57,89%**", "174"],
    ["0,24", "0,7724", "0,5574", "40,94%", "45,61%", "127"],
    ["**0,30** *(chính sách áp dụng)*", "0,7730", "0,5507", "44,44%", "35,09%", "90"],
    ["0,40", "0,7772", "0,5522", "53,33%", "28,07%", "60"],
    ["0,50 *(argmax)*", "0,7766", "0,5475", "53,57%", "26,32%", "56"]],
   ["l", "r", "r", "r", "r", "r"]))
B(("figure", "Hình 4.3. Độ nhạy của các chỉ số theo ngưỡng quyết định lớp Negative",
   "reports/figures/negative_threshold_sensitivity.png"))
B(("p", "Bảng này chứa một kết quả mà nhóm chọn báo cáo dù nó không có lợi. Dự kiến ban đầu "
       "của nhóm là ngưỡng 0,30 sẽ đưa Recall Negative lên khoảng 55–60%. Thực nghiệm **không "
       "xác nhận** dự kiến đó: tại 0,30 Recall chỉ đạt 35,09%. Mức Recall 57,89% chỉ đạt "
       "được tại ngưỡng **0,18**, kèm Macro F1 0,5545 — cao hơn cả phương án 0,30."))
B(("p", "Vậy tại sao không chuyển sang 0,18? Vì đó sẽ là một sai lầm về phương pháp. Ngưỡng "
       "0,18 được tìm ra bằng cách quét trên **chính tập kiểm tra cuối**. Nếu chọn nó làm "
       "chính sách chính thức rồi báo cáo Macro F1 0,5545 như kết quả đánh giá độc lập, nhóm "
       "sẽ đang tối ưu siêu tham số trên tập test và báo cáo con số đã bị thổi phồng. Bảng "
       "4.8 vì vậy được trình bày đúng bản chất của nó: **một phân tích độ nhạy hậu nghiệm, "
       "không phải một chính sách được chọn**. Tệp kết quả gốc cũng ghi rõ ghi chú này."))
B(("p", "Nếu nhóm muốn chính thức áp dụng ngưỡng khoảng 0,18, quy trình đúng là chọn ngưỡng "
       "trên tập validation hoặc bằng dự đoán out-of-fold trong tập phát triển, rồi đánh giá "
       "đúng một lần trên một tập test chưa từng chạm tới."))

B(("h2", "4.6. Phân tích lỗi định tính"))
B(("p", "Toàn bộ lỗi của mô hình được xuất ra tệp và 15 mẫu đại diện được đọc thủ công. Năm "
       "nhóm lỗi điển hình được nhận diện."))

B(("h3", "4.6.1. Review vừa khen vừa chê"))
B(("p", "Nhiều review 2 sao mở đầu bằng *môi trường năng động*, *sếp tâm lý*, *nhiều công "
       "nghệ mới*, rồi mới nêu *OT quá nhiều*, *lương thấp*. Mật độ tín hiệu tích cực ở phần "
       "đầu khiến mô hình kết luận Positive dù nhãn theo rating là Negative."))
B(("p", "Ví dụ điển hình là review nguồn `2668` của FPT Software: phần đầu khen môi trường "
       "và quản lý, phần sau lặp lại chuyện làm thêm giờ và phàn nàn lương. Mô hình gán "
       "`P(Negative) = 0,28%` — thấp đến mức **ngay cả ngưỡng 0,18 cũng không cứu được**. "
       "Đây là giới hạn của biểu diễn túi n-gram: nó đếm từ mà không biết câu nào là ý chính "
       "và câu nào là nhượng bộ."))

B(("h3", "4.6.2. Phủ định và sắc thái đảo chiều"))
B(("p", "Các cụm *không được trả*, *không có định hướng*, *gần như không có OT* mang ý nghĩa "
       "rất khác nhau tùy vào đối tượng bị phủ định — thậm chí *gần như không có OT* là một "
       "lời khen. TF-IDF không biểu diễn được quan hệ cú pháp nên có thể đánh đồng sự xuất "
       "hiện của *OT* và *không* với tín hiệu tiêu cực."))
B(("p", "Review nguồn `1828` có rating 5 sao nhưng nhắc tới *tạch*, *OT nhiều* và *áp lực*; "
       "mô hình gán `P(Negative) = 78,86%` và kết luận sai hoàn toàn. Thuật toán nhận diện "
       "phạm vi phủ định trình bày ở mục 2.3.4 xử lý được các mẫu phủ định cục bộ liền kề, "
       "nhưng không xử lý được phủ định trải dài qua nhiều mệnh đề."))

B(("h3", "4.6.3. Nhiễu từ nhãn yếu"))
B(("p", "Nhóm lỗi này khác hẳn ba nhóm còn lại: **mô hình có thể đang đúng còn nhãn mới là "
       "thứ sai**. Review nguồn `8096` có rating 3 sao (nhãn Neutral) nhưng nội dung mô tả "
       "quản lý kém, văn hóa tệ, thiếu đào tạo và quy trình thiếu chuyên nghiệp. Dự đoán "
       "Negative của mô hình hợp lý hơn nhãn yếu khi xét thuần túy nội dung văn bản."))
B(("p", "Đây chính là biểu hiện cụ thể của hiện tượng đã dự báo bằng số liệu ở mục 2.2.6: "
       "411 review Neutral không được chính người viết khuyến nghị. Một phần trong khoảng "
       "cách giữa Macro F1 0,5475 và mức hoàn hảo 1,0 không thể xóa bỏ bằng bất kỳ thuật "
       "toán nào, vì nó nằm ở chất lượng nhãn chứ không ở mô hình."))

B(("h3", "4.6.4. Từ lóng và ngữ cảnh ngành công nghệ thông tin"))
B(("p", "Các từ `OT`, `fresher`, `outsourcing`, `task`, `project`, `production` không mang "
       "một cực cảm xúc cố định. *OT có trả lương* khác hoàn toàn *OT không công*; *fresher "
       "được đào tạo bài bản* khác hẳn *fresher bị ném vào dự án*. Biểu diễn bigram bao phủ "
       "được một phần các tổ hợp phổ biến, nhưng các tổ hợp hiếm vẫn nằm ngoài từ vựng "
       "5.000 chiều."))

B(("h3", "4.6.5. Review dài trải rộng nhiều khía cạnh"))
B(("p", "Một review có thể đồng thời nói về lương, quản lý, văn hóa, dự án và cơ sở vật "
       "chất, với sắc thái khác nhau ở từng khía cạnh. Nhãn ba lớp buộc mô hình nén toàn bộ "
       "nội dung thành một kết luận duy nhất, làm mất hoàn toàn sắc thái theo khía cạnh. "
       "Đây không phải lỗi của mô hình mà là giới hạn của cách đặt bài toán, và là lý do "
       "trực tiếp để đề xuất chuyển sang bài toán ABSA ở mục 6.3."))

B(("h2", "4.7. Kết luận chương"))
B(("p", "Mô hình Stacking Ensemble đạt Accuracy 77,66% và Macro F1 0,5475 trên tập kiểm tra "
       "cuối đã khóa, vượt ViSoBERT zero-shot 0,1439 Macro F1. Chính sách ngưỡng 0,30 nâng "
       "Recall lớp Negative từ 26,32% lên 35,09% với chi phí là 9,13 điểm phần trăm "
       "Precision và 0,36 điểm phần trăm Accuracy."))
B(("p", "Ba kết luận về phương pháp đáng ghi nhận hơn các con số. **Thứ nhất**, bẫy Accuracy "
       "xuất hiện nhất quán ở cả ba thí nghiệm độc lập trong báo cáo — chọn biểu diễn, chọn "
       "chiến lược cân bằng lớp, và đánh giá mô hình cuối. **Thứ hai**, ngưỡng tốt nhất "
       "quan sát được trên tập test không được nhận làm chính sách, vì làm vậy là tối ưu "
       "trên tập đánh giá. **Thứ ba**, một phần lỗi còn lại nằm ở chất lượng nhãn yếu chứ "
       "không ở thuật toán, nên không thể khắc phục bằng cách đổi mô hình."))
B(("pagebreak",))

# ==========================================================================
# CHƯƠNG 5
# ==========================================================================
B(("h1", "CHƯƠNG 5. PHÂN TÍCH INSIGHT DOANH NGHIỆP VÀ TRIỂN KHAI ỨNG DỤNG"))

B(("h2", "5.1. Trực quan hóa từ khóa cảm xúc trên toàn bộ dữ liệu"))
B(("p", "Phần khai thác thông tin nghiệp vụ được thực hiện trên toàn bộ 8.417 review sạch. "
       "Cần nói rõ ngay từ đầu về bản chất của phần này: các tỷ lệ và đám mây từ khóa dưới "
       "đây **mô tả nội dung của tập review hiện có**, không chứng minh quan hệ nhân quả và "
       "không phải một bảng xếp hạng nơi làm việc. Người để lại đánh giá công khai trên nền "
       "tảng tuyển dụng không phải một mẫu ngẫu nhiên đại diện cho toàn bộ nhân viên."))
B(("table", "Bảng 5.1. Phân bố cảm xúc trên toàn bộ dữ liệu",
   ["Cảm xúc", "Số review", "Tỷ lệ"],
   [["Tích cực", "6.208", "73,76%"],
    ["Trung tính", "1.639", "19,47%"],
    ["Tiêu cực", "570", "6,77%"]],
   ["l", "r", "r"]))
B(("figure", "Hình 5.1. Đám mây từ khóa của nhóm review tích cực",
   "reports/figures/wordcloud_positive_all.png"))
B(("p", "Nhóm review tích cực tập trung vào ba cụm chủ đề. **Con người và không khí làm "
       "việc** chiếm tỷ trọng lớn nhất, với các từ khóa xoay quanh đồng nghiệp, hỗ trợ, "
       "thân thiện và môi trường. **Cơ hội phát triển chuyên môn** đứng thứ hai, gắn với "
       "đào tạo, học hỏi, công nghệ và dự án. **Chế độ và phúc lợi** xuất hiện nhưng ở mức "
       "thấp hơn đáng kể so với hai cụm trên."))
B(("figure", "Hình 5.2. Đám mây từ khóa của nhóm review tiêu cực",
   "reports/figures/wordcloud_negative_all.png"))
B(("p", "Nhóm review tiêu cực có cấu trúc chủ đề khác hẳn, chứ không đơn thuần là phiên bản "
       "phủ định của nhóm tích cực. Ba cụm nổi bật là **thời gian làm việc và áp lực** (làm "
       "thêm giờ, deadline, áp lực), **chế độ đãi ngộ** (lương, thưởng, tăng lương) và "
       "**quản lý cùng quy trình** (quản lý, quy trình, định hướng)."))
B(("p", "Đối chiếu hai đám mây từ khóa cho một nhận định có giá trị thực tiễn: **nhân viên "
       "khen con người nhưng chê hệ thống**. Các yếu tố được khen nhiều nhất thuộc về quan "
       "hệ đồng nghiệp và trải nghiệm học hỏi — những thứ hình thành tự nhiên trong đội "
       "nhóm. Các yếu tố bị chê nhiều nhất thuộc về chính sách đãi ngộ, phân bổ khối lượng "
       "công việc và năng lực quản lý — những thứ do cấp tổ chức quyết định. Nhận định này "
       "nhất quán với kết quả tương quan ở Bảng 2.8, nơi *quản lý quan tâm* và *lương và "
       "phúc lợi* là hai khía cạnh tương quan mạnh nhất với điểm tổng thể."))

B(("h2", "5.2. Phân tích cảm xúc theo doanh nghiệp"))
B(("p", "Do phân bố review rất không đồng đều giữa các công ty như đã phân tích ở mục 2.2.5, "
       "phần case study chỉ chọn doanh nghiệp đạt **tối thiểu 50 review** và lấy hai doanh "
       "nghiệp có số review lớn nhất."))
B(("table", "Bảng 5.2. Kết quả phân tích hai doanh nghiệp có nhiều review nhất",
   ["Doanh nghiệp", "Số review", "Rating trung bình", "Tích cực", "Trung tính", "Tiêu cực"],
   [["FPT Software", "2.014", "3,68/5", "57,75%", "33,37%", "8,89%"],
    ["NashTech", "308", "3,87/5", "69,16%", "26,30%", "4,55%"],
    ["*Toàn bộ dữ liệu*", "*8.417*", "—", "*73,76%*", "*19,47%*", "*6,77%*"]],
   ["l", "r", "r", "r", "r", "r"]))
B(("p", "Dòng tham chiếu *Toàn bộ dữ liệu* được thêm vào bảng để tránh một lỗi diễn giải phổ "
       "biến. Tỷ lệ tích cực 57,75% của FPT Software chỉ có nghĩa khi đặt cạnh mức trung "
       "bình 73,76% của toàn tập; nếu đọc riêng lẻ, con số này không nói lên điều gì."))

B(("h3", "5.2.1. Case study FPT Software"))
B(("figure", "Hình 5.3. Phân bố cảm xúc tại FPT Software",
   "reports/figures/company_fpt_software_sentiment_distribution.png"))
B(("figure", "Hình 5.4. Từ khóa tích cực tại FPT Software",
   "reports/figures/wordcloud_fpt_software_positive.png"))
B(("figure", "Hình 5.5. Từ khóa tiêu cực tại FPT Software",
   "reports/figures/wordcloud_fpt_software_negative.png"))
B(("p", "FPT Software chiếm 23,93% toàn bộ dữ liệu, là doanh nghiệp có mẫu lớn nhất và do đó "
       "có kết quả ổn định nhất về mặt thống kê. Tỷ lệ tích cực 57,75% thấp hơn mức chung "
       "16 điểm phần trăm, trong khi tỷ lệ trung tính 33,37% cao hơn mức chung gần 14 điểm."))
B(("p", "Cần thận trọng khi diễn giải chênh lệch này. Một phần đáng kể có thể đến từ hiệu "
       "ứng quy mô: doanh nghiệp càng lớn thì độ phân tán trải nghiệm giữa các dự án, các "
       "đội nhóm và các chi nhánh càng cao, và số lượng nhân viên cũ để lại đánh giá cũng "
       "càng nhiều. Dữ liệu hiện có không cho phép tách riêng hiệu ứng quy mô khỏi chất "
       "lượng môi trường làm việc thực tế."))

B(("h3", "5.2.2. Case study NashTech"))
B(("figure", "Hình 5.6. Phân bố cảm xúc tại NashTech",
   "reports/figures/company_nashtech_sentiment_distribution.png"))
B(("figure", "Hình 5.7. Từ khóa tích cực tại NashTech",
   "reports/figures/wordcloud_nashtech_positive.png"))
B(("figure", "Hình 5.8. Từ khóa tiêu cực tại NashTech",
   "reports/figures/wordcloud_nashtech_negative.png"))
B(("p", "NashTech có 308 review, đủ lớn để kết quả có ý nghĩa nhưng nhỏ hơn FPT Software gần "
       "bảy lần. Tỷ lệ tích cực 69,16% gần với mức chung hơn, và tỷ lệ tiêu cực 4,55% là "
       "mức thấp. Rating trung bình 3,87/5 cũng cao hơn FPT Software 0,19 điểm."))
B(("p", "Một lưu ý về phương pháp cần nêu: với 308 mẫu, sai số chuẩn của một tỷ lệ quanh mức "
       "5% vào khoảng 1,2 điểm phần trăm. Chênh lệch 4,34 điểm phần trăm về tỷ lệ tiêu cực "
       "giữa hai doanh nghiệp vì vậy là chênh lệch thực, nhưng không nên được trình bày với "
       "độ chính xác đến hai chữ số thập phân như thể đó là một phép đo tuyệt đối."))

B(("h2", "5.3. Ứng dụng web triển khai"))
B(("h3", "5.3.1. Kiến trúc và các phân hệ"))
B(("p", "Mô hình được đóng gói thành một ứng dụng web xây dựng bằng Streamlit, giao diện tối "
       "ưu cho màn hình rộng. Ứng dụng gồm bốn phân hệ."))
B(("table", "Bảng 5.3. Bốn phân hệ của ứng dụng web demo",
   ["Phân hệ", "Nội dung chính"],
   [["Tổng quan",
     "Thống kê 8.417 review, biểu đồ phân bố ba nhãn, phân bố độ dài văn bản và ma trận "
     "tương quan giữa các khía cạnh; kèm trình đọc review có phân trang, tìm kiếm và sắp xếp"],
    ["Insight doanh nghiệp",
     "Phân tích cảm xúc theo từng công ty với ngưỡng mẫu tối thiểu điều chỉnh được, xu "
     "hướng theo thời gian và đám mây từ khóa sinh theo yêu cầu"],
    ["Phân tích review",
     "Nhập văn bản tự do, dự đoán thời gian thực kèm giải thích quyết định, chuyển đổi giữa "
     "hai mô hình đã khóa, và diễn giải từng bước của pipeline xử lý"],
    ["Mô hình và đánh giá",
     "Bảng xếp hạng mô hình, ma trận nhầm lẫn tương tác, thanh trượt ngưỡng Negative và "
     "bảng kết quả thí nghiệm đối chứng đặc trưng"]],
   ["l", "l"]))
B(("p", "Toàn bộ số liệu hiển thị trong phân hệ *Mô hình và đánh giá* được nạp từ các tệp "
       "kết quả đã lưu, không tính lại bằng cách chạy mô hình trên tập test tại thời điểm "
       "người dùng mở trang. Ràng buộc này bảo đảm con số trên giao diện luôn trùng khớp "
       "với con số trong báo cáo."))

B(("h3", "5.3.2. Pipeline suy luận thời gian thực"))
B(("p", "Khi người dùng nhập một đoạn văn bản, hệ thống thực hiện đúng chuỗi xử lý đã mô tả "
       "ở các chương trước: tiền xử lý qua `TextPreprocessor`, vector hóa bằng phương thức "
       "`transform` của vectorizer đã fit trên tập huấn luyện (**không fit lại**), sinh xác "
       "suất bằng `predict_proba`, rồi áp dụng chính sách ngưỡng và Hybrid Decision Gate mô "
       "tả ở mục 3.6."))
B(("p", "Hai mô hình được nạp song song và người dùng có thể chuyển đổi tức thì: mô hình "
       "**Stacking Ensemble text-only 5.000 chiều** và mô hình **Text + Lexicon 5.005 "
       "chiều**. Cả hai đều được huấn luyện trên cùng một phép chia dữ liệu, nên kết quả "
       "của chúng đặt cạnh nhau so sánh được. Mô hình thứ hai ghi nhận Macro F1 0,5507 trên "
       "tập kiểm tra cuối theo manifest artifact của nó."))
B(("p", "Ứng dụng có một ràng buộc kiểm tra tính nhất quán chạy tại thời điểm nạp: nếu số "
       "chiều đặc trưng do bộ trích xuất sinh ra không khớp với số chiều mà mô hình kỳ vọng, "
       "hệ thống báo lỗi rõ ràng thay vì âm thầm dự đoán sai. Đây là biện pháp phòng ngừa "
       "trường hợp artifact mô hình và artifact đặc trưng bị lệch phiên bản."))

B(("h3", "5.3.3. Tính năng giải thích quyết định"))
B(("p", "Điểm khác biệt chính của ứng dụng so với một hộp đen dự đoán là khả năng giải thích. "
       "Với mỗi dự đoán, hệ thống hiển thị bốn thông tin: phân phối xác suất trên ba lớp; "
       "loại quyết định đã dẫn tới kết luận cuối (`ml`, `threshold` hay `hybrid`); danh sách "
       "cụm từ tích cực và tiêu cực mà từ điển đã khớp được, bao gồm cả các cụm đã bị thuật "
       "toán phủ định đảo chiều; và một câu giải thích bằng tiếng Việt nêu rõ căn cứ."))
B(("p", "Khả năng hiển thị cụm từ đã bị đảo chiều có giá trị sư phạm đặc biệt. Khi người dùng "
       "nhập câu *môi trường làm việc không được thân thiện*, giao diện chỉ ra rằng cụm "
       "*không được thân thiện* đã được tính là tín hiệu **tiêu cực** chứ không phải tích "
       "cực — làm lộ ra chính xác cơ chế mà mục 2.3.4 mô tả, thay vì chỉ công bố một nhãn."))

B(("h2", "5.4. Đề xuất ứng dụng thực tiễn"))
B(("p", "Từ kết quả hai mục trên, nhóm đề xuất ba hướng sử dụng hệ thống, được sắp xếp theo "
       "mức độ tin cậy giảm dần."))
B(("num", [
    "**Sàng lọc phản hồi tiêu cực để đọc thủ công.** Đây là kịch bản phù hợp nhất với năng "
    "lực hiện tại của mô hình. Với Recall lớp Negative 35,09% ở ngưỡng 0,30, hệ thống "
    "không thể thay thế con người, nhưng có thể thu hẹp khối lượng cần đọc và đưa các phản "
    "hồi có khả năng tiêu cực lên đầu hàng đợi.",
    "**Theo dõi xu hướng theo thời gian trong nội bộ một doanh nghiệp.** Ngay cả khi có sai "
    "số hệ thống, sai số đó ổn định qua các kỳ, nên chiều biến động của tỷ lệ tiêu cực vẫn "
    "mang thông tin. So sánh quý này với quý trước tin cậy hơn nhiều so với so sánh doanh "
    "nghiệp này với doanh nghiệp khác.",
    "**Xác định chủ đề cần ưu tiên xử lý.** Đám mây từ khóa của nhóm tiêu cực chỉ ra các "
    "cụm chủ đề lặp lại, giúp bộ phận nhân sự biết nên bắt đầu từ đâu. Kết quả ở mục 5.1 "
    "cho thấy điểm cần ưu tiên là chính sách đãi ngộ, phân bổ khối lượng công việc và năng "
    "lực quản lý cấp trung.",
]))
B(("p", "Ba kịch bản **không** nên sử dụng hệ thống, cần nêu rõ để tránh lạm dụng: xếp hạng "
       "doanh nghiệp công khai dựa trên tỷ lệ cảm xúc; đánh giá cá nhân một nhân viên hay "
       "một quản lý cụ thể; và ra quyết định nhân sự chỉ dựa trên kết quả mô hình mà không "
       "có người đọc lại. Cả ba đều vượt quá độ tin cậy mà số liệu ở Chương 4 cho phép."))
B(("pagebreak",))

# ==========================================================================
# CHƯƠNG 6
# ==========================================================================
B(("h1", "CHƯƠNG 6. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN"))

B(("h2", "6.1. Những kết quả chính đạt được"))
B(("p", "Đồ án đã hoàn thành cả bốn mục tiêu đặt ra ở mục 1.2. Bảng dưới đây đối chiếu từng "
       "mục tiêu với kết quả thực tế và bằng chứng tương ứng."))
B(("table", "Bảng 6.1. Đối chiếu mục tiêu đề ra và kết quả đạt được",
   ["Mục tiêu", "Kết quả đạt được", "Bằng chứng"],
   [["Hệ thống phân loại cảm xúc ba lớp",
     "Accuracy 77,66%, Macro F1 0,5475 trên tập kiểm tra cuối đã khóa",
     "Mục 4.2, Bảng 4.1–4.2"],
    ["So sánh ba nhóm phương pháp",
     "Stacking Ensemble 0,5619 CV; vượt ViSoBERT zero-shot 0,1439 Macro F1",
     "Mục 3.5.3 và 4.4"],
    ["Định lượng đóng góp từng nhóm đặc trưng",
     "Ablation 5 cấu hình kèm kiểm định theo cặp fold; phát hiện rủi ro data shortcut",
     "Mục 3.2, Bảng 3.3–3.4"],
    ["Khai thác thông tin và triển khai",
     "Phân tích 2 case study doanh nghiệp; ứng dụng web 4 phân hệ có giải thích quyết định",
     "Chương 5"]],
   ["l", "l", "l"]))
B(("p", "Ngoài các mục tiêu, nhóm xác định bốn đóng góp có giá trị riêng."))
B(("p", "**Thứ nhất, thuật toán đối sánh cụm từ tham lam kết hợp nhận diện phạm vi phủ "
       "định.** Việc chuyển từ đối sánh từ đơn sang đối sánh cụm dài nhất đã nâng độ bao "
       "phủ từ điển cảm xúc từ 12,26% lên 99,75% số review, đồng thời làm đặc trưng "
       "`sentiment_ratio` phân tách được ba lớp theo đúng thứ tự kỳ vọng. Cơ chế đảo chiều "
       "cực tính khi gặp tiền tố phủ định giải quyết được đúng loại cấu trúc mà biểu diễn "
       "n-gram cố định không xử lý nổi."))
B(("p", "**Thứ hai, bằng chứng định lượng về hiện tượng data shortcut.** Cấu hình chỉ dùng "
       "năm điểm khía cạnh, không đọc một từ nào trong review, vẫn đạt Macro F1 0,7388 — "
       "cao hơn cấu hình văn bản đầy đủ tới 0,18 điểm. Đây là bằng chứng trực tiếp cho thấy "
       "mức tăng khi thêm điểm khía cạnh phản ánh việc mô hình khôi phục thang điểm đã sinh "
       "ra nhãn, chứ không phải năng lực hiểu ngôn ngữ. Nhóm đã chọn loại nhóm đặc trưng "
       "này khỏi pipeline triển khai thay vì tận dụng nó để làm đẹp số liệu."))
B(("p", "**Thứ ba, phân tích nhất quán về bẫy Accuracy.** Ba thí nghiệm độc lập đều cho thấy "
       "cấu hình có Accuracy cao nhất lại là cấu hình có Recall lớp Negative thấp nhất: "
       "Bag-of-Words so với TF-IDF (mục 3.1.3), không xử lý mất cân bằng so với "
       "`class_weight='balanced'` (mục 3.3), và mô hình cuối trên tập kiểm tra (mục 4.3). "
       "Trường hợp cực đoan nhất đạt Accuracy 0,7676 nhưng bỏ sót hơn 90% review tiêu cực."))
B(("p", "**Thứ tư, bộ artifact có ràng buộc tái lập.** Mỗi tệp mô hình đi kèm manifest ghi "
       "phiên bản Python, giá trị băm SHA-256 của dữ liệu nguồn, Git SHA và checksum của "
       "artifact, cho phép người đọc kiểm chứng rằng kết quả trong báo cáo được sinh từ "
       "đúng phiên bản dữ liệu và mã nguồn nào."))

B(("h2", "6.2. Những hạn chế còn tồn tại"))
B(("p", "Nhóm xác định năm hạn chế, xếp theo mức độ ảnh hưởng tới kết quả."))
B(("p", "**Hạn chế 1 — Chất lượng nhãn.** Toàn bộ nhãn huấn luyện là nhãn yếu suy ra từ điểm "
       "đánh giá, không phải nhãn vàng do con người đọc nội dung và gán. Số liệu ở mục "
       "2.2.6 cho thấy mức độ nhiễu là có thật và không nhỏ: 411 review Neutral không được "
       "chính người viết khuyến nghị, 41 review Negative vẫn được khuyến nghị. Một phần "
       "khoảng cách giữa Macro F1 0,5475 và mức hoàn hảo không thể xóa bỏ bằng bất kỳ thuật "
       "toán nào. Nhóm đã chuẩn bị bộ 300 review phục vụ gán nhãn thủ công độc lập nhưng "
       "chưa hoàn tất khâu gán nhãn trong khung thời gian đồ án."))
B(("p", "**Hạn chế 2 — Recall lớp Negative còn thấp.** Ngay cả sau khi áp dụng chính sách "
       "ngưỡng 0,30, mô hình vẫn chỉ phát hiện 40 trên 114 review tiêu cực. Với kịch bản "
       "sàng lọc phản hồi tiêu cực, đây là mức chưa đủ để giao phó hoàn toàn cho hệ thống."))
B(("p", "**Hạn chế 3 — Chưa fine-tune mô hình Transformer.** ViSoBERT chỉ được benchmark ở "
       "chế độ zero-shot do giới hạn tài nguyên GPU. Kết quả Recall lớp Negative 0,7544 của "
       "nó cho thấy tiềm năng rõ rệt nếu được fine-tune đúng cách, nhưng đây vẫn là một giả "
       "thuyết chưa được kiểm chứng bằng thực nghiệm."))
B(("p", "**Hạn chế 4 — Hybrid Decision Gate chưa được kiểm định.** Các ngưỡng của ba luật ở "
       "mục 3.6 được chọn bằng quan sát thủ công trên ví dụ khó, chưa qua kiểm định chéo. "
       "Tầng này vì vậy chỉ hoạt động trong ứng dụng demo và không tham gia vào bất kỳ con "
       "số hiệu năng nào được báo cáo."))
B(("p", "**Hạn chế 5 — Bài toán một nhãn cho toàn văn bản.** Như đã phân tích ở mục 4.6.5, "
       "việc nén một review nói về năm khía cạnh khác nhau thành một nhãn duy nhất làm mất "
       "toàn bộ sắc thái theo khía cạnh. Đây là giới hạn của cách đặt bài toán chứ không "
       "phải của mô hình."))
B(("p", "Ngoài ra, về mặt dữ liệu, 110 trên 180 công ty có dưới 20 review nên phần lớn doanh "
       "nghiệp trong tập dữ liệu không thể phân tích riêng một cách có ý nghĩa thống kê."))

B(("h2", "6.3. Hướng phát triển"))
B(("p", "Bốn hướng dưới đây được sắp xếp theo thứ tự ưu tiên, dựa trên tỷ lệ giữa mức cải "
       "thiện kỳ vọng và chi phí thực hiện."))
B(("num", [
    "**Nâng chất lượng nhãn trước khi nâng cấp mô hình.** Hoàn tất khâu gán nhãn thủ công "
    "trên bộ 300 review đã chuẩn bị, đo mức đồng thuận giữa nhãn người và nhãn yếu, từ đó "
    "ước lượng trần hiệu năng thực tế của bài toán. Đây là hướng có chi phí thấp nhất và "
    "giá trị thông tin cao nhất: nếu trần hiệu năng chỉ ở mức 0,65 Macro F1, thì việc đầu "
    "tư công sức nâng mô hình từ 0,55 lên 0,60 là hợp lý, còn kỳ vọng đạt 0,85 là không "
    "thực tế.",
    "**Fine-tune ViSoBERT hoặc PhoBERT trên chính tập huấn luyện.** Kết quả zero-shot ở "
    "mục 4.4 cho thấy mô hình tiền huấn luyện nhạy hơn hẳn với tín hiệu tiêu cực; thứ nó "
    "thiếu là quy ước nhãn riêng của bài toán, đúng thứ mà fine-tune cung cấp. Cần giữ "
    "nguyên đầu vào `clean_basic_text` để tránh xung đột với tokenizer BPE.",
    "**Chuyển sang bài toán phân tích cảm xúc theo khía cạnh (ABSA).** Bộ dữ liệu đã có sẵn "
    "năm điểm khía cạnh; chúng không dùng được làm đặc trưng đầu vào vì lý do rò rỉ nhãn, "
    "nhưng hoàn toàn có thể dùng làm **nhãn mục tiêu** cho năm bài toán con độc lập. Hướng "
    "này vừa giải quyết hạn chế 5, vừa tận dụng đúng cách phần dữ liệu đang phải bỏ đi.",
    "**Kiểm định và mở rộng Hybrid Decision Gate.** Tinh chỉnh các ngưỡng của ba luật bằng "
    "dự đoán out-of-fold trên tập phát triển, sau đó đánh giá một lần trên một tập test "
    "chưa từng chạm tới, để có thể chính thức báo cáo đóng góp của tầng này.",
]))
B(("p", "Một hướng xa hơn là tích hợp mô hình ngôn ngữ lớn để tự động sinh bản tóm tắt hành "
       "động cho bộ phận nhân sự từ tập review của một doanh nghiệp. Tuy nhiên hướng này "
       "chỉ nên triển khai sau khi ba hướng đầu đã hoàn tất, vì chất lượng bản tóm tắt phụ "
       "thuộc trực tiếp vào chất lượng phân loại ở tầng dưới."))

B(("h2", "6.4. Kết luận"))
B(("p", "Đồ án đã xây dựng hoàn chỉnh một pipeline xử lý ngôn ngữ tự nhiên tiếng Việt cho "
       "bài toán phân tích cảm xúc đánh giá nhân sự, từ khâu tiền xử lý văn bản đặc thù "
       "miền công nghệ thông tin, qua trích xuất đặc trưng có kiểm chứng, mô hình hóa và "
       "tinh chỉnh, đến đánh giá độc lập và triển khai ứng dụng."))
B(("p", "Điều nhóm cho là có giá trị nhất khi nhìn lại không nằm ở con số Macro F1 0,5475. "
       "Nó nằm ở những lần nhóm chọn báo cáo kết quả bất lợi thay vì giấu đi: loại nhóm đặc "
       "trưng cho điểm cao nhất vì phát hiện nó rò rỉ nhãn; công bố rằng dự kiến Recall "
       "55–60% tại ngưỡng 0,30 đã không được thực nghiệm xác nhận; không nhận ngưỡng 0,18 "
       "làm chính sách dù nó cho điểm đẹp hơn, vì nó được tìm ra trên chính tập đánh giá; "
       "và ghi rõ rằng tầng quyết định lai trong ứng dụng chưa được kiểm định nên không "
       "được tính vào kết quả."))
B(("p", "Một mô hình đạt 0,55 Macro F1 mà người đọc biết chính xác nó mạnh ở đâu, yếu ở đâu "
       "và vì sao, có giá trị sử dụng cao hơn một mô hình đạt 0,74 nhờ một đặc trưng rò rỉ "
       "nhãn mà không ai nhận ra."))
B(("pagebreak",))

# ==========================================================================
# TÀI LIỆU THAM KHẢO & PHỤ LỤC
# ==========================================================================
B(("h1", "TÀI LIỆU THAM KHẢO"))
B(("lines", [
    "[1] Pedregosa, F. và cộng sự (2011). *Scikit-learn: Machine Learning in Python.* "
    "Journal of Machine Learning Research, 12, 2825–2830.",
    "[2] Chawla, N. V., Bowyer, K. W., Hall, L. O., Kegelmeyer, W. P. (2002). *SMOTE: "
    "Synthetic Minority Over-sampling Technique.* Journal of Artificial Intelligence "
    "Research, 16, 321–357.",
    "[3] Wolpert, D. H. (1992). *Stacked Generalization.* Neural Networks, 5(2), 241–259.",
    "[4] Sparck Jones, K. (1972). *A Statistical Interpretation of Term Specificity and Its "
    "Application in Retrieval.* Journal of Documentation, 28(1), 11–21.",
    "[5] Vu, T. và cộng sự. *underthesea: Vietnamese NLP Toolkit.* "
    "https://github.com/undertheseanlp/underthesea",
    "[6] Nguyen, N. và cộng sự (2023). *ViSoBERT: A Pre-Trained Language Model for "
    "Vietnamese Social Media Text Processing.* Proceedings of EMNLP 2023.",
    "[7] Nguyen, D. Q., Nguyen, A. T. (2020). *PhoBERT: Pre-trained language models for "
    "Vietnamese.* Findings of EMNLP 2020.",
    "[8] Sennrich, R., Haddow, B., Birch, A. (2016). *Neural Machine Translation of Rare "
    "Words with Subword Units.* Proceedings of ACL 2016.",
    "[9] Pang, B., Lee, L. (2008). *Opinion Mining and Sentiment Analysis.* Foundations and "
    "Trends in Information Retrieval, 2(1–2), 1–135.",
    "[10] Geirhos, R. và cộng sự (2020). *Shortcut Learning in Deep Neural Networks.* "
    "Nature Machine Intelligence, 2, 665–673.",
    "[11] Streamlit Inc. *Streamlit Documentation.* https://docs.streamlit.io",
]))
B(("pagebreak",))

B(("h1", "PHỤ LỤC. TÀI NGUYÊN TÁI LẬP KẾT QUẢ"))
B(("p", "Mọi con số trong báo cáo đều có thể tái lập bằng các tài nguyên liệt kê dưới đây, "
       "trong môi trường Python 3.11 khóa phiên bản theo tệp `requirements.lock`."))
B(("table", "Bảng A.1. Notebook và script thực nghiệm",
   ["Tệp", "Nội dung"],
   [["`notebooks/01_data_exploration_eda.ipynb`", "Phân tích khám phá và trích xuất đặc trưng"],
    ["`notebooks/02_text_preprocessing.ipynb`", "Pipeline tiền xử lý hai tầng"],
    ["`notebooks/03_sentiment_modeling_ml.ipynb`", "Huấn luyện, tinh chỉnh và Stacking Ensemble"],
    ["`notebooks/04_sentiment_modeling_deeplearning.ipynb`", "Benchmark ViSoBERT zero-shot trên GPU"],
    ["`notebooks/05_company_sentiment_insights.ipynb`", "Phân tích cảm xúc theo doanh nghiệp"],
    ["`notebooks/06_model_evaluation_error_analysis.ipynb`", "Đánh giá mô hình và phân tích lỗi"],
    ["`scripts/run_aspect_hybrid_ablation.py`", "Thí nghiệm đối chứng kèm kiểm định theo cặp fold"],
    ["`scripts/run_tv2_feature_experiments.py`",
     "Thống kê token rỗng, so sánh TF-IDF với BoW, so sánh chiến lược cân bằng lớp"],
    ["`scripts/build_hybrid_artifacts.py`", "Sinh artifact cho cấu hình kết hợp đặc trưng số"],
    ["`scripts/plot_ablation_figures.py`", "Sinh lại biểu đồ ablation từ kết quả đã lưu"],
    ["`scripts/build_final_report.py`", "Sinh chính tài liệu này ở định dạng .docx và .pdf"]],
   ["l", "l"]))
B(("table", "Bảng A.2. Module mã nguồn",
   ["Tệp", "Nội dung"],
   [["`src/preprocessing.py`",
     "Pipeline hai tầng, chuẩn hóa NFC, teencode, đối sánh cụm từ tham lam, nhận diện phạm "
     "vi phủ định"],
    ["`src/features.py`",
     "Trích xuất TF-IDF, xử lý văn bản trùng, chia phân tầng, SMOTE, ràng buộc artifact"],
    ["`src/models.py`", "Tinh chỉnh siêu tham số, Stacking Ensemble, biểu đồ so sánh mô hình"],
    ["`src/app_services.py`", "Pipeline suy luận, chính sách ngưỡng và Hybrid Decision Gate"],
    ["`app.py`, `app_pages/`", "Ứng dụng web bốn phân hệ"],
    ["`tests/`", "Bộ kiểm thử tự động cho tiền xử lý, đặc trưng, mô hình và giao diện"]],
   ["l", "l"]))
B(("table", "Bảng A.3. Artifact mô hình và tệp kết quả",
   ["Tệp", "Nội dung"],
   [["`models/best_sentiment_model.joblib`", "Stacking Ensemble text-only đã khóa"],
    ["`models/best_text_lexicon_model.joblib`", "Mô hình Text + Lexicon 5.005 chiều"],
    ["`models/train_test_features.joblib`", "Ma trận đặc trưng, nhãn và metadata cấu hình text-only"],
    ["`models/hybrid_train_test_features.joblib`", "Ma trận cấu hình văn bản kết hợp đặc trưng số"],
    ["`models/*_manifest.json`",
     "Phiên bản môi trường, băm dữ liệu, Git SHA và checksum artifact"],
    ["`reports/aspect_hybrid_ablation.csv`", "Kết quả ablation tổng hợp (Bảng 3.3)"],
    ["`reports/aspect_hybrid_ablation_per_fold.csv`", "Kết quả ablation chi tiết theo fold (Bảng 3.4)"],
    ["`reports/tv2_vectorizer_comparison.csv`", "So sánh TF-IDF với Bag-of-Words (Bảng 3.2)"],
    ["`reports/tv2_balancing_comparison.csv`", "So sánh chiến lược cân bằng lớp (Bảng 3.6)"],
    ["`reports/tv2_empty_token_stats.csv`", "Thống kê token rỗng (Bảng 2.7)"],
    ["`reports/evaluation/baseline_vs_negative_threshold.csv`", "So sánh chính sách ngưỡng (Bảng 4.6)"],
    ["`reports/evaluation/negative_threshold_sensitivity.csv`", "Phân tích độ nhạy ngưỡng (Bảng 4.8)"],
    ["`reports/evaluation/evaluation_snapshot.json`", "Ma trận nhầm lẫn và checksum mô hình"],
    ["`reports/evaluation/error_analysis_15_samples.csv`", "15 mẫu lỗi đại diện (mục 4.6)"],
    ["`reports/figures/`", "Toàn bộ biểu đồ trong báo cáo, độ phân giải 300 dpi"],
    ["`data/annotation/sentiment_audit_blind.csv`", "Bộ 300 review phục vụ gán nhãn thủ công độc lập"]],
   ["l", "l"]))
