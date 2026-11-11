# Paper Card — Sense and Sensitivity: Examining the Influence of Semantic Recall on Long Context Code Understanding

> Phạm vi nguồn (Source coverage): Full paper — toàn văn 19 trang PDF (arXiv 2505.13353v5), gồm phần chính, phụ lục A–G, mọi hình/bảng
> Độ tin cậy trích xuất (Extraction confidence): High (PyMuPDF, validation = valid; các trang hình đã kiểm tra trực quan)
> Locator mode: page-grounded — mọi con trỏ dùng chỉ số trang file PDF (`PDF p. N`); bài không có nhãn trang in riêng ngoài số chân trang trùng với chỉ số PDF
> Primary analytical lens: discovery (phát hiện thực nghiệm: sự phân ly lexical recall vs semantic recall theo vị trí)
> Secondary analytical lens: resource (task/benchmark SemTrace và thước đo semantic recall sensitivity)
> Context verification: Paper-only — không thực hiện kiểm chứng ngoài
> Card completeness: Complete relative to supplied source

**Tóm tắt trạng thái bằng chứng.** Toàn bộ số liệu chính (Table 1, Table 2, các mức giảm 53.36% / 92.73% / 44.15% / 59.74%, 71,994 hàm không hoàn chỉnh, GPT-4.1 4-digit/6-digit) đã đối chiếu với nguồn. Phần lớn kết quả chỉ được trình bày dưới dạng đồ thị (không có bảng số theo vị trí), không có kiểm định thống kê giữa các điều kiện; khoảng tin cậy chỉ có ở Figure 1 và Figure 3. Cách tổng hợp con số "median 92.73%" không được định nghĩa tường minh (xem Section 11, 13).

**Terminology Ledger (khóa thuật ngữ cho toàn card).**

| Canonical term | Định nghĩa lần đầu | Biến thể trong nguồn | Quyết định |
|---|---|---|---|
| lexical recall (R^L) | khả năng tái tạo nguyên văn đoạn code trong context | "Lexical Code Recall", "function retrieval" (tên task đo) | dùng "lexical recall"; "function-level retrieval" chỉ tên task |
| semantic recall (R^S) | khả năng hiểu code làm gì khi chạy (operational semantics) | "Semantic Code Recall" | dùng "semantic recall" |
| semantic recall sensitivity (Sens^T(C)) | mức độ một task đòi hỏi semantic recall thay vì pattern matching shortcuts | "sensitivity" | dùng nguyên dạng |
| pattern matching shortcuts | dùng mẫu thuật toán/tương quan I/O đã ghi nhớ từ pretraining | "pattern matching" | dùng nguyên dạng |
| SemTrace (-JS, -PHP) | task output prediction với các phép gán ngẫu nhiên | — | dùng nguyên dạng |
| CRUXEval-I / CRUXEval-O | input / output prediction trên CRUXEval | CRUXEval-JS, CRUXEval-PHP (từ CRUXEval-X) | dùng nguyên dạng |
| distractors | hàm không liên quan lấy từ CodeSearchNet | "distractor functions" | dùng "distractors" |
| relative accuracy Δ | % thay đổi so với accuracy cực đại của chính model ở cùng độ dài context | "relative accuracy", "median accuracy drop" | dùng "relative accuracy Δ" |
| partial match accuracy | % phần tử list dự đoán đúng | — | dùng nguyên dạng |
| unresolved outputs | đầu ra dạng biểu thức chưa tính (vd. `81 - 43`) | "resolution errors" | dùng "unresolved outputs" |

## 01 Thông tin cơ bản

| Trường | Nội dung |
|---|---|
| Tiêu đề | Sense and Sensitivity: Examining the Influence of Semantic Recall on Long Context Code Understanding [Paper: PDF p. 1, Title] |
| Tác giả, đơn vị | Adam Štorek, Mukur Gupta, Samira Hajizadeh, Prashast Srivastava, Suman Jana — Columbia University [Paper: PDF p. 1, Title block] |
| Venue | Không nêu trong PDF; bản arXiv 2505.13353v5 [cs.CL], ngày 10 Jul 2026 [Paper: PDF p. 1, arXiv stamp]. Phần Acknowledgments cảm ơn "anonymous reviewers" nhưng không nêu hội nghị [Paper: PDF p. 10, Acknowledgments] |
| Năm | 2025 (v1) – 2026 (v5) theo định danh arXiv |
| Loại bài | Nghiên cứu thực nghiệm (discovery) + đề xuất task đánh giá (resource) |
| Lĩnh vực | LLM cho code, long-context evaluation, program understanding |
| Từ khóa | lexical recall, semantic recall, semantic recall sensitivity, lost-in-the-middle, CRUXEval, SemTrace, counterfactual measurement |
| Mã nguồn | https://github.com/adamstorek/long-context-code-understanding [Paper: PDF p. 1, footnote 1] |
| Dữ liệu | CRUXEval (MIT), CodeSearchNet (MIT), CRUXEval-X (JS/PHP), SemTrace sinh tự động [Paper: PDF p. 18, Table 4] |
| Ngày đọc | 2026-11-06 |
| Vị trí trong hướng nghiên cứu của người dùng | Not assessable — người dùng chưa cung cấp hướng nghiên cứu cụ thể (thư mục dự án gợi ý chủ đề phân tích chương trình) |

## 02 Tóm tắt một câu

Bằng cách đặt một hàm mục tiêu ở 11 vị trí trong context gồm 20–80 distractors (~4k–16k token) và so sánh function-level retrieval với input/output prediction trên 10 LLM, bài báo báo cáo rằng lexical recall gần như không phụ thuộc vị trí trong khi semantic recall suy giảm theo vị trí — vừa phải trên CRUXEval (median relative accuracy Δ 53.36%) nhưng nặng trên SemTrace (92.73%) — và quy khác biệt này cho semantic recall sensitivity thấp của CRUXEval, được ước lượng bằng cách xóa dần dòng code [Paper: PDF p. 1, Abstract] [Paper: PDF p. 7, Figure 2].

## 03 Câu hỏi nghiên cứu

- **Vấn đề cụ thể:** Khi LLM giải task hiểu code trong long context, chúng có thực sự xử lý operational semantics của đoạn code cụ thể, hay dùng pattern matching shortcuts từ pretraining? [Paper: PDF p. 1, Introduction]
- **Tại sao quan trọng:** Trong môi trường production, code là đặc thù dự án, không có shortcut; khác biệt giữa code đúng và code có lỗ hổng có thể chỉ ở một dòng [Paper: PDF p. 3, Section 3.1].
- **Tại sao cách tiếp cận hiện có chưa đủ:** NIAH chỉ đo lexical recall; các benchmark code long-context chủ yếu đo code retrieval; benchmark output prediction như CRUXEval có thể giải bằng shortcut, che giấu lỗi semantic recall [Paper: PDF p. 2, Related Work 2.1] [Paper: PDF p. 3, Section 3].
- **Câu hỏi nghiên cứu (dạng Can … ?):** Liệu lexical recall và semantic recall có phân ly theo vị trí đoạn code trong long context hay không, và liệu mức độ suy giảm quan sát được có bị đánh giá thấp bởi các benchmark có semantic recall sensitivity thấp?

## 04 Bối cảnh nghiên cứu và lộ trình phát triển

[Paper-framed; external verification not performed]

| Giai đoạn / hướng | Đại diện (theo bài) | Ưu điểm | Hạn chế (theo bài) | Vị trí bài này tự nhận |
|---|---|---|---|---|
| Needle-in-a-haystack, long-context benchmark | NIAH, LongBench, ∞Bench, RULER | đo truy xuất ở quy mô dài | chủ yếu đo lexical recall/retrieval | thêm chiều semantic recall trên cùng đoạn code |
| Long-context cho code | LongCoder, RepoQA-like retrieval, code QA | sát thực tế repository | tập trung code retrieval, không phải operational semantics | đo cả retrieval và understanding trên code giống hệt |
| Positional bias / lost-in-the-middle | Liu et al. 2024b, Gao et al. 2024 | mô tả hiện tượng ở ngôn ngữ tự nhiên | chưa xét code semantics | tác giả tuyên bố là "đầu tiên" xét ảnh hưởng vị trí lên code understanding — claim chưa được kiểm chứng |
| Chống memorization | 1-indexed Python, LeetCode biến đổi, MATH-perturb | thay đổi lời giải để tránh ghi nhớ | — | cách bổ sung: xóa thông tin (counterfactual) thay vì biến đổi |

Nguồn: [Paper: PDF p. 2, Related Work 2.1–2.2] [Paper: PDF p. 3, Related Work 2.3]. Không tuyên bố "first" nào ở đây được xác minh độc lập.

## 05 Các điểm đau cốt lõi được bài báo chỉ ra

| Điểm đau | Biểu hiện | Nguyên nhân / giải thích của tác giả | Bằng chứng trong bài |
|---|---|---|---|
| Đồng nhất retrieval với understanding | NIAH đạt gần hoàn hảo nhưng không cho biết model có hiểu code | hai năng lực khác nhau, quan hệ chưa được hiểu | Figure 2a vs 2b/2c [Paper: PDF p. 7, Figure 2] |
| Benchmark cho phép shortcut | CRUXEval vẫn đúng khi code đã bị xóa 50% dòng | model dùng mẫu thuật toán phổ biến (sort, string, arithmetic) | Figure 3; giảm chỉ 44.15% (I) / 59.74% (O) [Paper: PDF p. 7, Figure 3] |
| Đánh giá thấp lỗi theo vị trí | CRUXEval chỉ cho thấy suy giảm vừa phải | shortcut bù đắp cho semantic recall suy giảm (giả thuyết của tác giả) | so sánh Figure 2b vs 2c [Paper: PDF p. 8, Section 5.2] |
| Ngay cả task "khó shortcut" cũng bị ghi nhớ | GPT-4.1 đạt 100% SemTrace, không phụ thuộc vị trí | ghi nhớ phép cộng/trừ 2 chữ số (giả thuyết của tác giả, kiểm bằng Figure 4) | [Paper: PDF p. 8, Figure 4] |

## 06 Ý tưởng cốt lõi

1. **Phương pháp bề mặt:** Đặt hàm mục tiêu ở vị trí có kiểm soát giữa các distractors; đo đồng thời function-level retrieval (lexical recall) và input/output prediction (semantic recall) trên cùng hàm; đo semantic recall sensitivity bằng xóa dòng; xây SemTrace với phép gán ngẫu nhiên [Paper: PDF p. 5, Experimental Setup].
2. **Insight cốt lõi:** Vị trí trong context được dùng như một nhiễu loạn có kiểm soát (diagnostic lens) chứ không phải mục tiêu: nếu hai năng lực có chung cơ chế thì chúng phải phản ứng giống nhau với vị trí; và mức suy giảm quan sát được phụ thuộc vào việc task có cho phép shortcut hay không [Paper: PDF p. 1–2, Introduction].
3. **Bài học tổng quát:** [Analysis] Độ khó/độ nhạy của một benchmark phải được đo như một thuộc tính riêng (ví dụ bằng counterfactual ablation đầu vào) trước khi diễn giải độ bền của model; một benchmark có shortcut sẽ "làm phẳng" các đường cong suy giảm và che giấu cơ chế thất bại.

## 07 Tổng quan phương pháp

- **Đầu vào:** prompt query-aware (query đặt trước và sau code) chứa hàm mục tiêu + 20/40/60/80 distractors từ CodeSearchNet (lọc 25th–75th percentile độ dài, ~200 token/hàm) [Paper: PDF p. 5–6, Experimental Design; Prompting].
- **Đầu ra:** (a) thân hàm nguyên văn (retrieval), (b) input hoặc output dự đoán, chấm exact match zero-shot, greedy decoding [Paper: PDF p. 5, Tasks].
- **Biến điều khiển:** vị trí hàm mục tiêu (11 vị trí cách đều), độ dài context (4 mức), task, model (10), ngôn ngữ (Python, JS, PHP).
- **Không có huấn luyện;** chỉ inference: vLLM 0.7.1 trên 8×H200, GPT-4.1 qua OpenAI API; 47 GPU-days + ~2 ngày API [Paper: PDF p. 18, Appendix G].
- **Giả định:** distractors không liên quan về ngữ nghĩa nên không gây nhiễu ngữ nghĩa; phép cộng/trừ 2 chữ số đủ dễ để không gây nhiễu reasoning [Paper: PDF p. 5, Section 3.3].

Luồng:

```text
CRUXEval (800 hàm) / SemTrace (800 hàm sinh) / CRUXEval-X JS,PHP
  -> chèn hàm mục tiêu tại 1 trong 11 vị trí giữa N distractors (N ∈ {20,40,60,80})
  -> prompt query-aware (Figure 12/13/14)
  -> LLM (10 model; GPT-4.1 dùng 1/8 dữ liệu)
  -> exact match accuracy
  -> relative accuracy Δ so với max của model ở cùng độ dài context (Figure 2, 5–11)
Song song: CRUXEval không distractor -> xóa mọi tổ hợp dòng (71,994 hàm) -> accuracy theo % dòng bị xóa
  -> so với Python interpreter (Figure 1) -> suy ra semantic recall sensitivity (Equation 1, Figure 3)
```

## 08 Phân rã các module cốt lõi

| Module | Chức năng | Tại sao cần | Đầu vào và đầu ra | Bằng chứng hỗ trợ | Hiệu ứng đã biết / dự kiến khi bỏ |
|---|---|---|---|---|---|
| Function-level retrieval với khóa hex 6 chữ số mỗi dòng | đo lexical recall | tách năng lực truy cập code khỏi hiểu code; khóa tránh model dựa vào tên hàm | khóa start/end → thân hàm nguyên văn | Figure 2a: frontier >95% mọi vị trí [Paper: PDF p. 6, Section 5.1] [Paper: PDF p. 19, Figure 14] | Dự kiến (không đo): không có khóa, retrieval khó định danh hơn; lexical recall có thể kém ổn định hơn → so sánh lexical/semantic không còn cân bằng cue |
| CRUXEval-I/O trong long context | đo semantic recall trên benchmark phổ biến | baseline của cộng đồng | hàm + assertion → input/output | Figure 2b, Figure 6: giảm 16.25–84.29% so với max [Paper: PDF p. 6, Section 5.1] | — (là điều kiện đối chứng) |
| Counterfactual line removal + Equation 1 | ước lượng semantic recall sensitivity | xác định task có cho phép shortcut hay không | CRUXEval gốc → 71,994 phiên bản thiếu dòng → accuracy theo % xóa | Figure 1 (interpreter) vs Figure 3 (LLM) [Paper: PDF p. 8, Section 5.2] | Không có module này thì không phân biệt được "task dễ" với "task cho shortcut" |
| SemTrace | task có sensitivity cao theo thiết kế | loại shortcut: mỗi dòng gán `arr[i] = x ± y`, y ∈ [-100, 99], k ∈ [4,10], thứ tự ngẫu nhiên; xác suất đoán đúng ≤ 6.25×10⁻¹⁰ | x → list kết quả | Listing 1, Table 1, Figure 2c [Paper: PDF p. 4, Listing 1] [Paper: PDF p. 5, Section 3.3] | Đo được gián tiếp: CRUXEval (task thay thế) cho suy giảm nhẹ hơn nhiều (53.36% vs 92.73%) |
| Biến thể digit của SemTrace (2–6 chữ số) | kiểm tra giả thuyết GPT-4.1 ghi nhớ số học | giải thích ngoại lệ GPT-4.1 | 80 distractors → relative accuracy Δ | Figure 4: 4 chữ số giảm tới 31 điểm %, 6 chữ số tới 43% tương đối [Paper: PDF p. 9, Section 5.3] | — |
| Partial match & unresolved outputs | chẩn đoán dạng lỗi | phân biệt suy giảm dần vs sụp đổ hoàn toàn; lỗi né tính toán | list dự đoán → % phần tử đúng; đếm biểu thức chưa tính | Figure 8, Figure 9 [Paper: PDF p. 14, Appendix C] | — |
| Mở rộng JS/PHP | kiểm tra tính tổng quát ngôn ngữ | loại trừ artefact riêng Python | CRUXEval-X + SemTrace dịch | Figure 10, Figure 11 [Paper: PDF p. 14, Appendix D] | — |

Lưu ý: bài không có ablation theo nghĩa bỏ module; cột cuối là hiệu ứng dự kiến trừ khi ghi "đo được".

## 09 Công thức và ký hiệu thiết yếu

**Equation 1 — semantic recall sensitivity** [Paper: PDF p. 4, Equation 1]

```text
Sens^T(C) = (1 / |Inc(C)|) · Σ_{C_inc ∈ Inc(C)} [ R^T(C) − R^T(C_inc) ] / [ R^T(C) + ε ]
```

- `T`: task (vd. output prediction); `C`: đoạn code gốc; `Inc(C)`: tập phiên bản thiếu dòng của C; `R^T(·)`: hiệu năng của model trên task T; `ε > 0`: ổn định số.
- **Mục đích:** đo mức suy giảm chuẩn hóa trung bình khi thông tin bị xóa; Sens cao → task phụ thuộc vào chi tiết cụ thể của C.
- **Trực giác:** tương đương diện tích dưới đường cong suy giảm khi xóa dần thông tin; tham chiếu là Python interpreter (giảm 76 điểm % khi xóa chỉ 1 dòng, gần 0 khi xóa >20%) [Paper: PDF p. 4, Figure 1].
- **Lưu ý:** ước lượng phụ thuộc model, được tổng hợp qua các model để ra mức benchmark [Paper: PDF p. 4, Section 3.2]. [Analysis] Bài không báo cáo giá trị số Sens cho từng benchmark; bằng chứng trình bày dưới dạng đường cong (Figure 3), và không có giá trị Sens của SemTrace đo bằng cùng thủ tục.

**Relative accuracy Δ** (định nghĩa bằng lời): % thay đổi so với accuracy cực đại của từng model tại cùng độ dài context [Paper: PDF p. 5, Tasks].

## 10 Thiết kế thực nghiệm và chuỗi bằng chứng

**Thiết lập.**
- Dữ liệu: CRUXEval 800 hàm Python (I và O); SemTrace 800 hàm sinh; CRUXEval-JS/PHP từ CRUXEval-X + SemTrace-JS/PHP; distractors từ CodeSearchNet-Python/JS/PHP [Paper: PDF p. 5, Tasks] [Paper: PDF p. 6, Experimental Setup].
- Model: 6 frontier (GPT-4.1, DeepSeek Coder V2 Instruct, Gemma 3 27B It, Llama 3.3 70B Instruct, Qwen 2.5 Coder 32B Instruct, Codestral 22B v0.1) + 4 nhỏ (Gemma 3 12B, Llama 3.1 8B, Qwen 2.5 Coder 7B, DeepSeek Coder V2 Lite) [Paper: PDF p. 5, Models]; giấy phép ở Table 3 và Table 4 [Paper: PDF p. 18, Table 3].
- Metric: exact match zero-shot; relative accuracy Δ; partial match accuracy; số unresolved outputs.
- Ngân sách: GPT-4.1 chỉ dùng 1/8 mỗi dataset (lấy mẫu ngẫu nhiên) [Paper: PDF p. 5, Models]; 47 GPU-days [Paper: PDF p. 18, Appendix G].
- Prompt templates: Figure 12 (input prediction), Figure 13 (output prediction, cấm biểu thức chưa rút gọn), Figure 14 (retrieval); dùng assistant prefill [Paper: PDF p. 18–19, Appendix F].
- Bất định: CI 95% bootstrap chỉ cho Figure 1 và Figure 3; không có error bar ở các đồ thị vị trí.

| Thí nghiệm | Claim được kiểm | So sánh và điều kiện | Kết quả | Kết luận được hỗ trợ | Kết luận mạnh hơn KHÔNG được hỗ trợ | Nguồn |
|---|---|---|---|---|---|---|
| Baseline không distractor | SemTrace không khó hơn về bản chất | 6 frontier, CRUXEval-I/O vs SemTrace | Median SemTrace 86.19% vs CRUXEval-I 45.06%, -O 55.38%; nhưng Gemma 3 27B 12.25%, Codestral 23.25% trên SemTrace | Với đa số frontier model, SemTrace ngắn dễ hơn CRUXEval | "SemTrace không khó hơn" cho mọi model — sai với Gemma 3 27B, Codestral | [Paper: PDF p. 6, Table 1] |
| Baseline model nhỏ | Mẫu hình giữ ở model nhỏ | 4 model nhỏ | SemTrace 4.12–22.25%, thấp hơn CRUXEval | Model nhỏ yếu hơn rõ trên SemTrace | Relative Δ của model nhỏ có ý nghĩa ổn định (baseline rất thấp → nhiễu lớn) | [Paper: PDF p. 12, Table 2] |
| Lexical recall theo vị trí | Lexical recall không phụ thuộc vị trí | function retrieval, 11 vị trí × 4 độ dài | Frontier >95% mọi vị trí; median giảm 2.39% | Truy xuất nguyên văn có cue khóa hex là ổn định đến ~16k token | Model "truy cập được" mọi code theo nghĩa rộng (cue ở task semantic khác) | [Paper: PDF p. 7, Figure 2] [Paper: PDF p. 2, Introduction] |
| Semantic recall CRUXEval | Semantic recall phụ thuộc vị trí | CRUXEval-O/I trong context dài | giảm 16.25–84.29% so với max; nặng nhất ở 60–80%; median 53.36% | Có hiệu ứng lost-in-the-middle cho output/input prediction | Cơ chế nhân quả của suy giảm | [Paper: PDF p. 6, Section 5.1] [Paper: PDF p. 13, Figure 6] |
| Semantic recall SemTrace | Suy giảm nặng hơn khi bỏ shortcut | SemTrace cùng giao thức | median tới 92.73%; Qwen 2.5 Coder 32B mất 91.38% (53 điểm %) ở 80 distractors vs 23.31% trên CRUXEval-O; Codestral, Gemma 3 27B về 0 | Suy giảm theo vị trí nghiêm trọng hơn hẳn trên SemTrace | Khác biệt chỉ do sensitivity (còn có exact match trên 4–10 phần tử, xem Section 13) | [Paper: PDF p. 6, Section 5.1] [Paper: PDF p. 7, Figure 2] |
| Counterfactual line removal | CRUXEval có sensitivity thấp | 71,994 hàm thiếu dòng; LLM vs Python interpreter | Xóa 50% dòng: chỉ giảm 44.15% (I), 59.74% (O); interpreter giảm 76 điểm % khi xóa 1 dòng | Model vẫn trả lời đúng khi code bị khuyết đáng kể → có dùng tri thức ngoài code | Toàn bộ thành công trên CRUXEval là shortcut; interpreter là tham chiếu "đúng" cho hiểu code (interpreter lỗi vì cú pháp/runtime) | [Paper: PDF p. 7, Figure 3] [Paper: PDF p. 4, Figure 1] [Paper: PDF p. 8, Section 5.2] |
| Loại trừ OOD | SemTrace không phải OOD | so sánh baseline ngắn và dạng đường cong | Đa số frontier tốt hơn trên SemTrace ngắn; các model có baseline khác nhau cho cùng dạng suy giảm | Lập luận chống OOD hợp lý ở mức định tính | Bằng chứng định lượng loại trừ OOD | [Paper: PDF p. 8, Section 5.1] |
| GPT-4.1 theo số chữ số | GPT-4.1 ghi nhớ số học 2 chữ số | SemTrace 2–6 chữ số, 80 distractors | 2–3 chữ số ổn định; 4 chữ số giảm tới 31 điểm %; 6 chữ số tới 43% tương đối, đường chữ U | Khi tăng chữ số, GPT-4.1 cũng phụ thuộc vị trí | "Ghi nhớ số học" là cơ chế duy nhất (khó số học cũng tăng đồng thời) | [Paper: PDF p. 8, Figure 4] [Paper: PDF p. 9, Section 5.3] |
| Model nhỏ | Phân ly tổng quát theo quy mô | 4 model nhỏ | Lexical recall dao động hơn (DeepSeek Coder V2 Lite giảm giữa context; Lite và Llama 3.1 8B giảm ở đầu); semantic recall suy giảm vừa (CRUXEval) và nặng (SemTrace) | Mẫu định tính giữ ở model nhỏ | Lexical recall "ổn định" ở model nhỏ | [Paper: PDF p. 13, Figure 5] [Paper: PDF p. 14, Figure 7] [Paper: PDF p. 12, Appendix A] |
| Partial match SemTrace | Suy giảm là dần dần, không sụp đổ | % phần tử đúng | Cùng xu hướng vị trí nhưng mượt hơn exact match | Lỗi thường là nhớ sai một số dòng gán | — | [Paper: PDF p. 15, Figure 8] |
| Unresolved outputs | Model né tính toán bằng lexical recall | đếm biểu thức như `81 − 43` | Gemma và Llama tạo nhiều hơn khi hàm ở giữa context | Mẫu tương quan với vị trí | "Cố tình" né semantic recall (giải thích của tác giả, chưa kiểm) | [Paper: PDF p. 15, Figure 9] [Paper: PDF p. 14, Appendix C] |
| JS / PHP | Phân ly không đặc thù Python | 4 model, CRUXEval-JS/PHP, SemTrace-JS/PHP | median giảm 34.72% (CRUXEval-JS), 14.35% (CRUXEval-PHP), 80.39% (SemTrace-JS), 76.12% (SemTrace-PHP); nhiều model baseline ≈0 trên SemTrace-PHP (vẽ ở −100% theo quy ước) | Mẫu định tính lặp lại ở 3 ngôn ngữ | So sánh định lượng SemTrace-PHP (relative Δ không xác định khi baseline = 0) | [Paper: PDF p. 6, Section 5.1] [Paper: PDF p. 16, Figure 10] [Paper: PDF p. 17, Figure 11] |

## 11 Diễn giải đúng các kết luận

- **Phạm vi task:** chỉ input/output prediction và function retrieval; không có code generation, debugging, multi-hop [Paper: PDF p. 9, Limitations].
- **Oracle / cue:** retrieval được cho khóa hex start/end của từng dòng — một cue định vị mà các task semantic không có [Paper: PDF p. 5, Tasks]. [Analysis] Vì vậy "lexical vs semantic" đồng thời là "có cue định vị vs không có".
- **End-to-end:** không — hàm mục tiêu được nêu bằng assertion; model không phải tự tìm code liên quan trong repository thật.
- **Độ dài context:** ~4k–16k token, xa dưới giới hạn context của model hiện đại [Paper: PDF p. 10, Limitations].
- **Distractors:** không liên quan ngữ nghĩa; real codebase có hàm liên quan [Paper: PDF p. 9, Limitations].
- **Phụ thuộc model:** GPT-4.1 là ngoại lệ trên SemTrace 2 chữ số; GPT-4.1 chỉ dùng 1/8 dữ liệu (~100 ví dụ mỗi task) nên đường cong của nó nhiễu hơn [Paper: PDF p. 5, Models].
- **Số liệu tổng hợp:** "median accuracy drop 92.73%" (Abstract) được chú thích ở Figure 2 là "plummeting up to 92.73%"; [Analysis] cách lấy median (qua model? vị trí? độ dài?) không được định nghĩa, nên con số nên đọc là thống kê mô tả trên đồ thị, không phải ước lượng có khoảng tin cậy [Paper: PDF p. 1, Abstract] [Paper: PDF p. 7, Figure 2].
- **Bất định:** không có kiểm định thống kê cho chênh lệch CRUXEval vs SemTrace.
- **Ca khó nhất:** SemTrace-PHP — nhiều model gần 0 ở mọi vị trí, relative Δ không xác định [Paper: PDF p. 17, Figure 11].

**Phát biểu lại có giới hạn:** Trên 10 LLM, với context 4k–16k token gồm distractors không liên quan và cue khóa hex cho retrieval, function retrieval gần như không phụ thuộc vị trí, còn exact-match output/input prediction giảm khi hàm nằm ở giữa context — giảm vừa trên CRUXEval và giảm mạnh trên SemTrace; thí nghiệm xóa dòng cho thấy model vẫn trả lời đúng CRUXEval khi code thiếu đáng kể, phù hợp (nhưng chưa chứng minh nhân quả) với giả thuyết rằng shortcut che giấu suy giảm semantic recall.

## 12 Hạn chế được tác giả thừa nhận rõ ràng

| Hạn chế | Biểu hiện cụ thể | Hướng tương lai tác giả đề xuất | Nguồn |
|---|---|---|---|
| Thiết kế distractor code | distractors ngẫu nhiên, không liên quan ngữ nghĩa; codebase thật có hàm liên quan có thể gây nhiễu | quan hệ giữa độ tương đồng ngữ nghĩa của code xung quanh và lỗi semantic recall là câu hỏi mở (dự đoán sẽ tệ hơn) | [Paper: PDF p. 9, Limitations] |
| Phạm vi task | chỉ input-output prediction và retrieval | mức áp dụng cho code generation, debugging, multi-hop reasoning cần nghiên cứu thêm | [Paper: PDF p. 9, Limitations] |
| Ràng buộc thiết kế SemTrace | số học đơn giản có thể không phản ánh code thuật toán phức tạp; GPT-4.1 ghi nhớ phép toán cho thấy khó thiết kế task chặn mọi shortcut | không nêu cụ thể | [Paper: PDF p. 9–10, Limitations] |
| Dải độ dài context | chỉ tới ~16k token | xem xu hướng ở độ dài cực lớn là future work | [Paper: PDF p. 10, Limitations] |
| Quy mô benchmark | 800 ví dụ mỗi task | đánh giá lớn hơn để thấy hiệu ứng tinh tế, phân tích failure mode chi tiết | [Paper: PDF p. 10, Limitations] |

**Ràng buộc liên quan được tác giả ghi nhận (không được trình bày như hạn chế chính thức):** GPT-4.1 chỉ chạy trên 1/8 dữ liệu vì chi phí [Paper: PDF p. 5, Models]; tổng chi phí thực tế có thể cao 1.5–2 lần so với lượt đánh giá cuối [Paper: PDF p. 18, Appendix G].

## 13 Phân tích phản biện

| `[Analysis]` Quan sát | Vấn đề tiềm ẩn hoặc giải thích thay thế | Tại sao quan trọng | Cách kiểm tra | Cơ sở |
|---|---|---|---|---|
| Retrieval có khóa hex ở mỗi dòng, task semantic thì không | Phân ly có thể do khác biệt cue định vị chứ không do "loại recall" | Lõi claim "lexical vs semantic dissociate" bị nhiễu bởi điều kiện cue | Chạy retrieval không khóa (theo tên/mô tả hàm) và task semantic có khóa; hoặc retrieve-then-trace (Section 16) | [Paper: PDF p. 5, Tasks] [Paper: PDF p. 19, Figure 14] |
| SemTrace chấm exact match trên 4–10 phần tử | Nếu xác suất nhớ đúng mỗi dòng giảm nhẹ theo vị trí, lỗi tích lũy theo k làm exact match giảm mạnh — khuếch đại so với CRUXEval | Chênh 92.73% vs 53.36% có thể một phần do metric, không chỉ do sensitivity | So sánh theo k; phân tích per-line accuracy; so CRUXEval với số dòng tương đương | Figure 8 cho thấy partial match mượt hơn [Paper: PDF p. 15, Figure 8] |
| Tham chiếu Python interpreter cho sensitivity | Interpreter thất bại vì lỗi cú pháp/runtime khi xóa dòng; LLM có thể "sửa" code hợp lý hoặc dòng bị xóa không ảnh hưởng output với input đã cho | Độ dốc của interpreter không phải chuẩn "hiểu code"; Sens có thể đo khả năng sửa lỗi thay vì shortcut | Chỉ xóa dòng ảnh hưởng output (dựa trên dataflow/slicing); dùng LLM trên hàm mới hoàn toàn để làm baseline | [Paper: PDF p. 4, Figure 1] [Paper: PDF p. 8, Section 5.2] |
| Không báo cáo Sens của SemTrace bằng cùng thủ tục | "SemTrace high sensitivity" được lập luận từ thiết kế, không đo bằng Equation 1 | Thiếu so sánh cùng thước đo giữa hai benchmark | Áp dụng line removal cho SemTrace và báo cáo Sens cho cả hai | [Paper: PDF p. 5, Section 3.3] |
| Relative Δ so với max theo vị trí | Với baseline thấp (Gemma 3 27B 12.25%, model nhỏ 4–22%) relative Δ cực nhạy với nhiễu; với retrieval gần trần 100% thì Δ bị nén tự nhiên | So sánh độ "ổn định" giữa task có mức trần khác nhau có thể bị thiên lệch | Báo cáo accuracy tuyệt đối + CI bootstrap theo vị trí; mô hình hồi quy có hiệu ứng vị trí × task | [Paper: PDF p. 6, Table 1] [Paper: PDF p. 12, Table 2] |
| Giải thích ngoại lệ GPT-4.1 bằng ghi nhớ số học | Tăng chữ số cũng tăng độ khó tính toán và số token, không chỉ loại bỏ ghi nhớ | Claim "memorization" chưa phân biệt với "khó hơn" | Đối chứng: cùng phép tính 4–6 chữ số ở vị trí đầu/cuối và không distractor; số học ngoài phân phối nhưng độ dài 2 chữ số (vd. cơ số khác) | [Paper: PDF p. 8, Figure 4] |
| Unresolved outputs tăng ở giữa context | Có thể do model mất ý tuân thủ chỉ dẫn (instruction following) ở context dài, không phải chiến lược né semantic recall | Diễn giải "cố gắng né" là giả thuyết | Đo tuân thủ chỉ dẫn với task trung tính cùng vị trí | [Paper: PDF p. 15, Figure 9] |
| Không có kiểm định thống kê, GPT-4.1 1/8 dữ liệu | Một số khác biệt vị trí có thể nằm trong nhiễu | Ảnh hưởng độ tin cậy của các đường cong riêng lẻ | Bootstrap CI theo vị trí; chạy đủ dữ liệu cho GPT-4.1 | [Paper: PDF p. 5, Models] |

## 14 Kiến thức thu được

**Agent-derived knowledge candidates**

- **Khái niệm:** tách *lexical recall* (truy xuất nguyên văn) khỏi *semantic recall* (operational semantics) như hai năng lực đo được trên cùng đoạn code [Paper: PDF p. 3, Section 3].
- **Thuộc tính benchmark:** *semantic recall sensitivity* — một benchmark tốt cho "hiểu code" phải có hiệu năng sụp mạnh khi code bị khuyết; đo bằng Equation 1 [Paper: PDF p. 4, Equation 1].
- **Thiết kế thí nghiệm:** dùng vị trí trong context như nhiễu loạn có kiểm soát để chẩn đoán cơ chế, thay vì mục tiêu đo; chèn mục tiêu ở 11 vị trí × 4 độ dài [Paper: PDF p. 5, Experimental Design].
- **Kỹ thuật dựng task chống shortcut:** phép gán ngẫu nhiên, độc lập, độ khó đồng đều để cho phép partial credit theo từng dòng (SemTrace) [Paper: PDF p. 5, Section 3.3].
- **Bài học đánh giá:** ngay cả task chống shortcut cũng có thể bị "chuyển" thành lexical recall bởi ghi nhớ (GPT-4.1, số học 2 chữ số) — cần kiểm tra bằng thang độ khó [Paper: PDF p. 9, Section 5.3].
- **Mẹo prompt:** query-aware contextualization (đặt query trước và sau code) cho decoder-only model [Paper: PDF p. 6, Prompting].

## 15 Liên hệ với tri thức hiện có

Context mode: paper-only — các liên hệ dưới đây là ứng viên, chưa kiểm chứng ngoài.

- **Tương đồng (paper-framed):** hiệu ứng lost-in-the-middle ở ngôn ngữ tự nhiên (Liu et al. 2024b) được bài mở rộng sang code semantics [Paper: PDF p. 2, Related Work 2.2].
- **Kết hợp (paper-framed):** bài nêu nghiên cứu thuế (Jurayj et al. 2026) cho thấy định vị luật và áp dụng luật cũng phân ly; hiệu năng tốt hơn khi trích luật vào symbolic solver — gợi ý kiến trúc "retrieve → execute bằng công cụ" [Paper: PDF p. 9, Broader Implications].
- **Ứng viên liên hệ — phân tích chương trình [Hypothesis]:** program slicing / dataflow analysis có thể dùng để chọn dòng bị xóa có ảnh hưởng thật tới output, làm phép đo sensitivity chặt hơn (chưa kiểm chứng ngoài).
- **Ứng viên liên hệ — phát hiện lỗ hổng [Paper-framed]:** Ding et al. 2025 (theo bài) cho thấy model khó phân biệt code đúng vs có lỗ hổng khi khác biệt tinh tế — phù hợp với lo ngại về shortcut [Paper: PDF p. 3, Section 3.1].
- **Miền chuyển giao:** tài liệu luật/chính sách, quy trình nhiều bước trong văn bản dài [Paper: PDF p. 9, Broader Implications].

## 16 Ý tưởng nghiên cứu

**Agent-derived research candidates** (hypotheses; prior-art search required)

### Ứng viên 1 — Distractors liên quan ngữ nghĩa có kiểm soát độ tương đồng

- **Nguồn gốc (hạn chế / quan sát):** Tác giả thừa nhận distractors ngẫu nhiên, không liên quan; quan hệ giữa độ tương đồng ngữ nghĩa và lỗi semantic recall là câu hỏi mở [Paper: PDF p. 9, Limitations].
- **Giả thuyết cốt lõi:** Khi độ tương đồng ngữ nghĩa/cú pháp giữa distractors và hàm mục tiêu tăng, semantic recall (SemTrace exact match) giảm mạnh hơn lexical recall; cụ thể, các "near-miss" distractor (cùng cấu trúc SemTrace, khác hằng số y) làm tăng lỗi lẫn dòng (output khớp với distractor) hơn là lỗi ngẫu nhiên.
- **Delta so với bài (data + evaluation):** thay CodeSearchNet ngẫu nhiên bằng distractors chia theo bin tương đồng (embedding cosine, hoặc SemTrace "anh em" khác hằng số); thêm metric "distractor-attributed error" (dự đoán trùng với output của distractor).
- **Phương pháp ban đầu:** 4 bin tương đồng × 11 vị trí × 2 độ dài (40, 80 distractors); 6 frontier model của bài; giữ nguyên prompt Figure 13/14.
- **Validation (cách kiểm chứng):** so sánh relative accuracy Δ và tỉ lệ distractor-attributed error giữa các bin; kiểm định hồi quy logistic accuracy ~ vị trí × bin × task. Kỳ vọng: hệ số tương tác bin × task (semantic) âm và có ý nghĩa; **kết quả bác bỏ:** đường cong vị trí không đổi giữa các bin hoặc lexical recall suy giảm tương đương semantic recall.
- **Possible failure modes (chế độ thất bại có thể):** (1) độ tương đồng embedding không phản ánh tương đồng operational semantics → nhiễu biến độc lập; (2) near-miss distractors làm retrieval cũng thất bại (khóa hex vẫn có thể giúp, nhưng không có khóa thì lẫn) → không còn phân ly; (3) chi phí: 4× số lượt inference của bài (~47 GPU-days gốc).
- **Innovation status:** unverified — prior-art search required.

### Ứng viên 2 — Retrieve-then-trace: thí nghiệm phân biệt "cue định vị" vs "loại recall"

- **Nguồn gốc (quan sát):** Retrieval dùng khóa hex mỗi dòng và gần như không phụ thuộc vị trí [Paper: PDF p. 7, Figure 2], trong khi SemTrace sụp ở giữa context [Paper: PDF p. 6, Section 5.1]; unresolved outputs gợi ý model có thể "copy" được phép tính nhưng không tính [Paper: PDF p. 15, Figure 9].
- **Giả thuyết cốt lõi:** Nếu suy giảm theo vị trí của SemTrace chủ yếu do khó *định vị và gom* các dòng liên quan trong context (không phải do không thể *áp dụng* semantics), thì buộc model trước tiên tái tạo nguyên văn hàm mục tiêu (lexical recall, có hoặc không có khóa hex) rồi mới dự đoán output sẽ làm phần lớn suy giảm theo vị trí biến mất. Ngược lại, nếu suy giảm vẫn còn dù bản sao chép đúng, semantic recall thật sự phụ thuộc vị trí của *biểu diễn gốc*.
- **Delta so với bài (mechanism + evaluation):** thêm điều kiện can thiệp 2 bước (copy → trace) và điều kiện bỏ khóa hex cho retrieval, tạo thiết kế 2×2 (cue có/không × copy-first có/không).
- **Phương pháp ban đầu:** SemTrace và CRUXEval-O, 80 distractors, 11 vị trí; chỉ tính các ví dụ mà bước copy đúng nguyên văn để tách lỗi recall khỏi lỗi trace.
- **Validation (cách kiểm chứng):** metric: exact match và partial match theo vị trí, có CI bootstrap; so sánh độ sâu "đáy chữ U" giữa 4 ô. Kỳ vọng nếu giả thuyết đúng: copy-first làm relative Δ trên SemTrace giảm từ mức ~90% xuống gần mức của lexical recall; **kết quả bác bỏ:** với bản copy đúng, SemTrace vẫn giảm mạnh ở vị trí giữa.
- **Possible failure modes (chế độ thất bại có thể):** (1) bản copy nằm ở cuối context nên mọi cải thiện có thể chỉ là hiệu ứng recency, không phân biệt được cơ chế — cần đối chứng chèn bản copy do người cung cấp; (2) bước copy thất bại nhiều khi bỏ khóa hex làm mẫu sau lọc bị thiên lệch (selection bias); (3) model có thể trace ngay trong lúc copy, làm nhòe ranh giới hai bước.
- **Innovation status:** unverified — prior-art search required.
