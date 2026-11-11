# 02 Evidence table

| # | Nhận định | Bằng chứng | Mức | Mục dùng | Rủi ro |
|---|---|---|---|---|---|
| C1 | LLM có thể chép lại code ở mọi vị trí nhưng hiểu hành vi code kém đi khi code nằm ở giữa ngữ cảnh dài (mức một hàm, ≤16k) | L1 | evidence-backed (một bài, 10 mô hình) | 1, 2 | L1 không có kiểm định thống kê |
| C2 | Benchmark kiểu CRUXEval cho phép trả lời bằng tri thức có sẵn (shortcut) | L1, L7, E1 | evidence-backed | 2, 4 | — |
| C3 | Ở mức repository, các công trình hiện có không kiểm soát vị trí và không có đối chứng lexical trên cùng mảnh | L2, L4, L5 (toàn văn); L3, N6, N7 (abstract) | plausible-inference (trong biên tìm kiếm) | 3 | Chưa đọc toàn văn N6 và LoCoBench |
| C4 | Phân tích chương trình (thực thi, vết gọi hàm động, slice def-use, đổi tên alpha) có thể làm oracle và công cụ kiểm soát | L2, L3; E2 | evidence-backed (về khả thi kỹ thuật) | 4 | Mảnh ở mức hàm thô hơn slice mức dòng của L2 |
| C5 | Đổi tên alpha làm giảm mạnh số mục đoán được mà không cần code | E1 | evidence-backed (pilot, 1 mô hình) | 4, 5 | Chỉ toolz |
| C6 | Với DeepSeek-V4-Flash tắt thinking, mục 3 hàm khó ngay cả khi chỉ đưa các mảnh (sàn) | E3, E5 | evidence-backed (pilot, n nhỏ) | 5, 6 | n=10 / 3 lần lặp |
| C7 | Ở 32k–64k chưa thấy suy giảm theo vị trí | E3 | hypothesis (n=10, nhiễu tới 0,2) | 5 | Không được viết như một kết luận |
| C8 | Tách H-ret/H-agg cho biết nên cải thiện retrieval (L6) hay khả năng suy luận | L2, L6; lập luận | plausible-inference | 1, 3 | Chỉ đúng nếu có suy giảm để tách |
| C9 | Bật thinking có thể làm mất phép so sánh H-ret/H-agg | E4 (thinking sửa được 1 mục sai) | hypothesis | 4, 6 | 1 mục |
