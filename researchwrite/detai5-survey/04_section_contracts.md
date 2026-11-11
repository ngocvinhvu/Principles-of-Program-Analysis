# 04 Section contracts (rút gọn)

| Mục | Mục đích | Nhận định được phép | Nhận định cấm | Kiểm tra |
|---|---|---|---|---|
| 1. Bối cảnh | Lý do việc LLM "hiểu" code repository là vấn đề của phân tích chương trình | C1, C2, C8 | "lần đầu tiên", "vô cùng quan trọng" | Có ít nhất 1 trích dẫn cho mỗi nhận định |
| 2. Khảo sát | 3 nhánh: (a) long-context và vị trí; (b) đánh giá hiểu ngữ nghĩa và shortcut; (c) repository-level, phân tích chương trình làm oracle. Mỗi nhánh kết thúc bằng điểm còn thiếu | C1–C4 | Nhận định về nội dung bài chỉ đọc tên (L8) | Ghi rõ mức đọc: toàn văn / abstract |
| 3. Khoảng trống & câu hỏi | Nêu câu hỏi trung tâm, H-ret/H-agg, trần kết luận | C3, C8 | "chưa ai làm" | Có câu "trong biên tìm kiếm" |
| 4. Phương pháp | Pipeline phân tích chương trình, thiết kế nhân tố, đo lường | C4, C5, C9 | Hứa thiết kế đầy đủ 5.400 lời gọi | Mỗi bước nêu công cụ hoặc kỹ thuật PA |
| 5. Kết quả sơ bộ | Pilot G1 và lượt 2 | C5, C6, C7 (ở dạng giả thuyết) | "đã chứng minh", "không có lost-in-the-middle" | Ghi n, mô hình, ngày |
| 6. Rủi ro | Sàn/trần, thiên lệch chọn mẫu, không tất định, một mô hình, tính mới | C6, C9 | — | Mỗi rủi ro có phương án |
| 7. Kế hoạch | Mốc đến 30/11 | — | — | Có cổng Go/No-Go |
| 8. Đề nghị duyệt | Các quyết định cần giảng viên | — | — | Câu hỏi đóng, chọn được |

# 05 Style guide (rút gọn)
- Viết tiếng Việt, câu ngắn, thuật ngữ tiếng Anh in nghiêng hoặc để trong ngoặc ở lần đầu.
- Không dùng: "mang ý nghĩa to lớn", "góp phần quan trọng", "lần đầu tiên", "toàn diện".
- Số liệu luôn kèm n và điều kiện. Kết quả pilot luôn gắn nhãn "sơ bộ".
- Trích dẫn dạng [số], danh mục ở cuối, có arXiv ID hoặc venue.
