# Mở rộng tài liệu — LLM hiểu chương trình

- **Ngày tìm:** 2026-11-06
- **Skill:** `nature-academic-search`, workflow `multi-source-search`.
- **Công cụ:** dùng phương án dự phòng không cần MCP, tức script `academic_search.py` truy vấn OpenAlex.
- **Truy vấn:** 16 truy vấn, chia 3 chủ đề, lọc từ năm 2021 trở đi, 15 kết quả mỗi truy vấn.
- **Kết quả:** 229 bài sau khi gộp trùng. Lọc thủ công còn 38 bài liên quan trực tiếp.
- **Bài gốc:** 4 bài trong `papers/` (ghi chú ở `cards/`).
- **BibTeX:** `library/expanded.bib` (38 mục), danh sách ID ở `library/expanded-refs.txt`.

> **Giới hạn:**
> - Mô tả dưới đây lấy từ abstract trên OpenAlex. Tôi chưa đọc toàn văn bài nào.
> - Số trích dẫn là số của OpenAlex, có độ trễ.
> - Nơi đăng là nhãn OpenAlex. "arXiv" nghĩa là chưa thấy bản đã qua bình duyệt, chứ không chắc chắn là chưa được đăng.
> - Nhiều bài 2026 mới có 0–2 trích dẫn và chưa được kiểm chứng.

## T1 — Hiểu code trong ngữ cảnh dài và hiệu ứng vị trí

Liên quan trực tiếp đến bài 2505.13353 (Sense and Sensitivity).

| Bài | Năm · Nơi đăng | Vì sao đáng đọc |
|---|---|---|
| Lost in the Middle | 2024 · TACL | Bài gốc về hiệu ứng "mất ở giữa". Bài 2505 kế thừa trực tiếp |
| Positional Biases Shift as Inputs Approach Context Window Limits | 2025 · arXiv | Cho thấy hiệu ứng vị trí thay đổi theo tỉ lệ độ dài đầu vào so với cửa sổ ngữ cảnh. Cần đối chiếu với kết quả 4k–16k của bài 2505 |
| Found in the Middle: Calibrating Positional Attention Bias | 2024 · Findings ACL | Cách giảm thiên lệch vị trí. Có thể dùng làm biến can thiệp |
| Michelangelo: Long Context Evaluations Beyond Haystacks | 2024 · arXiv | Đánh giá ngữ cảnh dài bằng dữ liệu tổng hợp, không rò rỉ, đo nhiều hơn khả năng truy hồi đơn thuần. Ý tưởng gần với SemTrace |
| RepoQA: Evaluating Long Context Code Understanding | 2024 · arXiv | Bài "needle" cho code: tìm hàm theo mô tả. Thuộc nhóm lexical recall |
| LONGCODEU | 2025 · ACL | Benchmark hiểu code dài: 4 khía cạnh, 8 tác vụ |
| RepoReasoner | 2026 · PACMSE (FSE) | Suy luận code ở mức repository, qua nhiều file và chuỗi phụ thuộc |
| LoCoBench-Agent | 2025 · arXiv | Agent tương tác nhiều lượt trong kỹ thuật phần mềm với ngữ cảnh dài |
| RepoBench | 2023 · arXiv | Benchmark hoàn thiện code ở mức repository. Thường dùng làm baseline |

## T2 — Hiểu ngữ nghĩa code: mẹo tắt, học thuộc và rò rỉ dữ liệu

Liên quan đến bài 2505 và phần "validity threats" của bài 2608.

| Bài | Năm · Nơi đăng | Vì sao đáng đọc |
|---|---|---|
| CRUXEval | 2024 · arXiv (ICML 2024) | Benchmark dự đoán input/output mà bài 2505 phản biện |
| CRUXEval-X | 2025 · ACL | Mở rộng CRUXEval sang nhiều ngôn ngữ lập trình |
| CodeMind | 2026 · TSE | Khung đo suy luận thực thi code theo hai kiểu ngầm và tường minh |
| Reasoning Runtime Behavior of a Program with LLM (REval) | 2025 · ICSE | Đo dự đoán đường thực thi và trạng thái trung gian, không chỉ đầu ra |
| Demystifying Errors in LLM Reasoning Traces | 2026 · TOSEM | Phân loại lỗi trong vết suy luận khi LLM mô phỏng thực thi |
| CoRE: Fine-Grained Code Reasoning Beyond Output Prediction | 2026 · Findings ACL | Kiểm tra tính nhất quán giữa các cài đặt tương đương về chức năng |
| Evaluating Exact Output and Checkpoint-State Prediction in Real Programs | 2026 · arXiv | Mở rộng CRUXEval với vết thực thi ngắn/dài và điểm kiểm tra giữa vòng lặp |
| **LLMs Lean on Priors, Not Programming Language Semantics** | 2025 · arXiv | Thay đổi luật ngữ nghĩa của ngôn ngữ, cho thấy LLM bám vào thói quen từ dữ liệu huấn luyện. **Rất gần luận điểm "mẹo tắt" của bài 2505** |
| **How Robustly Do LLMs Understand Execution Semantics?** | 2026 · AIware | Đo độ bền vững khi dự đoán đầu ra, phân biệt mô hình thế giới với khớp mẫu |
| Counterfactual Analysis for Code Predicates | 2024 · arXiv | Phân tích phản thực tế trên các cấu trúc logic của code |
| Do Code Semantics Help? Execution Trace-Based Information | 2025 · Findings EMNLP | Thông tin từ vết thực thi có giúp LLM hiểu code không |
| LiveCodeBench | 2024 · arXiv | Benchmark liên tục cập nhật để tránh rò rỉ dữ liệu, có tác vụ dự đoán thực thi |
| Quantifying Contamination in Evaluating Code Generation | 2024 · ACL | Định lượng mức rò rỉ dữ liệu của các benchmark code |
| Generalization or Memorization: Data Contamination … Code Generation | 2026 · TSE | Tách khái quát hóa khỏi học thuộc khi đánh giá sinh code |
| Dynamic Benchmarking of Reasoning … Under Data Contamination | 2025 · arXiv | Biến đổi benchmark động để chống rò rỉ |
| Benchmarking LLMs Under Data Contamination: Static to Dynamic | 2025 · EMNLP | Tổng quan về đánh giá tĩnh và động khi có rò rỉ dữ liệu |

## T3 — Hiểu và truy xuất code ở mức repository

Liên quan đến bài 2610.30016 (Code Comprehensor).

| Bài | Năm · Nơi đăng | Vì sao đáng đọc |
|---|---|---|
| **Code-QA-Bench: Separating Code Reasoning from Documentation Memorization** | 2026 · arXiv | Tách hiểu code thật khỏi việc nhớ tài liệu. **Phản biện trực tiếp cách Code Comprehensor dựa vào tài liệu do LLM sinh** |
| ReCUBE | 2026 · arXiv | Cô lập và đo mức LLM thực sự dùng ngữ cảnh repository |
| RepoAgent | 2024 · EMNLP Demo | Sinh tài liệu mức repository. Là baseline còn thiếu trong bài 2610 |
| RepoMind | 2026 · ICPC | Suy luận trên tài liệu repository có cấu trúc. Hướng rất gần với CodeScribe |
| RepoCoder | 2023 · EMNLP | Truy xuất và sinh code lặp, baseline kinh điển |
| GraphCoder | 2024 · ASE | Truy xuất từ thô đến tinh trên đồ thị ngữ cảnh code |
| Dataflow-Guided Retrieval Augmentation | 2024 · ACL | Truy xuất theo luồng dữ liệu, gắn trực tiếp với phân tích chương trình |
| GraphCodeAgent | 2025 · arXiv | Agent dẫn đường bằng hai đồ thị |
| CodeRAG-Bench | 2025 · Findings NAACL | Kiểm tra truy xuất có giúp sinh code không |
| Retrieval-Augmented Code Generation: Survey (repository-level) | 2025 · arXiv | Tổng quan mới về RAG cho code ở mức repository |
| CoCoSoDa | 2023 · ICSE | Học tương phản cho tìm kiếm code. Là baseline còn thiếu của CodeContrast |
| Using an LLM to Help With Code Understanding | 2024 · ICSE | Nghiên cứu người dùng về LLM hỗ trợ đọc hiểu code |

## Nhận xét

1. **Hướng của bài 2505 đã có nhiều công trình gần.** "LLMs Lean on Priors", "How Robustly…", CoRE và "Exact Output and Checkpoint-State" (2025–2026) đều tấn công vào câu hỏi mẹo tắt hay ngữ nghĩa thật. Ý tưởng mới cần phân biệt rõ với các bài này.
2. **Khoảng trống có thể có:** giao giữa T1 và T2, tức hiệu ứng vị trí cộng với ngữ nghĩa ở mức repository. RepoReasoner, LONGCODEU và RepoQA đo hiểu code dài, nhưng từ abstract chưa thấy bài nào kiểm soát vị trí cùng với độ nhạy ngữ nghĩa như bài 2505. Cần đọc toàn văn để xác nhận.
3. **Code-QA-Bench và ReCUBE** cho sẵn phương pháp để kiểm tra lại các tuyên bố của Code Comprehensor. Đây là chỗ thiếu baseline đã nêu trong card của bài 2610.
4. Lượt 1 thiếu SWE-bench và hướng phân tích chương trình truyền thống. Lượt 2 bên dưới đã bổ sung hai phần này.

---

# Lượt 2 — Semantic Scholar (có API key)

- **Ngày tìm:** 2026-11-06
- **Tìm theo từ khóa:** 8 truy vấn qua `paper_search.py --sources semanticscholar`, được 158 bài. Kết quả ở `library/search/s2-sweep.{json,md}`.
- **Tìm theo trích dẫn xuôi:** lấy các bài trích dẫn 6 bài gốc qua S2 API. Kết quả ở `library/search/s2-forward-citations.json`.
  - Sense and Sensitivity: 4 bài trích dẫn
  - CRUXEval: 410
  - RepoQA: 53
  - LLMs Lean on Priors: 7
  - Code Comprehensor và survey SE–Sec: 0 (cả hai đều quá mới)
- **Nơi đăng bài 2505.13353:** Semantic Scholar ghi bài đã được đăng ở **ACL 2025**.
- **Giới hạn:** cột "nơi đăng" lấy từ Semantic Scholar. Chưa kiểm tra hạng (rank) của venue.

## T4 — Phân tích chương trình truyền thống kết hợp LLM (sát tên môn học)

| Bài | Năm · Nơi đăng | Ghi chú |
|---|---|---|
| A Contemporary Survey of LLM Assisted Program Analysis | 2025 · IEEE Trans. AI | Tổng quan, nên đọc đầu tiên cho hướng này |
| Large Language Model Powered Symbolic Execution | 2025 · PACMPL (OOPSLA) | LLM đảm nhận vai trò của solver hoặc engine trong thực thi ký hiệu |
| Enchanting Program Specification Synthesis by LLMs using Static Analysis and Program Verification | 2024 | Kết hợp phân tích tĩnh với kiểm chứng để sinh đặc tả |
| Can LLMs Reason About Program Semantics? (Formal Specification Inference) | 2025 · ACL | Đánh giá LLM suy ra đặc tả hình thức |
| Assisting Static Analysis with LLMs: A ChatGPT Experiment | 2023 · ESEC/FSE | LLM hỗ trợ một công cụ phân tích tĩnh |
| Automatically Inspecting Thousands of Static Bug Warnings with LLM | 2024 · TOSEM | Lọc cảnh báo sai (false positive) của công cụ phân tích tĩnh |
| Teaching LLMs Program Semantics via Symbolic Execution Traces | 2026 · arXiv | Huấn luyện LLM bằng vết thực thi ký hiệu |
| EquiBench | 2025 · EMNLP | Đánh giá ngữ nghĩa qua kiểm tra tương đương chương trình |
| TF-Bench (type inference trong System F) | 2025 · NeurIPS | Ngữ nghĩa qua suy luận kiểu, loại bỏ yếu tố tên biến |
| RepoScope: Call Chain-Aware Multi-View Context | 2026 · ICSE | Dùng chuỗi lời gọi hàm làm ngữ cảnh. Gần với CodeGraph |

## T2 bổ sung — Độ bền ngữ nghĩa và mẹo tắt (từ các bài trích dẫn CRUXEval)

| Bài | Năm · Nơi đăng | Ghi chú |
|---|---|---|
| **RepoMirage: Probing Repository Context Reasoning in Code Agents with Perturbations** | 2026 · arXiv 2605.26177 | **Gần nhất với khoảng trống T1 × T2:** nhiễu loạn ngữ cảnh ở mức repository. Phải đọc toàn văn trước khi chốt đề tài |
| Are LLMs Robust in Understanding Code Against Semantics-Preserving Mutations? | 2025 · arXiv 2505.10443 | Biến đổi code giữ nguyên ngữ nghĩa |
| Re-Evaluating Code LLM Benchmarks Under Semantic Mutation | 2025 · arXiv 2506.17369 | Đánh giá lại benchmark sau khi đột biến ngữ nghĩa |
| CODECRASH | 2025 · arXiv | Kiểm tra sức chịu đựng dưới nhiễu loạn cấu trúc và ngữ nghĩa |
| Can LLMs Really Reason about Code? (input–code–output) | 2026 · AIware | Quan hệ giữa input, code và output |
| SemCoder | 2024 · NeurIPS | Huấn luyện code LLM với ngữ nghĩa thực thi |
| Predicting Program Exit Code with LLMs and PL Semantics | 2026 · ACM SIGPLAN workshop | Trích dẫn trực tiếp bài 2505 |

## Hiểu ngữ cảnh dài (bổ sung)

| Bài | Năm · Nơi đăng | Ghi chú |
|---|---|---|
| RULER: What's the Real Context Size of Your Long-Context LMs? | 2024 · arXiv (COLM) | Benchmark ngữ cảnh dài chuẩn, được trích dẫn nhiều nhất trong nhóm |
| **Retrieval Or Holistic Understanding? Dolce** | 2024 · arXiv 2409.06338 | Phân biệt tác vụ truy hồi với tác vụ hiểu toàn cục. **Tương đương lexical/semantic recall nhưng cho văn bản thường** |
| LongCodeZip | 2025 · ASE | Nén ngữ cảnh dài cho code LLM |

## SWE-bench và vấn đề học thuộc

| Bài | Năm · Nơi đăng | Ghi chú |
|---|---|---|
| SWE-bench | 2023 · ICLR 2024 | Bài gốc |
| **The SWE-Bench Illusion: When SOTA LLMs Remember Instead of Reason** | 2025 · ICSE workshop (SEIP) | LLM nhớ thay vì suy luận trên SWE-bench |
| Does SWE-Bench-Verified Test Agent Ability or Model Memory? | 2025 · arXiv | Cùng câu hỏi với bài trên |
| Are "Solved Issues" in SWE-bench Really Solved Correctly? | 2025 · ICSE 2026 | Test oracle yếu. Khớp với các mối đe dọa tính hợp lệ nêu trong bài 2608 |
| UTBoost | 2025 · ACL | Tăng cường test để đánh giá SWE-bench chặt hơn |

## Cập nhật nhận xét sau lượt 2

1. **Bài 2505 mới có 4 bài trích dẫn, và không bài nào nối tiếp trực tiếp câu hỏi vị trí cộng ngữ nghĩa.** Đây là dấu hiệu hướng này còn trống. Tuy vậy **RepoMirage** và **Dolce** là hai bài cần đọc toàn văn trước khi khẳng định tính mới.
2. **Nhánh T4 hợp với môn học:** dùng công cụ phân tích chương trình (call graph, data flow, symbolic execution) làm **oracle** để kiểm tra LLM có hiểu ngữ nghĩa thật hay không. Hướng này kết nối T2 với T4, và trong lượt tìm này chưa thấy bài nào làm đúng như vậy cho ngữ cảnh dài.
3. Cả SWE-bench và CRUXEval đều đã bị phản biện là cho phép học thuộc hoặc mẹo tắt. Điều này khẳng định nhận xét xuyên suốt của 4 card ban đầu.
