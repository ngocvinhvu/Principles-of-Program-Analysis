# QA — survey_detai5_v1 (06/11/2026, mức proposal, ngưỡng 7.0)

Đây là bản tự đánh giá, không có chuyên gia thật tham gia.

## Gate 2 — nội dung

**Khả thi:**
- Kế hoạch có cổng Go/No-Go; các rủi ro sàn/trần đều có phương án.
- Thiếu: chi phí API trên FPT chưa có số liệu thật.

**Tính mới:**
- Mọi nhận định đều gắn "trong biên tìm kiếm".
- N6 và LoCoBench được ghi là chưa đọc toàn văn.
- RepoReason được nêu rõ là công trình gần nhất.

## Gate 3 — tính đầy đủ
- Mọi con số đều có trong `01_research_canon.md`.
- Đã sửa một con số sai trước khi xuất file: 92 mục 3 hàm là của nhóm chuỗi ghép, không phải của toàn bộ dữ liệu.
- Các bài chỉ đọc abstract hoặc tiêu đề đều được ghi rõ mức đọc.
- Trích dẫn [1]–[15] liên tục.

## Gate 4 — điểm (thang 10)

| Tiêu chí | Điểm |
|---|---|
| Rõ câu hỏi | 8 |
| Bằng chứng | 7.5 |
| Logic | 8 |
| Khả thi | 7 |
| Trung thực về giới hạn | 9 |
| Văn phong | 7.5 |
| Cấu trúc | 8 |
| Đầy đủ trích dẫn | 6.5 |

- **Tổng:** khoảng 7.7, **PASS**.
- **Điểm yếu nhất:** trích dẫn [2], [3], [5], [9]–[15] thiếu tên tác giả, vì nguồn hiện có chỉ cho tiêu đề và venue.
- **Việc tiếp theo:** chạy `nature-ref-verifier` để bổ sung tác giả.
