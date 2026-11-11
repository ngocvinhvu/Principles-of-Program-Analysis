# Tóm tắt bài báo (bản gộp 2 tài liệu)

> Mục đích file này: tóm tắt bài báo khoa học sẽ nộp, kèm giải thích các thuật ngữ. Dùng làm bản nháp Abstract khi nộp và để cả nhóm hiểu chung.
> Trạng thái: bản nháp 09/11/2026. Chưa đóng băng — cần chạy được thí nghiệm chính (Go/No-Go 12/11) trước khi nộp.

---

## 1. Bài này hỏi câu gì? (nói bằng ví dụ)

Tưởng tượng một học sinh giỏi được cho một bài toán dài 10 trang. Có 2 việc khác nhau:

- Học sinh **chép lại** được công thức trong đề bài. → Dễ. (Gọi là khả năng chép, *lexical*.)
- Học sinh **tự ra đúng đáp số** khi bài bị đổi số. → Khó hơn nhiều. (*semantic*: hiểu và làm ra kết quả.)

Máy tính thông minh (gọi chung là **LLM**) cũng vậy. Khi ta nhét vào nó một đoạn chương trình rất dài, nó có thể **chép lại** được chương trình đó ở mọi vị trí, nhưng lại **đoán sai kết quả** khi phần quan trọng nằm ở **giữa** đoạn văn bản.

Câu hỏi của bài báo này:

> "Khi AI trả lời sai về một đoạn code dài, là vì nó (a) **không tìm thấy** đoạn code quan trọng, hay (b) **tìm thấy rồi mà không ghép nối** được để ra kết quả? Và sự kém này là do **vị trí** (code nằm giữa) hay chỉ vì **đoạn quá dài / lẫn quá nhiều thứ thừa**?"

Biết được câu trả lời rất quan trọng, vì:
- Nếu AI "không tìm thấy" (H-ret) → nên cải thiện phần **tìm kiếm/truy xuất** code.
- Nếu AI "không ghép được" (H-agg) → tìm kiếm giỏi hơn cũng không đủ, phải cải thiện **khả năng suy luận**.

**Cách làm của bài:** giữ nguyên độ dài và nội dung, CHỈ ĐỔI VỊ TRÍ của phần code quan trọng (đầu/giữa/cuối), rồi so với việc bắt AI "chép lại" trên đúng phần đó. Dùng **phân tích chương trình** (các kỹ thuật của môn học) để biết chính xác phần nào thật sự quyết định kết quả — thay vì đoán mò.

---

## 2. Từ điển thuật ngữ (giải thích ngắn)

| Thuật ngữ | Nghĩa dễ hiểu |
|---|---|
| LLM | Trí tuệ nhân tạo đã "đọc" rất nhiều văn bản/code, tạo ra câu trả lời. |
| Lexical recall | AI **chép lại đúng từng chữ** đoạn code. Dễ, như chép chính tả. |
| Semantic recall | AI hiểu đoạn code **chạy ra kết quả gì**. Khó, như hiểu bài để giải bài tập. |
| Ngữ cảnh dài / context window | Lượng văn bản AI nhìn được cùng lúc (giống độ rộng bàn học). |
| Lost in the middle ("mất ở giữa") | AI nhớ tốt thông tin ở đầu và cuối, quên thông tin ở giữa. |
| H-agg | AI tìm thấy code đúng, nhưng **không ghép được** các mảnh lại để ra kết quả. |
| H-ret | AI **không tìm thấy** đúng đoạn code quan trọng. |
| Oracle | **Đáp án chuẩn**: chạy thật code trên máy để biết kết quả đúng là gì. |
| Dynamic call trace | Chạy thử và ghi lại **những hàm nào thực sự chạy** (giống camera ghi ai vào phòng). |
| Backward slice (cắt lát ngược) | Chỉ giữ những dòng code thật sự quyết định đáp án, bỏ dòng thừa. |
| Đổi tên alpha (alpha-renaming) | Đổi tên mọi hàm thành tên vô nghĩa (fn_123...) để AI không "gian lận" bằng cách nhớ tên. |
| Hàm gây nhiễu (distractor) | Những đoạn code "mồi" đánh lạc hướng, không ảnh hưởng kết quả. |
| Pre-registration (đăng ký trước) | Viết sẵn giả thuyết + ngưỡng "thế nào là đúng" TRƯỚC khi chạy, để không tự bịa kết luận. |
| Positive control | Một thí nghiệm "chắc chắn ra hiện tượng" để làm mốc — nếu cái mốc này không chạy thì bài đo sai. |
| Mức bằng chứng E2 | Tuyên bố có kiểm soát trên benchmark, chưa khái quát ra nhà máy/thực tế. |

---

## 3. Tóm tắt bài báo (Abstract, tiếng Việt)

> LLM ngày càng được dùng để hiểu code. Nghiên cứu trước [1] cho thấy: AI chép được code ở mọi vị trí (lexical), nhưng dự đoán sai kết quả khi code nằm giữa ngữ cảnh (semantic recall). Tuy nhiên chưa ai tách được sự kém đó là do **vị trí**, do **độ dài/nhiễu**, hay do không **ghép được** các mảnh phụ thuộc. Các bài làm ở mức "cả kho code" [2, 16] lại để AI tự đi tìm code, nên không kiểm soát được vị trí và không có đối chứng chép lại.
>
> Bài này đưa ra **một phép đo có kiểm soát**: dùng code Python thật (toolz), **giữ nguyên độ dài, chỉ đổi vị trí** của phần code cần thiết (đầu/giữa/cuối), rồi so độ chính xác dự đoán kết quả với tác vụ chép lại trên cùng phần code đó. Dynamic call trace + backward slice xác định phần nào quyết định kết quả; đổi tên alpha (kiểm chứng bằng cách chạy lại) chặn AI gian lận nhờ tên hàm. Kết quả tách được "không tìm thấy" (H-ret) và "không ghép được" (H-agg), đồng thời tách riêng hiệu ứng vị trí khỏi độ dài/nhiễu — giúp biết nên đầu tư vào tìm kiếm hay vào suy luận. Giả thuyết và ngưỡng bác bỏ được đăng ký trước khi chạy; tuyên bố giữ ở mức bằng chứng E2.

---

## 4. Bài báo đóng góp gì? (4 điểm, nói dễ hiểu)

1. **Cách đo tách riêng vị trí:** giữ độ dài cố định, chỉ đổi chỗ code quan trọng, kèm so sánh với "chép lại" trên cùng phần đó. Giúp biết suy giảm là "mất ở giữa" thật hay chỉ "vì dài/nhiễu". (Các bài gần nhất chưa làm được điều này.)
2. **Tách H-ret và H-agg:** nếu bắt AI chép mảnh ra trước rồi mới trả lời mà vẫn sai → là lỗi ghép nối; hết sai → là lỗi tìm kiếm. Kết quả quyết định nên sửa truy xuất hay sửa suy luận.
3. **Bằng chứng benchmark dễ đo sai:** chứng tỏ tên hàm là "đường tắt" khiến benchmark đánh giá quá cao năng lực AI; dùng đổi tên (so sánh ghép cặp trên cùng tập) để làm benchmark đáng tin hơn. (Đóng góp về độ tin cậy của phép đo, không phải kỹ thuật mới.)
4. **Pipeline + dữ liệu tái lập:** code thật toolz, đổi tên đã kiểm chứng, oracle thực thi, đăng ký ngưỡng trước khi chạy, báo cáo theo chuẩn E2.

**Không nói trong bài:** dùng đồ thị gọi hàm để chọn code (hướng tương lai); SemTrace-Dep như đóng góp chính (chưa chạy, code tự sinh xa code thật); kiểm chứng bằng thực thi như câu hỏi chính (gần như hiển nhiên).

---

## 5. Cấu trúc bài (6 phần)

1. Giới thiệu — vấn đề + câu hỏi nghiên cứu.
2. Liên quan — Sense-and-Sensitivity [1], RepoReason [2], RepoReasoner [16], Distractor-Aware [17], MUDDLE [18]; nêu rõ chỗ mình hơn và chỗ **không cho là mới**.
3. Phương pháp — pipeline: doctest → đột biến → backward slice → dynamic call trace → oracle → đổi tên kiểm chứng; các điều kiện (semantic / lexical / retrieve-then-trace / oracle / không ngữ cảnh); vị trí × tác vụ × đổi tên.
4. Thiết kế & đăng ký trước — ngưỡng (chênh lệch ≥ 15 điểm %, bác bỏ nếu cận trên < 5 điểm %), ≥ 2 mô hình + positive control, lặp lại, thống kê hỗn hợp, cổng Go/No-Go.
5. Kết quả — pilot (đường tắt tên hàm; sàn/trần) + thí nghiệm chính.
6. Kết luận + giới hạn.

---

## 6. Tiêu đề đề xuất

- Tiếng Việt: "Mất ở giữa hay mất trong nhiễu? Tách hiệu ứng vị trí, khả năng chép lại và khả năng tổng hợp khi LLM hiểu code trong ngữ cảnh dài".
- English (để nộp arXiv): "Lost in the Middle or Lost in the Noise? Separating Position, Lexical, and Aggregation Failure in LLM Code Understanding".

---

## 7. Những lưu ý trung thực (quan trọng)

- **Trước 30/11 nhất định phải chạy được thí nghiệm chính và có positive control.** Nếu chạy xong mà không ra hiệu ứng, bài vẫn nộp được (đủ điều kiện arXiv) nhưng ở mức "measurement report", kỳ vọng thấp hơn — phải nói rõ.
- **Quyền tác giả:** cần thống nhất với trưởng nhóm trước khi nộp.
- **Trần kết luận:** chỉ nói đúng trong phạm vi toolz, mức hàm, ngữ cảnh tĩnh, tắt chế độ suy nghĩ, Python và mô hình đã thử — không khái quát ra cả repository thật.

---

*Nguồn tài liệu liên quan:* Tài liệu tham khảo ngoài: RepoReason [2], RepoReasoner [16], Distractor-Aware Truncation [17], MUDDLE [18].
