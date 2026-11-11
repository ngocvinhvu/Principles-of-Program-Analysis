# Rà soát tính mới, phản biện và khả thi — nature-social-science (Step 6–8)

- **Ngày chạy:** 2026-11-06
- **Chế độ:** Mode C. Hướng nghiên cứu đã có sẵn, nên đây là lượt rà soát (audit), không phải lượt sinh đề tài.
- **Lưu ý áp dụng:**
  - Skill được thiết kế cho khoa học xã hội và nói về "luận án PhD". Ở đây tôi giữ nguyên logic gate và hệ trạng thái của skill.
  - Riêng Step 7 được đổi sang thang **đề tài môn học / luận văn**, vì đây là Đề tài 5 của môn "Kỹ thuật phân tích chương trình".
  - Không có đánh giá nào ở đây là chứng minh tính mới. `SURVIVE ≠ novel`.

---

## Current Research State

| Mục | Trạng thái |
|---|---|
| Hướng gốc | Vị trí × độ nhạy ngữ nghĩa trong hiểu code ngữ cảnh dài ở quy mô repository, dùng phân tích chương trình làm đáp án chuẩn (oracle) |
| Bằng chứng đã có | 6 paper card (`cards/`); 3 lượt tìm (OpenAlex; Semantic Scholar từ khóa và trích dẫn xuôi; Semantic Scholar + arXiv có mục tiêu); đọc toàn văn có mục tiêu 1 bài (RepoReason) |
| Ứng viên | C1, C2, C3 (bên dưới). C1 được sửa thành C1′ |
| Step 6 Gate | **PASS (có điều kiện):** C1′ = SURVIVE trong biên tìm kiếm hiện tại; C2 gộp vào C1′; C3 = PARK |
| Step 7 Gate | **PASS có điều kiện** (cập nhật 06/11): hạn 30/11; dùng API DeepSeek V4 Flash, bỏ RTX 3060. Đã cắt thành C1′-mini; điều kiện giữ PASS là G1 (10/11) |
| Step 8 Gate | **PASS** → viết đề cương bằng `researchwrite` |
| Việc chặn tiếp theo | G1 (10/11): đọc N6 + LoCoBench; xác minh giá và chế độ của API; bước thử 10 mục. Giảng viên xác nhận phạm vi |

---

## Ba ứng viên câu hỏi nghiên cứu

Các ứng viên được tách ra từ hướng gốc và các phần 16 của card.

**C1 (lõi):** Ở quy mô repository, khi code liên quan bị phân tán qua nhiều file và đặt ở các vị trí khác nhau trong một ngữ cảnh tĩnh, semantic recall có suy giảm theo vị trí như bài 2505 thấy ở mức hàm không, trong khi lexical recall thì không?

**C2 (đo lường):** Có thể dùng program slice làm phép phản thực tế, thay cho việc xóa dòng ngẫu nhiên như bài 2505, để đo "semantic recall sensitivity" chặt hơn không? Cụ thể: so sánh mức nhạy của mô hình khi xóa dòng **trong** slice và khi xóa dòng **ngoài** slice.

**C3 (agent):** Đáp án chuẩn từ call graph và data flow tĩnh, khi dùng để chấm các quan hệ phụ thuộc mà agent ghi ra (RepoAnchor), có dự báo việc agent giải được bài tốt hơn số file đã mở không?

---

## Step 6 — Novelty Audit

**Biên tìm kiếm:**
- **Nguồn:** OpenAlex và Semantic Scholar (có key) cộng arXiv, chỉ tiếng Anh, năm 2021–2026.
- **Truy vấn:** khoảng 32 truy vấn.
- **Trích dẫn xuôi:** lấy bài trích dẫn của 2505, CRUXEval, RepoQA, Lean-on-Priors.
- **Không tìm:** ACM DL và IEEE Xplore trực tiếp, Google Scholar, các hội nghị chưa có bản ghi.
- **Truy vấn thất bại:** "data flow question answering benchmark LLM code" trên Semantic Scholar trả về 0 kết quả (có thể do bị giới hạn tốc độ).

### Các công trình gần nhất

| # | Công trình | Mức bằng chứng | Đã trả lời gì | Chưa trả lời gì (so với C1/C2) |
|---|---|---|---|---|
| N1 | **Sense and Sensitivity** (2505.13353, ACL 2025) | Toàn văn (card) | Phân ly lexical/semantic recall theo vị trí ở **mức một hàm**, 4k–16k token; đo sensitivity bằng xóa dòng ngẫu nhiên | Không có quy mô repository, code liên quan không bị phân tán qua nhiều file, không dùng slice/call graph |
| N2 | **RepoReason** (2601.03731, ACL 2026 main) | **Toàn văn, đọc có mục tiêu** | Repository thật tới 776k LoC; môi trường thực thi làm oracle ngữ nghĩa (đột biến input, chạy lại để lấy giá trị đúng); **dynamic program slicing** làm thước chẩn đoán (ESV, MCL, DFI); phát hiện "aggregation deficit"; phê phán việc hỏi trực tiếp giá trị trong vết thực thi là để mô hình dùng mẹo tắt (mục 2.3) | **Theo cách agent làm việc:** agent tự đi tìm code nên không kiểm soát vị trí trong ngữ cảnh; không có nhóm đối chứng lexical recall; slice dùng để giải thích độ khó, không dùng làm phép phản thực tế |
| N3 | **CORE** (NeurIPS 2025) | Abstract | Phân tích tĩnh (data/control dependency, information flow) làm đáp án chuẩn, 12.553 bài, C/C++/Java/Python | Ở mức chương trình hoặc hàm, không có ngữ cảnh dài, không xét vị trí |
| N4 | **RepoMirage** (2605.26177) | Toàn văn (card) | Làm nhiễu repository, đo agent | Không kiểm soát vị trí, chủ yếu là định vị code, không dùng oracle tĩnh |
| N5 | **Dolce** (2409.06338) | Toàn văn (card) | Phân loại tác vụ truy hồi hay hiểu toàn cục bằng phản thực tế cửa sổ quan sát | Không xét vị trí, không chạy code, cửa sổ liên tiếp chứ không theo slice |
| N6 | Robustness & Reasoning Fidelity in Long-Context Code QA (2026, arXiv) | Abstract | Nhiễu loạn định dạng đáp án, đoạn gây nhiễu, quy mô ngữ cảnh trên LongCodeBench | Từ abstract: không thấy phân ly lexical/semantic và không thấy kiểm soát vị trí theo slice. **Chưa đọc toàn văn** |
| N7 | RepoQA, LONGCODEU, LoCoBench, RepoReasoner | Abstract | Đo hiểu code dài và mức repository | Từ abstract: không thấy thiết kế vị trí × độ nhạy ngữ nghĩa |
| N8 | Counterfactual Analysis for Code Predicates (2402.05980); Semantics-preserving mutations (2505.10443); CodeCrash | Abstract | Phản thực tế và đột biến giữ ngữ nghĩa trên code ngắn | Không có ngữ cảnh dài, không theo slice |

**Hiện có thể nói:**
- Trong biên tìm kiếm này, chưa thấy công trình nào kiểm soát **vị trí của các mảnh slice** trong ngữ cảnh tĩnh ở quy mô repository, đồng thời có nhóm đối chứng lexical trên **cùng các mảnh** đó.
- RepoReason (N2) đã chiếm phần "slicing + oracle thực thi + repository".

**Hiện chưa thể nói:**
- Rằng "chưa ai làm vị trí × ngữ nghĩa ở mức repository".
- Rằng việc dùng slice làm oracle là mới. N2 và N3 đã dùng phân tích chương trình làm đáp án chuẩn hoặc thước đo.

---

## Step 6 — Reviewer 2 Sheet

### C1 → REDESIGN → C1′

| Mặt bị tấn công | Phản biện |
|---|---|
| Tính mới | "Chỉ là ghép bài 2505 với ngữ cảnh lớn hơn, kiểu RULER" (ngụy biện tổ hợp chính xác). Nếu kết quả chỉ là "ở repository cũng có lost-in-the-middle" thì đóng góp gần bằng 0 |
| Khái niệm (construct) | Phép đo "semantic recall" trong bài 2505 bằng khớp tuyệt đối trên 4–10 phần tử đã bị chính card 2505 phê phán. Cần đáp án một giá trị, như kiểu mask-assert của N2, hoặc cho điểm từng phần |
| Lý thuyết | Thiếu các dự đoán cạnh tranh. Cần nêu rõ: (H-ret) suy giảm do **không định vị được** mảnh code, hay (H-agg) suy giảm do **không tổng hợp được** nhiều mảnh nằm xa nhau. N2 gợi ý H-agg nhưng không tách được, vì agent tự định vị |
| Bằng chứng | Repository có extension C hoặc có hành vi không tất định làm oracle sai. N2 đã phải loại các trường hợp này. Nên dùng lại bộ repository thuần Python của N2 |
| Logic phương pháp | Biến vị trí bị lẫn với khoảng cách giữa các mảnh và với độ dài ngữ cảnh, nên phải điều khiển ba biến này riêng |
| Giải thích thay thế | (a) Card 2505 đã chỉ ra yếu tố gây nhiễu là **mã hex làm dấu định vị**: tác vụ lexical có dấu, tác vụ semantic không có. (b) Rò rỉ dữ liệu: repository phổ biến đã có trong dữ liệu huấn luyện, nên phải đột biến input như N2. (c) Đoạn gây nhiễu được chọn không giống code thật |
| Đóng góp | Chỉ có giá trị nếu trả lời được H-ret hay H-agg. Câu trả lời này quyết định việc nên sửa ở retrieval/RAG (như Code Comprehensor) hay ở khả năng suy luận của mô hình |

- **Phản biện mạnh nhất:** C1 ở dạng gốc chỉ mở rộng phạm vi. Nếu không tách được H-ret khỏi H-agg thì không thay đổi hiểu biết nào so với 2505 + N2.
- **Giả định ẩn:** mảnh slice tĩnh hoặc động đủ chính xác để làm "đoạn code liên quan".
- **Trần kết luận:** chỉ kết luận được cho các mô hình, repository thuần Python và mức độ dài ngữ cảnh đã thử. Không suy ra được cho agent tự điều hướng.
- **Cách sửa (đã thực hiện):** chuyển thành C1′.

**C1′ (sau khi sửa):**

> Trong ngữ cảnh tĩnh mức repository (lấy từ các repository thuần Python, với input đã đột biến để tránh học thuộc), khi các mảnh của **dynamic slice** dẫn tới một giá trị cần dự đoán được đặt theo một thiết kế giai thừa **vị trí × độ phân tán (1 mảnh hay k mảnh, gần nhau hay xa nhau) × độ dài ngữ cảnh**, mức suy giảm khi **dự đoán giá trị** có khác mức suy giảm khi **chép lại đúng các mảnh đó** không? Mức chênh này được giải thích chủ yếu bởi khả năng định vị (H-ret) hay khả năng tổng hợp (H-agg)?

Các điều kiện kiểm soát bắt buộc:
- dùng cùng mảnh code cho cả hai tác vụ;
- hoặc cả hai tác vụ đều có dấu định vị, hoặc cả hai đều không, nhờ thiết kế 2×2 có/không mã hex lấy từ phần 16 của card 2505;
- thêm điều kiện "chép mảnh trước rồi mới dự đoán" (retrieve-then-trace). Nếu suy giảm biến mất trong điều kiện này thì ủng hộ H-ret; nếu vẫn còn thì ủng hộ H-agg.

**Tấn công lại C1′:**
- *Tính mới:* N2 không có ngữ cảnh tĩnh, không có nhóm đối chứng lexical, không có điều kiện retrieve-then-trace. N1 không có các mảnh phân tán ở mức repository. Khác biệt này **thay đổi đánh giá về mặt hiểu biết**: tách được H-ret khỏi H-agg.
- *Rủi ro còn lại:* N6 và LoCoBench chưa đọc toàn văn.
- **Xử lý: SURVIVE** (trong biên tìm kiếm hiện tại, chưa chứng minh tính mới).

### C2 → gộp vào C1′ (REDESIGN thành công cụ đo)

- **Phản biện mạnh nhất:**
  - Xóa dòng ngoài slice chính là một phép đột biến giữ ngữ nghĩa, đã được nghiên cứu (N8).
  - Xóa dòng trong slice làm đầu ra thay đổi, nên mô hình phải tính lại. Như vậy đây chỉ là CRUXEval chạy trên code đã đột biến.
  - Đứng riêng thì đóng góp mỏng.
- **Giá trị còn lại:** dùng làm **thước đo độ nhạy của tác vụ** trong C1′. Cụ thể: đo mức nhạy với dòng trong slice trừ mức nhạy với dòng ngoài slice. Đây là phiên bản có oracle, tốt hơn cách xóa dòng ngẫu nhiên của 2505.
- **Xử lý: REDESIGN.** Không là câu hỏi độc lập, mà thành công cụ trong C1′.

### C3 → PARK

- **Phản biện mạnh nhất:** N2 đã dùng các chỉ số tính từ slice (ESV, MCL, DFI) để giải thích việc agent giải được bài, có phân tích tương quan riêng phần (Appendix B.3, Table 6). C3 chỉ khác ở chỗ chấm "phát biểu của agent", và còn cần chạy agent trên môi trường kiểu SWE-bench.
- **Bằng chứng còn thiếu:**
  - Artifact của RepoMirage và RepoAnchor có công khai không: UNKNOWN.
  - Chi phí chạy agent: UNKNOWN.
- **Xử lý: PARK.** Chỉ mở lại nếu cả hai điều trên được xác nhận.

### Việc kiểm chứng quyết định cho Step 6

1. Đọc toàn văn N6 (*Robustness & Reasoning Fidelity in Long-Context Code QA*) và **LoCoBench** để xác nhận hai bài không có thiết kế vị trí × lexical/semantic.
2. Kiểm tra RepoReason có công khai bộ dữ liệu và code slicing không (để dùng lại thay vì tự viết).
3. Hỏi ý kiến giảng viên môn học: khác biệt H-ret/H-agg có được coi là đủ đóng góp cho đề tài không. **Đây là quyết định của người, AI không quyết thay được.**

---

## Step 7 — Feasibility Dossier (cập nhật 2026-11-06 sau khi có thông tin từ người dùng)

Ứng viên: C1′, quy đổi sang thang đề tài môn học.

Thông tin người dùng cung cấp:
- **Hạn nộp:** cuối tháng 11/2026. Tôi giả định là ngày 30/11, tức còn khoảng 3,5 tuần.
- **Tài nguyên:** ban đầu là 1 GPU RTX 3060 12GB. **Cập nhật cùng ngày:** người dùng có API DeepSeek V4 Flash và không dùng 3060 nữa.
- **Kỹ năng:** quen Python, chưa vững tracing và AST.

### Các điều kiện cứng

| # | Điều kiện | Trạng thái | Căn cứ / việc tiếp theo |
|---|---|---|---|
| 1 | Bằng chứng cốt lõi | RESOLVABLE DEPENDENCY | Dùng repository thuần Python. Hạ dynamic slice **từ mức dòng xuống mức hàm** (xem điều kiện 6). Kiểm tra trên 10 mẫu ở bước thử G1 |
| 2 | Truy cập & giấy phép | RESOLVABLE DEPENDENCY | Repository mã nguồn mở. Người dùng đã có API DeepSeek V4 Flash (ACCESS-CONFIRMED theo lời người dùng). Cần đọc điều khoản sử dụng API |
| 3 | Đạo đức | CONFIRMED (không áp dụng) | Không có người tham gia, không có dữ liệu cá nhân |
| 4 | An toàn người nghiên cứu | CONFIRMED (không áp dụng) | — |
| 5 | Thời gian | **RESOLVABLE DEPENDENCY (sát)** | 3,5 tuần chỉ đủ cho bản đã cắt bên dưới. Không đủ cho 2×2 mã hex hay cho slice mức dòng. Dùng API nên không còn mất thời gian cài đặt và chạy GPU |
| 6 | Kỹ năng cần có | **RESOLVABLE DEPENDENCY** | Thay slicer mức dòng bằng **vết gọi hàm động** (dynamic call trace): `sys.setprofile` lọc các sự kiện `call` thuộc file của repository, khoảng 20 dòng code. Lấy input từ doctest bằng `doctest.DocTestFinder` của thư viện chuẩn, không cần AST. AST chỉ dùng để xóa docstring (`ast.get_docstring` / `ast.unparse`). Thống kê: hồi quy logistic bằng `statsmodels` |
| 7 | Hướng dẫn & tài nguyên | **CONFIRMED** (giá: DOCUMENTED) | DeepSeek V4 Flash qua API. Theo các trang bên thứ ba (chưa đối chiếu trang giá chính thức): ngữ cảnh khoảng 1M token; khoảng $0,14 / 1M token đầu vào và $0,28 / 1M token đầu ra. Với thiết kế bên dưới (khoảng 91 triệu token đầu vào), chi phí ước tính **khoảng $13–15**. Giới hạn tốc độ gọi API: UNKNOWN, đo ở G1 |
| 8 | Lượng thông tin khoa học | RESOLVABLE DEPENDENCY | Vẫn tách được H-ret/H-agg nhờ retrieve-then-trace. Chi phí thấp nên lấy lại được nhiều mức độ dài ngữ cảnh. Trần kết luận: **một mô hình** (DeepSeek V4 Flash) |

**Rủi ro phương pháp mới khi dùng API:**
- **Chế độ suy nghĩ (thinking).** Nếu API có chế độ này và nó được bật, mô hình có thể tự chép code liên quan ra trong phần suy nghĩ. Như vậy, điều kiện semantic thường sẽ trở thành retrieve-then-trace ngầm, và phép so sánh H-ret/H-agg mất tác dụng. Lượt chạy chính phải dùng **chế độ không suy nghĩ**. Thinking có thể chạy thêm như một yếu tố phụ trên một tập con.
- **Học thuộc.** Mô hình lớn có thể đã học thuộc toolz và more-itertools. Vì vậy, đột biến input và điều kiện không ngữ cảnh là bắt buộc.
- **Mô hình đổi phiên bản phía nhà cung cấp.** Phải ghi lại tên model, ngày chạy và tham số. Dùng `temperature=0`, nhưng không giả định kết quả tất định.
- **API key:** tự đặt `DEEPSEEK_API_KEY` vào `.claude/settings.local.json` (`env`) hoặc biến môi trường. Không dán key vào chat.

### Những gì bị cắt và lý do

| Phần trong C1′ gốc | Quyết định | Lý do |
|---|---|---|
| Dynamic slice mức dòng | Thay bằng vết gọi hàm động (mức hàm) | Chưa vững tracing; mức hàm làm được trong 1 ngày. Trần kết luận: "mảnh" nghĩa là hàm, không phải dòng |
| 2×2 có/không mã hex | Bỏ. Cả hai tác vụ dùng **tên hàm** làm dấu định vị | Tên hàm là dấu định vị tự nhiên trong code và giống nhau ở cả hai tác vụ, nên vẫn khử được yếu tố gây nhiễu mà card 2505 chỉ ra. Cách này còn bớt một nửa số lời gọi |
| Độ dài ngữ cảnh | **Lấy lại**: 8k / 16k / 32k / 64k | API rẻ và có ngữ cảnh lớn |
| Mô hình thứ hai | Bỏ | Chỉ có API DeepSeek. Trần kết luận: một mô hình |
| Đọc toàn văn N6, LoCoBench | **Giữ**, giới hạn 2 giờ, làm ngay tuần 1 | Nếu một trong hai bài đã làm đúng thiết kế này thì phải biết trước khi tốn công chạy |

### Nghiên cứu tối thiểu khả thi (bản cắt cho 3,5 tuần)

**Dữ liệu (mục, item):**
- Lấy từ 2–3 repository thuần Python có nhiều doctest, ví dụ toolz, more-itertools, boltons. Danh sách này **chưa kiểm tra**; sẽ chọn theo kết quả G1.
- Mỗi mục là một lời gọi lấy từ doctest, với **input đã đột biến**. Đáp án chuẩn có được bằng cách **chạy thật** (oracle là trình thông dịch). Chạy hai lần để loại các mục không tất định.
- Vết gọi hàm động xác định các hàm của repository thực sự được thực thi. Đây là các "mảnh".
- Giữ khoảng 40 mục chỉ đi qua 1 hàm, và khoảng 40 mục đi qua đúng 3 hàm (ưu tiên 3 hàm nằm ở ≥2 file).
- Xóa toàn bộ docstring trong ngữ cảnh, vì docstring chứa sẵn đáp án của doctest.

**Ngữ cảnh:** các hàm thật khác của cùng repository được dùng làm phần gây nhiễu, lấp đầy tới 8k hoặc 16k token (đếm bằng tokenizer của chính mô hình).

**Bố cục:**
- Mục 1 hàm: đặt hàm ở đầu, giữa hoặc cuối ngữ cảnh.
- Mục 3 hàm: gom cả 3 hàm ở đầu, giữa hoặc cuối, hoặc **rải đều** khắp ngữ cảnh. So sánh "gom ở giữa" với "rải đều" cho biết riêng ảnh hưởng của độ phân tán.

**Tác vụ (cùng mảnh, cùng dấu định vị là tên hàm):**
- **Semantic:** "`f(<input>)` trả về gì?"
- **Lexical:** "Chép lại nguyên văn thân của hàm X (và Y, Z)."
- **Retrieve-then-trace** (chỉ cho mục 3 hàm): mô hình chép các hàm liên quan ra trước, rồi mới dự đoán.
- **Không ngữ cảnh:** hỏi câu semantic mà không đưa code. Điều kiện này đo phần đoán mò và học thuộc.
- **Phản thực tế (C2 rút gọn):** với mục 3 hàm ở bố cục rải đều, độ dài 16k, xóa 1 hàm **trong vết** và xóa 1 hàm **ngoài vết**. Chênh lệch câu trả lời giữa hai trường hợp là một phép kiểm tra rằng mô hình thực sự dựa vào đúng các mảnh đó.

**Mô hình:** DeepSeek V4 Flash qua API, chế độ không suy nghĩ, `temperature=0`. Ở mỗi lời gọi, ghi lại số token prompt mà API báo về, để kiểm tra ngữ cảnh không bị cắt.

**Ước tính số lời gọi:**

| Nhóm | Phép tính | Số lời gọi |
|---|---|---|
| Mục 1 hàm | 40 mục × 3 vị trí × 4 độ dài × 2 tác vụ | 960 |
| Mục 3 hàm | 40 × 4 bố cục × 4 độ dài × 3 tác vụ | 1.920 |
| Không ngữ cảnh | 80 mục × 1 | 80 |
| Phản thực tế | 40 × 2 | 80 |
| **Tổng** | | **khoảng 3.040** |

- Độ dài trung bình khoảng 30k token, tổng khoảng **91 triệu token đầu vào**, tức **khoảng $13** theo giá chưa đối chiếu. Thêm khoảng $0,3 cho đầu ra ở chế độ không suy nghĩ.
- Nếu chạy thêm thinking trên một tập con, token đầu ra sẽ tăng mạnh. Phải ước tính lại sau bước thử.
- **Nếu giới hạn tốc độ API chặt, cắt theo thứ tự:** bỏ độ dài 64k → bỏ 8k → giảm xuống 30 mục mỗi nhóm.

**Phân tích:**
- Hồi quy logistic: đúng/sai ~ bố cục × tác vụ × độ dài, có hiệu ứng ngẫu nhiên theo mục nếu đủ dữ liệu; nếu không, dùng khoảng tin cậy bootstrap theo mục.
- Câu hỏi chính:
  1. Tương tác bố cục × tác vụ: vị trí làm hại semantic nhiều hơn lexical không?
  2. So sánh retrieve-then-trace với semantic thường ở bố cục rải đều: suy giảm biến mất (ủng hộ H-ret) hay còn (ủng hộ H-agg)?
- Mục nào mô hình trả lời đúng ở điều kiện không ngữ cảnh thì phân tích riêng hoặc loại ra.

**Trả lời được:** với DeepSeek V4 Flash (không suy nghĩ), trên code Python thật ở mức hàm và ngữ cảnh 8k–64k, việc suy giảm theo vị trí và độ phân tán chủ yếu do định vị hay do tổng hợp.

**Không trả lời được:** khái quát cho các mô hình khác; agent tự điều hướng; mức dòng; ngôn ngữ khác Python; ngữ cảnh trên 64k; chế độ suy nghĩ (trừ phần chạy thêm).

### Kế hoạch thời gian và cổng kiểm tra

| Thời gian | Việc | Cổng |
|---|---|---|
| 06–10/11 | (a) Đọc N6 + LoCoBench, tối đa 2 giờ. (b) Đối chiếu giá và giới hạn tốc độ trên trang chính thức của DeepSeek; xác nhận tắt được chế độ suy nghĩ; đo độ trễ ở 64k. (c) Viết pipeline doctest → đột biến → chạy → vết gọi hàm trên 1 repository. (d) Bước thử 10 mục | **G1, 10/11** |
| 11–16/11 | Dựng đủ khoảng 80 mục từ 2–3 repository; bộ dựng ngữ cảnh; chạy toàn bộ | G2: chạy xong |
| 17–21/11 | Phản thực tế, thinking trên tập con (nếu còn thời gian), phân tích | — |
| 22–28/11 | Viết báo cáo, vẽ hình, slide | — |
| 29–30/11 | Dự phòng | — |

**G1 thành công khi đạt cả 4 điều kiện:**
- ≥7/10 mục thử có vết gọi hàm đúng khi kiểm tra bằng mắt;
- tìm được ít nhất 5 mục đi qua 3 hàm trong repository đầu tiên;
- lexical gần trần ở vị trí đầu, và semantic không bằng 0% hay 100% ở mọi ô;
- tắt được chế độ suy nghĩ; giá đúng với ước tính; lời gọi ở 64k không bị cắt ngữ cảnh.

**G1 thất bại thì:**
- **Thiếu mục 3 hàm:** chuyển sang mục 2 hàm, hoặc tự viết một số chuỗi gọi hàm. Trần kết luận hẹp hơn và phải ghi rõ trong báo cáo.
- **N6 hoặc LoCoBench đã làm đúng thiết kế này:** quay lại Step 6, giữ phần mở rộng sang code thật nếu bài kia dùng code tổng hợp.
- **Không tắt được chế độ suy nghĩ:** chuyển thinking thành điều kiện cố định và báo cáo rõ. Khi đó retrieve-then-trace phải là chép ra **trong câu trả lời** để còn so sánh được.

### Điều kiện thất bại và phương án dự phòng

- **Điều kiện thất bại:** gần như không có mục nào đi qua ≥3 hàm ở ≥2 file. Khi đó không còn biến "độ phân tán", và đề tài quay về đúng bài 2505.
- **Dự phòng:** độ phân tán được tạo bằng cách đặt các hàm cách xa nhau trong ngữ cảnh, không cần chúng thuộc nhiều file. Đây vẫn là "phân tán trong ngữ cảnh", nhưng mất ý nghĩa "mức repository". Phải ghi rõ điều này trong báo cáo.

### Cần người thật xác nhận

- **Giảng viên:**
  - Hạ slice từ mức dòng xuống vết gọi hàm có còn đủ "phân tích chương trình" cho môn học không?
  - Tách H-ret/H-agg có đủ đóng góp không?
- **Bạn:**
  - Hạn chính xác có phải 30/11 không?
  - Có chấp nhận trần kết luận "chỉ DeepSeek V4 Flash, Python, mức hàm" không?

**Xử lý ở Step 7: PROCEED TO COMPARISON** (với bản cắt). **Step 7 Gate: PASS có điều kiện:** chỉ giữ nguyên nếu G1 (10/11) thành công.

---

### Nhật ký G1 — kiểm tra API (06/11, đã TESTED)

Thông tin kết nối:
- **Endpoint:** FPT Cloud Marketplace (`LLM_BASE_URL`), tương thích API OpenAI.
- **Key:** nằm trong `.claude/settings.local.json` (`LLM_API_KEY`).
- **Mô hình hiện có:**
  - DeepSeek-V4-Flash;
  - Qwen3.6-27B, Llama-3.3-70B-Instruct, gpt-oss-120b, gemma-3-27b-it, gemma-4-31B-it, gemma-4-26B-A4B-it;
  - GLM-5.2, Minimax-M3, cùng một số mô hình embedding và vision.

| Kiểm tra | Kết quả |
|---|---|
| Chế độ suy nghĩ | **Bật sẵn theo mặc định** (có `reasoning_tokens`). Tắt được bằng `"thinking": {"type": "disabled"}`; khi tắt, `reasoning_tokens` không còn |
| Ngữ cảnh dài | Prompt khoảng 220k ký tự được tính đủ **51.155 token**, không bị cắt. Tỷ lệ khoảng 4,3 ký tự/token với code Python |
| Độ trễ ở 51k token | 0,9–3,6 giây mỗi lời gọi |
| Cache tiền tố | Lời gọi thứ hai trùng tiền tố có `cached_tokens` = 50.688. Cache làm giảm chi phí, không ảnh hưởng thiết kế |
| Thử 1 mục, hàm đặt ở giữa ngữ cảnh 51k | Lexical (chép hàm): **đúng nguyên văn**. Semantic, tắt thinking: **sai** (15, đáp án đúng 20). Semantic, bật thinking: **đúng** (20) |

Diễn giải: đây mới là **1 mục**, nên **không phải bằng chứng**. Kết quả chỉ cho thấy:
1. Quy trình chạy được.
2. Tác vụ ở chế độ tắt thinking không bị trần (không dễ tới mức luôn đúng).
3. Thinking đúng là một yếu tố gây nhiễu như đã lo: nó sửa được lỗi semantic.

**Hệ quả cho thiết kế:**
- Mọi lời gọi chính phải gửi `"thinking": {"type": "disabled"}` một cách tường minh.
- Endpoint có thêm mô hình khác loại (Qwen3.6-27B, Llama-3.3-70B, gpt-oss-120b), nên có thể bỏ trần kết luận "một mô hình" nếu thêm 1 mô hình thứ hai. **Độ dài ngữ cảnh tối đa của từng mô hình trên endpoint này chưa kiểm tra.**
- **Giá trên FPT Marketplace: UNKNOWN.** Giá này có thể khác giá chính thức của DeepSeek. Giới hạn tốc độ gọi cũng: UNKNOWN.

### Nhật ký G1 — dựng dữ liệu toolz và chạy thử (06/11)

Chi tiết nằm trong `experiments/README.md`.

| Tiêu chí G1 | Kết quả |
|---|---|
| Vết gọi hàm đúng ≥7/10 | **Đạt**: 21/21 mục có k≥2 đều đúng khi kiểm tra bằng mắt |
| ≥5 mục có 3 hàm trong repository đầu | **Đạt sát nút**: 7 mục k_core≥3 đã đột biến, nhưng phần lớn trong số đó đoán được mà không cần code |
| Lexical gần trần, semantic không ở 0%/100% | Đạt: lexical 1,00; semantic 0,6–0,8 ở 16k |
| Tắt thinking; giá; ngữ cảnh không bị cắt | Đạt: không lọt token thinking; 100 lời gọi ở 16k dùng khoảng 1,5 triệu token đầu vào, phần lớn được cache |

**Hai phát hiện mới làm thay đổi thiết kế:**
1. **Đoán được mà không cần code.** 77/116 mục trả lời đúng khi không đưa code. Chỉ còn 27 mục k=1 và **8 mục k≥2** dùng được. Không đủ dữ liệu cho thiết kế đã định.
2. **Không tất định ở `temperature=0`.** Cùng một prompt, ô có thể chênh tới 0,2 giữa các lần chạy. Cần lặp lại hoặc dùng mô hình thống kê có hiệu ứng ngẫu nhiên theo mục.

**Các hướng xử lý (chờ người dùng chọn):**
- **(A) Đổi tên định danh, khuyến nghị.** Đổi tên mọi hàm và class của thư viện, ở cả ngữ cảnh lẫn câu hỏi, thành tên trung tính (ví dụ `fn_17`). Cách này cắt đường tắt "đoán theo tên" và học thuộc, buộc mô hình phải đọc code. Đây cũng là một thao tác phân tích chương trình (đổi tên alpha bằng AST), và được kiểm chứng lại bằng trình thông dịch. Rủi ro: bài toán khó hơn và xa với code thật hơn. Phải nêu rõ trong trần kết luận.
- **(B) Thêm repository** như more-itertools, boltons. Cách này tăng số mục, nhưng không chữa được nguyên nhân là tên hàm dễ hiểu.
- **(C) Tự sinh biểu thức ghép nhiều hàm thật** (kiểu `pipe(x, f, g, h)`). Cách này điều khiển được k chính xác, nhưng tác vụ nhân tạo hơn.

Đề xuất: A + C trên toolz, và chỉ thêm B nếu vẫn thiếu mục. Ở 16k chưa thấy suy giảm theo vị trí, nên lượt tiếp theo phải chạy ở 32k/64k.

### Nhật ký G1 — lượt 2: A + C (06/11)

Chi tiết nằm trong `experiments/README.md`.

**Kết quả của A + C:**
- Đổi tên (A) làm số mục đoán được mà không cần code giảm từ 66% xuống 5%.
- Chuỗi ghép (C) tạo đủ mục nhiều hàm.

**Phát hiện chặn mới: hiệu ứng sàn/trần.**
- Lexical đạt 1,00 ở mọi ô, kể cả 64k.
- Semantic k=3 chỉ đạt 0,10 ngay ở điều kiện oracle (chỉ đưa các mảnh).
- Như vậy, khi tắt thinking, độ khó nằm ở việc tính chuỗi hàm chứ không nằm ở ngữ cảnh. Đây chính là dấu hiệu dừng đã ghi cho G1 ("sàn hoặc trần, không còn gì để so"), lần này áp dụng cho nhóm k=3.

**Hướng sửa đề xuất (chưa làm):**
1. **Lọc theo độ giải được.** Chỉ dùng mục giải đúng 3/3 ở oracle, rồi đo mức suy giảm do ngữ cảnh dài và vị trí trên các mục đó. Đây là cách điều kiện hóa thường dùng, nhưng tạo thiên lệch chọn mẫu: kết luận chỉ áp dụng cho mục "mô hình giải được khi không có nhiễu", và phải ghi rõ điều này.
2. **Làm chuỗi ghép dễ hơn và sinh nhiều hơn** (list 4–6 phần tử, phép kết thúc đơn giản, khoảng 1.500 ứng viên), để có ≥40 mục giải được ở k=3.
3. **Thay lexical bằng một đối chứng khó hơn**, vì lexical chạm trần nên không cho phép so sánh tương tác "vị trí × tác vụ". Ví dụ: hỏi "hàm X gọi những hàm nào", vẫn có thể chấm tự động bằng vết gọi hàm.

**Hệ quả cho câu hỏi H-ret/H-agg:** dữ liệu hiện tại (n nhỏ) không cho thấy suy giảm do ngữ cảnh dài ở 32k–64k. Nếu điều này vẫn đúng sau khi lọc, thì kết quả là một bằng chứng phản bác việc khái quát kết quả của bài 2505 lên mô hình này. Đó vẫn là một kết quả báo cáo được.

## Step 8 — Final Shortlist

Chỉ còn một ứng viên: C2 đã gộp vào C1′, C3 bị PARK. Vì vậy Step 8 không phải chọn giữa nhiều ứng viên, mà là chốt lại một Topic Card.

**Topic Card — C1′-mini**

| Mục | Nội dung |
|---|---|
| Tên tạm | Định vị hay tổng hợp? Tách nguồn gốc suy giảm theo vị trí khi LLM suy luận về code Python phân tán trong ngữ cảnh dài |
| Vấn đề | Bài 2505 thấy semantic recall suy giảm theo vị trí còn lexical thì không, nhưng không cho biết nguyên nhân là mô hình không **tìm** được code hay không **ghép** được nhiều mảnh. RepoReason (N2) để agent tự tìm code, nên cũng không tách được hai nguyên nhân này |
| Câu hỏi | Xem C1′ ở Step 6, phạm vi theo bản cắt ở Step 7 |
| Phân tích chương trình trong đề tài | Trình thông dịch làm oracle cho đáp án; vết gọi hàm động xác định mảnh liên quan; phản thực tế xóa hàm trong vết và ngoài vết để kiểm tra độ hợp lệ |
| Trần kết luận | Một mô hình (DeepSeek V4 Flash, không suy nghĩ); Python; mức hàm; ngữ cảnh 8k–64k; ngữ cảnh tĩnh, không phải agent |
| Kết quả nào cũng có giá trị | H-ret thắng → nên đầu tư vào truy xuất (RAG, Code Comprehensor). H-agg thắng → truy xuất tốt hơn không đủ. Không có suy giảm → bằng chứng phản bác việc khái quát kết quả của 2505 lên code thật |
| Rủi ro lớn nhất | Thiếu mục đi qua 3 hàm; N6/LoCoBench đã làm trước; chế độ suy nghĩ gây nhiễu. Cả ba đều được kiểm tra ở G1 |
| Việc kiểm chứng tiếp theo | G1 (10/11); giảng viên xác nhận phạm vi |

**Step 8 Gate: PASS** để chuyển sang viết đề cương (`researchwrite`). Gate này sẽ trở thành REVISE nếu G1 thất bại.

---

## Những gì skill này KHÔNG chứng minh

- Không chứng minh C1′ là mới. Hai bài N6 và LoCoBench mới được kiểm tra ở mức abstract.
- Không chứng minh C1′ sẽ cho kết quả thú vị. Có thể H-ret giải thích hết, và đó vẫn là một kết quả, nhưng đóng góp khiêm tốn hơn.
- Các đánh giá ở đây đến từ AI phản biện trên một bộ tài liệu có giới hạn. Giảng viên và chuyên gia trong lĩnh vực mới là người đánh giá cuối cùng.
