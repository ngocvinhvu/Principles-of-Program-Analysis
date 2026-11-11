# 03 Argument map

- **Mâu thuẫn khoa học:**
  - L1 thấy semantic recall giảm theo vị trí ở mức một hàm, còn lexical thì không.
  - Ở mức repository, code liên quan nằm rải ở nhiều nơi. Các bài ở mức repository (L2, L4) thì cho agent tự tìm code, nên không biết suy giảm đến từ việc *không tìm thấy* (H-ret) hay *không ghép được* (H-agg).
  - Hai nguyên nhân này dẫn tới hai hướng sửa khác nhau: retrieval (L6) hoặc suy luận.
- **Câu hỏi trung tâm:** trong ngữ cảnh tĩnh dài gồm code Python thật, khi các hàm cần thiết được đặt có kiểm soát (vị trí, độ phân tán, độ dài), độ chính xác dự đoán giá trị có giảm hơn so với tác vụ chép lại cùng các hàm đó không? Phần giảm có mất đi khi mô hình chép các hàm ra trước không (retrieve-then-trace)?
- **Luận điểm** (đã hạ mức cam kết): đề tài đóng góp một **khung đo có kiểm soát dựa trên phân tích chương trình**, áp dụng cho một mô hình, cùng kết quả sơ bộ trung thực. Đề tài không hứa xác nhận H-ret hay H-agg.
- **Lập luận hỗ trợ:**
  1. Cần kiểm soát vị trí và đối chứng lexical (C1, C3).
  2. Phân tích chương trình cho phép kiểm soát chặt hơn bằng: oracle thực thi, vết gọi hàm động, slice def-use trên setup, đổi tên alpha (C4, C5).
  3. Pilot cho thấy khung đo chạy được và đã phát hiện các mối đe dọa đến tính hợp lệ mà nhiều benchmark bỏ qua: đoán được nhờ tên hàm, không tất định, thinking (C5, C6, E4).
- **Phản biện:**
  - (a) "Chỉ là bài 2505 mở rộng": trả lời bằng thiết kế tách H-ret/H-agg, nhưng đánh giá này dựa trên tìm kiếm có giới hạn.
  - (b) "Đổi tên làm code kém tự nhiên": đúng, và phải đưa vào trần kết luận.
  - (c) "Không thấy suy giảm thì đề tài rỗng": một kết quả âm tính có kiểm soát vẫn là kết quả, nhưng khi đó không còn trả lời được câu hỏi H-ret/H-agg.
  - (d) "Một mô hình": có thể thêm mô hình thứ hai trên cùng endpoint.
- **Thông điệp cuối:** hướng đi khả thi trong 3,5 tuần nếu (i) lọc mục theo khả năng giải được ở điều kiện oracle, (ii) thay đối chứng lexical bằng một đối chứng không chạm trần, và (iii) giảng viên chấp nhận đóng góp ở mức một khung đo cộng kết quả sơ bộ.
