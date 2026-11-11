# Paper Card — Retrieval Or Holistic Understanding? Dolce: Differentiate Our Long Context Evaluation Tasks

> Phạm vi nguồn (Source coverage): Full paper — PDF 44 trang (arXiv 2409.06338v1). Đã đọc đầy đủ thân bài (PDF pp. 1–9), Appendix A (phần đầu), B.2–B.3, C (Algorithm 1), D–I, K, L; đọc lướt Appendix J (bảng tham số chi tiết của QuALITY/LongFQA, PDF pp. 28–33) và phần dẫn xuất tổ hợp chi tiết (PDF pp. 16–18). Algorithm 2 (PDF p. 21) chỉ đọc tiêu đề.
> Độ tin cậy trích xuất (Extraction confidence): Mixed — văn bản thân bài và phụ lục trích xuất tốt (PyMuPDF, validation = valid_with_warnings, cảnh báo duy nhất: "document title is unavailable" trong metadata); công thức tổ hợp bị vỡ ký hiệu khi trích xuất; Figure 2 đã kiểm tra trực quan, các hình còn lại chỉ đọc qua caption và lời văn.
> Locator mode: page-grounded — mọi con trỏ dùng chỉ số trang file PDF (`PDF p. N`); số chân trang in trùng chỉ số PDF.
> Primary analytical lens: methods (khung DOLCE: lấy mẫu span ngắn + mixture model + MLE để ước lượng λ, k và gán category)
> Secondary analytical lens: resource (kết quả phân loại 44 task của ba benchmark suite — một "bản đồ" benchmark, dù không công bố dữ liệu/mã)
> Context verification: Paper-only — không thực hiện kiểm chứng ngoài; liên hệ với bài 2505.13353 dựa trên card nội bộ của dự án (cards/2505.13353v5/paper-card.md) do người dùng cung cấp bối cảnh.
> Card completeness: Complete relative to supplied source (với các phần phụ lục đọc lướt đã nêu ở trên)

**Tóm tắt trạng thái bằng chứng.** Các con số chính (44 task; 0–67% COW / 0–29% PIG thuộc Category III; tỷ lệ Category V; 29 task chạy Dip Test → 4/10/15; median δ, ρ giữa Gemini 1.5 Flash và PaLM 2-S; take-every-5 ρ(λ)=0.93) đã đối chiếu với nguồn. Phát hiện hai chỗ không nhất quán nội bộ: (i) cận dưới tỷ lệ Category V trong PIG là "0%" ở Abstract/Introduction nhưng "8%" ở Section 5 [Paper: PDF p. 1, Abstract] [Paper: PDF p. 2, Introduction] [Paper: PDF p. 7, Section 5]; (ii) khoảng ρ(λ) cho COW ở Section 6/K.2 ("0.54–0.80") khớp với cột δ(λ) chứ không phải cột ρ(λ) của Table 8 (0.55–0.82) [Paper: PDF p. 9, Section 6] [Paper: PDF p. 39, Table 8]. Kết quả phân loại chủ yếu trình bày dưới dạng biểu đồ thanh (Figure 2, 9, 10) không kèm bảng số theo task; không có xác minh bằng nhãn người (tác giả tự nêu) [Paper: PDF p. 44, Appendix L].

**Terminology Ledger (khóa thuật ngữ cho toàn card).**

| Canonical term | Định nghĩa lần đầu | Biến thể trong nguồn | Quyết định |
|---|---|---|---|
| DOLCE | Differentiate Our Long Context Evaluation Tasks — khung tự động phân loại problem | "Dolce" (tiêu đề), "Distinguish Our Long Context Evaluation Tasks" (tiêu đề Section 3) | dùng "DOLCE"; ghi nhận biến thể tên ở Section 3 [Paper: PDF p. 3, Section 3] |
| problem / task / benchmark suite | một input; nhóm problem cùng use case; nhóm task | — | dùng nguyên dạng [Paper: PDF p. 1, footnote 1] |
| retrieval vs holistic understanding | tìm một/vài "needle" vs phần lớn context có liên quan, thứ tự có thể quan trọng | — | dùng nguyên dạng |
| λ (complexity) | độ dài span tối thiểu đủ để trả lời (COW) / số aspect (PIG), tính theo unit | "necessary context length", "complexity degree" | dùng "λ (complexity)" |
| k (redundancy) | số lần lặp của ground-truth span/aspect | — | dùng "k (redundancy)" |
| unit | đơn vị chia context (câu, dòng, block…) | "granularity" | dùng "unit"; "unit granularity" khi nói lựa chọn |
| observation span (độ dài C) | span liên tiếp được lấy mẫu từ context đưa cho probing model | "observation", "sampled short context" | dùng "observation span" |
| COW / PIG | correct-or-wrong / partial-point-in-grading scenario | — | dùng viết tắt |
| background noise component (N) / oracle component (O) | hai thành phần của mixture model | "noise", "hybrid oracle component" | dùng nguyên dạng |
| probing model | LLM dùng để quan sát outcome (Gemini 1.5 Flash, PaLM 2-S) | — | dùng nguyên dạng |
| Category I–V | CBZS, Easy, Retrieval, Balanced, Holistic Understanding | "focus category" | dùng "Category I–V" kèm tên |
| CBZS | closed-book or zero-shot (λ = 0) | — | dùng viết tắt |
| IDK (∅) | outcome "không đủ thông tin" khi được hướng dẫn | "Unanswerable", "E" | dùng "IDK" |
| semantic recall sensitivity | (từ bài 2505.13353, không có trong bài này) | — | chỉ dùng ở Section 13–16, gắn nhãn [User]/[Analysis] |

## 01 Thông tin cơ bản

| Trường | Nội dung |
|---|---|
| Tiêu đề | Retrieval Or Holistic Understanding? Dolce: Differentiate Our Long Context Evaluation Tasks [Paper: PDF p. 1, Title] |
| Tác giả, đơn vị | Zi Yang — Google DeepMind (một tác giả) [Paper: PDF p. 1, Title block] |
| Venue | arXiv Preprint (header mọi trang); không nêu hội nghị [Paper: PDF p. 1, Header] |
| Năm | 2024 (arXiv:2409.06338v1 [cs.CL], 10 Sep 2024) [Paper: PDF p. 1, arXiv stamp] |
| Loại bài | methods (khung ước lượng/phân loại) + resource phụ (phân loại 44 task) |
| Lĩnh vực | Long-context evaluation cho LLM, benchmark analysis |
| Từ khóa | long context, retrieval, holistic understanding, λ complexity, k redundancy, mixture model, EM, COW/PIG, Hartigans' Dip Test |
| Mã nguồn / dữ liệu | Không thấy liên kết mã hoặc dữ liệu được công bố trong thân bài/phụ lục đã đọc. Tác giả có nhắc "We have developed tools" để phân tích độ dài unit nhưng không công bố [Paper: PDF p. 22, Appendix F] |
| Ngày đọc | 2026-11-06 |
| Vị trí trong hướng nghiên cứu của người dùng | [User] Người dùng tìm khoảng trống quanh "Sense and Sensitivity" (2505.13353). [Analysis] DOLCE là một phương pháp counterfactual ở mức input (giữ lại một cửa sổ liên tiếp, bỏ phần còn lại) để đo "cần bao nhiêu context" — ứng viên gần nhất để định lượng hóa độ nhạy của task code với thông tin trong context. |

## 02 Tóm tắt một câu

Để phân biệt problem thiên về retrieval với problem thiên về holistic understanding trong các benchmark long-context, bài báo đề xuất DOLCE: lấy mẫu các observation span ngắn từ context, quan sát outcome của một probing model, rồi dùng mixture model (background noise + hybrid oracle) với MLE/EM để ước lượng cho từng problem cặp tham số λ (complexity) và k (redundancy) và gán vào 5 category; áp dụng lên 44 task của L-Eval, BAMBOO, LongBench, bài báo báo cáo 0–67% problem COW và 0–29% problem PIG thuộc Category III (retrieval), còn Category V (holistic) chiếm tới 89% (COW) và 90% (PIG) tùy task [Paper: PDF p. 1, Abstract] [Paper: PDF p. 7, Section 5].

## 03 Câu hỏi nghiên cứu

- **Vấn đề cụ thể:** Các benchmark long-context gộp chung problem có bản chất khác nhau; nhãn focus category thường không có, và suy từ tên task (đuôi -QA, -Ret) hoặc kiểm tra thủ công là không tin cậy và tốn công [Paper: PDF p. 1, Introduction].
- **Tại sao quan trọng:** Theo tác giả, phân biệt này liên quan tới thiết kế kiến trúc: divide-and-conquer (blockwise parallel attention, parallel decoding) có thể không hại retrieval nhưng nghi ngờ với holistic understanding; recurrent model được cho là hợp với holistic; RAG cho trường hợp cân bằng [Paper: PDF p. 1, Introduction].
- **Tại sao cách cũ chưa đủ:** Các benchmark trước không tách độ dài input L khỏi độ dài context cần thiết λ (trừ trường hợp synthetic); các phân loại mới (full-text comprehension, short/long dependency, scope câu/đoạn/global, spotlight→chain of reasoning) đều gán thủ công; LC-Boost tìm "minimal necessary context" nhưng không có k, phụ thuộc retriever và không báo cáo độ dài [Paper: PDF p. 3, Related Work]. Cách đơn giản "retrieve span rồi đếm" phụ thuộc retriever và khó bắt các span cần cho suy luận [Paper: PDF p. 2, Introduction].
- **Câu hỏi dạng Can … ?:** Liệu có thể ước lượng tự động, từ outcome của một probing model không hoàn hảo trên các span ngắn được lấy mẫu, độ dài span tối thiểu đủ (λ) và độ lặp (k) của từng problem, để phân loại problem thành retrieval hay holistic understanding?

## 04 Bối cảnh nghiên cứu và lộ trình phát triển

[Paper-framed; external verification not performed]

| Giai đoạn | Đại diện (theo bài) | Ưu điểm | Hạn chế (theo bài) | Vị trí bài tự nhận |
|---|---|---|---|---|
| Benchmark suite long-context | LRA, ZeroSCROLLS, L-Eval, LongBench, BAMBOO, LooGLE, Loong, LV-Eval, ∞Bench, Ruler, LOFT… | nhiều domain, độ dài, mức synthetic | quan sát suy giảm theo độ dài nhưng không tách L với λ [Paper: PDF p. 2, Related Work] [Paper: PDF p. 3, Related Work] | — |
| Benchmark theo use case | Needle-In-A-Haystack, SummHay, NovelQA, FLenQA, NoCha, RepoQA… | kiểm soát được loại khó | như trên | — |
| Phân loại độ khó thủ công | Ada-LEval, LooGLE, NoCha, Loong | có taxonomy | thủ công, tốn, không tin cậy; tác giả cho rằng độ khó nên là phổ liên tục [Paper: PDF p. 3, Related Work] | — |
| Tìm minimal context tự động | LC-Boost (Qian et al.) | tự động | không có k; phụ thuộc retriever/LLM; không báo cáo độ dài | DOLCE định nghĩa và ước lượng cả λ, k |
| Hai chiều độ khó (position paper) | Goldman et al. 2024: scope và diffusion | khái niệm hai chiều | không ước lượng định lượng | tác giả tự nhận "first to study the problem of automatic categorization of long context tasks" [Paper: PDF p. 3, Related Work] — claim chưa kiểm chứng |

## 05 Các điểm đau cốt lõi được bài báo chỉ ra

| Pain point | Biểu hiện | Nguyên nhân / giải thích của tác giả | Bằng chứng trong bài |
|---|---|---|---|
| Thiếu nhãn focus category | Không biết task đo retrieval hay holistic | nhãn không có; suy từ tên không tin cậy | lập luận [Paper: PDF p. 1, Introduction]; ví dụ cùng task khác suite cho phân bố khác nhau [Paper: PDF p. 41, Table 9] |
| Probing model không hoàn hảo | Đoán may, trả lời từ trí nhớ, mắc lỗi khi context ngắn | background noise: đoán 1/4 với 4 lựa chọn; memorization context lúc huấn luyện | Table 1 ví dụ P(x=1)>0 từ C=1 nhưng vẫn có P(x=0)>0 tới C=10 [Paper: PDF p. 4, Table 1] |
| Lỗi "đúng kiểu oracle" | Hỏi "topic đầu tiên" nhưng chỉ thấy topic thứ hai → trả lời topic đó | oracle cũng sai khi C < λ, khác với nhiễu ngẫu nhiên | ví dụ TopicRet [Paper: PDF p. 4, Section 3.2] [Paper: PDF p. 5, Section 3.2] |
| Metric liên tục mơ hồ | F-1/ROUGE vừa có thể là fuzzy match nhị phân vừa là điểm từng phần | hai kịch bản COW/PIG cùng tồn tại trong một task | Dip Test: 4 task COW-only, 10 PIG-only, 15 hỗn hợp [Paper: PDF p. 6, Section 4] [Paper: PDF p. 26, Table 5] |
| "Lost in the middle" khi đưa full context | hiệu năng phụ thuộc vị trí | dùng span ngắn để tránh | chỉ là lập luận thiết kế, không có thí nghiệm riêng [Paper: PDF p. 2, Introduction] |

## 06 Ý tưởng cốt lõi

1. **Phương pháp bề mặt:** Cắt context thành L unit; lấy mẫu observation span liên tiếp độ dài C ∈ {0,1,2,5,10,20,…,L}; cho probing model trả lời chỉ với span đó (có hướng dẫn trả lời IDK); fit mixture model để tìm (λ, k) cho mỗi problem; gán category theo ngưỡng [Paper: PDF p. 3, Section 3.1] [Paper: PDF p. 6, Section 3.4].
2. **Insight cốt lõi:** Cách tỷ lệ trả lời đúng tăng theo C khi chỉ nhìn một cửa sổ ngẫu nhiên mang thông tin về cấu trúc bằng chứng: đường cong phủ π(λ, k; L, C) có dạng tổ hợp xác định bởi λ và k, nên có thể suy ngược λ, k bằng likelihood; mixture model tách phần outcome "không dựa vào context" khỏi phần "oracle" [Paper: PDF p. 4, Equation 3] [Paper: PDF p. 2, Introduction].
3. **Bài học tổng quát:** [Analysis] Độ khó/loại năng lực mà một problem đo có thể được định lượng như một thuộc tính của problem bằng can thiệp có kiểm soát vào input (giữ lại phần nhỏ context) cộng mô hình nhiễu cho người làm bài; đây là cùng họ với ablation input kiểu counterfactual của bài 2505.13353, nhưng DOLCE thêm một mô hình sinh tường minh để đọc ra tham số có diễn giải.

## 07 Tổng quan phương pháp

- **Input:** problem (instruction + question + context); metric gốc của task; probing model [Paper: PDF p. 6, Section 4].
- **Output:** λ, k, phân phối noise P(x|z=N), prior P(z) cho mỗi problem; nhãn Category I–V [Paper: PDF p. 6, Section 3.4] [Paper: PDF p. 2, Figure 1].
- **Không huấn luyện model;** chỉ suy luận + EM. EM chạy 10 bước (COW) và 5 bước (PIG) [Paper: PDF p. 6, Section 4].
- **Giả định chính:** ground-truth span liên tiếp, không chồng lấn, phân bố đều (không mô hình hóa vị trí) [Paper: PDF p. 4, Assumption 1]; PIG: λ aspect độ dài 1, mỗi aspect lặp k lần [Paper: PDF p. 5, Assumption 2]; oracle không trả lời được khi chỉ thấy một phần span [Paper: PDF p. 4, Section 3.2].

```text
context -> chia unit (câu/dòng/block…, Table 3) -> lấy mẫu observation span độ dài C (exponential grid)
  -> probing model trả lời (prompt có lựa chọn IDK) -> chấm bằng metric gốc
  -> Hartigans' Dip Test (bins 0.1, p<0.5 -> COW, ngược lại PIG); COW: nhị phân hóa ngưỡng 0.5
  -> EM: E-step q(z|x); M-step P(x|N) (chia sẻ theo task), P(z) (theo problem), P_nonpar(x|O)
  -> brute-force argmax (λ,k) trên lưới ứng viên {C_ij} ∪ {0, max C+1, L}
  -> gán Category bằng ngưỡng λp, kp (tertile đầu), λq = max C (Figure 1)
```

[Paper: PDF p. 3, Section 3.1] [Paper: PDF p. 6, Section 4] [Paper: PDF p. 20, Algorithm 1]

## 08 Phân rã các module cốt lõi

| Module | Chức năng | Vì sao cần | Input và output | Bằng chứng hỗ trợ | Ảnh hưởng khi bỏ (đo được / dự kiến) |
|---|---|---|---|---|---|
| Unit segmentation | chia context thành unit có nghĩa | span token/ký tự không mạch lạc, document thì quá thô; quy tắc: chọn unit có độ dài ít phương sai [Paper: PDF p. 22, Appendix F] | context → L unit (Table 3 regex; Table 4 lựa chọn theo task) [Paper: PDF p. 23, Table 3] [Paper: PDF p. 24, Table 4] | Đổi unit trên 7 task: COW ρ(λ) 0.55–0.82 theo Table 8 [Paper: PDF p. 39, Table 8] | Đo được: thứ hạng λ bảo toàn ở mức trung bình–mạnh; giá trị λ tuyệt đối không so được giữa unit |
| Sampling & observation | lấy mẫu span độ dài C, quan sát outcome | tránh retriever; tránh lost-in-the-middle [Paper: PDF p. 2, Introduction] | problem → {(C_ij, x_ij)} | K.1: take-every-5 trên SFcition giữ ρ(λ)=0.93, ρ(k)=0.99, KL=3.7×10⁻⁵ với 80% ít tài nguyên [Paper: PDF p. 33, Appendix K.1] [Paper: PDF p. 38, Figure 13] [Paper: PDF p. 37, Figure 12] | Đo được: ít mẫu → tương quan với enumerate-all giảm |
| IDK instruction | cho phép outcome ∅ | phân biệt "không đủ thông tin" với "sai" | prompt mở rộng [Paper: PDF p. 22, Appendix E] | không có ablation | Dự kiến: không có ∅ thì π khó tách khỏi lỗi; tác giả nêu model "humble/conceited" ảnh hưởng [Paper: PDF p. 44, Appendix L] |
| Dip Test COW/PIG split | gán mỗi problem vào COW hay PIG | metric liên tục mơ hồ | điểm theo bin 0.1 → COW/PIG [Paper: PDF p. 26, Appendix H] [Paper: PDF p. 27, Figure 6] [Paper: PDF p. 28, Figure 7] [Paper: PDF p. 34, Figure 8] | Table 5 [Paper: PDF p. 26, Table 5] | Không có ablation trực tiếp; ngưỡng nhị phân hóa: xem K.4 |
| Background noise component (N) | mô hình outcome không dựa vào context | đoán may / memorization | P(x|N) phi tham số, chia sẻ theo task [Paper: PDF p. 4, Equation 2] | KL của P(x|N) giữa các thiết lập ≤ 0.18 [Paper: PDF p. 9, Section 6] | Dự kiến: không có N, problem đoán đúng ở C nhỏ sẽ bị gán λ nhỏ sai |
| Hybrid oracle component (O) | parametric khi C ≥ λ, phi tham số khi C < λ | oracle cũng mắc lỗi "chaotic" khi thấy span thiếu | Eq. 3 + Eq. 4 [Paper: PDF p. 4, Equation 3] [Paper: PDF p. 5, Equation 4] | Không có ablation parametric-only vs hybrid; tác giả thử multiplicative mixture, khó ước lượng nếu không regularize [Paper: PDF p. 43, Appendix L] | Chưa đo |
| MLE/EM + brute-force | tìm (λ, k) | hàm tổ hợp không lồi; dùng lưới ứng viên | Algorithm 1 [Paper: PDF p. 20, Algorithm 1]; Algorithm 2 (PIG) [Paper: PDF p. 21, Algorithm 2] | — | — |
| Category assignment | ánh xạ (λ, k) → I–V | đơn giản hóa phổ liên tục | ngưỡng λp, kp, λq [Paper: PDF p. 2, Figure 1] [Paper: PDF p. 6, Section 4] | tác giả thừa nhận ngưỡng chủ quan [Paper: PDF p. 6, Section 5] | Đổi ngưỡng nhị phân hóa: tăng ngưỡng đẩy problem từ II/III sang IV/V [Paper: PDF p. 42, Figure 16] |

## 09 Công thức và ký hiệu thiết yếu

**Equation 1 — mixture COW** [Paper: PDF p. 4, Equation 1]: `P(x_ij) = Σ_{z∈{N,O}} P(x_ij | z_ij = z) P(z_ij = z)`. i: problem, j: observation; x ∈ {1, 0, ∅}. Mục đích: tách outcome do nhiễu và do oracle.

**Equation 2 — background noise** [Paper: PDF p. 4, Equation 2]: `P(x|N) = p_{N,1}^[x=1] p_{N,0}^[x=0] p_{N,∅}^[x=∅]` — ba tham số hằng, không phụ thuộc C.

**Equation 3 — oracle parametric** [Paper: PDF p. 4, Equation 3]: `P_par(x|O; λ, k) = π^[x=1] · 0^[x=0] · (1−π)^[x=∅]`, với π(λ, k; L, C) là xác suất observation span phủ trọn ít nhất một trong k ground-truth span độ dài λ.

**Công thức π (Appendix A.1)** [Paper: PDF p. 15, Appendix A.1]: `π = 1 − [2·C(w+λ, k+1) + (k−1)/(k+1)·(2kλ + 2λ + w − 2k − ku − 1)·C(w+u, k)] / [C(w+C, k)·(L − C + 1)]`, với `w = L − C − kλ + k`, `u = min(C, 2λ − 2)`; π = 0 khi k < 1, kλ > L hoặc C < λ. Trực giác: đếm tổ hợp (stars-and-bars) ba trường hợp không phủ. Ví dụ L=50, C=5: π đạt đỉnh tại λ=2, k=20 [Paper: PDF p. 17, Figure 3] [Paper: PDF p. 19, Appendix B.3]. [Analysis] Ký hiệu tổ hợp bị vỡ khi trích xuất; cấu trúc trên được tái dựng từ văn bản và nên đối chiếu với PDF gốc trước khi tái hiện.

**Equation 4 — hybrid oracle** [Paper: PDF p. 5, Equation 4]: `P(x|O; λ, k) = P_nonpar(x|O)^[C<λ] · P_par(x|O; λ, k)^[C≥λ]`.

**Equation 5 — mixture PIG** [Paper: PDF p. 5, Equation 5]: `p(x_ij = s_ij) = Σ_z p(x_ij = s_{z,ij} | z) P(z)`, với `s_ij = s_O P(z=O) + s_N P(z=N)` ở mức sub-unit (unigram…); noise giả định uniform.

**Equation 6 — oracle PIG** [Paper: PDF p. 5, Equation 6]: `p(x = s_O | O; λ, k) = ρ(s_O, λ, k; L, C)`; ρ̃ tính bằng inclusion–exclusion, nội suy tuyến tính giữa bội của 1/λ và chuẩn hóa xấp xỉ bằng nhân (λ+1) [Paper: PDF p. 18, Appendix B.1] [Paper: PDF p. 19, Appendix B.2] [Paper: PDF p. 19, Figure 4].

**Thước đo so sánh thiết lập** [Paper: PDF p. 9, Section 6]: `δ(λ) = |λ_ref − λ_test| / max(λ_ref, λ_test)` (tương tự δ(k)), Spearman ρ của λ, k, và KL của P(x|z=N).

## 10 Thiết kế thực nghiệm và chuỗi bằng chứng

- **Dữ liệu:** 44 task từ L-Eval, BAMBOO, LongBench (bao gồm phần lớn ZeroSCROLLS); LongBench chỉ dùng phần tiếng Anh; BAMBOO bỏ hai task sắp xếp [Paper: PDF p. 6, Section 4] [Paper: PDF p. 22, Appendix D]. Context phần lớn < 100K token ("moderately long") [Paper: PDF p. 6, Section 4].
- **Task code có mặt:** L-Eval CodeU (unit dòng `l` hoặc block `b`, C tới 500 dòng, Accuracy), LongBench LCC (`l`, EditSim), LongBench RepoBench-p (`b`/`l`, EditSim), BAMBOO PrivateEval 4K/16K (`l`/`b`, RougeL; context là các dòng giữa `# [start]` và `# [end]`) [Paper: PDF p. 24, Table 4] [Paper: PDF p. 25, Table 4] [Paper: PDF p. 22, Appendix D].
- **Metric:** Accuracy, F-1, ROUGE-L, EditSim theo task; answer extractor theo task [Paper: PDF p. 23, Appendix G].
- **Probing model:** Gemini 1.5 Flash chính; PaLM 2-S để so sánh. Tác giả cố ý tránh model lớn vì khả năng closed-book mạnh [Paper: PDF p. 6, Section 4] [Paper: PDF p. 44, Appendix L].
- **Observation length:** lưới exponential; dừng khi vượt độ dài context tối đa hoặc span vượt 16K token [Paper: PDF p. 23, Appendix G]. Minh họa thống kê độ dài [Paper: PDF p. 23, Figure 5].
- **Không có uncertainty/CI** cho tỷ lệ category; không có nhãn người làm chuẩn.

| Thí nghiệm | Claim kiểm tra | So sánh và điều kiện | Kết quả | Kết luận được hỗ trợ | Kết luận mạnh hơn không được hỗ trợ | Nguồn |
|---|---|---|---|---|---|---|
| Phân loại chính | Benchmark trộn nhiều focus | 44 task, COW và PIG | III: 0–67% (COW), 0–29% (PIG); V: 0–89% (COW), 8–90% (PIG; Abstract ghi 0–90%) | Các task khác nhau mạnh về tỷ lệ retrieval/holistic theo DOLCE + Gemini 1.5 Flash | Đây là "loại năng lực thật" của task, độc lập probing model | [Paper: PDF p. 7, Figure 2] [Paper: PDF p. 7, Section 5] |
| Xếp hạng theo III và V | Task QA/information seeking thiên retrieval; code/đếm/thứ tự thiên holistic | Figure 9 (COW), Figure 10 (PIG) | MeetingQA đứng đầu III; PassageCount, GSM, TopicRet, LCC (COW) ít retrieval nhất; Category V gồm code (LCC COW, CodeU), PassageCount, TopicRet | Phù hợp trực giác về loại task | Task code "đòi hỏi hiểu toàn cục" theo nghĩa semantics | [Paper: PDF p. 7, Section 5.1] [Paper: PDF p. 35, Figure 9] [Paper: PDF p. 36, Figure 10] |
| Category I/II | Memorization / đoán | COW và PIG | TriviaQA, GSM nhiều Category I; PrivateEval và RepoBench-p (PIG) là Category I; SenHallu/AbsHallu/TREC nhiều Category II | DOLCE phát hiện problem giải được không cần context | Nguyên nhân là memorization (chỉ "suspect") | [Paper: PDF p. 7, Section 5.1] [Paper: PDF p. 8, Section 5.2] |
| Ví dụ đại diện | Category có ý nghĩa định tính | QuALITY, LongFQA | Ví dụ λ, k từng category; V: "How many sentences…" (λ=L) | Minh họa hợp lý | Không phải đánh giá hệ thống | [Paper: PDF p. 8, Table 2] [Paper: PDF p. 36, Figure 11] [Paper: PDF pp. 28-33, Appendix J] |
| Sampling strategy | Có thể giảm chi phí | TOEFL, SFcition, nhiều chiến lược | take-every-5: ρ(λ)=0.93, ρ(k)=0.99; "take" tốt hơn random sampling | Tiết kiệm ~80% trên SFcition | Tổng quát cho mọi task (chỉ 2 task) | [Paper: PDF p. 33, Appendix K.1] [Paper: PDF p. 37, Figure 12] [Paper: PDF p. 38, Figure 13] |
| Unit granularity | Thứ hạng λ, k ổn định | 7 task, hai unit | COW ρ(λ) .55–.82 (Table 8; lời văn ghi 0.54–0.80); PIG ρ(λ) .35–.84; KL ≤ .18 | Thứ hạng ổn định ở mức trung bình–mạnh | λ là đại lượng bất biến theo unit | [Paper: PDF p. 9, Section 6] [Paper: PDF p. 39, Table 8] |
| Probing model | Độ bền theo model | Gemini 1.5 Flash vs PaLM 2-S, bỏ Category I | median δ(λ)=0.30, δ(k)=0.16; median ρ(λ)=0.43, ρ(k)=0.41 | Tương quan trung bình | λ, k là thuộc tính riêng của problem | [Paper: PDF p. 9, Section 6] [Paper: PDF p. 40, Figure 14] [Paper: PDF p. 41, Figure 15] |
| Ngưỡng nhị phân hóa | Ngưỡng 0.5 hợp lý | 0, 0.25, 0.75, 1 | ρ(λ), ρ(k) > 0.48, 0.41 trừ hai task; ngưỡng 0 làm sụp tương quan | Ngưỡng phải > 0 | 0.5 tối ưu | [Paper: PDF p. 40, Appendix K.4] [Paper: PDF p. 42, Figure 16] [Paper: PDF p. 43, Figure 17] |
| Cùng task khác suite | Phân bố phụ thuộc cách chọn problem | 4 task chung | Qasper tương tự; MultiNews, NarrativeQA (L-Eval) holistic hơn; GovReport ngược lại; giải thích bằng median context length | Tương thích với giải thích độ dài | Nhân quả của độ dài | [Paper: PDF p. 9, Section 6] [Paper: PDF p. 41, Table 9] |

## 11 Diễn giải đúng các kết luận

- **Phạm vi task:** chỉ 44 task, context chủ yếu < 100K token; observation span ≤ 16K token, nên "Category V" nghĩa là λ > max C — tức cần nhiều hơn cửa sổ lớn nhất được thử, không nhất thiết toàn bộ context [Paper: PDF p. 6, Section 4] [Paper: PDF p. 23, Appendix G].
- **Phụ thuộc model:** tương quan giữa hai probing model chỉ ở mức trung bình (median ρ ≈ 0.4) [Paper: PDF p. 9, Section 6]. Nhãn là thuộc tính của cặp (problem, probing model, unit, metric, ngưỡng).
- **Ground truth:** không có nhãn người; chỉ kiểm tra thủ công vài ví dụ đại diện [Paper: PDF p. 44, Appendix L].
- **Ngưỡng category chủ quan** [Paper: PDF p. 6, Section 5].
- **Vị trí:** DOLCE giả định span phân bố đều và không mô hình hóa vị trí; observation span được đưa riêng lẻ (không đặt trong context dài) [Paper: PDF p. 4, Section 3.2] [Paper: PDF p. 2, Introduction].
- **Bất định:** không báo cáo CI cho tỷ lệ category; có hai điểm không nhất quán số liệu (xem header).
- **Phát biểu giới hạn:** Với Gemini 1.5 Flash làm probing model, unit và ngưỡng do tác giả chọn, DOLCE cho thấy các task long-context trong ba suite có tỷ lệ problem retrieval-focused và holistic-focused rất khác nhau, với độ ổn định thứ hạng tham số ở mức trung bình giữa các thiết lập.

## 12 Hạn chế được tác giả thừa nhận rõ ràng

| Hạn chế | Biểu hiện cụ thể | Hướng tương lai do tác giả đề xuất | Nguồn |
|---|---|---|---|
| Mixture assumption | additive không bắt buộc; multiplicative khó ước lượng nếu không regularize | regularization / dạng khác | [Paper: PDF pp. 41-43, Appendix L] |
| Oracle component assumptions | COW/PIG có thể không đúng với mọi task; span liên tiếp; aspect độ dài 1; không có thứ tự | span không liên tiếp; aspect dài hơn (FLenQA, BABILong); giả định thứ tự để tách sequential reasoning khỏi summarization; unit dùng chung | [Paper: PDF p. 43, Appendix L] [Paper: PDF p. 44, Appendix L] |
| MLE objective & sampling | trọng số đều mỗi mẫu; ít mẫu làm giảm chính xác | trọng số theo độ dài; sampling động/importance; kết hợp retrieval | [Paper: PDF p. 44, Appendix L] |
| Probing model | bỏ qua hướng dẫn, dùng trí nhớ, lạm dụng/né IDK; toàn "0" thì không tách được N và O | chọn model cỡ vừa | [Paper: PDF p. 44, Appendix L] |
| Evaluation | nhiễu ROUGE có thể vượt khả năng khử nhiễu; không dùng script executor, người hay LLM-rater | dùng executor/LLM-as-rater | [Paper: PDF p. 44, Appendix L] |
| Human verification | không xác minh λ, k bằng người | so với nhãn thủ công của NoCha/Loong | [Paper: PDF p. 44, Appendix L] |
| Ngưỡng nhị phân hóa | ngưỡng hợp lý phụ thuộc task/problem | ngưỡng theo problem | [Paper: PDF p. 39, Appendix K.4] |

**Ràng buộc liên quan do tác giả nêu (không trình bày như limitation chính thức):** context chỉ "moderately long" [Paper: PDF p. 6, Section 4]; không mô hình hóa vị trí ground-truth span [Paper: PDF p. 4, Section 3.2] [Paper: PDF p. 36, Appendix K.2].

## 13 Phân tích phản biện

| `[Analysis]` Quan sát | Vấn đề tiềm ẩn / giải thích thay thế | Vì sao quan trọng | Cách kiểm tra | Cơ sở |
|---|---|---|---|---|
| Code task (CodeU, LCC COW) xếp Category V | Với code, phụ thuộc (định nghĩa hàm, biến, import) thường không liên tiếp; giả định span liên tiếp buộc λ phải bao trọn khoảng cách giữa các phụ thuộc → λ bị thổi phồng, "holistic" có thể chỉ là "multi-hop rải rác" | Diễn giải sai về năng lực code cần | Ước lượng lại với unit theo program slice / dependency graph; so sánh λ | [Paper: PDF p. 7, Section 5.1] [Paper: PDF p. 4, Assumption 1] [Paper: PDF p. 8, Section 5.1] |
| Dòng code bị nhận xét kém "self-contained" so với đoạn văn | Cửa sổ dòng code cắt ngang hàm → model không chạy được, outcome ∅ do cú pháp thiếu chứ không do thiếu thông tin | λ phản ánh độ dài hàm hơn là nhu cầu thông tin | Dùng unit = hàm/khối AST; kiểm tra tương quan λ với độ dài hàm | [Paper: PDF p. 8, Section 5.1] [Paper: PDF p. 39, Table 8] |
| RepoBench-p, PrivateEval (PIG) là Category I | EditSim cho điểm cao với code sinh "na ná" mà không cần context (pattern matching), chứ không chỉ memorization context | Category I trộn memorization với shortcut metric | So sánh với exact-match/execution-based metric; tác giả không dùng executor | [Paper: PDF p. 8, Section 5.2] [Paper: PDF p. 44, Appendix L] |
| Không có hiệu ứng vị trí | Span được đưa riêng lẻ; một problem retrieval (λ nhỏ) vẫn có thể thất bại ở context đầy đủ do lost-in-the-middle — DOLCE không đo khoảng cách này | Category III/V không dự báo được độ bền theo vị trí | Đặt observation span ở các độ sâu khác nhau trong distractors và ước lượng lại | [Paper: PDF p. 2, Introduction] [Paper: PDF p. 4, Section 3.2] |
| Tương quan giữa hai probing model chỉ ~0.4 | Một phần biến thiên là do instruction following/format (PassageRetrieval), không phải thuộc tính problem | Hạn chế tính "khách quan" của λ | Ước lượng nhiều model, mô hình phân cấp problem × model | [Paper: PDF p. 9, Section 6] [Paper: PDF p. 39, Appendix K.3] |
| Số liệu lời văn và bảng lệch nhau | Lời văn "ρ(λ) 0.54–0.80" khớp cột δ(λ); "0% vs 8%" cận dưới PIG Category V | Người trích dẫn có thể dùng sai số | Đối chiếu Table 8 / phiên bản sau của arXiv | [Paper: PDF p. 39, Table 8] [Paper: PDF p. 7, Section 5] [Paper: PDF p. 1, Abstract] |

**Đánh giá theo câu hỏi của người dùng (tách phát biểu tác giả và phân tích của Agent).**

1. **Trục phân loại và cơ chế.** [Paper] Hai trục: λ (complexity — độ dài span tối thiểu đủ) và k (redundancy — số lần lặp); năm category trên mặt phẳng λ-k: I CBZS (λ=0), II Easy (λ ≤ λp, k > kp), III Retrieval (λ ≤ λp, k ≤ kp), IV Balanced (λp < λ ≤ λq), V Holistic (λ > λq) [Paper: PDF p. 2, Figure 1]. Cơ chế: lấy mẫu observation span + mixture model + MLE/EM [Paper: PDF p. 3, Section 3] [Paper: PDF p. 6, Section 3.4]. [Analysis] Retrieval vs holistic do λ quyết định chủ yếu; k chỉ tách Easy khỏi Retrieval khi λ nhỏ.
2. **Có áp dụng cho code task không.** [Paper] Có: CodeU, LCC, RepoBench-p, PrivateEval 4K/16K [Paper: PDF pp. 24-25, Table 4]. Kết quả: LCC (COW) và CodeU nằm trong nhóm holistic nhất / ít retrieval nhất [Paper: PDF p. 7, Section 5.1]; RepoBench-p và PrivateEval (PIG) là Category I [Paper: PDF p. 8, Section 5.2]; CodeU đổi unit dòng→block ρ(λ)=0.82 [Paper: PDF p. 39, Table 8]. [Analysis] Bài không phân tích code riêng, không dùng executor, chỉ một câu giải thích về "lines of code" kém self-contained [Paper: PDF p. 8, Section 5.1].
3. **Hiệu ứng vị trí.** [Paper] Không mô hình hóa vị trí; giả định phân bố đều [Paper: PDF p. 4, Section 3.2]; dùng span ngắn để tránh lost-in-the-middle [Paper: PDF p. 2, Introduction]; K.2 nhắc lại không mô hình hóa vị trí [Paper: PDF p. 36, Appendix K.2]. Quan sát duy nhất về vị trí tương đối: span lân cận có correctness tương quan dương ("continuity") [Paper: PDF p. 33, Appendix K.1]. [Analysis] DOLCE không trả lời được câu hỏi vị trí của bài 2505.
4. **Có dùng để định lượng semantic recall sensitivity (2505) được không.** [Analysis] Có thể một phần. Giống: cả hai là counterfactual giảm thông tin input và quan sát hiệu năng LLM; Category I/II của DOLCE ≈ phần problem giải được khi thiếu context (tương ứng sensitivity thấp, pattern matching shortcuts). Khác: (a) DOLCE giữ lại một cửa sổ liên tiếp và bỏ phần còn lại, 2505 xóa dòng rải rác bên trong chính hàm mục tiêu; (b) DOLCE xuất ra (λ, k) theo problem và nhãn rời rạc, 2505 xuất một đại lượng liên tục Sens^T(C) (diện tích dưới đường suy giảm chuẩn hóa) [User: cards/2505.13353v5/paper-card.md, Section 09]; (c) DOLCE có mô hình nhiễu tách N/O và lựa chọn IDK — 2505 thì không; 2505 có tham chiếu Python interpreter — DOLCE thì không; (d) đơn vị "context" của DOLCE là tài liệu dài cần tìm, còn của 2505 là đoạn code mục tiêu ngắn. Do vậy p_{N,1}, P(z=N) hoặc tỷ lệ Category I của DOLCE có thể dùng làm thước đo "độ dùng shortcut" bổ sung, nhưng cần thay giả định span liên tiếp bằng giả định xóa dòng/phụ thuộc.

## 14 Kiến thức thu được

**Agent-derived knowledge candidates**

- **Khái niệm:** tách độ dài input L khỏi độ dài context cần thiết λ và độ lặp k [Paper: PDF p. 3, Related Work] [Paper: PDF p. 2, Figure 1].
- **Phương pháp:** đo đặc trưng problem bằng đường cong "tỷ lệ đúng theo độ dài cửa sổ quan sát" + mô hình sinh tổ hợp + EM; mixture noise/oracle để chịu được probing model không hoàn hảo [Paper: PDF p. 4, Equation 1] [Paper: PDF p. 5, Equation 4].
- **Kỹ thuật thực hành:** dùng Hartigans' Dip Test để quyết định coi metric liên tục là nhị phân hay điểm từng phần [Paper: PDF p. 3, Section 3.1]; take-every sampling giảm 80% chi phí [Paper: PDF p. 33, Appendix K.1]; báo cáo độ bền bằng δ, Spearman ρ và KL [Paper: PDF p. 9, Section 6].
- **Thiết kế thực nghiệm:** kiểm tra độ nhạy của một thước đo theo probing model, unit, sampling, ngưỡng — khuôn mẫu tốt để đánh giá bất kỳ "benchmark property metric" nào (kể cả Sens của 2505).

## 15 Liên hệ với tri thức hiện có

- **[User] Bài 2505.13353 (Sense and Sensitivity):** đo semantic recall sensitivity bằng xóa dòng code và đặt hàm mục tiêu ở 11 vị trí giữa distractors (theo card nội bộ cards/2505.13353v5/paper-card.md). [Analysis] Bổ sung lẫn nhau: DOLCE trả lời "cần bao nhiêu context liên tiếp" mà không xét vị trí; 2505 trả lời "model có thật sự dùng semantics của đoạn code không" và "có phụ thuộc vị trí không". Khoảng trống giao nhau: chưa có (trong hai bài) phương pháp ước lượng tham số theo mô hình sinh cho độ nhạy thông tin của code task, có tách nhiễu memorization, và có xét vị trí.
- **[Paper-framed] Goldman et al. 2024 (scope, diffusion)** là hai chiều tương tự λ, k nhưng chỉ ở mức position paper [Paper: PDF p. 3, Related Work]. Chưa kiểm chứng ngoài.
- **[Analysis] Kết hợp:** mixture model của DOLCE có thể khử nhiễu cho đường cong xóa dòng của 2505; ngược lại, interpreter của 2505 có thể làm "oracle tham chiếu" cho DOLCE trên code task, vốn là thứ DOLCE thiếu (tác giả nói không dùng script executor) [Paper: PDF p. 44, Appendix L].
- **[Analysis] Xung đột tiềm năng:** DOLCE xếp code task vào holistic (λ lớn), còn 2505 cho thấy CRUXEval cho phép shortcut (sensitivity thấp). Hai kết luận không mâu thuẫn trực tiếp vì đo các đối tượng khác (repo/file dài vs hàm ngắn), nhưng cảnh báo rằng nhãn "holistic" không bảo đảm task đòi hỏi semantic recall.
- Không thực hiện tra cứu ngoài; mọi liên hệ ngoài hai bài trên chưa được kiểm chứng.

## 16 Ý tưởng nghiên cứu

**Agent-derived research candidates**

**Ứng viên 1 — DOLCE theo phụ thuộc chương trình để ước lượng semantic recall sensitivity có khử nhiễu**
- **Nguồn gốc:** DOLCE giả định span liên tiếp và nêu mở rộng sang span không liên tiếp là hướng tương lai [Paper: PDF p. 43, Appendix L]; code task bị xếp holistic, nhưng dòng code được nhận xét kém self-contained [Paper: PDF p. 8, Section 5.1]; 2505 đo Sens bằng xóa dòng nhưng không tách nhiễu memorization [User: cards/2505.13353v5/paper-card.md, Section 09].
- **Giả thuyết:** Nếu thay "observation span liên tiếp" bằng "tập con dòng giữ lại theo program slice" và fit mixture N/O, thì (a) tỷ trọng P(z=N) trên CRUXEval cao hơn đáng kể so với SemTrace, và (b) λ_slice (số dòng phụ thuộc tối thiểu) tương quan âm với tỷ lệ Category I và dương với Sens của 2505. Bác bỏ nếu P(z=N) không khác giữa hai benchmark hoặc tương quan |ρ| < 0.3.
- **Delta so với bài:** biểu diễn (unit = dòng theo dependency/slice, không liên tiếp); cơ chế (công thức phủ cho tập con không liên tiếp); đánh giá (dùng Python interpreter làm oracle tham chiếu).
- **Phương pháp ban đầu:** sinh tập con dòng theo tỷ lệ giữ lại 0–100%; với interpreter tính đường cong oracle thật; thay π bằng xác suất "giữ đủ slice" (có thể ước tính bằng Monte Carlo); EM như Algorithm 1.
- **Kiểm chứng (Validation):** CRUXEval-O vs SemTrace, ≥3 LLM; so với Sens của 2505; độ ổn định theo model bằng δ, ρ, KL như Section 6 của DOLCE.
- **Rủi ro thất bại (Failure modes):** code bị xóa dòng thường lỗi cú pháp/runtime → outcome ∅ do lỗi chứ không do thiếu thông tin (nhiễu đo); không có công thức đóng cho π không liên tiếp → chi phí tính toán; tương quan giữa model thấp (~0.4 như DOLCE) làm λ không ổn định.
- **Innovation status:** unverified — cần prior-art search.

**Ứng viên 2 — λ phụ thuộc vị trí: ghép sampling của DOLCE với thiết kế đặt vị trí của 2505**
- **Nguồn gốc:** DOLCE không mô hình hóa vị trí và đưa span riêng lẻ [Paper: PDF p. 4, Section 3.2] [Paper: PDF p. 2, Introduction]; 2505 báo cáo semantic recall suy giảm theo vị trí còn lexical recall thì không [User: cards/2505.13353v5/paper-card.md, Section 02].
- **Giả thuyết:** Khi observation span chứa hàm mục tiêu được nhúng ở độ sâu d trong distractors, λ hiệu dụng ước lượng cho task semantic (output prediction) tăng ở vị trí giữa, còn λ cho task lexical (function retrieval) gần như không đổi. Bác bỏ nếu đường λ(d) của hai task không khác nhau có ý nghĩa (ví dụ bootstrap CI chồng lấn).
- **Delta so với bài:** đánh giá (thêm biến vị trí d vào likelihood: P(z=O) hoặc π phụ thuộc d); dữ liệu (task code có kiểm soát vị trí).
- **Phương pháp ban đầu:** với mỗi C và d, đo outcome; fit mô hình phân cấp λ_i(d) = λ_i + f(d); so sánh hai task trên cùng hàm.
- **Kiểm chứng (Validation):** CRUXEval/SemTrace với 11 vị trí như 2505; metric: λ(d), P(z=N)(d); kỳ vọng hình chữ U cho task semantic.
- **Rủi ro thất bại (Failure modes):** số tổ hợp (C × d) làm chi phí gấp nhiều lần (dù take-every có thể giảm ~80% [Paper: PDF p. 33, Appendix K.1]); hiệu ứng vị trí có thể đi vào P(z=N) thay vì λ → khó diễn giải; confounding giữa độ dài context tổng và vị trí.
- **Innovation status:** unverified — cần prior-art search.

### Danh mục bằng chứng (inventory) đã đối chiếu

- Figures: Figure 1 (p. 2), Figure 2 (p. 7), Figure 3 (p. 17), Figure 4 (p. 19), Figure 5 (p. 23), Figure 6 (p. 27), Figure 7 (p. 28), Figure 8 (p. 34), Figure 9 (p. 35), Figure 10 (p. 36), Figure 11 (p. 36), Figure 12 (p. 37), Figure 13 (p. 38), Figure 14 (p. 40), Figure 15 (p. 41), Figure 16 (p. 42), Figure 17 (p. 43).
- Tables: Table 1 (p. 4), Table 2 (p. 8), Table 3 (p. 23), Table 4 (pp. 24–25), Table 5 (p. 26), Table 8 (p. 39), Table 9 (p. 41). Bundle không phát hiện Table 6–7; Appendix J trình bày tham số dạng bảng không caption [Paper: PDF pp. 28-33, Appendix J].
- Equations: Equation 1–3 (p. 4), Equation 4–6 (p. 5); công thức π, ρ̃, ρ ở Appendix A–B.
