# Điều chỉnh giao diện Sentiment Lab — 09/09/2026

## Phạm vi và hành vi

- Chuẩn hóa header ba trang, tăng cỡ chữ nền lên 16px, dùng DM Sans cho nội dung/nhãn và JetBrains Mono cho số liệu/kỹ thuật.
- Tăng độ tương phản mô tả, giữ dark theme và giới hạn nội dung 1920px trên màn hình ultrawide.
- Tổng quan: biểu đồ có nhãn số, tên cảm xúc nằm ngang; thêm khối phản hồi cần chú ý và đường dẫn trực tiếp tới insight/dự đoán.
- Insight: bộ lọc hai cột, KPI thích ứng theo chiều rộng và màu cảm xúc nhất quán.
- Workspace WordCloud hiển thị sẵn khi vào trang Insight; có bộ chọn góc nhìn tích cực/tiêu cực, ngữ cảnh công ty và tỷ trọng mẫu, ba KPI ngôn ngữ cùng bảng xếp hạng từ khóa. Nền ảnh tối đồng bộ dashboard và không còn thao tác tải PNG.
- Dự đoán: vùng nhập và kết quả đặt cạnh nhau trên desktop, xếp dọc trên mobile; trạng thái chờ và badge kết quả rõ ràng; mô tả pipeline nằm trong expander.
- Sidebar dùng trạng thái tự động theo thiết bị. Các thao tác mở lại và điều hướng đã kiểm tra trực tiếp.
- Sidebar được thiết kế lại với nhóm điều hướng chữ mono, icon/viền active rõ hơn, nền ambient nhẹ và thẻ workspace hiển thị số review, số công ty, trạng thái dữ liệu/model theo dữ liệu thật.

## Nghiệm thu cục bộ

- `python -m pytest -q tests/test_streamlit_app.py`: 5 passed.
- Playwright MCP: mở tổng quan, insight, dự đoán; nhập review thật và nhận kết quả Tích cực.
- Chọn FPT Software: 2.014 review; đổi WordCloud giữa nhóm cảm xúc tích cực và tiêu cực; số liệu và biểu đồ cập nhật đúng phạm vi.
- Kiểm tra viewport 390, 768, 1440, 3440px: không tràn ngang trang; canvas ultrawide tối đa 1920px.
- Sidebar mở trên viewport 390px vẫn nằm gọn trong khung 300px và đủ nội dung trạng thái; khi đóng, nội dung chính không có horizontal scroll.
- Ảnh QA lưu tại `.playwright-mcp/` (được Git ignore).
- Có cảnh báo Vega về miền dữ liệu rỗng trong lúc chart đang tải; chart render dữ liệu sau đó. Mở trang con bằng URL trực tiếp có các request dò đường dẫn 404 của Streamlit; điều hướng bằng sidebar đã kiểm tra không có lỗi console mới.

## Chạy, bàn giao và rollback

```powershell
.\.venv311\Scripts\python.exe -m streamlit run app.py --server.port 8502 --server.address 127.0.0.1 --server.headless true --server.fileWatcherType none
```

Phiên demo tắt file watcher vì watcher quét các module Transformers không phục vụ màn hình hiện tại và phát sinh lỗi import dependency tùy chọn. Sau khi sửa module Python cần restart phiên chạy này.

Chỉ thay đổi hiển thị; không huấn luyện lại model hay sửa dữ liệu. CSS dùng test ID và key của Streamlit, cần kiểm tra lại khi nâng phiên bản. Font Google có fallback hệ thống nếu mạng không tải được font.

Bàn giao: review diff giao diện trước khi commit/push. Rollback bằng revert commit UI sau khi commit, hoặc khôi phục riêng các hunk UI trong sáu file ứng dụng; không khôi phục dữ liệu/model hay `.venv311`. Chưa triển khai lên môi trường public.
