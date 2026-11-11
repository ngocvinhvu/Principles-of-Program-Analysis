# Paper Card — RepoMirage: Probing Repository Context Reasoning in Code Agents with Perturbations

> Phạm vi nguồn (Source coverage): Full paper — toàn văn 22 trang PDF (arXiv 2605.26177v1), gồm phần chính, phụ lục A–E, mọi hình/bảng
> Độ tin cậy trích xuất (Extraction confidence): High (PyMuPDF, validation = valid; các trang chứa Table 1–3, Figure 2–5, 7, 11, 12 đã kiểm tra trực quan qua ảnh trang render)
> Locator mode: page-grounded — mọi con trỏ dùng chỉ số trang file PDF (`PDF p. N`); số chân trang in trùng với chỉ số PDF
> Primary analytical lens: resource (evaluation suite / benchmark RepoMirage-Perturb và RepoMirage-Extend)
> Secondary analytical lens: discovery (chẩn đoán "exploration drift" và can thiệp structural hints)
> Context verification: Paper-only — không thực hiện kiểm chứng ngoài
> Card completeness: Complete relative to supplied source

**Tóm tắt trạng thái bằng chứng.** Các số chính đã đối chiếu với nguồn và tính lại từ bảng: trung bình resolved rate 66.80% → 49.78% (Table 1), số file truy cập 4.77 → 13.24, Extend trung bình 25.25% (Table 2), hints 27.60 → 62.60 (GPT-5) và 39.80 → 76.80 (DeepSeek-V3.2) (Table 3). Hai điểm lệch nhỏ được ghi ở Section 13: con số "giảm tương đối 27.0% trung bình" [Paper: PDF p. 2, Introduction] không khớp chính xác với trung bình cột Drop của Table 1 (≈27.24%); và hai giá trị "Org." của Qwen3.6-35B-A3B trong Table 2 không tương ứng với số nguyên instance trên n = 142/144. Không có kiểm định thống kê hay khoảng tin cậy cho resolved rate; mỗi cấu hình dường như chạy một lần. Figure 5 và Figure 11 có đánh dấu mức ý nghĩa (***), nhưng không nêu tên kiểm định.

**Terminology Ledger (khóa thuật ngữ cho toàn card).**

| Canonical term | Định nghĩa lần đầu | Biến thể trong nguồn | Quyết định |
|---|---|---|---|
| repository context reasoning | khả năng xác định thông tin liên quan tới task trải trên nhiều file và suy luận trên quan hệ giữa chúng | "multi-file understanding", "cross-file reasoning" | dùng nguyên dạng |
| RepoMirage | evaluation suite hai giai đoạn dựa trên perturbation, xây trên SWE-Bench Verified | "REPOMIRAGE" | dùng "RepoMirage" |
| RepoMirage-Perturb | giai đoạn 1: áp 3 perturbation, giữ nguyên task issue resolution | "Perturb" | dùng nguyên dạng |
| RepoMirage-Extend | giai đoạn 2: 4 task family trên repository đã áp đủ 3 perturbation | "Extend" | dùng nguyên dạng |
| dependency-path indirection | thay import trực tiếp bằng proxy chain 4 tầng | "Indirect" (Figure 3) | dùng nguyên dạng |
| runtime-target masking | đổi tên file mục tiêu, tạo wrapper package `__init__.py`, thêm fake files | "Mask" (Figure 3), "decoy files" | dùng nguyên dạng; "fake files" = "decoy files" |
| local-value externalization | chuyển hằng số cục bộ sang file JSON bên ngoài | "External" (Figure 3) | dùng nguyên dạng |
| Multi-File Issue Resolution / Proxy Chain Completion / Runtime Target Identification / Missing-Constant Recovery | 4 task family của RepoMirage-Extend | "Proxy Chain Recovery" (p. 6), "Missing Constant" | dùng tên ở Section 4.1; ghi chú "Proxy Chain Recovery" là biến thể |
| exploration drift | agent truy cập nhiều context hơn nhưng không chuyển được thành quyết định edit | — | dùng nguyên dạng |
| structural hints | prompt mô tả chung cơ chế perturbation, chèn trước task | "hints" | dùng nguyên dạng |
| RepoAnchor | workflow hai stage: exploration viết INSTRUCTION.md → problem solving | "INSTRUCTIONS.md" / "INSTRUCTION.md" | dùng "RepoAnchor", "INSTRUCTION.md" |
| resolved rate | % instance được giải (pass test/checker) | "success rate", "Resolve Rate" | dùng "resolved rate" |
| PASS_TO_PASS / FAIL_TO_PASS | bộ test chính thức của SWE-Bench | — | dùng nguyên dạng |

## 01 Thông tin cơ bản

| Trường | Nội dung |
|---|---|
| Tiêu đề | RepoMirage: Probing Repository Context Reasoning in Code Agents with Perturbations [Paper: PDF p. 1, Title] |
| Tác giả và đơn vị | Hanyu Li (BUPT), Yichi Zhang, Hang Su, Jun Zhu, Yinpeng Dong (Tsinghua University), Speed Zhu (Tencent); Li và Zhang đóng góp ngang nhau [Paper: PDF p. 1, Title block] |
| Nơi công bố / năm | Preprint arXiv, cs.SE, 25/05/2026; chưa có venue bình duyệt [Paper: PDF p. 1, arXiv stamp] |
| Định danh | arXiv:2605.26177v1 [Paper: PDF p. 1] |
| Loại bài | Benchmark / evaluation suite kèm phân tích chẩn đoán và một prototype giảm thiểu |
| Lĩnh vực / từ khóa | software engineering, code agents, repository-level evaluation, perturbation, SWE-Bench Verified, trajectory analysis |
| Code | Repository ẩn danh https://anonymous.4open.science/r/RepoMirage; phát hành dạng toolkit sinh benchmark, không phải dataset tĩnh [Paper: PDF p. 20, Appendix D] |
| Dataset | Dựng lại từ SWE-Bench Verified (500 instance, phân ra 70/144/142/144 trong Extend) [Paper: PDF p. 6, Figure 4] |
| Ngày đọc | 2026-11-06 |
| Vị trí trong hướng nghiên cứu của người dùng | `[User]` Người dùng đang tìm khoảng trống quanh "Sense and Sensitivity" (arXiv 2505.13353): lexical recall vs semantic recall theo vị trí trong long context. RepoMirage là bài liền kề ở quy mô repository + agent tương tác, nhưng đo ở trục khác (cấu trúc phụ thuộc giữa file, không phải vị trí token) — xem Section 15. |

## 02 Tóm tắt một câu

Bằng cách áp ba perturbation được tác giả gọi là semantics-preserving (proxy chain cho import, che file runtime bằng wrapper và fake files, đẩy hằng số ra JSON) lên SWE-Bench Verified rồi biến chúng thành bốn task tường minh, bài báo báo cáo rằng resolved rate trung bình của 8 model với mini-swe-agent giảm từ 66.80% xuống 49.78% (Perturb) và xuống 25.25% (Extend), quy nguyên nhân cho "exploration drift", và cho thấy structural hints hoặc workflow hai stage RepoAnchor bù lại một phần [Paper: PDF p. 4, Section 3.2] [Paper: PDF p. 6, Section 4.2] [Paper: PDF p. 8, Table 3] [Paper: PDF p. 9, Figure 7].

## 03 Câu hỏi nghiên cứu

- **Vấn đề cụ thể:** Điểm số cao trên benchmark end-to-end như SWE-Bench Verified có thật sự phản ánh repository context reasoning không, hay agent thành công nhờ cue cục bộ? [Paper: PDF p. 1, Abstract]
- **Tại sao quan trọng:** Task cấp dự án đòi hỏi gom bằng chứng phân tán qua nhiều file (truy call relationships, ràng buộc thực thi) [Paper: PDF p. 1, Introduction].
- **Vì sao cách hiện có chưa đủ:** Đánh giá hiện có là end-to-end, không cô lập năng lực; benchmark mới nhiều file hơn thì đổi môi trường và cách đặt task nên khó quy lỗi [Paper: PDF p. 2, Introduction]. Bằng chứng mở đầu: với GPT-5, 53.8% instance đã giải chỉ mở 1 file, 88.0% không quá 3 file [Paper: PDF p. 3, Figure 2].
- **Câu hỏi nghiên cứu:** Can semantics-preserving repository-level perturbations, giữ nguyên task và codebase gốc, tách được repository context reasoning khỏi khả năng giải issue nhờ cue cục bộ — và điều gì làm agent thất bại khi cue bị loại bỏ?

## 04 Bối cảnh nghiên cứu và lộ trình phát triển

[Paper-framed; external verification not performed]

| Giai đoạn | Cách tiếp cận đại diện (theo bài) | Ưu điểm | Hạn chế | Nguồn |
|---|---|---|---|---|
| Function-level / single-file | HumanEval-style, sinh chương trình một file | đơn giản, dễ chấm | không cần context repository | [Paper: PDF p. 9, Related Work 6.1] |
| Repository-level end-to-end | SWE-bench, SWE-bench Verified, các bản mở rộng (fresher tasks, đa hệ sinh thái, SWE-bench Pro) | task thật, test chính thức | đo thành công cuối, không cô lập năng lực | [Paper: PDF p. 9, Related Work 6.1] |
| Perturbation để kiểm tra độ bền | biến đổi đầu vào trong NLP; đổi tên biến, biến đổi code, codebase-level understanding dưới input bị thay đổi | lộ heuristic giòn | thường đóng khung là robustness | [Paper: PDF p. 9, Related Work 6.2] |
| Vị trí bài tự nhận | perturbation như công cụ chẩn đoán một năng lực cụ thể, trên chính instance gốc | so sánh được với gốc, quy lỗi rõ | — | [Paper: PDF p. 9, Related Work 6.2] |

Bài trích dẫn hai kết quả tiền đề: >80% instance SWE-Bench Verified chỉ cần sửa một file, và model có thể đoán đúng đường dẫn file lỗi tới 76% kể cả khi không có cấu trúc repository [Paper: PDF p. 3, Section 2.2]. Hai kết quả này chưa được kiểm chứng ngoài trong card này.

## 05 Các điểm đau cốt lõi được bài báo chỉ ra

| Điểm đau | Biểu hiện | Nguyên nhân / giải thích của tác giả | Bằng chứng trong bài |
|---|---|---|---|
| Thành công trên benchmark mang tính cục bộ | GPT-5: avg. 2.15 file / instance đã giải; DeepSeek-V3.2: 3.97 | import, tên file, hằng số cục bộ là cue trực tiếp | [Paper: PDF p. 3, Figure 2] |
| Benchmark mới khó quy lỗi | môi trường và cách đặt task khác nhau | không có điều kiện đối chứng trên cùng instance | [Paper: PDF p. 2, Introduction] (lập luận, không có thí nghiệm riêng) |
| Agent không tổ chức được thông tin nhiều file | đọc nhiều file hơn nhưng explore→edit giảm | thiếu "structural scaffold" | [Paper: PDF p. 7, Figure 5] [Paper: PDF p. 8, Section 5.1] |

Giải thích "thiếu structural scaffold" là diễn giải của tác giả, được hỗ trợ gián tiếp bởi Table 3 — không phải nguyên nhân gốc đã được chứng minh (xem Section 13).

## 06 Ý tưởng cốt lõi

1. **Phương pháp bề mặt:** Biến đổi repository bằng LibCST theo 3 kiểu, kiểm tra bằng test chính thức, rồi biến mỗi "nút thắt" cấu trúc thành một task có checker xác định [Paper: PDF p. 14, Appendix A.4] [Paper: PDF p. 15, Appendix A.5].
2. **Insight cốt lõi:** Giữ nguyên task và ngữ nghĩa thực thi, chỉ thay *cách thông tin được phơi ra* (exposure) trong repository; mọi sụt giảm khi đó có thể quy cho repository context reasoning thay vì cho task khó hơn [Paper: PDF p. 4, Section 3.1].
3. **Bài học tổng quát `[Analysis]`:** Một benchmark end-to-end có thể được "chẩn đoán" bằng các phép biến đổi bảo toàn hành vi, nhắm vào từng loại cue; thiết kế ma trận cue × task cho phép đo mức phụ thuộc vào shortcut. Tính hợp lệ phụ thuộc vào việc perturbation không đưa thêm tín hiệu nhân tạo (vd. tiền tố `proxy_`, `dependency_`).

## 07 Tổng quan phương pháp

- **Input:** instance SWE-Bench Verified (repository Docker + issue + test) [Paper: PDF p. 3, Section 2.1].
- **Perturbation (LibCST):** (a) dependency-path indirection — chỉ cho absolute import độc lập layout (vd. `json`, `re`), proxy chain 4 tầng xác định; (b) runtime-target masking — đổi tên file, wrapper `__init__.py` nạp động bằng đường dẫn file, fake files không bao giờ được import; (c) local-value externalization — gom mỗi 3 hằng số vào một file JSON, target file đọc và merge [Paper: PDF p. 4, Section 3.1] [Paper: PDF p. 14-15, Appendix A.4].
- **Kiểm tra:** PASS_TO_PASS sau perturbation (bảo toàn chức năng); áp gold patch → perturb → FAIL_TO_PASS (bảo toàn khả năng giải) [Paper: PDF p. 14, Appendix A.4].
- **Extend:** mỗi instance gán đúng một task family; checker được chạy trên repository Perturb trước khi xóa để đảm bảo có lời giải; prompt giới hạn file được sửa và checker kiểm tra không sửa file khác [Paper: PDF p. 15, Appendix A.5].
- **Agent:** mini-swe-agent, bash-only, step budget 250, nhiệt độ mặc định; 8 backbone LLM [Paper: PDF p. 14, Appendix A.2-A.3].
- **Phân tích trajectory:** phân loại lệnh shell theo luật thành edit/test/search/read; gộp search+read = explore; tính ma trận chuyển trạng thái [Paper: PDF p. 16, Appendix A.6].
- **Can thiệp:** structural hints chung (Figure 8) và RepoAnchor hai stage — sơ đồ ở Figure 6, prompt stage 1 ở Figure 9, prompt stage 2 ở Figure 10 (cho phép agent kiểm lại điểm chưa rõ thay vì tin mù INSTRUCTION.md) [Paper: PDF p. 17, Figure 8] [Paper: PDF p. 8, Figure 6] [Paper: PDF p. 18, Figure 9] [Paper: PDF p. 19, Figure 10].

Luồng: `SWE-Bench Verified instance → LibCST perturb ×3 → test PASS_TO_PASS/FAIL_TO_PASS → (Perturb: issue resolution) | (Extend: xóa proxy / wrapper ref / JSON keys → checker) → mini-swe-agent × 8 LLM → resolved rate + trajectory metrics → hints / RepoAnchor`.

**Giả định chính:** test chính thức đủ để chứng nhận bảo toàn ngữ nghĩa; các cue bị loại bỏ là "shortcut" chứ không phải thông tin chính đáng; mọi khác biệt hành vi là do perturbation chứ không do artefact tạo sinh (tên file vô nghĩa như `flux_cinder_hh.py`) [Paper: PDF p. 21, Figure 13].

## 08 Phân rã các module cốt lõi

| Module | Chức năng | Vì sao cần | Input và output | Bằng chứng hỗ trợ | Hiệu ứng khi bỏ (đo được / dự kiến) |
|---|---|---|---|---|---|
| Dependency-path indirection | che quan hệ import trực tiếp | import lộ quan hệ cross-file | file mục tiêu → file + 4 tầng proxy | Figure 3: GPT-5 65.0 → 60.0; DeepSeek 70.0 → 64.0; Gemini 70.6 → 70.0; MiniMax 78.2 → 74.4 [Paper: PDF p. 5, Figure 3] | Đo được (ablation đơn lẻ): giảm nhỏ nhất ở Gemini |
| Runtime-target masking | tách cue tên file khỏi file thực thi | tên file làm định vị quá dễ | file → wrapper + file đổi tên + fake files | Figure 3: 58.2 / 58.2 / 60.2 / 67.2 (GPT-5 / DeepSeek / Gemini / MiniMax) [Paper: PDF p. 5, Figure 3] | Đo được: perturbation đơn mạnh nhất ở cả 4 model |
| Local-value externalization | đẩy hằng số ra JSON | giá trị cục bộ cho phép hiểu trong 1 file | hằng số → `dep[...]` + JSON | Figure 3: 61.4 / 67.6 / 68.0 / 69.0 [Paper: PDF p. 5, Figure 3] | Đo được: giảm nhỏ với DeepSeek, Gemini |
| Kết hợp 3 perturbation | — | kiểm tra tính bổ sung | — | All: 49.0 / 52.0 / 54.4 / 65.4 [Paper: PDF p. 5, Figure 3] | Thấp hơn mọi perturbation đơn |
| Task Extend + checker | chuyển nút thắt thành mục tiêu tường minh | đo trực tiếp thay vì gián tiếp | repository Perturb + xóa thành phần → checker xác định | Table 2 [Paper: PDF p. 7, Table 2] | Không có ablation |
| Structural hints | cung cấp mô tả cơ chế perturbation | kiểm tra giả thuyết "thiếu scaffold" | prompt chung → resolved rate | Table 3 [Paper: PDF p. 8, Table 3] | — |
| RepoAnchor | tách exploration (viết INSTRUCTION.md) khỏi giải | biến khám phá thành cấu trúc dùng được | task → INSTRUCTION.md → patch | Figure 7: avg +17.0 / +16.0 / +7.2 / +8.6 điểm (GPT-5 / DeepSeek / MiniMax / Gemini) [Paper: PDF p. 9, Figure 7] | Không có ablation bên trong (vd. chỉ tăng budget, hay không có prompt "runtime evidence") |

## 09 Công thức và ký hiệu thiết yếu

- **Xác suất chuyển trạng thái hành động:** `p_{a→b} = #(a→b) / Σ_{s∈S} #(a→s)`, với `a, b ∈ {explore, edit, test}` [Paper: PDF p. 7, Section 5.1].
  - Ký hiệu: `#(a→b)` = số lần hành động `a` theo sau bởi `b` trong một trajectory.
  - Mục đích: đo agent có "kẹt" trong explore (explore→explore tăng) hay chuyển sang edit.
  - Trực giác: hàng của ma trận chuyển Markov ước lượng từ đếm.
  - Ghi chú: ma trận tính cho từng trajectory rồi tổng hợp qua instance [Paper: PDF p. 16, Appendix A.6]; cách tổng hợp (trung bình ma trận hay gộp đếm) không nêu rõ.
- **Drop / Ratio trong Table 1:** Drop = (Perturb − SWE-Bench)/SWE-Bench; Ratio = Avg. #Files Perturb / SWE-Bench (suy ra từ số liệu, vd. GPT-5: (49−65)/65 = −24.6%) [Paper: PDF p. 5, Table 1].

## 10 Thiết kế thực nghiệm và chuỗi bằng chứng

**Thiết lập chung.**
- Dataset: 500 instance SWE-Bench Verified; Extend chia Multi-File 70 (14.0%), Proxy Chain 144 (28.8%), Runtime Target 142 (28.4%), Missing Constant 144 (28.8%) [Paper: PDF p. 6, Figure 4].
- Model: GPT-4.1, GPT-5, Gemini-3.1-Pro, Claude-Sonnet-4.6, DeepSeek-V3.2, MiniMax-M2.7, Qwen3-Coder-Next, Qwen3.6-35B-A3B [Paper: PDF p. 14, Appendix A.3].
- Agent: mini-swe-agent bash-only, 250 bước; Qwen chạy vLLM trên 4× A800 [Paper: PDF p. 14, Appendix A.1-A.2].
- Metric: resolved rate (test chính thức hoặc checker xác định), số file được mở (đã chuẩn hóa, loại file tạm), tỷ lệ bước trước edit đầu tiên, Δp chuyển trạng thái [Paper: PDF p. 16, Appendix A.6].
- Không báo cáo số lần chạy lặp, seed, chi phí token, hay khoảng tin cậy cho resolved rate.

| Thí nghiệm | Claim được kiểm tra | So sánh và điều kiện | Kết quả | Kết luận được hỗ trợ | Kết luận mạnh hơn không được hỗ trợ | Nguồn |
|---|---|---|---|---|---|---|
| File access trên SWE-Bench | thành công mang tính cục bộ | instance đã giải, GPT-5 / DeepSeek-V3.2 | GPT-5: 53.8% chỉ 1 file, 88.0% ≤ 3; DeepSeek: 55.7% ≤ 3 | thành công thường đạt sau khi đọc ít file | ít file ⇒ không suy luận cross-file (có thể đã đủ thông tin) | [Paper: PDF p. 3, Figure 2] |
| RepoMirage-Perturb | thành công không bền khi tăng nhu cầu context | 8 model, gốc vs Perturb, cùng task | 66.80% → 49.78%; drop từ −15.96% (Claude-Sonnet-4.6) đến −52.60% (GPT-4.1); file 4.77 → 13.24 | resolved rate giảm nhất quán cho cả 8 model trong điều kiện này | giảm chỉ do thiếu reasoning (có thể do artefact/nhiễu, chi phí budget) | [Paper: PDF p. 5, Table 1] |
| Ablation perturbation | ba perturbation bổ sung cho nhau | 4 model, từng perturbation vs All | All thấp nhất; masking mạnh nhất | mỗi perturbation đơn lẻ đều giảm ở 4 model; kết hợp giảm nhiều hơn | "bổ sung" theo nghĩa nhắm vào năng lực khác nhau (chưa có phân tích tương tác) | [Paper: PDF p. 5, Figure 3] |
| RepoMirage-Extend | năng lực repository context reasoning thấp khi đo tường minh | Org. (cùng subset) vs Extend | trung bình 66.80% → 25.25%; Proxy Chain 17.19%, Multi-File 17.86%, Runtime 28.26%, Missing Constant 33.94% | task Extend khó hơn nhiều; xếp hạng model thay đổi (MiniMax-M2.7: 78.20 → 14.80 avg) | so sánh Org. vs Extend đo cùng năng lực (task khác nhau, mục tiêu khác) | [Paper: PDF p. 6-7, Table 2] |
| Trajectory (Extend) | exploration drift | Δ Extend − Origin, GPT-5 / DeepSeek | Files inspected Δ̄ +18.71 / +15.45; explore stage +0.44 / +0.26; explore→explore +0.17 / +0.12; explore→edit −0.04 / −0.09 | agent đọc nhiều hơn, ở lâu hơn trong explore | explore không chuyển thành edit *vì* không tổ chức được cấu trúc (tương quan, không nhân quả) | [Paper: PDF p. 7, Figure 5] |
| Trajectory (Perturb) | drift cũng có khi task không đổi | Δ Perturb − Origin | Files Δ̄ +4.21 / +9.69; explore→edit −0.05 / −0.04 | xu hướng nhất quán | — | [Paper: PDF p. 19, Figure 11] |
| Heatmap theo task (GPT-5) | khác biệt theo task family | 4 task | explore→explore +0.08 đến +0.12; test→explore +0.42 ở Missing Constant | mỗi task có kiểu dịch chuyển khác | — | [Paper: PDF p. 20, Figure 12] |
| Structural hints | nút thắt là tổ chức cấu trúc | GPT-5, DeepSeek-V3.2, có/không hints | GPT-5 27.60 → 62.60 (Proxy 11.11 → 81.94); DeepSeek 39.80 → 76.80 (Proxy 11.80 → 86.11); Multi-File chỉ +2.86 / +4.29 | biết cơ chế perturbation giúp mạnh trên task dẫn xuất | hints "xấp xỉ kết quả exploration lý tưởng" (hints tiết lộ quy ước tạo sinh như tiền tố `proxy_`, `dependency_`) | [Paper: PDF p. 8, Table 3] [Paper: PDF p. 17, Figure 8] |
| RepoAnchor | scaffolding structure-first giúp | 4 model, gốc vs RepoAnchor trên Extend | avg GPT-5 27.6 → 44.6; DeepSeek 39.8 → 55.8; MiniMax 14.8 → 22.0; Gemini 41.4 → 50.0; Multi-File GPT-5 25.7 → 40.0 (> hints 28.57) | tăng nhất quán trên mọi ô | gain do "structure" chứ không do thêm bước / tách ngữ cảnh / prompt "runtime evidence" | [Paper: PDF p. 9, Figure 7] |

## 11 Diễn giải đúng các kết luận

- **Phạm vi task:** chỉ Python, chỉ SWE-Bench Verified, chỉ một agent framework (mini-swe-agent bash-only) [Paper: PDF p. 20, Appendix C.1] [Paper: PDF p. 14, Appendix A.2].
- **Oracle / ground truth:** Perturb dùng test chính thức; Extend dùng checker xác định từ quá trình xây dựng (so sánh module được resolve, file wrapper trỏ tới, key JSON sau merge) [Paper: PDF p. 15-16, Appendix A.5].
- **End-to-end:** Perturb là end-to-end; ba task Extend là task tổng hợp có cấu trúc định sẵn, không phải tình huống tự nhiên.
- **Chi phí tính toán:** không báo cáo chi phí token / số bước trung bình; việc đọc nhiều file hơn có thể làm cạn budget 250 bước — không được phân tích.
- **Phụ thuộc model:** xếp hạng model thay đổi mạnh giữa Org. và Extend (MiniMax-M2.7) [Paper: PDF p. 6, Section 4.2].
- **Ca khó nhất:** Proxy Chain Completion (GPT-4.1 4.17%, MiniMax 7.64%) [Paper: PDF p. 7, Table 2].
- **Bất định:** không có khoảng tin cậy hay lặp; khác biệt nhỏ (vd. Indirect của Gemini 70.6 → 70.0) có thể nằm trong nhiễu.

**Phát biểu bị giới hạn:** Trên các instance Python của SWE-Bench Verified với mini-swe-agent, ba biến đổi bảo toàn hành vi (theo test) làm resolved rate trung bình giảm ~17 điểm phần trăm và làm agent đọc gấp ~2.8 lần số file; các task tường minh dẫn xuất từ những biến đổi này chỉ đạt ~25%; và việc cung cấp mô tả cấu trúc (hints) hoặc tách stage khám phá (RepoAnchor) cải thiện kết quả — nhất quán với, nhưng chưa chứng minh, giả thuyết rằng nút thắt là tổ chức thông tin cấu trúc.

## 12 Hạn chế được tác giả thừa nhận rõ ràng

| Hạn chế | Biểu hiện cụ thể | Hướng tương lai tác giả đề xuất | Nguồn |
|---|---|---|---|
| Chỉ Python | perturbation cấp repository phức tạp về kỹ thuật; Python thuận tiện cho syntax-tree transform và runtime validation | mở rộng sang ngôn ngữ có build system / ràng buộc biên dịch chặt hơn | [Paper: PDF p. 20, Appendix C.1] |
| Định dạng task cổ điển | agent sửa repository để thỏa mục tiêu | code review, repository-level test generation, refactoring, maintenance | [Paper: PDF p. 20, Appendix C.1] |

**Related constraints noted by the authors** (không được bài trình bày như hạn chế chính thức):
- RepoAnchor được gọi là "prototype" / "initial mitigation" [Paper: PDF p. 8, Section 5.3].
- Dependency-path indirection chỉ áp cho absolute import độc lập layout repository, tránh lỗi relative import [Paper: PDF p. 14, Appendix A.4].
- Phân tích trajectory chính chỉ trên GPT-5 và DeepSeek-V3.2 [Paper: PDF p. 3, Section 2.1].
- Broader impacts: agent mạnh hơn có thể bị lạm dụng hoặc quá tin cậy [Paper: PDF p. 20, Appendix C.2].

## 13 Phân tích phản biện

| `[Analysis]` Quan sát | Vấn đề tiềm ẩn / giải thích thay thế | Vì sao quan trọng | Cách kiểm tra | Cơ sở |
|---|---|---|---|---|
| Hints nêu tiền tố `proxy_`, `dependency_`, "decoy files", wrapper folder | gain lớn (Proxy 11 → 82) có thể đến từ việc biết *quy ước tạo sinh của benchmark*, không phải từ năng lực tổ chức cấu trúc chung | giả thuyết "nút thắt là tổ chức cấu trúc" dựa chủ yếu vào thí nghiệm này | hints chỉ mô tả trừu tượng (không tên file/tiền tố); hoặc đổi tên proxy ngẫu nhiên; so sánh gain | [Paper: PDF p. 17, Figure 8] [Paper: PDF p. 8, Table 3] |
| Multi-File hầu như không hưởng lợi từ hints (+2.86 / +4.29) | ba task dẫn xuất có thể đo khả năng "giải câu đố tổng hợp" nhiều hơn reasoning repository tự nhiên | giới hạn validity của Extend | tương quan Extend-score với các benchmark multi-file độc lập | [Paper: PDF p. 8, Table 3] |
| Tên file perturb vô nghĩa (`flux_cinder_hh.py`), fake files, proxy layers | biến đổi tạo phân phối code "bất thường"; sụt giảm có thể một phần do OOD/obfuscation chứ không chỉ do thiếu cross-file reasoning | tác giả khẳng định không đo robustness to obfuscation | điều kiện đối chứng: chỉ đổi tên file (không wrapper), hoặc thêm file nhiễu không liên quan cùng số lượng | [Paper: PDF p. 21, Figure 13] [Paper: PDF p. 15, Appendix A.4] |
| Số file tăng gần 3× nhưng budget cố định 250 bước | lỗi có thể do cạn budget / dài context, không phải do không suy luận được | ảnh hưởng tới diễn giải exploration drift | báo cáo tỷ lệ chạm giới hạn bước; chạy lại với budget 500 | [Paper: PDF p. 14, Appendix A.2] [Paper: PDF p. 5, Table 1] |
| Exploration drift đo bằng tương quan Δ trajectory | explore→explore tăng có thể là hệ quả tự nhiên của task cần nhiều đọc hơn, không phải "drift" bất lợi | nhãn "drift" mang tính diễn giải | so sánh trajectory instance thành công vs thất bại trong cùng điều kiện | [Paper: PDF p. 7, Figure 5] |
| RepoAnchor không có ablation | gain có thể do thêm một lượt chạy (gấp đôi budget), do context sạch ở stage 2, hoặc do prompt khuyến khích runtime evidence | không tách được cơ chế "structure" | ablation: hai lượt chạy không có INSTRUCTION.md; một lượt với prompt "runtime evidence" | [Paper: PDF p. 9, Figure 7] [Paper: PDF p. 18, Figure 9] |
| Bảo toàn ngữ nghĩa chỉ kiểm bằng test | PASS_TO_PASS/FAIL_TO_PASS chỉ phủ hành vi được test; nạp động bằng `spec_from_file_location` có thể đổi hành vi ngoài test (pickling, `__module__`, reload) | tuyên bố "semantics-preserving" mạnh hơn bằng chứng | so sánh call graph / tracing thực thi trước–sau, hoặc chạy thêm test suite đầy đủ | [Paper: PDF p. 14, Appendix A.4] [Paper: PDF p. 21, Figure 13] |
| Không có lặp lại / CI | khác biệt nhỏ (Gemini Indirect −0.6) có thể là nhiễu | claim "mỗi perturbation đều giảm" | chạy ≥3 seed, bootstrap CI | [Paper: PDF p. 5, Figure 3] |
| Lệch số nhỏ | "giảm tương đối 27.0% trung bình" vs trung bình cột Drop ≈ 27.24%; Qwen3.6-35B-A3B Org. 72.41 (n=142) và 68.00 (n=144) không ứng với số nguyên instance | có thể có instance thiếu / lỗi chạy | yêu cầu số liệu thô từng instance | [Paper: PDF p. 2, Introduction] [Paper: PDF p. 5, Table 1] [Paper: PDF p. 7, Table 2] |

**Đánh giá chồng lấn với hướng của người dùng `[Analysis]`** (tách khỏi phát biểu tác giả):

1. **RepoMirage có kiểm soát VỊ TRÍ code liên quan trong context không?** Không. Agent tương tác qua shell, tự quyết định đọc file nào; không có context cố định nên không có biến "vị trí token" [Paper: PDF p. 14, Appendix A.2]. Biến điều khiển là *độ sâu / phân tán cấu trúc* (4 tầng proxy, số file JSON, số fake file) [Paper: PDF p. 4, Section 3.1] [Paper: PDF p. 15, Appendix A.4], và biến kết quả là số file mở, không phải vị trí trong cửa sổ. Hiệu ứng vị trí kiểu lost-in-the-middle vì vậy *không được đo*.
2. **Đo semantic (hành vi thực thi) hay chỉ retrieval/định vị?** Lai, thiên về định vị cấu trúc. Runtime Target Identification yêu cầu chỉ ra file đúng (checker kiểm tra wrapper trỏ đúng), dù fake files khác biệt có ý nghĩa hành vi (đảo điều kiện bool, đổi alias, lệch key) [Paper: PDF p. 15, Appendix A.5]. Proxy Chain Completion đo resolve import — quan hệ phụ thuộc, không phải ngữ nghĩa giá trị [Paper: PDF p. 15, Appendix A.5]. Missing-Constant Recovery gần semantic nhất (suy vai trò giá trị từ loop control, index offset) [Paper: PDF p. 15-16, Appendix A.5]. Không có task dự đoán output/trạng thái thực thi kiểu CRUXEval/SemTrace; Multi-File chấm bằng test end-to-end.
3. **Perturbation có giữ nguyên ngữ nghĩa không?** Theo tác giả, có — kiểm bằng PASS_TO_PASS và gold patch + FAIL_TO_PASS [Paper: PDF p. 14, Appendix A.4]; fake files cố ý khác ngữ nghĩa nhưng không bao giờ được thực thi [Paper: PDF p. 15, Appendix A.4]. Bảo toàn là *test-based*, không phải tương đương hình thức.
4. **Có dùng phân tích tĩnh làm oracle không?** Không theo nghĩa oracle. LibCST chỉ dùng để *xây dựng* perturbation [Paper: PDF p. 14, Appendix A.4]; checker là script xác định dựa trên tri thức xây dựng (resolve import, merge JSON), dựa vào thực thi chứ không dùng call graph / data flow / symbolic execution để kiểm hiểu biết của agent [Paper: PDF p. 15-16, Appendix A.5]. Không có đo lường agent "hiểu" quan hệ nào (chỉ pass/fail cuối).

## 14 Kiến thức thu được

**Agent-derived knowledge candidates**

- **Thiết kế "cùng instance, khác exposure":** giữ task/test, chỉ biến đổi cách lộ thông tin → so sánh cặp có đối chứng; áp dụng được cho mọi benchmark có test thực thi [Paper: PDF p. 2, Introduction].
- **Kiểm tra bảo toàn 2 phía:** PASS_TO_PASS sau perturb + (gold patch → perturb → FAIL_TO_PASS) — mẫu xác nhận rẻ cho biến đổi code [Paper: PDF p. 14, Appendix A.4].
- **Chuyển nút thắt thành task có checker:** xóa một thành phần đã biết (proxy, wrapper ref, key) và chấm bằng tái dựng chức năng chứ không bằng khớp chuỗi [Paper: PDF p. 15, Appendix A.5].
- **Metric trajectory:** ma trận chuyển explore/edit/test và tỷ lệ bước trước edit đầu tiên [Paper: PDF p. 16, Appendix A.6].
- **Can thiệp hints như phép thử chẩn đoán:** cung cấp "kết quả lý tưởng" của một giai đoạn để xem nút thắt nằm trước hay sau giai đoạn đó [Paper: PDF p. 8, Section 5.2] — cần cẩn thận rò rỉ thông tin (Section 13).

## 15 Liên hệ với tri thức hiện có

Context mode: paper-only — các liên hệ dưới đây là ứng viên, chưa kiểm chứng ngoài.

- **`[User]` / `[Analysis]` So với "Sense and Sensitivity" (arXiv 2505.13353, card ở `cards/2505.13353v5/paper-card.md`):** bài đó kiểm soát vị trí hàm mục tiêu trong context tĩnh và đo semantic recall bằng output prediction; RepoMirage không kiểm soát vị trí, dùng agent tương tác, đo định vị/tái dựng cấu trúc cross-file và issue resolution. Hai bài *bổ sung* nhau: RepoMirage cho thấy agent mở nhiều file hơn (4.77 → 13.24) [Paper: PDF p. 5, Table 1] — tức context tích lũy dài hơn và thông tin liên quan có thể rơi vào "giữa" lịch sử hội thoại, đúng vùng mà Sense and Sensitivity báo semantic recall suy giảm. Không bài nào đo giao nhau này.
- **Tương đồng (paper-framed):** perturbation code như variable renaming để kiểm phụ thuộc pattern bề mặt [Paper: PDF p. 9, Related Work 6.2].
- **Kết hợp `[Hypothesis]`:** checker của RepoMirage là ground truth do xây dựng; phân tích chương trình (call graph, def-use / data flow) có thể đóng vai trò oracle *trung gian* — chấm xem INSTRUCTION.md của RepoAnchor (Figure 13) có nêu đúng các cạnh phụ thuộc không, thay vì chỉ chấm pass/fail cuối [Paper: PDF p. 21, Figure 13].
- **Mâu thuẫn tiềm năng `[Analysis]`:** RepoMirage quy lỗi cho "tổ chức cấu trúc"; Sense and Sensitivity quy cho suy giảm semantic recall theo vị trí. Với agent, hai giải thích có thể chồng lên nhau và RepoMirage không có thiết kế để phân biệt.
- **Miền chuyển giao:** ngôn ngữ biên dịch (Java/C++) được tác giả nêu [Paper: PDF p. 20, Appendix C.1]; các task code review / test generation.

## 16 Ý tưởng nghiên cứu

**Agent-derived research candidates** (hypotheses; prior-art search required)

### Ứng viên 1 — Vị trí × độ sâu cấu trúc: tách "lost-in-the-middle" khỏi "thiếu tổ chức cấu trúc" ở quy mô repository

- **Nguồn gốc (quan sát):** Perturb làm agent mở ~2.8× số file và tăng explore [Paper: PDF p. 5, Table 1] [Paper: PDF p. 7, Figure 5]; hints giúp rất mạnh [Paper: PDF p. 8, Table 3]; nhưng bài không kiểm soát vị trí của nội dung liên quan trong context (Section 13, mục 1).
- **Giả thuyết cốt lõi:** Một phần đáng kể sụt giảm dưới perturbation là do nội dung file quyết định (file runtime thật, proxy cuối, JSON chứa key) bị đẩy vào giữa lịch sử context dài; nếu giữ cùng cấu trúc perturbation nhưng đặt các nội dung đó ở đầu/cuối context, độ chính xác trên task có đáp án ngữ nghĩa (output prediction) sẽ phục hồi nhiều hơn so với task định vị (chỉ ra tên file).
- **Delta so với bài (evaluation + representation):** chuyển từ agent tương tác sang "repository snapshot" tĩnh dựng từ trajectory/perturbation RepoMirage; điều khiển vị trí (11 vị trí) × độ sâu proxy (1–4 tầng) × loại câu hỏi (định vị vs dự đoán output của hàm mục tiêu trên input cho trước).
- **Phương pháp ban đầu:** lấy instance RepoMirage-Perturb; nối các file liên quan + file nhiễu cùng repository thành context 16k–64k token; sinh câu hỏi output prediction bằng cách chạy thật hàm mục tiêu (oracle thực thi).
- **Validation:** hồi quy logistic accuracy ~ vị trí × độ sâu × loại câu hỏi; kỳ vọng tương tác vị trí × semantic âm có ý nghĩa; **bác bỏ:** đường cong vị trí phẳng cho cả hai loại câu hỏi, hoặc độ sâu giải thích toàn bộ phương sai.
- **Possible failure modes:** (1) context tĩnh mất bản chất agent — kết quả có thể không chuyển sang agent; (2) tên file vô nghĩa và proxy làm câu hỏi định vị trở nên tầm thường hoặc bất khả, che mất hiệu ứng vị trí; (3) chi phí context dài × 11 vị trí × nhiều model.
- **Innovation status:** unverified — prior-art search required.

### Ứng viên 2 — Oracle phân tích chương trình cho "hiểu cấu trúc" trung gian của agent

- **Nguồn gốc (hạn chế):** checker chỉ chấm pass/fail cuối; bảo toàn ngữ nghĩa chỉ dựa trên test [Paper: PDF p. 14, Appendix A.4] [Paper: PDF p. 15-16, Appendix A.5]; INSTRUCTION.md có chứa phát biểu cấu trúc kiểm chứng được nhưng không được chấm [Paper: PDF p. 21, Figure 13].
- **Giả thuyết cốt lõi:** Độ chính xác của các phát biểu cấu trúc trong INSTRUCTION.md (cạnh import/call/def-use) đối chiếu với call graph và data-flow tĩnh sẽ dự báo thành công ở stage 2 tốt hơn số file đã mở; và lỗi tập trung ở cạnh data-flow (giá trị JSON → điều khiển vòng lặp) hơn cạnh import.
- **Delta so với bài (evaluation + feedback):** thêm oracle tĩnh (vd. call graph Python, def-use qua JSON load) chấm precision/recall từng cạnh agent khẳng định; tùy chọn dùng sai lệch cạnh làm feedback cho stage 1 của RepoAnchor.
- **Phương pháp ban đầu:** trích cạnh từ INSTRUCTION.md bằng parser có cấu trúc (format cố định ở Figure 9); dựng đồ thị ground truth từ metadata perturbation + phân tích tĩnh; thêm kiểm tra tracing thực thi để xác nhận bảo toàn ngữ nghĩa ngoài test.
- **Validation:** AUC dự báo thành công từ edge-F1 vs từ số file mở; thí nghiệm can thiệp: sửa các cạnh sai trong INSTRUCTION.md rồi chạy lại stage 2 — kỳ vọng gain tỷ lệ với số cạnh sửa; **bác bỏ:** edge-F1 không dự báo tốt hơn số file, hoặc sửa cạnh không cải thiện.
- **Possible failure modes:** (1) phân tích tĩnh không resolve được nạp động (`spec_from_file_location`) — cần kết hợp metadata xây dựng, làm oracle phụ thuộc benchmark; (2) trích cạnh từ ngôn ngữ tự nhiên gây nhiễu đo lường; (3) gain từ sửa cạnh có thể chỉ là rò rỉ đáp án (tương tự vấn đề của hints).
- **Innovation status:** unverified — prior-art search required.
