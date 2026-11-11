# Khảo sát đề tài: Định vị hay tổng hợp? Đo khả năng LLM suy luận về code Python nằm rải rác trong ngữ cảnh dài, dùng phân tích chương trình làm thước đo

**Môn học:** Kỹ thuật phân tích chương trình. **Đề tài 5** (Chương 13)
**Phiên bản:** bản khảo sát để duyệt, ngày 06/11/2026. **Hạn nộp đề tài:** 30/11/2026
**Trạng thái:** đề xuất hướng nghiên cứu và kết quả thử nghiệm sơ bộ; chưa phải kết luận

---

## Tóm tắt

Các mô hình ngôn ngữ lớn (LLM) ngày càng được dùng để đọc và giải thích code ở quy mô cả repository. Một nghiên cứu gần đây [1] cho thấy, ở mức **một hàm**:
- mô hình vẫn *chép lại* được đoạn code ở mọi vị trí trong ngữ cảnh dài (*lexical recall*);
- nhưng khả năng *hiểu đoạn code đó làm gì khi chạy* (*semantic recall*) giảm mạnh khi đoạn code nằm ở giữa ngữ cảnh.

Ở quy mô repository, code liên quan thường nằm rải ở nhiều hàm, nhiều file. Lúc đó có hai cách giải thích cho việc mô hình trả lời sai:
- **H-ret:** mô hình không *tìm thấy* đúng các đoạn code;
- **H-agg:** mô hình tìm thấy nhưng không *ghép* được chúng lại để suy ra kết quả.

Các nghiên cứu ở mức repository hiện có [2, 4] để agent tự đi tìm code, nên không tách được hai nguyên nhân này. Mỗi nguyên nhân lại đòi hỏi một hướng cải tiến khác: cải thiện truy xuất (như [6]) hay cải thiện khả năng suy luận.

Đề tài đề xuất một **khung đo có kiểm soát**, trong đó các kỹ thuật phân tích chương trình đóng vai trò cốt lõi:
- trình thông dịch làm *oracle* cho đáp án đúng;
- *dynamic call trace* xác định các hàm thực sự quyết định kết quả;
- *backward slice* theo quan hệ def-use loại phần code thừa;
- *đổi tên alpha* có kiểm chứng để chặn việc đoán theo tên hàm.

Thử nghiệm sơ bộ trên thư viện toolz với DeepSeek-V4-Flash cho thấy:
- khung đo chạy được;
- đổi tên làm tỷ lệ câu hỏi "trả lời đúng mà không cần đọc code" giảm từ 66% xuống 5%;
- nhưng đồng thời lộ ra một vấn đề sàn/trần mà thiết kế phải xử lý trước khi chạy thí nghiệm chính (mục 5).

Báo cáo này đề nghị giảng viên duyệt **phạm vi đã thu hẹp** và **mức đóng góp** nêu ở mục 8.

---

## 1. Bối cảnh

Hiểu chương trình là bài toán gốc của phân tích chương trình. Các công cụ như *program slicing*, *call graph* hay *data-flow analysis* trả lời câu hỏi "giá trị này phụ thuộc vào những đoạn code nào". Ngày nay, LLM được dùng để trả lời chính những câu hỏi đó bằng ngôn ngữ tự nhiên. Hai bài tổng quan [7, 8] cùng chỉ ra rằng điểm yếu lớn của mảng này nằm ở **cách đánh giá**: rò rỉ dữ liệu (*data leakage*) và các benchmark cho phép mô hình trả lời bằng "đường tắt" thay vì thật sự đọc code.

Bài [1] cụ thể hóa vấn đề này cho ngữ cảnh dài:
- **Thiết kế:** đặt một hàm mục tiêu ở 11 vị trí giữa 20–80 hàm gây nhiễu (khoảng 4k–16k token), thử trên 10 LLM.
- **Lexical:** độ chính xác chép lại gần như không đổi theo vị trí.
- **Semantic:** độ chính xác dự đoán đầu ra giảm theo vị trí, với median Δ 53,36% trên CRUXEval và tới 92,73% trên SemTrace.
- **Bằng chứng về đường tắt:** khi xóa 50% số dòng code, độ chính xác trên CRUXEval chỉ giảm 44,15% (dự đoán input) và 59,74% (dự đoán output). Mô hình vẫn trả lời được phần lớn khi code đã bị khuyết, tức là đang dựa vào tri thức có sẵn.

**Vì sao vấn đề này thuộc môn học:** câu hỏi "mô hình có thật sự dùng *đúng các đoạn code mà kết quả phụ thuộc vào* hay không" chỉ đo được chặt chẽ khi ta biết chính xác tập phụ thuộc đó. Đó là việc của phân tích chương trình.

---

## 2. Khảo sát các công trình liên quan

Tài liệu được tìm qua OpenAlex, Semantic Scholar và arXiv (khoảng 32 truy vấn, năm 2021–2026), có lần theo các bài trích dẫn [1]. Sáu bài được đọc toàn văn và lập *paper card*; RepoReason [2] được đọc toàn văn có mục tiêu; các bài còn lại chỉ được đọc ở mức abstract hoặc mới biết tiêu đề, và được ghi rõ như vậy.

### 2.1. Ngữ cảnh dài và ảnh hưởng của vị trí

- *Lost in the Middle* [9] mô tả hiện tượng mô hình dùng thông tin ở giữa ngữ cảnh kém hơn ở hai đầu, trên tác vụ văn bản.
- RepoQA [10] và LONGCODEU [11] mở rộng sang code dài, nhưng chủ yếu đo khả năng *tìm* code. *(Chỉ đọc abstract.)*
- [1] là bài gần nhất: tách lexical và semantic recall theo vị trí. Tuy vậy, bài chỉ làm ở **mức một hàm**, ngữ cảnh ≤16k, và đo độ nhạy bằng cách xóa dòng ngẫu nhiên.
- DOLCE [5] phân loại 44 tác vụ ngữ cảnh dài thành dạng "truy hồi" hay "hiểu toàn cục" bằng cách lấy mẫu các đoạn quan sát. Bài không có code thực thi và không xét vị trí.

**Còn thiếu:** chưa có thiết kế nào đặt **nhiều mảnh code phụ thuộc nhau** ở các vị trí có kiểm soát, kèm đối chứng lexical trên **cùng các mảnh đó**.

### 2.2. Đánh giá hiểu ngữ nghĩa code và vấn đề đường tắt

- CRUXEval [12] là chuẩn dự đoán input/output phổ biến. [1] chỉ ra rằng CRUXEval có độ nhạy ngữ nghĩa thấp.
- Một số bài dùng phép phản thực tế hoặc đột biến giữ ngữ nghĩa [13] để kiểm tra mô hình có hiểu code thật hay không. Một số bài khác gợi ý rằng LLM dựa vào tri thức có sẵn nhiều hơn ngữ nghĩa của ngôn ngữ lập trình [14]. *(Chỉ đọc abstract hoặc tiêu đề.)*
- Hai bài tổng quan [7, 8] xếp rò rỉ dữ liệu và việc tự sinh tập test vào nhóm điểm yếu chung. Bài [8] còn đề xuất thang bằng chứng E1–E4 để đánh giá mức tin cậy của các tuyên bố.

**Bài học cho thiết kế:** phải chủ động chặn đường tắt. Đề tài dùng ba cách: đột biến input, điều kiện "hỏi khi không đưa code", và đổi tên định danh.

### 2.3. Mức repository và phân tích chương trình làm thước đo

- **RepoReason** [2] (ACL 2026) là công trình gần nhất ở mức repository. Bài dùng:
  - repository thật;
  - môi trường thực thi làm oracle, với input đã đột biến;
  - *dynamic program slicing* làm thước đo độ khó.
  
  Bài nêu hiện tượng mô hình yếu ở khâu tổng hợp (*aggregation deficit*). Tuy nhiên, agent tự đi tìm code, nên bài **không kiểm soát vị trí** của code trong ngữ cảnh và **không có đối chứng lexical**. Vì vậy chưa tách được H-ret khỏi H-agg.
- **CORE** [3] (NeurIPS 2025) dùng phân tích tĩnh (phụ thuộc dữ liệu, phụ thuộc điều khiển, luồng thông tin) làm đáp án chuẩn cho 12.553 bài, nhưng ở mức chương trình ngắn. *(Chỉ đọc abstract.)*
- **RepoMirage** [4] làm nhiễu repository trên SWE-Bench Verified. Kết quả: tỷ lệ giải được giảm từ 66,80% xuống 49,78%, còn số file agent mở tăng từ 4,77 lên 13,24. Tác giả gọi đây là "trôi khi khám phá" (*exploration drift*). Bài đo agent, không kiểm soát vị trí.
- **Code Comprehensor** [6] đại diện cho hướng **giải bằng truy xuất**: dùng call graph tĩnh, tài liệu phân cấp và tìm kiếm đa phương thức cho repository lớn. Hướng này ngầm giả định rằng nút thắt nằm ở khâu tìm code (gần với H-ret).

**Kết luận của khảo sát, trong biên tìm kiếm đã nêu:** chưa thấy công trình nào vừa kiểm soát vị trí và độ phân tán của **các mảnh phụ thuộc** trong ngữ cảnh tĩnh, vừa có đối chứng lexical trên cùng các mảnh đó. Hai bài *Robustness & Reasoning Fidelity in Long-Context Code QA* và LoCoBench [15] mới được kiểm tra ở mức abstract; cần đọc toàn văn trước khi khẳng định.

---

## 3. Khoảng trống và câu hỏi nghiên cứu

**Khoảng trống.** Từ [1] và [2], ta biết LLM hiểu code kém đi trong ngữ cảnh dài hoặc ở mức repository, nhưng **chưa biết vì sao**: do không tìm thấy (H-ret) hay do không ghép được (H-agg). Hai cách giải thích dẫn tới hai hướng cải tiến khác nhau, nên đây là một câu hỏi có hệ quả thực tế, không chỉ là "chưa nhiều người làm".

**Câu hỏi nghiên cứu (RQ).**
- **RQ1:** Code Python thật được đặt trong ngữ cảnh tĩnh dài, với các mảnh cần thiết đặt có kiểm soát về vị trí (đầu/giữa/cuối), độ phân tán (gom một chỗ hay rải đều) và độ dài ngữ cảnh (8k–64k). Độ chính xác **dự đoán giá trị** có giảm so với điều kiện chỉ đưa đúng các mảnh (*oracle*) không, và giảm nhiều hơn tác vụ đối chứng trên cùng mảnh không?
- **RQ2:** Khi mô hình phải **chép các mảnh liên quan ra trước rồi mới trả lời** (*retrieve-then-trace*), phần suy giảm có mất đi không? Nếu mất đi thì ủng hộ H-ret; nếu vẫn còn thì ủng hộ H-agg.

**Trần kết luận (đã thu hẹp).** Kết luận chỉ áp dụng cho:
- 1–2 mô hình, chạy ở chế độ không suy nghĩ (*non-thinking*);
- code Python, mảnh ở mức hàm;
- định danh đã đổi tên, ngữ cảnh tĩnh (không phải agent).

---

## 4. Phương pháp: pipeline phân tích chương trình

Pipeline đã được cài đặt trong `experiments/` (Python, thư viện chuẩn và `ast`). Mỗi bước dùng một kỹ thuật của môn học:

| Bước | Kỹ thuật phân tích chương trình | Vai trò |
|---|---|---|
| 1. Lấy mục từ doctest | `doctest.DocTestFinder` | Lấy các lời gọi thật kèm kết quả mong đợi |
| 2. Đột biến hằng số | Biến đổi AST, ánh xạ đơn ánh nhất quán | Chống học thuộc kết quả trong docstring |
| 3. Cắt phần setup | **Backward slice tĩnh** theo quan hệ def-use, giữ cả các câu lệnh có thể sửa đổi đối tượng (thận trọng) | Chỉ giữ code mà kết quả phụ thuộc |
| 4. Xác định mảnh | **Dynamic call trace** (`sys.setprofile`), quy mỗi lời gọi về hàm hoặc class cấp module | Tập "mảnh" chính là các hàm thực sự được chạy |
| 5. Oracle | **Thực thi** hai lần, so sánh kết quả, kiểm tra lại trong namespace chỉ chứa những gì mô hình được thấy | Đáp án đúng; loại mục không tất định |
| 6. Chặn đoán theo tên | **Đổi tên alpha** mọi hàm và class (`fn_NNN`) trên AST, **kiểm chứng bằng cách chạy lại** trong một namespace phẳng: phải cùng đáp án và cùng tập mảnh | Buộc mô hình đọc code |
| 7. Sinh mục nhiều hàm | Ghép chuỗi các hàm thật của thư viện trên dữ liệu ngẫu nhiên | Kiểm soát được số mảnh k |
| 8. Dựng ngữ cảnh | Chèn mảnh theo vị trí tính bằng số ký tự; phần độn là các hàm khác của thư viện, sau đó đến stdlib | Thiết kế nhân tố |

**Các điều kiện thí nghiệm:**
- **semantic:** dự đoán `repr(result)`;
- **đối chứng lexical:** chép lại các mảnh;
- **retrieve-then-trace:** chép rồi dự đoán;
- **oracle:** chỉ đưa các mảnh;
- **không ngữ cảnh:** đo mức đoán mò.

**Thiết lập gọi mô hình:**
- Mô hình chính là DeepSeek-V4-Flash qua API tương thích OpenAI.
- **Thinking phải tắt tường minh**, vì nó bật theo mặc định và sẽ biến mọi câu hỏi thành retrieve-then-trace ngầm.
- `temperature=0`. Mỗi lời gọi được ghi lại số token thực tế mà API báo về.

**Phân tích dự kiến:**
- hồi quy logistic: đúng/sai ~ vị trí × tác vụ × độ dài, có hiệu ứng ngẫu nhiên theo mục;
- khoảng tin cậy bootstrap theo mục;
- lặp lại mỗi ô, vì mô hình không tất định (mục 5).

---

## 5. Kết quả sơ bộ (pilot, 06/11/2026)

Tất cả kết quả dưới đây là **sơ bộ**, với n nhỏ và một mô hình. Chúng được dùng để sửa thiết kế, không dùng để kết luận.

**5.1. Dữ liệu.**
- Từ toolz 1.0.0 có 159 ví dụ doctest ứng viên; giữ được 116 mục. Phần lớn chỉ dùng 1 hàm (88 mục).
- Thêm 389 mục chuỗi ghép. Riêng nhóm này cho 92 mục có đúng 3 hàm lõi và 232 mục có ≥4 hàm, so với chỉ 6 mục 3 hàm lấy từ doctest.
- Đổi tên alpha được kiểm chứng trên **497/503 mục**.
- Kiểm tra bằng mắt 21 mục nhiều hàm: vết gọi hàm đúng ở cả 21.

**5.2. Đường tắt nhờ tên hàm.** Khi hỏi mà **không đưa code**:
- trước khi đổi tên: **77/116 mục (66%)** vẫn trả lời đúng;
- sau khi đổi tên: còn **25/497 (5%)**; riêng mục chuỗi ghép chỉ 4/389.

Đây là bằng chứng trực tiếp rằng benchmark dựng từ thư viện phổ biến có thể đo sai nếu không chặn đường tắt.

**5.3. Ảnh hưởng của ngữ cảnh** (20 mục, 32k và 64k, 360 lời gọi):

| Điều kiện | 1 hàm | 3 hàm |
|---|---|---|
| Đối chứng lexical (chép lại) | 1,00 | 1,00 |
| Semantic, ngữ cảnh 32k/64k | 0,5–0,7 | 0,1–0,4 |
| Semantic, oracle (chỉ đưa các mảnh) | 0,50 | 0,10 |

- Đối chứng lexical **chạm trần** ở mọi ô.
- Mục 3 hàm **chạm sàn ngay ở điều kiện oracle**. Với các mục này, độ khó nằm ở việc tính nhẩm chuỗi hàm, chưa nằm ở ngữ cảnh dài.
- Ở n=10, **chưa quan sát được** suy giảm theo vị trí. Đây là giả thuyết cần kiểm tra lại, không phải kết luận.

**5.4. Các mối đe dọa tính hợp lệ đã phát hiện:**
- Mô hình **không tất định** ở `temperature=0`: cùng prompt, ô có thể chênh tới 0,2.
- Ở một mục thử, bật thinking **sửa được** câu trả lời sai.
- Chạy oracle 3 lần, số mục giải đúng cả 3 lần: 36 mục 1 hàm, 22 mục 2 hàm, 18 mục 3 hàm.

---

## 6. Rủi ro và phương án

| Rủi ro | Phương án |
|---|---|
| Sàn ở mục nhiều hàm (5.3) | Chỉ dùng mục giải đúng 3/3 ở oracle. Sinh thêm chuỗi ghép dễ hơn (list 4–6 phần tử, phép kết thúc đơn giản) để có ≥40 mục mỗi nhóm. Ghi rõ **thiên lệch chọn mẫu** do bước lọc này |
| Trần ở đối chứng lexical | Thay bằng một đối chứng khó hơn, chấm được bằng vết gọi hàm, ví dụ "hàm X gọi trực tiếp những hàm nào" |
| Không có suy giảm nào để giải thích | Báo cáo như một kết quả âm tính có kiểm soát: hiện tượng của [1] không lặp lại ở điều kiện này. Khi đó RQ2 không trả lời được, và phải nói rõ |
| Chỉ một mô hình | Thêm Qwen3.6-27B hoặc Llama-3.3-70B trên cùng endpoint, nếu độ dài ngữ cảnh cho phép (chưa kiểm tra) |
| Code đổi tên kém tự nhiên | Đưa vào trần kết luận; báo cáo song song kết quả trên một tập nhỏ không đổi tên |
| Tính mới | Đọc toàn văn N6 và LoCoBench trước 10/11. Nếu một trong hai đã làm đúng thiết kế này thì quay lại bước rà soát tính mới |
| Mảnh mức hàm thô hơn slice mức dòng của [2] | Nêu rõ trong giới hạn. Mức dòng là hướng mở rộng |

---

## 7. Kế hoạch đến 30/11/2026

| Thời gian | Công việc | Cổng |
|---|---|---|
| 07–10/11 | Đọc toàn văn N6 và LoCoBench; sinh thêm chuỗi ghép dễ; hiệu chỉnh oracle; thay đối chứng lexical | **Go/No-Go:** đủ ≥30–40 mục giải được ở mỗi nhóm k |
| 11–17/11 | Chạy thí nghiệm chính: 3–4 bố cục × 3 độ dài (16k/32k/64k) × các tác vụ, lặp 2–3 lần | Dữ liệu đầy đủ |
| 18–22/11 | Phân tích (logistic có hiệu ứng ngẫu nhiên, bootstrap); thêm mô hình thứ hai nếu còn thời gian | — |
| 23–28/11 | Viết báo cáo, vẽ hình, chuẩn bị slide | — |
| 29–30/11 | Dự phòng | — |

Chi phí API ước tính ở mức vài chục triệu token đầu vào; phần lớn được cache nhờ các prompt có chung phần đầu.

**Sản phẩm bàn giao:**
1. Pipeline phân tích chương trình tái sử dụng được (`experiments/`).
2. Bộ dữ liệu toolz đã đổi tên và kiểm chứng bằng thực thi.
3. Báo cáo thực nghiệm có ghi rõ các giới hạn.

---

## 8. Đề nghị giảng viên và nhóm duyệt

1. **Phạm vi:** đồng ý thu hẹp về *một thư viện Python (toolz), mảnh ở mức hàm, 1–2 mô hình, ngữ cảnh tĩnh*?
2. **Nội dung phân tích chương trình:** bộ kỹ thuật gồm vết gọi hàm động, backward slice def-use, đổi tên alpha có kiểm chứng và oracle thực thi có đủ cho yêu cầu của môn không? Hay cần thêm slice mức dòng hoặc call graph tĩnh?
3. **Mức đóng góp:** chấp nhận kết quả ở dạng *khung đo cộng kết quả thực nghiệm trung thực*, kể cả khi kết quả âm tính, thay vì cam kết xác nhận H-ret hay H-agg?
4. **Lọc theo độ giải được:** đồng ý chỉ dùng các mục mô hình giải được ở điều kiện oracle, và chấp nhận thiên lệch chọn mẫu đi kèm?

---

## Tài liệu tham khảo

[1] A. Štorek, M. Gupta, S. Hajizadeh, P. Srivastava, S. Jana. *Sense and Sensitivity: Examining the Influence of Semantic Recall on Long Context Code Understanding.* arXiv:2505.13353v5.
[2] *From Laboratory to Real-World Applications: Benchmarking Agentic Code Reasoning at the Repository Level* (RepoReason). ACL 2026; arXiv:2601.03731.
[3] *CORE: Benchmarking LLMs Code Reasoning Capabilities through Static Analysis Tasks.* NeurIPS 2025.
[4] H. Li, Y. Zhang, H. Su, J. Zhu, Y. Dong, S. Zhu. *RepoMirage: Probing Repository Context Reasoning in Code Agents with Perturbations.* arXiv:2605.26177.
[5] *Retrieval Or Holistic Understanding? Dolce: Differentiate Our Long Context Evaluation Tasks.* arXiv:2409.06338.
[6] S. Roychowdhury, J. H. R. Isaac, J. Gao, M. Klitte, D. Corcoran. *Code Comprehensor: Hierarchical Documentation and Cross-Modal Retrieval for Large Repositories.* arXiv:2610.30016.
[7] Q. Zhang et al. *A Survey on Large Language Models for Software Engineering.* arXiv:2312.15223v2.
[8] W. Lin, T. Zhou, Z. Xie, C. Hong. *Large Language Models at the Intersection of Software Engineering and Software Security: An Evidence-Centered Structured Survey and Research Agenda.* arXiv:2608.21107.
[9] *Lost in the Middle: How Language Models Use Long Contexts.* Transactions of the ACL, 2024.
[10] *RepoQA: Evaluating Long Context Code Understanding.* arXiv:2406.06025, 2024.
[11] *LONGCODEU: Benchmarking Long-Context Language Models on Long Code Understanding.* ACL 2025; arXiv:2503.04359.
[12] *CRUXEval: A Benchmark for Code Reasoning, Understanding and Execution.* arXiv:2401.03065, 2024.
[13] *Do Large Code Models Understand Programming Concepts? Counterfactual Analysis for Code Predicates.* arXiv:2402.05980, 2024.
[14] *LLMs Lean on Priors, Not Programming Language Semantics.* arXiv:2510.03415, 2025.
[15] *LoCoBench: A Benchmark for Long-Context Large Language Models in Complex Software Engineering* (chỉ đọc abstract).

*Tài liệu nội bộ kèm theo:*
- `cards/`: 6 paper card;
- `library/novelty-audit.md`: rà soát tính mới, phản biện, khả thi;
- `experiments/README.md`: pipeline và số liệu pilot.
