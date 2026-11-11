# Paper Card — Large Language Models at the Intersection of Software Engineering and Software Security: An Evidence-Centered Structured Survey and Research Agenda

> Source coverage: Full paper (23 trang PDF, gồm References PDF p. 19-23; không có phụ lục/supplement)
> Extraction confidence: High (PyMuPDF; đã kiểm tra trực quan PDF p. 5 chứa Figure 1, Figure 2, Equation 1)
> Locator mode: page-grounded
> Primary analytical lens: review (structured narrative + tertiary survey, có đề xuất framework khái niệm)
> Secondary analytical lens: None
> Context verification: Paper-only
> Card completeness: Complete relative to supplied source
> Ghi chú số trang: mọi pointer dùng chỉ số trang PDF (`PDF p. N`). Số trang in ở chân trang trùng với chỉ số PDF; các nhãn "printed page" 2026/2023 trong source bundle (PDF p. 2, 5) là năm bị nhận nhầm, không phải số trang in.

**Bảng thuật ngữ (Terminology Ledger, khóa cho toàn card)**

| Thuật ngữ chuẩn | Định nghĩa lần đầu | Biến thể trong bài | Quyết định |
|---|---|---|---|
| LLM4SE / LLM4Security | LLM cho software engineering / software security | "LLM4SE+Security", "LLM4SE & Security" | Dùng LLM4SE và LLM4Security riêng; "giao SE–security" cho phần giao |
| evaluation configuration E | E = ⟨A, C, M, T, V, B, H⟩ | "configuration E", "evaluation configuration" | Dùng "evaluation configuration E" |
| J@k | joint functional-and-security success tại k ứng viên | "joint secure-and-functional outcome" | Dùng J@k |
| evidence ladder E1–E4 | thang bằng chứng claim–evidence | "claim–evidence ladder", "evidence levels" | Dùng "evidence ladder E1–E4" |
| authority tiers G0–G3 | bậc quyền hạn của agent | "agent authority" | Dùng "authority tiers G0–G3" |
| minimum reporting protocol | Table 5 | "reporting protocol" | Dùng "minimum reporting protocol" |
| APR | automated program repair | "program repair" | Dùng APR |
| RAG | Retrieval-Augmented Generation | "retrieval" | Dùng RAG khi nói chiến lược, "retrieval" khi nói thành phần |
| harness | khung agent thực thi model | "scaffolding", "agent framework" | Dùng harness; chú ý bài dùng lẫn "scaffolding" ở PDF p. 7 |

---

## 01 Thông tin cơ bản

| Trường | Nội dung |
|---|---|
| Tiêu đề | Large Language Models at the Intersection of Software Engineering and Software Security: An Evidence-Centered Structured Survey and Research Agenda [Paper: PDF p. 1, Title] |
| Tác giả và đơn vị | Wei Lin, Tao Zhou, Zhaofei Xie, Changgui Hong — Nanjing Liancheng Intelligent Technology Group, Nanjing, China [Paper: PDF p. 1, Title block] |
| Venue | arXiv preprint (cs.AI), arXiv:2608.21107v1, 21 Aug 2026; chưa thấy thông tin peer-review [Paper: PDF p. 1, arXiv stamp] |
| Năm | 2026; search cutoff 31/05/2026 [Paper: PDF p. 2, Section 2.1] |
| Loại bài | Evidence-centered structured narrative và tertiary survey, tác giả tự nói *không* phải systematic literature review (SLR) theo protocol hoàn chỉnh [Paper: PDF p. 2, Section 2.1] |
| Lĩnh vực | Software engineering, software security, LLM cho code, agentic systems |
| Keywords | large language models, software engineering, software security, code generation, vulnerability detection, automated program repair, agentic systems [Paper: PDF p. 1, Keywords] |
| DOI / arXiv | arXiv:2608.21107v1; DOI: không có trong nguồn |
| Code / dữ liệu | Bài nói có "source package" (review protocol, seed corpus máy đọc được, search-log, extraction template, quality rubric, script) [Paper: PDF p. 3-4, Section 2.3] nhưng **không cung cấp URL hay archival identifier** trong văn bản (Not assessable — không tìm thấy link trong nguồn) |
| Số tài liệu tham khảo | 53 [Paper: PDF p. 19-23, References] |
| Ngày đọc | 2026-11-06 |
| Vị trí trong hướng nghiên cứu của người dùng | Not assessable (người dùng chưa cung cấp); Agent-derived candidate: bài là khung đánh giá/đo lường cho đề tài phân tích chương trình có dùng LLM, đặc biệt ở giao giữa APR/vulnerability repair và kiểm chứng bảo mật |

## 02 Tóm tắt một câu

[Paper] Bài tổng hợp có cấu trúc (không meta-analysis) các công trình LLM cho SE và security đến 31/05/2026, đề xuất một taxonomy hợp nhất, một assurance framework (evaluation configuration E, chỉ số J@k, evidence ladder E1–E4, authority tiers G0–G3) và một minimum reporting protocol, rồi kết luận — ở mức lập luận khái niệm chứ không bằng số liệu gộp — rằng năng lực của LLM nên được đánh giá như một assurance case nhiều loại bằng chứng thay vì một điểm benchmark đơn lẻ [Paper: PDF p. 1, Abstract] [Paper: PDF p. 18-19, Section 9].

## 03 Câu hỏi nghiên cứu

- **Vấn đề cụ thể** [Paper]: Bằng chứng cho hệ thống LLM bị chia đôi — đánh giá SE tập trung vào hoàn thành chức năng; đánh giá security tập trung vào phát hiện lỗ hổng, secure generation hay exploit — nên không trả lời được khi nào một artifact vừa đúng chức năng, vừa an toàn, tái lập được và do agent có quyền hạn đáng kể tạo ra [Paper: PDF p. 1, Abstract] [Paper: PDF p. 2, Section 1].
- **Tại sao quan trọng** [Paper]: LLM chuyển từ code completion sang repository-scale agents có quyền sửa file, chạy công cụ, tham gia workflow nhạy cảm bảo mật [Paper: PDF p. 1, Abstract].
- **Tại sao cách tiếp cận cũ chưa đủ** [Paper]: Các survey trước mạnh ở từng mảng (Table 1) nhưng bỏ ngỏ câu hỏi liên miền về mức bằng chứng đủ [Paper: PDF p. 2, Section 1, Table 1].
- **Bốn RQ của bài** [Paper: PDF p. 3, Section 2.1]: RQ1 — task và artifact/context; RQ2 — prompting, fine-tuning, retrieval, agentic tool use thay đổi năng lực và failure mode ra sao; RQ3 — benchmark/metric nào là bằng chứng đáng tin và validity threat nào chặn so sánh chéo; RQ4 — SE và security giao nhau ở đâu, cần cơ chế đánh giá/quản trị gì cho agent tích hợp.
- **Câu hỏi gộp** [Analysis]: *Can* một khung đánh giá thống nhất (E, J@k, E1–E4, G0–G3, reporting protocol) làm cho các tuyên bố về LLM trong SE và security trở nên so sánh được và tương xứng với bằng chứng?

## 04 Bối cảnh nghiên cứu và lộ trình phát triển

> [Paper-framed; external verification not performed]

| Giai đoạn | Đại diện | Ưu điểm (theo bài) | Hạn chế (theo bài) | Pointer |
|---|---|---|---|---|
| Encoder-only (2020) | CodeBERT | Biểu diễn ngữ cảnh cho vulnerability detection, clone detection, code search | Không sinh mở | [Paper: PDF p. 4, Section 3.1] [Paper: PDF p. 5, Figure 2] |
| Encoder-decoder (2021) | CodeT5 | Summarization, translation, repair | — | [Paper: PDF p. 4, Section 3.1] |
| Decoder-only (2021–2024) | Codex, GPT-3.5/4, StarCoder, CodeLlama, DeepSeek-Coder | Sinh mở, tương tác qua tool | Nhãn kiến trúc không quyết định hiệu năng; dữ liệu, context length, adaptation, execution feedback quan trọng ngang bằng | [Paper: PDF p. 4, Section 3.1] [Paper: PDF p. 5, Figure 2] |
| Agentic SE (2024–2026) | SWE-bench-oriented agents, vibe coding, autonomous security agents | Retrieval, editing, tool execution, lặp | Harness dependence, chi phí, khó tái lập, bề mặt tấn công lớn hơn | [Paper: PDF p. 5, Figure 2] [Paper: PDF p. 18, Section 9] |
| Các survey trước | Hou et al., Xu et al., Zhou et al., Guo et al., Gao et al., Basic & Giaretta | Kiến thức sâu theo mảng | Không coi SE và security là hai trụ đồng đẳng + agentic + benchmark + giao | [Paper: PDF p. 2, Table 1] |

Vị trí tự nhận của bài: survey duy nhất trong Table 1 được đánh dấu "primary focus" (•) ở cả 5 cột SE, Security, Agentic, Benchmarks, Intersection [Paper: PDF p. 2, Table 1]. [Analysis] Đây là tự đánh giá của tác giả, bảng chỉ so với 6 survey chọn lọc, và không có tiêu chí mã hóa •/◦/– được công bố.

## 05 Các pain point cốt lõi bài nêu ra

| Pain point | Biểu hiện | Nguyên nhân / giải thích của tác giả | Bằng chứng trong bài |
|---|---|---|---|
| Nén hệ thống thành một con số | Leaderboard thay đổi khi đổi harness/môi trường | Workflow LLM là "compound intervention" (context, model, tools, validators, budget, human) | Lập luận khái niệm [Paper: PDF p. 5, Section 4, Equation 1] |
| Chức năng ≠ bảo mật | Execution feedback/repo access tăng task completion nhưng không chứng minh security; nhãn static analysis không chứng minh correctness | Validator lệch với threat model | Lập luận + trích dẫn SecRepoBench, RealSec-bench, SEC-bench [Paper: PDF p. 6, Section 4.1] |
| Test oracle yếu | Lời giải pass test suite hạn chế vẫn sai edge case | pass@k chỉ đo so với test có sẵn | Trích HumanEval+ [Paper: PDF p. 7, Section 5.1] [Paper: PDF p. 13, Section 7.4] |
| Dữ liệu trùng lặp, leakage theo thời gian | Random split thổi phồng hiệu năng; nhãn nhiễu | Near-duplicate, commit sửa lỗi chứa thay đổi không liên quan, negative sample quá "sạch" | Trích PrimeVul [Paper: PDF p. 16, Section 8.2] |
| Agent harness thay đổi | So sánh SWE-bench 1.96% → 78.4% không phải thí nghiệm dọc có kiểm soát | Biến thể benchmark, model version, scaffolding, tool access đều đổi | [Paper: PDF p. 7, Section 5.1, Table 3] |
| Proxy-only security check | Static analyzer bất đồng đáng kể với nhãn bảo mật thật theo từng mẫu | Analyzer là validator không hoàn hảo | Trích Firouzi & Ghafari [53] [Paper: PDF p. 13, Section 7.4] |
| Budget và can thiệp người không được báo cáo | best-of-k tăng nhưng chi phí, độ trễ, số ứng viên không an toàn bị loại cũng tăng | Tìm kiếm ẩn và lao động người bị tính là năng lực tự động | [Paper: PDF p. 13, Section 7.4] [Paper: PDF p. 16, Section 8.3] |
| Khoảng cách học thuật–công nghiệp | Học thuật tập trung task code-level kiểm tra tự động được | Benchmark công khai nhỏ không đại diện repo triệu dòng, dependency riêng, quy định | Trích Yu et al. [38] [Paper: PDF p. 17, Section 8.5] |

[Analysis] Các nguyên nhân trên là giải thích của tác giả kèm trích dẫn thứ cấp; bài không tự đo tần suất các vấn đề này trong tập tài liệu.

## 06 Ý tưởng cốt lõi

1. **Phương pháp bề mặt** [Paper]: Survey kể chuyện theo task + so sánh có cấu trúc, không gộp thống kê [Paper: PDF p. 3, Section 2.3].
2. **Insight cốt lõi** [Paper]: Đơn vị tổng hợp không phải bài báo mà là *claim* được hỗ trợ bởi một artifact, dataset, môi trường thực thi, metric và threat model cụ thể [Paper: PDF p. 3, Section 2.1]; do đó năng lực phải được đánh giá như assurance case với bằng chứng phù hợp task [Paper: PDF p. 1, Abstract].
3. **Bài học tổng quát** [Analysis]: Một kết quả đánh giá LLM chỉ có nghĩa khi gắn với (i) cấu hình đầy đủ sinh ra nó và (ii) phạm vi tuyên bố mà loại bằng chứng đó cho phép; nguyên lý này chuyển được sang mọi lĩnh vực có "agent + validator" (ví dụ: verification, data engineering).

## 07 Tổng quan phương pháp

Vì là review, "phương pháp" = quy trình tổng hợp tài liệu và xây khung khái niệm.

- **Input** [Paper]: Nguồn tìm qua backward chaining từ các survey gần đây + tìm kiếm có mục tiêu (tên task, chiến lược adaptation, model, benchmark) trên arXiv, ACM, IEEE; bốn concept block: language/code models; SE; software security; adaptation/agent mechanisms [Paper: PDF p. 3, Section 2.2].
- **Tiêu chí giữ** [Paper]: giới thiệu model/dataset/benchmark/method quan trọng; có bằng chứng thực nghiệm liên quan RQ; tổng hợp một tiểu lĩnh vực có ranh giới rõ; hoặc phơi bày validity threat [Paper: PDF p. 3, Section 2.2].
- **Tiêu chí loại** [Paper]: bài chỉ quan điểm, phiên bản trùng, thiếu chi tiết phương pháp, cybersecurity chung không có software artifact [Paper: PDF p. 3, Section 2.2].
- **Seed corpus** [Paper]: "sinh tự động từ citation keys trong file nguồn", dedupe theo DOI, arXiv ID, tiêu đề chuẩn hóa [Paper: PDF p. 3, Section 2.2].
- **Coding fields và quality rubric** [Paper]: publication status, task family, granularity, ngôn ngữ, model, adaptation, context, tools, benchmark, split, metric, kết quả chính, hạn chế, giao SE–security; rubric chấm 11 tiêu chí (RQ clarity, provenance, split validity, ... security validation). Phán quyết reviewer và screening agreement "cố ý để lại cho coding người thật" [Paper: PDF p. 3, Section 2.2].
- **Synthesis** [Paper]: narrative theo task + so sánh cấu trúc ở mức claim (function-level correctness, repository-level completion, vulnerability classification, secure generation, operational behavior); không pooling [Paper: PDF p. 3, Section 2.3].
- **Claim calibration** [Paper]: evidence levels E1–E4 [Paper: PDF p. 4, Section 2.4].
- **Output**: taxonomy (Figure 1), timeline (Figure 2), assurance framework (Equation 1, Equation 2, Table 2, G0–G3), bảng benchmark (Table 4), minimum reporting protocol (Table 5), ma trận adaptation (Table 6), cross-task synthesis (Table 7), research agenda (Table 8).
- **Giả định** [Analysis]: (a) tập trích dẫn của tác giả đủ đại diện; (b) phân loại task theo Figure 1 là trực giao đủ để so sánh; (c) các ký hiệu •/◦/– ở Table 1 và Table 6 phản ánh tài liệu chứ không chỉ phán đoán chuyên gia.

Luồng văn bản:

```text
Tìm kiếm (backward chaining + targeted search, cutoff 31/05/2026)
-> lọc theo tiêu chí giữ/loại -> seed corpus (từ citation keys, dedupe)
-> coding fields + quality rubric (chưa có coding người, chưa có agreement)
-> narrative synthesis theo task (Section 5, 6) + so sánh benchmark (Section 7)
-> calibrate claim theo E1–E4
-> xây assurance framework (E, J@k, ladder, G0–G3) và reporting protocol
-> cross-task synthesis (Table 7) trả lời RQ1–RQ4 -> research agenda (Table 8)
```

## 08 Phân rã module cốt lõi

Không có ablation thực nghiệm; cột cuối là **hiệu ứng dự kiến** [Analysis], không phải đo được.

| Module | Chức năng | Tại sao cần | Input và output | Bằng chứng hỗ trợ | Hiệu ứng dự kiến nếu bỏ |
|---|---|---|---|---|---|
| Unified taxonomy (Figure 1) | Xếp task SE (5), task security (4), adaptation strategies (4) thành cây | Tạo khung trả lời RQ1 và nối hai miền | Tài liệu → nhãn task/strategy | Định nghĩa khái niệm [Paper: PDF p. 5, Section 3.3, Figure 1] | Mất khung tổ chức Section 5–6; nhưng [Analysis] Figure 1 không thể hiện artifact granularity hay agent authority dù contribution (i) hứa hẹn [Paper: PDF p. 2, Section 1] |
| Evaluation configuration E (Equation 1) | Mô tả mọi kết quả bằng 7 thành phần A, C, M, T, V, B, H | Hai điểm chỉ so sánh được khi khác biệt thành phần được kiểm soát/phân tích | Một kết quả → bộ 7 thuộc tính | Lập luận + ví dụ SWE-bench [Paper: PDF p. 5, Section 4, Equation 1] [Paper: PDF p. 7, Table 3] | Không phân biệt được gain từ model hay từ harness/budget |
| J@k (Equation 2) | Tỉ lệ task có ít nhất một trong k ứng viên thỏa *cả* F và S | Trung bình F và S có thể che thất bại nghiêm trọng ở một chiều | k ứng viên/task + F_i, S_i → J@k | Chỉ định nghĩa; không tính trên dữ liệu nào [Paper: PDF p. 6, Section 4.1, Equation 2] | Quay lại báo cáo F, S rời; không bắt được failure shifting |
| Evidence ladder E1–E4 (Table 2) | Gắn thiết lập bằng chứng với claim mạnh nhất bảo vệ được | Tách "chạy tốt trên benchmark" với "đáng tin trong thực tế" | Thiết kế đánh giá → mức claim cho phép | Định nghĩa [Paper: PDF p. 4, Section 2.4] [Paper: PDF p. 6, Section 4.2, Table 2] | Mất cơ chế calibrate claim; [Analysis] bài không báo cáo phân bố E1–E4 của các nghiên cứu được khảo sát |
| Authority tiers G0–G3 | Phân bậc quyền: chỉ đọc → đề xuất patch → sửa/chạy trong sandbox → tác động repo chung/credential/deploy | Bằng chứng đủ cho G0 không đủ cho G3; kiểm soát tỉ lệ với tác động | Năng lực agent → yêu cầu kiểm soát | Định nghĩa [Paper: PDF p. 7, Section 4.3] [Paper: PDF p. 17, Section 8.4] | Mọi "agent" bị coi tương đương |
| Minimum reporting protocol (Table 5) | 8 chiều công bố bắt buộc (task, model, harness, budget/human, data/contamination, validation, uncertainty, reproducibility) | Cho phép reviewer xác định gain đến từ đâu | Một nghiên cứu → checklist công bố | Đề xuất chuẩn mực [Paper: PDF p. 13, Section 7.5] [Paper: PDF p. 14, Table 5] | Kết quả không tái lập/không quy được nguồn gain |
| Adaptation matrix (Table 6) | Đánh dấu strategy chính/phổ biến/hiếm cho 8 task | Trả lời RQ2 | Task → mức sử dụng strategy | Không nêu cơ sở đếm [Paper: PDF p. 14, Table 6] | Mất tóm tắt RQ2 (nhỏ) |
| Cross-task synthesis (Table 7) | Với 8 task family: artifact/context, adaptation, evidence điển hình, validity threat chính | Tổng hợp trả lời RQ1–RQ4 | Narrative → bảng | [Paper: PDF p. 15, Section 7.6, Table 7] | Mất phần tổng hợp chính |
| Research agenda (Table 8) | 6 hướng với câu hỏi kiểm chứng được + đánh giá tối thiểu | Biến gap thành câu hỏi falsifiable | Gap → RQ + thiết kế | [Paper: PDF p. 17-18, Section 8.7, Table 8] | Agenda chỉ còn khẩu hiệu |

## 09 Công thức và ký hiệu thiết yếu

**Equation 1 — evaluation configuration** [Paper: PDF p. 5, Section 4, Equation 1]

E = ⟨A, C, M, T, V, B, H⟩

- A: software artifact và task; C: context khả dụng; M: model và adaptation; T: tools và permissions; V: validators; B: inference và retry budget; H: human intervention.
- Mục đích: điều kiện so sánh — hai điểm chỉ so sánh trực tiếp được khi khác biệt giữa các thành phần được kiểm soát hoặc phân tích.
- Trực giác [Analysis]: một "điểm" là hàm của cả 7 biến, không chỉ của M.

**Equation 2 — joint functional and security success** [Paper: PDF p. 6, Section 4.1, Equation 2]

J@k = (1/N) Σ_{i=1..N} 𝕀[ ∃ y ∈ Y_i^(k) : F_i(y) ∧ S_i(y) ]

- N: số task; Y_i^(k): tập tối đa k ứng viên cho task i; F_i(y): y thỏa functional tests; S_i(y): y thỏa security check phù hợp threat model; 𝕀: hàm chỉ thị.
- Mục đích: thước đo giao chính; phải báo cáo kèm F và S riêng vì cùng một J@k có thể đến từ failure profile khác nhau. Với repair/agent, mở rộng phép hội với regression freedom, environment reproducibility, policy compliance [Paper: PDF p. 6, Section 4.1].
- Trực giác [Analysis]: tương tự pass@k nhưng điều kiện "pass" là phép AND của hai oracle; vì là "∃ trong k" nên J@k vẫn thừa hưởng vấn đề selection by repeated sampling mà bài nêu ở Section 7.4 nếu không cố định budget và không có cơ chế chọn ứng viên không cần oracle.

## 10 Thiết kế thực nghiệm và chuỗi bằng chứng

**Thiết lập**: Không có thí nghiệm gốc. "Dữ liệu" là 53 tài liệu tham khảo [Paper: PDF p. 19-23, References]; không báo cáo số bài được sàng lọc/giữ lại, không có PRISMA flow, không có inter-rater agreement [Paper: PDF p. 3, Section 2.2]. Không pooling [Paper: PDF p. 3, Section 2.3]. Các con số duy nhất là trích từ nguồn khác: SWE-bench 1.96% (Jimenez et al.) và 78.4% (Bhati et al., review thứ cấp) [Paper: PDF p. 7, Table 3]; HumanEval 164 bài Python, MBPP ~1,000 bài, MultiPL-E thêm 18 ngôn ngữ [Paper: PDF p. 11, Section 7.1]; SecurityEval 130 prompt Python phủ 75 CWE [Paper: PDF p. 12, Section 7.3]. Benchmarks liệt kê ở Table 4 [Paper: PDF p. 12, Table 4].

| Phân tích | Claim được kiểm | So sánh và điều kiện | Kết quả | Kết luận được hỗ trợ | Kết luận mạnh hơn không được hỗ trợ | Nguồn |
|---|---|---|---|---|---|---|
| So sánh survey (Table 1) | Bài lấp khoảng trống giao SE–security | 6 survey, 5 cột, tự chấm •/◦/– | Chỉ "This survey" có • ở cả 5 cột | Bài có phạm vi rộng hơn các survey được chọn | Bài là survey toàn diện nhất / duy nhất về giao | [Paper: PDF p. 2, Table 1] |
| Minh họa SWE-bench (Table 3) | Agent tiến bộ nhanh nhưng không so sánh trực tiếp được | 2 dòng, cấu hình khác nhau | 1.96% vs 78.4% resolved | Cấu hình E thay đổi làm điểm không so sánh được | Năng lực model tăng ~40 lần; 78.4% là kết quả đã kiểm chứng chính gốc (đến từ review thứ cấp, biến thể benchmark không nêu) | [Paper: PDF p. 7, Section 5.1, Table 3] |
| Danh mục benchmark (Table 4) + Section 7.3 | Benchmark đo năng lực khác nhau, không gộp được leaderboard | Mô tả định tính theo category | Benchmark mới (SecRepoBench, RealSec-bench, SEC-bench) ghép functional + security | Xu hướng chuyển sang đánh giá kết hợp | Các benchmark này đủ đại diện/đã giải quyết construct validity | [Paper: PDF p. 12, Table 4] [Paper: PDF p. 12-13, Section 7.3] |
| Ma trận adaptation (Table 6) | Strategy khác nhau phù hợp task khác nhau (RQ2) | 8 task × 4 strategy, ký hiệu định tính | Repo-level codegen: RAG và agent là chính; vuln detection: fine-tuning và RAG là chính | Mô tả phán đoán của tác giả | Phân bố sử dụng thực nghiệm (không có đếm) | [Paper: PDF p. 14, Table 6] |
| Cross-task synthesis (Table 7) | Ba pattern trả lời RQ1–RQ4 | 8 task family × 4 thuộc tính | (1) context mở rộng → adaptation dịch sang retrieval/agent; (2) validity phụ thuộc unit of deployment; (3) giao SE–security là tập ràng buộc, không phải task riêng | Khung diễn giải nhất quán với tài liệu trích | Các pattern đã được kiểm định định lượng | [Paper: PDF p. 15, Section 7.6, Table 7] |
| Metric gaps (Section 7.4) | Sáu khoảng trống đánh giá | Lập luận + trích dẫn | Test adequacy, saturation, leakage, security validity, agentic attribution, repeated sampling | Danh mục threat hợp lý, có nguồn | Mức độ phổ biến/tác động định lượng của mỗi threat | [Paper: PDF p. 13, Section 7.4] |
| Research agenda (Table 8) | Hướng tương lai kiểm chứng được | 6 hướng | Mỗi hướng có RQ falsifiable + minimum credible evaluation | Agenda có thể vận hành | Đây là các hướng ưu tiên nhất (không có xếp hạng bằng chứng) | [Paper: PDF p. 18, Table 8] |

## 11 Diễn giải đúng các kết luận

- **Phạm vi task**: Rộng (9 task SE+security + 4 strategy) nhưng chiều sâu mỗi task là vài đoạn [Paper: PDF p. 7-11, Section 5, Section 6].
- **Oracle / ground truth**: Bài không chạy oracle nào; các kết luận về oracle yếu là tổng hợp từ nguồn trích [Paper: PDF p. 13, Section 7.4].
- **End-to-end**: Không áp dụng (không có hệ thống). J@k, E1–E4, G0–G3 và Table 5 chưa được áp dụng thử lên bất kỳ nghiên cứu nào trong bài [Analysis].
- **Chi phí tính toán**: Not applicable; bài khuyến nghị báo cáo Pareto frontier quality–security–cost–latency [Paper: PDF p. 16, Section 8.3].
- **Phụ thuộc dữ liệu lịch sử / thời gian**: Temporal validity "đặc biệt mong manh"; cutoff 31/05/2026 [Paper: PDF p. 17, Section 8.6].
- **Phụ thuộc model**: Không áp dụng trực tiếp; bài nhấn mạnh kết quả là thuộc tính của toàn cấu hình E [Paper: PDF p. 9, Section 5.6].
- **Ca khó nhất**: Lifecycle maintainability, multilingual transfer, adversarial robustness, chi phí giám sát tổ chức — "under-evidenced" [Paper: PDF p. 18-19, Section 9].
- **Biên miền**: Thiên về Python, open-source, preprint tiếng Anh [Paper: PDF p. 17, Section 8.6].
- **Bất định**: Không có định lượng bất định vì không pooling [Paper: PDF p. 3, Section 2.3].

**Phát biểu kết quả có giới hạn** [Analysis]: Dựa trên tập tài liệu chọn lọc phi hệ thống (53 tham khảo) đến 31/05/2026, bài *lập luận* — không chứng minh bằng thực nghiệm hay meta-analysis — rằng execution feedback và repository access cải thiện task completion nhưng không tự thiết lập security, và đề xuất một bộ công cụ khái niệm (E, J@k, E1–E4, G0–G3, Table 5) mà giá trị thực tiễn còn chờ được kiểm chứng khi áp dụng.

## 12 Hạn chế được tác giả thừa nhận rõ ràng

| Hạn chế | Biểu hiện cụ thể | Hướng tương lai tác giả đề xuất | Nguồn |
|---|---|---|---|
| Selection validity | Structured narrative review từ seed corpus truy vết được, không phải tìm kiếm toàn diện + dual-reviewer screening; có thể thiếu công trình liên quan; bài tiếng Anh và preprint nổi bật có thể bị đại diện quá mức | Protocol và template giúp kiểm toán; một bản cập nhật toàn diện trong tương lai còn phải sàng lọc | [Paper: PDF p. 17, Section 8.6] [Paper: PDF p. 4, Section 2.3] |
| Không claim recall toàn diện | "does not claim exhaustive recall"; "We do not claim exhaustive coverage" | — | [Paper: PDF p. 3, Section 2.1] [Paper: PDF p. 2, Section 1] |
| Chưa có coding/agreement của người | Reviewer judgments và screening agreement để lại cho coding người thật | Coding bởi người | [Paper: PDF p. 3, Section 2.2] |
| Construct validity | Thuật ngữ correctness, agent, autonomy, vulnerability detection, secure generation dùng không nhất quán trong tài liệu | Taxonomy và assurance framework giảm nhưng không loại bỏ được | [Paper: PDF p. 17, Section 8.6] |
| Conclusion validity | Task và cấu hình dị biệt nên không pooling điểm | — | [Paper: PDF p. 17, Section 8.6] |
| External validity | Chi phối bởi ít ngôn ngữ, repo open-source, dataset curated, cửa sổ đánh giá ngắn | Continuous và multilingual evaluation (Table 8) | [Paper: PDF p. 17, Section 8.6] [Paper: PDF p. 18, Table 8] |
| Temporal validity | Model, API, scaffold, leaderboard đổi nhanh | Cutoff date và phiên bản benchmark phải đi kèm khi tái sử dụng kết luận | [Paper: PDF p. 17, Section 8.6] |

## 13 Phân tích phê phán

| `[Analysis]` Quan sát | Vấn đề tiềm ẩn hoặc giải thích thay thế | Tại sao quan trọng | Cách kiểm chứng | Cơ sở |
|---|---|---|---|---|
| Seed corpus "sinh tự động từ citation keys trong file nguồn" | Tính vòng: corpus = danh mục tham khảo của chính bài, nên "traceable" không đồng nghĩa với "đại diện"; tiêu chí giữ/loại không được áp dụng có thể kiểm chứng | Kết luận RQ1–RQ4 có thể phản ánh lựa chọn trích dẫn hơn là tài liệu | Chạy lại search string trên arXiv/ACM/IEEE, đo recall của 53 tham khảo so với tập thu được | [Paper: PDF p. 3, Section 2.2] [Paper: PDF p. 19-23, References] |
| Source package được mô tả nhưng không có URL/identifier | Không thể kiểm toán protocol, rubric, search log mà bài dựa vào để tự nhận "auditable" | Tự mâu thuẫn với chiều Reproducibility trong Table 5 (archival identifier) | Kiểm tra phiên bản arXiv sau hoặc liên hệ tác giả | [Paper: PDF p. 3-4, Section 2.3] [Paper: PDF p. 14, Table 5] |
| Quality rubric 11 tiêu chí được định nghĩa nhưng không có điểm nào được báo cáo | Evidence ladder E1–E4 không được dùng để phân loại tài liệu khảo sát | Không biết bao nhiêu % bằng chứng hiện có đạt E3/E4 — đây chính là "evidence-centered" claim | Mã hóa 53 nguồn (hoặc các nghiên cứu sơ cấp) theo E1–E4 với 2 coder, báo cáo phân bố và kappa | [Paper: PDF p. 3, Section 2.2] [Paper: PDF p. 6, Table 2] |
| Table 1 và Table 6 dùng •/◦/– không có quy tắc mã hóa | Phán đoán chuyên gia đơn lẻ trình bày như tổng hợp | Table 6 trả lời RQ2; ví dụ Vulnerability Detection "Agent-based: –" trong khi Section 6.3 nói về autonomous security agents | Công bố tiêu chí (ví dụ ngưỡng số bài), cho coder độc lập chấm lại | [Paper: PDF p. 2, Table 1] [Paper: PDF p. 14, Table 6] [Paper: PDF p. 10, Section 6.3] |
| Contribution (i) nói taxonomy nối task với artifact granularity, context, adaptation và agent authority | Figure 1 chỉ có task và adaptation; granularity/context nằm ở Table 7, authority ở Section 4.3 | Taxonomy kém trực giao: "Testing & Fuzzing" (SE) và "Security Testing" (security) chồng lấn | Xây taxonomy đa trục (task × granularity × authority) và kiểm tra mỗi nghiên cứu rơi vào đúng một ô | [Paper: PDF p. 2, Section 1] [Paper: PDF p. 5, Figure 1] |
| Table 3 chỉ có 2 dòng; 78.4% lấy từ review thứ cấp [20] | Không nêu biến thể SWE-bench (Full/Lite/Verified) hay system cụ thể | Số liệu nổi bật nhất bài không truy được về nguồn sơ cấp | Truy xuất nguồn sơ cấp của 78.4% và ghi rõ biến thể, cấu hình E | [Paper: PDF p. 7, Table 3] [Paper: PDF p. 20, References] |
| J@k được đề xuất nhưng không được tính thử | Chưa biết J@k có phân biệt hệ thống tốt hơn F@k, S@k riêng hay chỉ tương quan cao với F@k | Giá trị thực tiễn của chỉ số trung tâm chưa được chứng minh | Tính F@k, S@k, J@k trên SecRepoBench/RealSec-bench cho nhiều model; đo rank correlation và trường hợp đảo hạng | [Paper: PDF p. 6, Equation 2] [Paper: PDF p. 12, Section 7.3] |
| J@k dùng ∃ trong k ứng viên | Giả định có oracle chọn ứng viên thỏa F∧S lúc triển khai, mâu thuẫn với chính cảnh báo "selection by repeated sampling" | J@k có thể thổi phồng năng lực triển khai thực tế | So sánh J@k với "J@1 sau bộ chọn không oracle" (ví dụ chọn theo test sinh tự động) | [Paper: PDF p. 6, Section 4.1] [Paper: PDF p. 13, Section 7.4] |
| Section 2.4 roadmap liệt kê Section 3, 5–9 nhưng bỏ Section 4 (framework chính) | Lỗi trình bày nhỏ | Không ảnh hưởng kết luận | — | [Paper: PDF p. 4, Section 2.4] |

## 14 Kiến thức thu được

**Agent-derived knowledge candidates**

- **Khái niệm**: "Unit of synthesis là claim, không phải paper" — mỗi kết quả gắn với artifact, dataset, môi trường, metric, threat model [Paper: PDF p. 3, Section 2.1].
- **Khung**: Evaluation configuration E = ⟨A, C, M, T, V, B, H⟩ như checklist để đọc bất kỳ bài LLM-for-code nào [Paper: PDF p. 5, Equation 1].
- **Metric**: J@k và nguyên tắc "báo cáo F, S, J riêng; mở rộng phép hội với regression freedom, reproducibility, policy compliance" [Paper: PDF p. 6, Section 4.1].
- **Calibrate claim**: E1 feasibility → E2 comparative → E3 system-level trên project mẫu → E4 operational [Paper: PDF p. 6, Table 2].
- **Governance**: G0–G3 với kiểm soát tương ứng (least-privilege, network/secret isolation, approval gate, rollback) [Paper: PDF p. 7, Section 4.3].
- **Thiết kế đánh giá**: Table 5 làm checklist khi viết phần thực nghiệm của chính mình [Paper: PDF p. 14, Table 5]; benchmark nên được quản trị như "versioned scientific instrument" với stable core + sequestered set + refresh track [Paper: PDF p. 16, Section 8.2].
- **Vulnerability datasets**: Điểm giữa Big-Vul, Devign, ReVeal, DiverseVul, PrimeVul không hoán đổi được do khác labeling, balance, dedupe, temporal split [Paper: PDF p. 10, Section 6.1].
- **Đo can thiệp người**: số lần can thiệp, thời gian chủ động, review burden, loại sửa, quyết định accept/rollback [Paper: PDF p. 9, Section 5.6].

## 15 Liên hệ với tri thức hiện có

Context mode: paper-only — không có liên hệ nào dưới đây được kiểm chứng bên ngoài.

- **Tương đồng** [Analysis, unverified]: Evidence ladder E1–E4 có cấu trúc giống thang mức bằng chứng trong y học thực chứng và khái niệm "assurance case" trong kỹ thuật an toàn hệ thống; bài không trích các nguồn này nên mối liên hệ chỉ là candidate.
- **Kết hợp** [Analysis, unverified]: Table 5 có thể ghép với các chuẩn báo cáo thực nghiệm trong SE (empirical standards) để thành checklist cho reviewer; cần tra cứu bên ngoài.
- **Mâu thuẫn tiềm năng** [Analysis]: J@k (∃ trong k) vs khuyến nghị cố định budget và cảnh giác best-of-k của chính bài [Paper: PDF p. 13, Section 7.4] [Paper: PDF p. 18, Table 8].
- **Miền chuyển giao** [Analysis, Agent-derived candidate]: Phân tích chương trình truyền thống (static analysis, symbolic execution, fuzzing) như validator V trong E; khung G0–G3 áp dụng cho agent DevOps/infra-as-code.
- Liên hệ với tri thức của người dùng: Not assessable (người dùng chưa cung cấp).

## 16 Ý tưởng nghiên cứu

**Agent-derived research candidates** — đều là candidate idea; prior-art search required.

### Candidate 1 — Kiểm định thực nghiệm J@k: có thêm thông tin so với F@k và S@k không?

- **Hạn chế khởi nguồn**: J@k chỉ được định nghĩa, chưa được tính trên dữ liệu nào; bài nói cùng một J@k có thể đến từ failure profile khác nhau [Paper: PDF p. 6, Section 4.1, Equation 2]; agenda hỏi "intervention improve J@k rather than shifting failures" [Paper: PDF p. 18, Table 8].
- **Giả thuyết cốt lõi** [Hypothesis]: Trên benchmark repository-level kết hợp (SecRepoBench, RealSec-bench), thứ hạng hệ thống theo J@k khác đáng kể so với thứ hạng theo F@k (Kendall τ < 0.7), và một tỉ lệ đáng kể "cải thiện F@k" thực chất là failure shifting sang S.
- **Delta so với bài**: evaluation — từ định nghĩa khái niệm sang đo thực nghiệm; thêm biến thể J@1 với bộ chọn không oracle.
- **Phương pháp ban đầu**: Chạy ≥6 model/agent với k ∈ {1, 5, 10}, budget cố định; tính F@k, S@k, J@k và J@1-selected (chọn bằng test sinh tự động + static analyzer).
- **Validation (how to test)**: So sánh rank correlation F@k vs J@k; đếm cặp hệ thống đảo hạng; kiểm soát model size, budget, harness. Kết quả kỳ vọng: τ thấp và có đảo hạng. **Falsifier**: τ ≥ 0.9 và không đảo hạng → J@k dư thừa so với F@k.
- **Possible failure modes**: (1) Security oracle (PoV tests) quá thưa khiến S gần như hằng → J≈F; (2) benchmark nhỏ, khoảng tin cậy rộng, không đủ power phát hiện đảo hạng; (3) contamination làm F cao giả tạo.
- **Innovation status**: unverified (prior-art search required — các benchmark trích [21, 23] có thể đã báo cáo joint outcome).

### Candidate 2 — Phân bố bằng chứng E1–E4 và G0–G3 trong tài liệu LLM4SE/LLM4Security

- **Hạn chế khởi nguồn**: Bài định nghĩa evidence ladder và authority tiers nhưng không phân loại tài liệu khảo sát theo chúng; quality rubric chưa được chấm; screening agreement chưa có [Paper: PDF p. 3, Section 2.2] [Paper: PDF p. 6, Table 2] [Paper: PDF p. 17, Section 8.6].
- **Giả thuyết cốt lõi** [Hypothesis]: Trong các nghiên cứu sơ cấp 2023–2026 về agent sửa lỗi/vá lỗ hổng, < 10% đạt E3 với security check phù hợp threat model, và < 5% đạt E4; các nghiên cứu ở G2–G3 không báo cáo nhiều hơn các chiều Table 5 so với G0–G1.
- **Delta so với bài**: data + evaluation — áp dụng chính khung của bài như công cụ đo lên một tập SLR có protocol, dual coding.
- **Phương pháp ban đầu**: SLR theo PRISMA với search string tái lập; 2 coder độc lập chấm E-level, G-tier, 8 chiều Table 5; báo cáo Cohen's kappa.
- **Validation (how to test)**: Kappa ≥ 0.6 cho E-level và G-tier là điều kiện để khung "vận hành được"; so sánh tỉ lệ đạt từng chiều Table 5 theo G-tier (chi-square). **Falsifier**: kappa < 0.4 (khung không đủ rõ để mã hóa) hoặc tỉ lệ E3+ cao (> 30%), bác bỏ nhận định bằng chứng còn yếu.
- **Possible failure modes**: (1) Ranh giới E2/E3 mơ hồ với benchmark "repository-level" nhưng không có môi trường thực thi đầy đủ → kappa thấp; (2) publication bias: nghiên cứu công nghiệp E4 ít công bố → đánh giá thấp bằng chứng thực tế; (3) chi phí coding lớn khi số bài vượt vài trăm.
- **Innovation status**: unverified (prior-art search required).
