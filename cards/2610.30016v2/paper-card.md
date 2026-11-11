# Paper Card — Code Comprehensor: Hierarchical Documentation and Cross-Modal Retrieval for Large Repositories

> Phạm vi nguồn (Source coverage): Full paper (11 trang PDF, gồm Figure 1–5, Table I–III, Equation 1–3, tài liệu tham khảo; không có supplementary material)
> Độ tin cậy trích xuất (Extraction confidence): High (PyMuPDF, validation = valid; trang được đối chiếu trực quan qua ảnh trang PDF)
> Locator mode: page-grounded (mọi con trỏ dùng chỉ số trang PDF; bài không có printed page label)
> Primary analytical lens: methods (hệ thống / framework)
> Secondary analytical lens: None (dữ liệu huấn luyện D1–D3 là phương tiện của phương pháp, không phát hành như tài nguyên độc lập)
> Context verification: Paper-only (không kiểm chứng ngoài; lịch sử lĩnh vực ở Section 04 là paper-framed)
> Card completeness: Complete relative to supplied source

**Ngày đọc:** 2026-11-06. **Ghi chú trích xuất:** script `prepare_paper.py` nhận diện 5 figure và 3 equation nhưng không nhận diện được Table I–III (cùng nằm ở PDF p. 9); ba bảng này được kiểm kê thủ công từ ảnh trang.

### Terminology Ledger (khóa thuật ngữ dùng trong card)

| Thuật ngữ chuẩn | Định nghĩa lần đầu | Biến thể trong bài | Quyết định |
|---|---|---|---|
| Code Comprehensor | Toàn bộ framework retrieval–reasoning | — | giữ nguyên |
| CodeGraph | Call graph sinh từ static analysis, phơi qua FastAPI | "Code Graph" (Figure 1) | dùng "CodeGraph" |
| CodeScribe | Engine sinh hierarchical documentation theo cây thư mục | — | giữ nguyên |
| SynTD | Synthesized Technical Descriptions — đầu ra của CodeScribe | "Synthesized Technical Descriptions" | viết đầy đủ một lần rồi dùng SynTD |
| CodeContrast | Dual-encoder kiểu CLIP, multi-positive InfoNCE | "contrastive model", "CM agent" | dùng "CodeContrast" |
| MA | Master Agent — LLM orchestrator qua MCP gateway | "Master Agent" | dùng "MA" |
| MCP | Model Context Protocol | — | giữ nguyên |
| D1 / D2 / D3 | Ba cấu hình giám sát văn bản tăng dần | — | giữ nguyên |
| Repo-A | Kho mã C độc quyền >5M LOC | — | giữ nguyên |
| AC / FF | Answer Correctness / Faithfulness (RAGAS) | — | giữ nguyên |
| t→c / c→t | Text→Code / Code→Text retrieval | "text→code", "c→t" | dùng "Text→Code", "Code→Text" |

---

## 01 Thông tin cơ bản

| Trường | Nội dung |
|---|---|
| Tiêu đề | Code Comprehensor: Hierarchical Documentation and Cross-Modal Retrieval for Large Repositories [Paper: PDF p. 1, Title] |
| Tác giả | Sujoy Roychowdhury, Joseph H. R. Isaac, Jiangning Gao, Martin Klitte, Diarmuid Corcoran [Paper: PDF p. 1, Title block] |
| Đơn vị | Ericsson R&D [Paper: PDF p. 1, Title block] |
| Venue / năm | arXiv preprint, cs.SE, v2 ngày 22 Oct 2026 [Paper: PDF p. 1, arXiv stamp]; chưa thấy thông tin hội nghị/tạp chí |
| Định danh | arXiv:2610.30016v2 |
| Loại bài | methods (hệ thống tích hợp + đánh giá thực nghiệm) |
| Lĩnh vực | Software engineering; code comprehension; semantic code retrieval; LLM agent |
| Từ khóa | LLMs, code comprehension, semantic code retrieval, contrastive learning, CLIP-style encoders, repository analysis, program analysis, hybrid retrieval-reasoning [Paper: PDF p. 1, Index Terms] |
| Code / dataset | Không công bố code; Repo-A là độc quyền; OpenCV là công khai [Paper: PDF p. 8, Section V-B] |
| Vị trí trong hướng nghiên cứu của người dùng | Not assessable — người dùng chưa cung cấp; liên quan trực tiếp tới chủ đề phân tích chương trình (call graph + LLM) của đề tài |

## 02 Tóm tắt một câu

Để giúp LLM hiểu kho mã rất lớn, bài xây dựng CodeGraph (call graph tĩnh), dùng CodeScribe sinh tài liệu phân cấp bằng LLM với chunking post-order trên cây DFS, rồi huấn luyện CodeContrast (dual-encoder multi-positive InfoNCE) trên tài liệu đó cho một MA qua MCP; trên OpenCV và Repo-A, thêm ngữ cảnh parent/sibling và câu hỏi tổng hợp (D3) nâng Top-1 Text→Code trên tập synthetic từ 66.05% lên 80.64% (OpenCV) và 67.46% lên 76.18% (Repo-A) so với D2, còn MA đạt Faithfulness 93.4–94.6% theo RAGAS [Paper: PDF p. 9, Table I, Table III].

## 03 Câu hỏi nghiên cứu

- **Vấn đề cụ thể:** kho mã doanh nghiệp lớn (hàng triệu LOC) khó tài liệu hóa và khó đưa vào LLM; LLM cần hiểu không chỉ một method mà cả các method liên quan trong toàn kho [Paper: PDF p. 1, Abstract, Section I].
- **Tại sao quan trọng:** ảnh hưởng onboarding, bảo trì, refactoring, impact analysis; context window lớn vẫn tốn chi phí và được dẫn là cho kết quả kém hơn; mã trùng lặp khiến LLM thiếu tin cậy/khó lặp lại [Paper: PDF p. 1, Section I].
- **Vì sao cách hiện có chưa đủ (theo tác giả):** tài liệu hóa dựa AST/call graph chỉ cho tài liệu tĩnh; contrastive code search thiếu tài liệu miền sâu nên kém trên kho lớn; CodeRetriever/CoCoSoDa không có bản C/C++ công khai [Paper: PDF p. 1, Section I] [Paper: PDF p. 3, Section II-D].
- **Câu hỏi dạng Can…?** `[Analysis]` Liệu tài liệu phân cấp do LLM sinh theo call graph (cùng ngữ cảnh parent/sibling và câu hỏi tổng hợp) có thể làm tín hiệu giám sát đủ tốt để một dual-encoder truy hồi chính xác method trong kho C/C++ hàng triệu LOC, và làm nền cho một agent trả lời câu hỏi trung thực (faithful)?

## 04 Bối cảnh nghiên cứu và lộ trình phát triển

`[Paper-framed; external verification not performed]`

| Giai đoạn / hướng | Đại diện (theo bài) | Ưu điểm | Hạn chế (theo bài) | Nguồn |
|---|---|---|---|---|
| Neural code search | context-aware translation, meta-learning, cross-language, query reformulation, fusion | kết hợp embedding text–code | làm trên snippet rời rạc | [Paper: PDF p. 2, Section II-A] |
| Contrastive pre-training cho code | text/code embeddings (Neelakantan), CodeRetriever, CoCoSoDa | embedding căn chỉnh text–code | thiếu tài liệu miền; chủ yếu Python/Java | [Paper: PDF p. 3, Section II-C, Section II-D] |
| Repository-level documentation | RepoAgent, CodeWiki, hierarchical engine (Code-Craft) | tài liệu ở mức kho | chỉ sinh tài liệu, cần LLM mỗi truy vấn | [Paper: PDF p. 2–3, Section II-B, Section II-D] |
| Vị trí tự nhận của bài | Code Comprehensor | dùng tài liệu sinh ra làm tín hiệu huấn luyện retriever; chunking post-order cho cây lớn | — | [Paper: PDF p. 3, Section II-D] |

## 05 Pain points cốt lõi được bài nêu

| Pain point | Biểu hiện | Nguyên nhân / giải thích của tác giả | Bằng chứng trong bài |
|---|---|---|---|
| Kho mã quá lớn cho context | Kho >5M LOC; cây DFS vượt context window | token lớn, chi phí, context dài cho kết quả kém hơn | Lập luận + trích dẫn [7], [8]; không có thí nghiệm riêng [Paper: PDF p. 1, Section I] [Paper: PDF p. 4, Section IV-B] |
| Mã trùng lặp làm LLM thiếu ổn định | file/method/biến giống nhau ở nhiều nơi | LLM là cơ chế xác suất | Lập luận, không đo [Paper: PDF p. 1, Section I] |
| Tài liệu thưa / lỗi thời | thiếu comment, tài liệu cũ, viết tắt miền | đặc thù kho lớn | Động cơ cho synthetic data; không đo mức thiếu [Paper: PDF p. 5, Section IV-D] |
| Truy hồi trên snippet rời rạc | không nắm quan hệ giữa method | thiếu ngữ cảnh call graph | Gián tiếp qua D2→D3 trên synthetic [Paper: PDF p. 9, Table I, Table II] |
| Truy vấn thực là câu hỏi, không phải mô tả | lệch phân phối truy vấn | — | Động cơ cho câu hỏi tổng hợp [Paper: PDF p. 5, Section IV-D] |

## 06 Ý tưởng cốt lõi

1. **Phương pháp bề mặt:** pipeline CodeGraph → CodeScribe → parser → synthetic QA → CodeContrast → MA qua MCP [Paper: PDF p. 2, Figure 1].
2. **Insight cốt lõi:** biến tài liệu phân cấp mà LLM sinh theo cấu trúc call graph thành *tín hiệu giám sát one-to-many* (nhiều text view cho một code unit) cho retriever, để lúc suy luận chỉ cần một forward pass thay vì gọi LLM mỗi truy vấn [Paper: PDF p. 3, Section II-D] [Paper: PDF p. 7, Section IV-E].
3. **Bài học tổng quát:** `[Analysis]` một LLM đắt tiền chạy offline một lần trên cấu trúc chương trình có thể "chưng cất" hiểu biết cấu trúc vào một encoder rẻ; cấu trúc chương trình (parent/sibling) đóng vai trò nguồn positive/ngữ cảnh bổ sung cho contrastive learning.

## 07 Tổng quan phương pháp

- **Input:** Git repository (C/C++), prompt và file cấu hình theo thư mục (chapter, viết tắt, include/exclude) [Paper: PDF p. 3, Section III] [Paper: PDF p. 4, Section IV-B].
- **Output:** Markdown phân cấp kèm PlantUML; embedding text/code; câu trả lời ngôn ngữ tự nhiên của MA kèm diagram và code block [Paper: PDF p. 3, Section III].
- **Huấn luyện:** chỉ CodeContrast được huấn luyện (SBERT hoặc BERT backbone, FSDP, 4× A100, 15 epoch ≈ 24 giờ); LLM dùng nguyên (Sonnet 4.5 cho CodeScribe, Sonnet 4.0 cho các tác vụ sinh khác) [Paper: PDF p. 7, Section IV-E] [Paper: PDF p. 8, Section V-B, Section V-D].
- **Công cụ ngoài:** Tree-sitter, NetworkX, FastAPI, RAGAS [Paper: PDF p. 3, Section IV-A] [Paper: PDF p. 8, Section V-A].
- **Vòng phản hồi:** recursive synthesis (self-loop "S" trong Figure 1); cập nhật incremental theo git commit (Figure 2); người dùng hỏi tiếp MA [Paper: PDF p. 3, Section III] [Paper: PDF p. 4, Figure 2].
- **Giả định:** call graph tĩnh đủ chính xác (dependency giải bằng compile commands hoặc heuristic); tài liệu do LLM sinh đủ đúng để làm nhãn; truy vấn thực tế giống câu hỏi tổng hợp.

**Luồng:**
```text
Git repo -> static analysis (Tree-sitter) -> CodeGraph (NetworkX + FastAPI: BFS/DFS, invokes)
 -> CodeScribe: start methods (in-degree 0) -> DFS tree -> post-order chunking -> LLM (rolling summary)
 -> Markdown + PlantUML (SynTD) -> Markdown->JSON -> tách code/text -> phân loại block -> parent/sibling/module context
 -> synthetic questions (anchors) -> post-processing -> CodeContrast (dual-encoder, multi-positive InfoNCE)
 -> MA (MCP): CodeContrast agent + CodeGraph agent + CodeScribe RAG agent -> câu trả lời
```

## 08 Phân rã module cốt lõi

| Module | Chức năng | Vì sao cần | Input → Output | Bằng chứng hỗ trợ | Tác động khi bỏ (đo được / dự kiến) |
|---|---|---|---|---|---|
| CodeGraph | call graph tĩnh, node `method_name:::file_name[:::line]`, comment dev/LLM làm thuộc tính | cung cấp cây DFS và quan hệ cho CodeScribe, agent | mã nguồn → đồ thị NetworkX + API [Paper: PDF p. 3, Section IV-A] | Không có đánh giá độ chính xác call graph | Dự kiến: mất cấu trúc cho chunking và parent/sibling; chưa đo |
| CodeScribe + post-order chunking | sinh tài liệu theo chapter, chunk cây DFS bằng post-order, rolling summary của callee | cây vượt context window | cây DFS → Markdown/PlantUML [Paper: PDF p. 4, Section IV-B] | Chỉ đánh giá chủ quan (SME, so sánh định tính với CodeWiki, Figure 5) [Paper: PDF p. 8, Section V-C] | Không có ablation so với chunking khác; chưa đo |
| Incremental processing | tìm root methods bị ảnh hưởng theo git diff | tránh tái sinh toàn bộ | commit → tập root cần cập nhật [Paper: PDF p. 4, Figure 2] | Chỉ mô tả; nói chi phí "significantly less" không kèm số [Paper: PDF p. 8, Section V-D] | Chưa đo |
| Parser + relational features | Markdown→JSON, depth id (1.2.3), phân loại Code/UML/Pseudocode, parent/sibling/module context | tạo nhãn one-to-many | Markdown → bản ghi quan hệ [Paper: PDF p. 4–5, Section IV-C] | Gộp trong D3 [Paper: PDF p. 9, Table I] | Gộp chung với QA trong D3 nên không tách được (tác giả thừa nhận) |
| Synthetic question generation | 3 câu hỏi/method với BEHAVIOR/PARAM/CONTEXT/KEY anchors; lọc định dạng, trùng, thiếu anchor | khớp truy vấn dạng câu hỏi, bù tài liệu thưa | bản ghi → câu hỏi [Paper: PDF p. 5–6, Section IV-D, Figure 3] | Tập test synthetic dùng chính loại câu hỏi này [Paper: PDF p. 9, Table II] | Gộp trong D3; chưa tách |
| CodeContrast | dual-encoder, projection về chiều d, ℓ2-norm, global batch qua all-gather FSDP, multi-positive symmetric InfoNCE | truy hồi nhanh, không gọi LLM mỗi truy vấn | (text, code) → embedding [Paper: PDF p. 7, Section IV-E, Figure 4] | Table I; latency <50 ms [Paper: PDF p. 8, Section V-D] | Không có ablation global-batch hay multi-positive vs single-positive |
| MA (MCP orchestrator) | gọi CodeContrast/CodeGraph/CodeScribe agent, ghép câu trả lời | giao diện hỏi đáp trong IDE | câu hỏi → câu trả lời [Paper: PDF p. 3, Section III] | RAGAS AC/FF [Paper: PDF p. 9, Table III] | Không có so sánh MA với baseline (vd. RAG thuần, LLM không retrieval) |

## 09 Công thức và ký hiệu thiết yếu

**Equation 1 — Text→Code multi-positive InfoNCE** [Paper: PDF p. 7, Equation 1]

$$\mathcal{L}^{t\to c} = -\frac{1}{B}\sum_{i=1}^{B}\log\frac{\sum_{j\in P(i)}\exp(S_{ij})}{\sum_{j=1}^{B}\exp(S_{ij})}$$

- $B$: kích thước global batch; $S_{ij}$: độ tương đồng (cosine, có temperature) giữa text anchor $t_i$ và code $j$; $\ell_i$: nhãn lớp suy từ `id_i`; $P(i)=\{j \mid \ell_j=\ell_i\}$: tập positive.
- **Mục đích / trực giác:** một code unit có nhiều text view nên trong batch có thể có nhiều cặp dương; log-sum-exp gộp chúng thay vì coi các bản sao là negative.

**Equation 2 — Code→Text** [Paper: PDF p. 7, Equation 2]: cùng dạng, áp lên $S^\top$ (đổi vai trò text/code).

**Equation 3 — Mục tiêu đối xứng** [Paper: PDF p. 7, Equation 3]: $\mathcal{L}=\tfrac12(\mathcal{L}^{t\to c}+\mathcal{L}^{c\to t})$.

`[Analysis]` Bài không nêu giá trị temperature, chiều $d$, backbone cụ thể được dùng cho kết quả Table I, hay kích thước batch — các tham số này cần để tái lập.

## 10 Thiết kế thực nghiệm và chuỗi bằng chứng

**Thiết lập** [Paper: PDF p. 7–9, Section V]:
- **Dữ liệu:** OpenCV (~1.2M LOC, .c/.h/.cpp) và Repo-A (C độc quyền, >5M LOC, viễn thông) [Paper: PDF p. 8, Section V-B].
- **Chia tập:** held-out theo method; test non-synthetic (cặp code – mô tả gốc/LLM khi thiếu) và synthetic (thêm câu hỏi do LLM sinh) [Paper: PDF p. 7–8, Section V-A]. N: OpenCV 2813 / 12658; Repo-A 3800 / 23480 [Paper: PDF p. 9, Table I].
- **Cấu hình:** D1 = method + docstring (baseline); D2 = D1 + self-comments; D3 = D2 + parent/sibling + QA [Paper: PDF p. 8–9, Section V-E].
- **Metric:** Top-K accuracy hai chiều, Recall@K cho Code→Text [Paper: PDF p. 7, Section IV-E]; RAGAS AC (precision/recall/F1) và FF cho MA [Paper: PDF p. 8, Section V-A].
- **Baseline:** chỉ D1 (cấu hình nội bộ); không có baseline ngoài (CodeRetriever, CoCoSoDa, BM25, RepoAgent…) vì lý do thiếu bản C/C++ [Paper: PDF p. 3, Section II-D].
- **Ngân sách:** CodeScribe OpenCV ≈ 48 giờ, $3,200; Repo-A ≈ 8 ngày, "a few thousand USD"; huấn luyện 4× A100 ≈ 24 giờ; truy hồi <50 ms; MA 3–5 giây/truy vấn [Paper: PDF p. 8, Section V-D].
- **Độ bất định:** không có seed lặp, khoảng tin cậy hay kiểm định thống kê.

| Thí nghiệm | Claim kiểm tra | So sánh & điều kiện | Kết quả | Kết luận được hỗ trợ | Kết luận mạnh hơn KHÔNG được hỗ trợ | Nguồn |
|---|---|---|---|---|---|---|
| E1: D1 vs D2, non-synthetic | self-comments của CodeScribe giúp truy hồi | cùng test non-synthetic | Top-1 t→c: OpenCV 92.68→94.45; Repo-A 74.82→79.54. Top-1c c→t: 91.99→94.66; 74.21→79.28 | Thêm self-comments cải thiện Top-1 (≈+1.8 và +4.7 điểm) trong một lần chạy | "≥9% so với baseline" (claim ở contributions) không khớp với chênh lệch D1→D2 | [Paper: PDF p. 9, Table I] |
| E2: D2 vs D3, synthetic | parent/sibling + QA giúp truy vấn đa dạng | cùng test synthetic | Top-1 t→c: OpenCV 66.05→80.64 (+14.59); Repo-A 67.46→76.18 (+8.72). Top10 OpenCV 89.37→97.61 | D3 tốt hơn rõ trên test synthetic có cùng phân phối với dữ liệu huấn luyện QA | D3 tốt hơn với câu hỏi thật của developer; đóng góp riêng của parent/sibling | [Paper: PDF p. 9, Table I, Section VI] |
| E3: D2 vs D3 theo query type (OpenCV) | lợi ích phân bố theo loại truy vấn | 7 query type, function-name đã bị xóa khỏi câu hỏi | doc_brief_merged: D2 96.43 > D3 93.94; qa_doc_gen 57.39→78.38; qa_sibling 44.78→63.93; qa_parent 54.17→69.44 | Đánh đổi: D3 kém nhẹ trên mô tả người viết, tốt hơn nhiều trên câu hỏi tổng hợp | D3 vượt trội toàn cục | [Paper: PDF p. 9, Table II] |
| E4: Code→Text (Top-Kc, Recall@K) | hai chiều căn chỉnh | như trên | OpenCV synthetic: D2 Top1c 96.53 vs D3 93.67 (D3 thấp hơn); Repo-A D3 81.24 > D2 80.41 | Chiều Code→Text không nhất quán giữa hai kho | "Richer supervision consistently enhances performance" cho mọi chiều | [Paper: PDF p. 9, Table I] |
| E5: Kiểm tra rò rỉ | parent/sibling có thể chứa mã test | bỏ cross-reference tới test methods | Top-1 OpenCV đổi <1% | Rò rỉ qua ngữ cảnh có ảnh hưởng nhỏ trên OpenCV | Không rò rỉ trên Repo-A (không báo cáo) | [Paper: PDF p. 10, Section VII] |
| E6: MA RAGAS | MA trả lời trung thực | tập con câu hỏi synthetic; LLM-as-a-judge | FF: Repo-A 94.6, OpenCV 93.4; AC F1: 60.0 / 76.4; N = 4986 / 4971 | Câu trả lời bám ngữ cảnh truy hồi theo judge | MA trả lời đúng (AC F1 chỉ 60–76); hữu ích cho kỹ sư thật | [Paper: PDF p. 9, Table III, Section V-F] |
| E7: Chất lượng CodeScribe | tài liệu đúng và hữu ích | SME đánh giá (Repo-A), tác giả so với CodeWiki (OpenCV) | "largely correct and useful, but somewhat verbose"; Figure 5 so sánh định tính | Bằng chứng định tính, không có thang đo | Tài liệu tốt hơn CodeWiki một cách định lượng | [Paper: PDF p. 8, Section V-C, Figure 5] |

**Mâu thuẫn số liệu ghi nhận** (theo quy tắc contradictions):
- Section VI ghi Repo-A D2 synthetic Top-1 = "67.6%" nhưng Table I ghi 67.46; hiệu 8.72 khớp với 67.46 → khả năng lỗi đánh máy trong văn bản [Paper: PDF p. 9, Section VI, Table I].
- Contributions ghi cải thiện "at least 9% Top-1 accuracy over baseline approaches" [Paper: PDF p. 2, Section I-A], nhưng các mức tăng báo cáo là +14.59 (OpenCV, D2→D3) và +8.72 (Repo-A, D2→D3) — 8.72 < 9 — và đây là so với D2 chứ không phải baseline D1 hay baseline ngoài. Kết luận "≥9%" vì vậy chưa được bảng hỗ trợ.
- Tổng N trong Table II (209+2804+8049+351+418+144+402 = 12,377) khác N = 12,658 của OpenCV synthetic ở Table I; bài không giải thích (có thể do lọc) [Paper: PDF p. 9, Table I, Table II].
- Văn bản gọi ví dụ prompt là "Listing 3" nhưng đó là Figure 3 [Paper: PDF p. 6, Figure 3].
- Footnote 1 để placeholder `[GEN_MODEL]`, `[TEMP]`, `[TOP_P]`, `[MAX_TOKENS]` chưa điền [Paper: PDF p. 5, Section IV-D].

## 11 Diễn giải đúng các kết luận

- **Phạm vi tác vụ:** truy hồi method-level trên tập held-out nội bộ; "code comprehension" được đo bằng proxy Top-K/Recall và RAGAS (tác giả thừa nhận ở construct validity) [Paper: PDF p. 10, Section VII].
- **Oracle / ground truth:** test synthetic dùng câu hỏi do cùng pipeline LLM sinh; ground truth của RAGAS là câu trả lời sinh lúc tạo câu hỏi → đánh giá phần lớn "in-distribution" với chính pipeline [Paper: PDF p. 8, Section V-A].
- **End-to-end:** MA được đánh giá end-to-end nhưng không có baseline; retrieval được đánh giá cô lập.
- **Chi phí:** chi phí offline đáng kể ($3,200 cho 1.2M LOC); suy luận rẻ [Paper: PDF p. 8, Section V-D].
- **Phụ thuộc mô hình:** kết quả gắn với Sonnet 4.5/4.0; LLM non-determinism không được định lượng.
- **Trường hợp khó nhất:** qa_sibling và qa_parent có Top-1 thấp nhất (63.93, 69.44 ở D3) [Paper: PDF p. 9, Table II].
- **Biên miền:** chỉ C/C++, hai kho [Paper: PDF p. 10, Section VII].
- **Bất định:** một lần chạy, không CI.

**Phát biểu bị chặn:** Trên hai kho C/C++ (OpenCV, Repo-A), một dual-encoder huấn luyện trên tài liệu do CodeScribe sinh đạt Top-1 Text→Code 94–96% với mô tả người viết; việc thêm ngữ cảnh parent/sibling cùng câu hỏi tổng hợp (D3) cải thiện mạnh truy hồi trên câu hỏi tổng hợp cùng phân phối (+8.7 đến +14.6 điểm Top-1) nhưng giảm nhẹ trên mô tả gốc; MA đạt FF > 90% theo LLM-as-a-judge với AC F1 60–76%, chưa có so sánh với baseline ngoài.

## 12 Hạn chế được tác giả thừa nhận rõ ràng

| Hạn chế | Biểu hiện cụ thể | Hướng tương lai tác giả đề xuất | Nguồn |
|---|---|---|---|
| Chỉ hai kho thuộc systems programming (C/C++) | không thể khẳng định language-agnostic | đánh giá trên Java, Python, Go, Rust… | [Paper: PDF p. 10, Section VII, Section VIII] |
| LLM non-determinism và dùng hai phiên bản model | Sonnet 4.5 vs 4.0 có thể gây lệch phân phối dữ liệu huấn luyện | Không nêu | [Paper: PDF p. 10, Section VII] |
| Rò rỉ tiềm năng qua parent/sibling | ngữ cảnh có thể chứa tham chiếu tới method test | đã giảm thiểu; kiểm tra <1% trên OpenCV | [Paper: PDF p. 10, Section VII] |
| Construct validity | Top-K/Recall và RAGAS chỉ là proxy cho "comprehension" | Không nêu | [Paper: PDF p. 10, Section VII] |
| D3 gộp hai thay đổi | không thể quy cải thiện cho riêng parent/sibling hay QA | cần thêm ablation | [Paper: PDF p. 10, Section VII] |
| Thiếu model fine-tuned cho đánh giá agentic | có thể ảnh hưởng điểm RAGAS | Không nêu | [Paper: PDF p. 10, Section VII] |
| Ngôn ngữ ít xuất hiện trong dữ liệu LLM | CodeScribe phụ thuộc LLM nên có thể kém | Không nêu | [Paper: PDF p. 10, Section VIII] |
| AC thấp hơn FF | ít claim → mẫu số nhỏ, nhạy với sai lệch đơn lẻ | Không nêu | [Paper: PDF p. 9, Section V-F] |

**Hướng tương lai khác do tác giả nêu:** tích hợp structural graph, sequence diagram, visual artifact (đa phương thức); dùng CodeGraph như một modality để retrieval theo độ gần node; cải thiện sinh câu hỏi tổng hợp (prompting, intent modeling, curriculum, adversarial) [Paper: PDF p. 10–11, Section VIII].

**Related constraints noted by the authors (không được trình bày như hạn chế chính thức):** tài liệu CodeScribe "somewhat verbose", khó cho người đọc duyệt [Paper: PDF p. 8, Section V-C]; CodeGraph cần parser theo ngôn ngữ [Paper: PDF p. 3, Section IV-A].

## 13 Phân tích phản biện

| `[Analysis]` Quan sát | Vấn đề tiềm ẩn / giải thích thay thế | Vì sao quan trọng | Cách kiểm tra | Cơ sở |
|---|---|---|---|---|
| Không có baseline ngoài (BM25, CodeBERT/UniXcoder zero-shot, embedding thương mại, RepoAgent+RAG) | Top-1 94% có thể đạt được bằng retriever chung hoặc lexical match; đóng góp của CodeScribe chưa được cô lập | Claim "improves over baseline approaches" chỉ so với D1 nội bộ | Chạy BM25 và một code-embedding pre-trained (không fine-tune) trên cùng test | [Paper: PDF p. 9, Table I] [Paper: PDF p. 3, Section II-D] |
| Test synthetic sinh bởi cùng pipeline/prompt như dữ liệu huấn luyện D3 | Lợi ích D2→D3 có thể là khớp phân phối (style/anchor) chứ không phải hiểu ngữ cảnh | Kết luận "D3 tốt cho developer queries đa dạng" phụ thuộc giả định này | Đánh giá trên câu hỏi thật của developer (log IDE, issue tracker) hoặc câu hỏi do LLM khác/prompt khác sinh | [Paper: PDF p. 5–6, Section IV-D] [Paper: PDF p. 9, Table II] |
| D1 không được đánh giá trên synthetic, D3 không được đánh giá trên non-synthetic trong Table I | Không thấy toàn bộ ma trận cấu hình × loại test | Đánh đổi D2/D3 chỉ thấy gián tiếp qua Table II | Báo cáo đủ 3×2 ô | [Paper: PDF p. 9, Table I] |
| KEY_TERMS bắt buộc ≥3 từ khớp nguyên văn với signature/tài liệu | Câu hỏi có thể dễ do trùng từ vựng, dù đã xóa function name | Có thể thổi phồng Top-K | So sánh với biến thể câu hỏi bị paraphrase/bỏ anchor | [Paper: PDF p. 6, Figure 3] |
| Không có seed lặp, CI, kiểm định | Chênh lệch nhỏ (vd. D1→D2 OpenCV +1.77) có thể nằm trong nhiễu | Ảnh hưởng claim "consistently" | ≥3 seed, bootstrap CI | [Paper: PDF p. 9, Table I] |
| RAGAS AC/FF do LLM chấm, ground truth do LLM sinh | Vòng lặp LLM-chấm-LLM; FF cao không đồng nghĩa đúng | Claim chất lượng MA | Đánh giá con người trên mẫu nhỏ; đối chiếu với AC | [Paper: PDF p. 9, Table III] |
| Chất lượng call graph tĩnh với C (function pointer, macro) không được đo | Cạnh thiếu làm sai start methods và parent/sibling | Toàn bộ chuỗi phụ thuộc CodeGraph | Đo precision/recall cạnh so với dynamic trace trên một module | [Paper: PDF p. 3, Section IV-A] |
| Post-order chunking và incremental update chỉ được mô tả | Không biết chất lượng tài liệu so với chunking ngây thơ, hay sai lệch tích lũy qua nhiều commit | Đây là contribution số 1 | Ablation chunking; so sánh incremental vs full rerun sau N commit | [Paper: PDF p. 4, Section IV-B, Figure 2] |

## 14 Kiến thức thu được

**Agent-derived knowledge candidates**
- **Khái niệm:** dùng LLM offline sinh tài liệu theo cấu trúc chương trình để làm *tín hiệu giám sát* cho retriever rẻ (distillation qua dữ liệu) [Paper: PDF p. 3, Section II-D].
- **Thuật toán:** post-order chunking trên cây DFS với rolling summary của callee để vượt giới hạn context [Paper: PDF p. 4, Section IV-B].
- **Kỹ thuật dữ liệu:** depth id dạng 1.2.3 để khôi phục parent/sibling từ Markdown; synthetic question với anchor từ vựng (BEHAVIOR/PARAM/CONTEXT/KEY) và hạn chế keyword dumping [Paper: PDF p. 5, Section IV-C, Section IV-D].
- **Công thức:** multi-positive symmetric InfoNCE (Equation 1–3) cho giám sát one-to-many [Paper: PDF p. 7, Equation 1, Equation 3].
- **Kỹ thuật huấn luyện:** differentiable all-gather dưới FSDP để có global batch lớn, kèm placeholder tensor cho rank rỗng [Paper: PDF p. 7, Section IV-E].
- **Thiết kế thực nghiệm:** tăng dần lớp giám sát (D1→D3) và tách theo query type để lộ đánh đổi; xóa function-name khỏi câu hỏi để giảm shortcut [Paper: PDF p. 9, Table II].
- **Định danh node:** `method_name:::file_name:::line_number` để xử lý overloading/trùng tên [Paper: PDF p. 3, Section IV-A].

## 15 Liên hệ với kiến thức hiện có

`[Analysis]` Các liên hệ dưới đây là ứng viên, chưa kiểm chứng ngoài (context mode: paper-only).
- **Tương đồng:** cùng họ với RepoAgent/CodeWiki (tài liệu cấp kho) và CodeRetriever/CoCoSoDa (contrastive code search) mà bài trích dẫn [Paper: PDF p. 2–3, Section II]; điểm khác là nối hai hướng bằng dữ liệu.
- **Kết hợp tiềm năng:** tác giả tự đề xuất dùng CodeGraph như modality bổ sung [Paper: PDF p. 10, Section VIII] — gần với ý tưởng graph-augmented retrieval (cần kiểm chứng tài liệu ngoài).
- **Xung đột / căng thẳng:** Table II cho thấy giám sát "giàu hơn" không đơn điệu tốt hơn (doc_brief_merged giảm) — liên hệ ứng viên với hiện tượng distribution shift trong dense retrieval; cần nguồn ngoài.
- **Miền chuyển giao:** `[Hypothesis]` hệ thống nhúng/viễn thông khác (Linux kernel, firmware) và kho đa ngôn ngữ; tài liệu hóa legacy code (COBOL) nơi comment thưa.
- **Liên hệ với đề tài người dùng:** Not assessable — người dùng chưa cung cấp kiến thức liên quan.

## 16 Ý tưởng nghiên cứu

**Agent-derived research candidates** — tất cả là candidate idea / hypothesis; prior-art search required.

### Ứng viên 1: Graph-proximity positives cho CodeContrast (tách đóng góp của cấu trúc)

- **Hạn chế xuất phát:** D3 gộp parent/sibling và QA nên không biết cấu trúc đóng góp bao nhiêu (tác giả thừa nhận); tác giả đề xuất dùng CodeGraph như modality [Paper: PDF p. 10, Section VII, Section VIII]; qa_sibling/qa_parent là loại khó nhất [Paper: PDF p. 9, Table II].
- **Giả thuyết cốt lõi:** định nghĩa positive/soft-positive theo khoảng cách trên CodeGraph (callee/caller trực tiếp với trọng số giảm theo khoảng cách) thay vì nhúng văn bản parent/sibling vào text view sẽ tăng Top-1 trên qa_parent/qa_sibling ít nhất 5 điểm mà không làm giảm doc_brief_merged quá 1 điểm.
- **Delta so với bài:** thay đổi *objective* (Equation 1: tập $P(i)$ mở rộng theo đồ thị, có trọng số) và *representation* (tách ngữ cảnh cấu trúc khỏi văn bản).
- **Phương pháp ban đầu:** chạy 4 cấu hình ablation: D2, D2+parent/sibling-text, D2+QA, D2+graph-positive; cùng backbone, cùng số epoch, cùng batch.
- **Validation:** OpenCV (công khai) theo đúng split method-level; metric Top-1/Top-5 Text→Code theo query type như Table II; 3 seed + bootstrap CI; kỳ vọng graph-positive ≥ D3 trên qa_parent/qa_sibling; bác bỏ nếu cải thiện < CI hoặc doc_brief_merged giảm >1 điểm. Ngân sách: ~4× (4 A100 × 24 giờ) theo số liệu bài [Paper: PDF p. 8, Section V-D].
- **Possible failure modes (failure mode):** (1) call graph tĩnh với C thiếu cạnh do function pointer/macro → positive sai; (2) method gần trên đồ thị nhưng khác ngữ nghĩa → embedding bị kéo nhòe, giảm precision; (3) lợi ích D3 thực chất do khớp phân phối câu hỏi, không do cấu trúc → graph-positive không giúp.
- **Innovation status:** unverified.

### Ứng viên 2: Benchmark câu hỏi developer thật để kiểm tra lệch phân phối của test synthetic

- **Quan sát xuất phát:** test synthetic và dữ liệu QA của D3 sinh bởi cùng pipeline/prompt; ground truth RAGAS cũng do LLM sinh [Paper: PDF p. 5–6, Section IV-D, Figure 3] [Paper: PDF p. 8, Section V-A]; tác giả thừa nhận construct validity [Paper: PDF p. 10, Section VII].
- **Giả thuyết cốt lõi:** trên câu hỏi do người viết (trích từ GitHub issues/discussions của OpenCV có liên kết tới method được sửa trong PR), mức tăng D2→D3 sẽ nhỏ hơn đáng kể (< một nửa của +14.59 điểm) so với trên test synthetic; nếu mức tăng giữ ≥ 10 điểm thì giả thuyết bị bác bỏ và lợi ích D3 được củng cố.
- **Delta so với bài:** thay đổi *evaluation* (nguồn truy vấn) và thêm baseline ngoài (BM25, code-embedding pre-trained không fine-tune).
- **Phương pháp ban đầu:** thu thập ~300–500 cặp (issue text, method sửa trong PR liên kết) từ OpenCV, lọc method có trong tập test held-out; thêm một tập câu hỏi do LLM khác (không phải Sonnet) với prompt khác sinh để tách hiệu ứng style.
- **Validation:** so sánh Top-1/Top-10 của D1, D2, D3, BM25, embedding zero-shot trên ba nguồn truy vấn (synthetic gốc, synthetic LLM khác, issue thật); controlled variables: cùng corpus code, cùng split; bootstrap CI. Ngân sách: chủ yếu công gán nhãn, không cần huấn luyện lại.
- **Possible failure modes (failure mode):** (1) liên kết issue→method nhiễu (PR sửa nhiều method) → nhãn sai; (2) số cặp hợp lệ trong tập held-out quá nhỏ cho CI hẹp; (3) issue text mô tả triệu chứng chứ không mô tả hành vi method → mọi hệ thống đều thấp, không phân biệt được cấu hình.
- **Innovation status:** unverified.
