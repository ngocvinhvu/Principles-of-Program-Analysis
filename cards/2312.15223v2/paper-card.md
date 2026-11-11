# Paper Card — A Survey on Large Language Models for Software Engineering (arXiv:2312.15223v2)

> Source coverage: Full paper (61 trang PDF; thân bài PDF p. 1-30, tài liệu tham khảo PDF p. 30-52, Appendix A PDF p. 53-57, Appendix B PDF p. 58-61). Thân bài, các bảng/hình chính và phần đầu Appendix đã đọc; danh mục tài liệu tham khảo và phần lớn Appendix A/B chỉ được rà soát cấu trúc, không đọc từng mục.
> Extraction confidence: High (PyMuPDF, `validation = valid_with_warnings`, cảnh báo duy nhất: thiếu title trong metadata PDF). Figure 1 và Table 5 đã được kiểm tra trực quan bằng ảnh trang.
> Locator mode: page-grounded (chỉ số trang PDF; nhãn trang in trùng với chỉ số PDF ở PDF p. 1-52, nhưng Appendix đánh số lại — ví dụ PDF p. 58 mang nhãn in "6").
> Primary analytical lens: review (systematic/mapping survey)
> Secondary analytical lens: None
> Context verification: Paper-only (không thực hiện tra cứu bên ngoài; mọi lịch sử lĩnh vực là `paper-framed`)
> Card completeness: Complete relative to supplied source (riêng Appendix A/B và danh mục tham khảo chỉ đọc lướt cấu trúc)

**Phân loại:** `paper_type = review` — bài là một survey dạng systematic mapping: có quy trình tìm kiếm, lọc, snowballing, phân loại (taxonomy) và tổng hợp mô tả; không có thực nghiệm mới ngoài Table 6 (bảng trích dẫn kết quả). Không chọn lens phụ vì "living repository" AwesomeLLM4SE không được đánh giá như một resource có bằng chứng độc lập.

**Terminology Ledger (khóa thuật ngữ cho toàn card)**

| Canonical term | Định nghĩa lần đầu | Biến thể trong bài | Quyết định |
|---|---|---|---|
| LLM | Large Language Model | "LLMs", "LLms", "PLM", "Pre-trained model" | dùng "LLM"; lưu ý bài gộp cả mô hình cỡ nhỏ (CodeBERT 125M) vào "LLM" |
| LLM of Code / Code LLM | LLM được thiết kế/huấn luyện cho mã nguồn | "LLMs of Code", "Code LLMs" | dùng "Code LLM" |
| SE | Software Engineering | — | giữ "SE" |
| LLM4SE / LLM-based SE | nghiên cứu áp dụng LLM cho tác vụ SE | "LLM-based SE research" | dùng "LLM-based SE" |
| SE phase | 5 giai đoạn: Requirements & Design, Development, Testing, Maintenance, Management | "SE activity" (Table 5) | dùng "SE phase" |
| APR | Automated Program Repair | "program repair", "code refinement" | dùng "program repair" |
| data leakage | mẫu đánh giá xuất hiện trong dữ liệu pre-training | "data contamination", "memorization" | dùng "data leakage" |

---

## 01 Thông tin cơ bản

- **Tiêu đề:** A Survey on Large Language Models for Software Engineering [Paper: PDF p. 1, title block]
- **Tác giả:** Quanjun Zhang, Chunrong Fang, Yang Xie, Yaxin Zhang, Yun Yang, Weisong Sun, Shengcheng Yu, Zhenyu Chen [Paper: PDF p. 1, author block]
- **Đơn vị:** State Key Laboratory for Novel Software Technology, Nanjing University; Nanyang Technological University; Swinburne University of Technology [Paper: PDF p. 1, affiliation footnote]
- **Venue / năm:** arXiv preprint, v2 ngày 8/9/2024 (cs.SE) [Paper: PDF p. 1, arXiv stamp]. Venue xuất bản chính thức: Not assessable from supplied material.
- **Loại bài:** Survey / systematic literature mapping.
- **Lĩnh vực / từ khóa:** Software Engineering, Large Language Model, AI and Software Engineering, LLM4SE [Paper: PDF p. 1, Index Terms]
- **DOI / ID:** arXiv:2312.15223v2. DOI: không có trong nguồn.
- **Code / dữ liệu:** living repository https://github.com/iSEngLab/AwesomeLLM4SE [Paper: PDF p. 1, Abstract; PDF p. 2, Availability]
- **Ngày đọc:** 2026-11-06
- **Vị trí trong hướng nghiên cứu của người dùng:** Not assessable — người dùng chưa cung cấp. `Agent-derived candidate`: dùng như bản đồ nền (taxonomy 112 tác vụ) cho đề tài thuộc "Kỹ thuật phân tích chương trình" (static analysis, fault localization, program repair, test generation).

## 02 Tóm tắt một câu

Bài tổng hợp có hệ thống 1009 công trình (đến 08/2024) về LLM trong SE, phân loại 62 Code LLM theo kiến trúc/pre-training objective/downstream task/open science và 947 nghiên cứu ứng dụng vào 112 tác vụ thuộc 5 SE phase, cho thấy ứng dụng tập trung mạnh ở Development (341) và Testing (240) trong khi Requirements & Design (43) và Management (5) còn thưa, và từ đó đề xuất các thách thức như data leakage, mô hình chuyên miền và benchmark đa chiều [Paper: PDF p. 1, Abstract; PDF p. 12, Table 5; PDF p. 28-29, Section 6].

## 03 Câu hỏi nghiên cứu

- **Vấn đề cụ thể:** Số lượng nghiên cứu LLM-based SE tăng nhanh, quy trình SE phức tạp và nhiều tác vụ chuyên biệt khiến nhà nghiên cứu khó nắm được hiện trạng; các LLM mới liên tục xuất hiện với kiến trúc, cách huấn luyện, nguồn và phương pháp fine-tuning khác nhau [Paper: PDF p. 1-2, Section 1].
- **Tại sao quan trọng:** SE là hạ tầng của nhiều ngành; LLM (ví dụ ChatGPT) đang thay đổi cách tự động hóa tác vụ mã [Paper: PDF p. 1, Section 1].
- **Vì sao survey trước chưa đủ (theo tác giả):** các survey 2022 tập trung ML/DL chứ không phải LLM; Niu et al. và Zan et al. chỉ phủ 20 và 27 LLM cho NL2Code; các preprint đồng thời (Wang et al. — chỉ testing; Fan et al.; Hou et al.) hoặc hẹp hoặc khác trọng tâm [Paper: PDF p. 2, Comparison with Existing Surveys]. `[Paper-framed; external verification not performed]`
- **RQ chính thức:** RQ1 (LLM Perspective: RQ1.1-RQ1.4), RQ2 (SE Perspective), RQ3 (Integration Perspective) [Paper: PDF p. 2, Section 2.1].
- **Câu hỏi dạng "Can ...?":** Can một quy trình tìm kiếm từ khóa + lọc thủ công + snowballing tạo ra một bản đồ đủ bao quát và phân loại ổn định của các Code LLM và ứng dụng LLM trong toàn bộ vòng đời SE? `[Analysis]`

## 04 Bối cảnh nghiên cứu và lộ trình phát triển

`[Paper-framed; external verification not performed]`

| Giai đoạn | Cách tiếp cận đại diện | Ưu điểm (theo bài) | Hạn chế (theo bài) | Nguồn |
|---|---|---|---|---|
| ML/DL cho SE | các survey Watson et al., Wang et al., Yang et al. (2022) | nền tảng cho học tự động trong SE | chưa bao phủ LLM | [Paper: PDF p. 2, Comparison with Existing Surveys] |
| Encoder-only Code LLM | CuBERT, CodeBERT, GraphCodeBERT | biểu diễn ngữ cảnh, phù hợp code search, vulnerability detection | không dùng cho sinh chuỗi | [Paper: PDF p. 5, Section 3.1.1; PDF p. 7, Answer to RQ1.1] |
| Encoder-decoder Code LLM | PyMT5, PLBART, CodeT5, CodeT5+ | sequence-to-sequence (summarization, repair) | — | [Paper: PDF p. 5-6, Section 3.1.2] |
| Decoder-only Code LLM | Codex, CodeGen, StarCoder, Code Llama, DeepSeek-Coder | sinh mã tự hồi quy; xu hướng tăng kích thước | chi phí huấn luyện, triển khai | [Paper: PDF p. 6-7, Section 3.1.3; PDF p. 5, Figure 2] |
| Chuyển dịch paradigm trong program repair | downstream task → LLM như thành phần (CURE) → fine-tuning → zero-shot cloze (AlphaRepair) → kết hợp với APR truyền thống (GAMMA) | giảm phụ thuộc dữ liệu cặp bug-fix | data leakage, chất lượng dữ liệu | [Paper: PDF p. 20-21, Section 4.4.1] |
| Agent / RAG / repository-level | các hướng "cutting-edge" được nhắc lướt | — | chưa phân tích sâu | [Paper: PDF p. 14, Section 4.2.1, "Others"] |

Vị trí bài tự nhận: survey phủ "toàn bộ SE scope" với ba trọng tâm LLM / SE / Integration và repository crowd-sourced đầu tiên [Paper: PDF p. 2, Comparison with Existing Surveys]. Tuyên bố "first public repository" chưa được kiểm chứng bên ngoài.

## 05 Các điểm đau cốt lõi được bài chỉ ra

| Điểm đau | Biểu hiện | Nguyên nhân / giải thích của tác giả | Bằng chứng trong bài |
|---|---|---|---|
| Khó nắm hiện trạng | khối lượng lớn và đa dạng nghiên cứu LLM-based SE | quy trình SE phức tạp, LLM mới xuất hiện liên tục | [Paper: PDF p. 1-2, Section 1]; số lượng: Figure 1 [Paper: PDF p. 3, Figure 1] |
| Tái lập (open science) | 54/62 Code LLM công bố artifact; một số không có code/dataset/model | chi phí GPU, cấu hình phức tạp, lý do thương mại ("perhaps") | [Paper: PDF p. 10-11, Section 3.4, Table 4] |
| Data leakage | mẫu Defects4J xuất hiện trong CodeSearchNet; ChatGPT trả lời bài LeetCode chỉ từ số hiệu | LLM huấn luyện trên mọi repo công khai; LLM đóng không công bố dữ liệu | [Paper: PDF p. 25, Section 5.1.2; PDF p. 28-29, Section 6 "Clean Evaluation Datasets"] — bằng chứng là trích dẫn, không phải đo đạc của bài |
| Chi phí kích thước mô hình | CodeT5-base 220M mất 12 ngày trên 16 A100; Code Llama-34B ~63GB | xu hướng mô hình lớn hơn | [Paper: PDF p. 28, Section 6 "Trade-off"] |
| Phân bố ứng dụng lệch | Requirements & Design 43, Management 5 so với Development 341 | các tác vụ dev/test là downstream task tự nhiên dạng seq2seq | [Paper: PDF p. 12, Table 5; PDF p. 24, Answer to RQ2] |
| An toàn và độ tin cậy | adversarial, backdoor, imitation attack trên Code LLM | LLM nhạy với biến đổi bảo toàn ngữ nghĩa | [Paper: PDF p. 26-27, Section 5.2] |
| Thiếu giải thích | đánh giá chủ yếu bằng accuracy/precision | black-box, tham số lớn | [Paper: PDF p. 29, Section 6 "Explainable LLM-based Research"] |

## 06 Ý tưởng cốt lõi

1. **Phương pháp bề mặt:** tìm kiếm từ khóa hai nhóm (SE × LLM) trên Google Scholar, ACM DL, IEEE Xplore → lọc 3 giai đoạn → snowballing → phân loại theo ba góc nhìn (LLM / SE / Integration) [Paper: PDF p. 3, Section 2.2-2.3].
2. **Insight cốt lõi:** tách bản đồ thành hai trục độc lập — "mô hình" (kiến trúc, pre-training objective, downstream task, mức open-source) và "tác vụ SE" (112 tác vụ trong 5 SE phase) — rồi thêm trục thứ ba về các vấn đề tích hợp (đánh giá, bảo mật, domain tuning, nén) [Paper: PDF p. 2, Section 2.1; PDF p. 5, Figure 2; PDF p. 12, Table 5].
3. **Bài học tổng quát `[Analysis]`:** một bản đồ mapping theo vòng đời SE giúp phát hiện vùng thưa (requirements, management) nhanh hơn so với survey theo mô hình; nhưng số lượng bài theo tác vụ phản ánh mức độ quan tâm, không phản ánh hiệu quả hay độ chín của kỹ thuật.

## 07 Tổng quan phương pháp

- **Đầu vào:** 32,560 bài từ tìm kiếm tự động tới 08/2024 [Paper: PDF p. 3, Section 2.2].
- **Lọc:** (1) bỏ bài trước 2017 (Transformer); (2) bỏ bài < 7 trang và trùng lặp; (3) đánh giá thủ công độc lập bởi hai tác giả, bất đồng do tác giả thứ ba quyết định → 59 bài Code LLM + 912 bài LLM-based SE [Paper: PDF p. 3, Section 2.3].
- **Snowballing:** thêm 3 bài Code LLM + 36 bài LLM-based SE [Paper: PDF p. 3-4, Section 2.3].
- **Đầu ra:** 1009 bài; 62 Code LLM; 947 nghiên cứu cho 112 tác vụ; Table 1 (venue), Table 2-4 (Code LLM), Table 5 (tác vụ), Figure 3 / Appendix B (danh sách tham chiếu theo tác vụ) [Paper: PDF p. 4, Section 2.4; PDF p. 58, Figure 3].
- **Tổng hợp:** mô tả tường thuật (narrative synthesis) theo từng tác vụ, mỗi RQ kết thúc bằng hộp "Answer to RQ" [Paper: PDF p. 7, Answer to RQ1.1; PDF p. 24, Answer to RQ2; PDF p. 27-28, Answer to RQ3].
- **Giả định ngầm `[Analysis]`:** từ khóa đủ bao phủ; tiêu chí "quality assessment criteria" (không được liệt kê) là đáng tin; mỗi bài được gán vào một tác vụ chính.

Luồng: `Keywords (SE × LLM) → 3 database (32,560) → lọc năm/độ dài/trùng → thẩm định thủ công 2+1 tác giả (971) → snowballing (+39) → 1009 bài → phân loại RQ1 (62 Code LLM) / RQ2 (947 nghiên cứu, 112 tác vụ) / RQ3 (4 khía cạnh tích hợp) → Challenges & Opportunities`

## 08 Phân rã các module cốt lõi

Đối với review, "module" = các trục phân loại/thành phần của quy trình survey; câu hỏi ablation được thay bằng độ vững của taxonomy và độ bao phủ.

| Module | Chức năng | Vì sao cần | Đầu vào và đầu ra | Bằng chứng hỗ trợ | Ảnh hưởng (đo được hoặc dự kiến) khi bỏ |
|---|---|---|---|---|---|
| Search strategy (2 nhóm từ khóa) | thu thập ứng viên | phủ cộng đồng SE, AI, NLP | từ khóa → 32,560 bài | [Paper: PDF p. 3, Section 2.2] | Dự kiến: hụt các bài dùng thuật ngữ khác (ví dụ "agent", "foundation model" không có trong danh sách từ khóa) — chưa đo |
| Study selection 3 giai đoạn | lọc | loại bài không liên quan | 32,560 → 971 | [Paper: PDF p. 3, Section 2.3] | Không báo cáo inter-rater agreement; tiêu chí chất lượng không liệt kê |
| Snowballing | bổ sung | giảm bỏ sót | +3 / +36 | [Paper: PDF p. 3-4, Section 2.3] | Đo được: +39 bài (~3.9% tổng) |
| Taxonomy RQ1 (Figure 2, Table 2, Table 3, Table 4) | phân loại Code LLM | so sánh kiến trúc/objective/open science | 62 LLM → 3 kiến trúc, 15 objective/4 nhóm, downstream tasks, 54/62 open | [Paper: PDF p. 5, Figure 2; PDF p. 6, Table 2; PDF p. 7, Table 3; PDF p. 11, Table 4] | Không có kiểm tra độ vững |
| Taxonomy RQ2 (Table 5, Figure 3) | ánh xạ nghiên cứu → tác vụ → SE phase | trả lời "tác vụ nào đã được hỗ trợ" | 947 nghiên cứu → 112 tác vụ / 5 phase | [Paper: PDF p. 12, Table 5; PDF p. 58, Figure 3] | Các ô nhỏ (nhiều tác vụ chỉ có 1 bài) cho thấy độ chi tiết không đồng đều |
| RQ3 Integration | các vấn đề xuyên tác vụ | đánh giá, bảo mật, tuning, nén | → 4 tiểu mục | [Paper: PDF p. 24-28, Section 5] | Không định lượng số bài trong mỗi khía cạnh |
| Challenges & Opportunities | định hướng | chỉ ra hướng tương lai | → 7 hướng | [Paper: PDF p. 28-29, Section 6] | Là đề xuất của tác giả, không có bằng chứng thực nghiệm mới |

## 09 Công thức và ký hiệu thiết yếu

Not applicable (survey không có mô hình toán học trung tâm). Bài chỉ mô tả phi hình thức các pre-training objective, ví dụ CLM dự đoán $x_i$ từ $(x_j : j < i)$ cho chuỗi $x = (x_1, \dots, x_n)$; MLM che 15% token; Edge Prediction che ~20% nút trong data flow graph [Paper: PDF p. 7-8, Section 3.2.1-3.2.3]. Ý nghĩa: giúp phân biệt objective tuần tự (CLM, MLM, MSP) với objective nhận biết cấu trúc (EP, NA, CAP).

**Ghi chú về inventory phương trình của bundle:** source bundle đánh dấu 21 mục "phương trình" — Equation 1, Equation 2, Equation 3, Equation 4, Equation 5, Equation 6, Equation 7, Equation 8, Equation 10, Equation 12, Equation 13, Equation 17, Equation 18, Equation 19, Equation 20, Equation 24, Equation 34, Equation 41, Equation 46, Equation 66, Equation 76. Kiểm tra ngữ cảnh cho thấy đây là artifact trích xuất: Equation 2 là câu văn ở [Paper: PDF p. 3, Section 2.2], các mục còn lại là các số đếm trong ngoặc của Table 5 (ví dụ "Ambiguity Detection (5)", tổng "341") [Paper: PDF p. 12, Table 5]. Bài không có phương trình được đánh số.

## 10 Thiết kế thực nghiệm và chuỗi bằng chứng

**Thiết lập (cho review):** tập dữ liệu = 1009 bài (382 arXiv chưa peer-review; top venue ICSE 95, FSE 51, ACL 31, ASE 30, ISSTA 28) [Paper: PDF p. 4, Table 1, Section 2.4]; giai đoạn 2017-08/2024; không có meta-analysis, không có thang chất lượng/risk of bias được báo cáo; Table 6 là bảng duy nhất có số liệu hiệu năng (BLEU/Accuracy trên BFP-Small/BFP-Medium) và không nêu nguồn số liệu trong chú thích [Paper: PDF p. 21, Table 6].

| Bằng chứng | Claim được kiểm | So sánh / điều kiện | Kết quả | Kết luận được hỗ trợ | Kết luận mạnh hơn KHÔNG được hỗ trợ | Nguồn |
|---|---|---|---|---|---|---|
| Figure 1 | số nghiên cứu tăng nhanh từ 2020 | đếm theo năm, 2024 chỉ tới tháng 8 | tổng 13 → 32 → 91 → 376 → 496 (Code LLM 4/6/11/15/26; SE 9/26/80/361/470) | số bài thu thập được tăng mạnh, nhất là 2023-2024 | LLM "hiệu quả hơn" — Figure 1 chỉ đo số lượng; cộng các cột cho 1008 (Code LLM 62, SE 946) so với 1009/947 trong văn bản | [Paper: PDF p. 3, Figure 1] |
| Table 1 | phân bố venue rộng, nhiều preprint | top-30 venue | arXiv 382/1009; 25/30 venue là hội nghị | lĩnh vực đa cộng đồng, nghiêng về hội nghị | chất lượng bằng chứng cao — 37.9% chưa qua peer review | [Paper: PDF p. 4, Table 1] |
| Figure 2 + Table 2 + Table 3 | Code LLM theo 3 kiến trúc; objective theo 4 nhóm | 62 Code LLM | decoder-only ngày càng phổ biến; objective dịch chuyển từ NLP-derived sang code-aware | mô tả xu hướng | một kiến trúc "tốt nhất" — tác giả tự nói không xác định được | [Paper: PDF p. 5, Figure 2; PDF p. 6, Table 2; PDF p. 7, Table 3, Answer to RQ1.1, RQ1.2] |
| Table 4 | mức open science | kiểm tra link trong bài gốc | 54/62 Code LLM có artifact; GitHub và Hugging Face chiếm ưu thế | phần lớn có artifact công khai | các artifact đó tái lập được — không kiểm tra khả năng chạy lại | [Paper: PDF p. 10-11, Section 3.4, Table 4] |
| Table 5 | phân bố 112 tác vụ / 5 SE phase | đếm số bài mỗi tác vụ | Dev 341, Testing 240, Maintenance 211, Req & Design 43, Management 5; lớn nhất: Code Generation 155, Vulnerability Detection 76, Program Repair 66, Test Generation 46, Code Summarization 41 | sự tập trung vào dev/test/maintenance | "947 nghiên cứu" — cộng các cột Total = 840; cộng các ô của Maintenance = 210 (không phải 211) | [Paper: PDF p. 12, Table 5; PDF p. 10, Section 4] |
| Section 4 (narrative) | LLM được dùng cho nhiều tác vụ theo các paradigm (fine-tuning, prompt, zero-shot, kết hợp truyền thống) | mô tả theo tác vụ | ví dụ chuỗi 5 giai đoạn trong program repair | các paradigm cùng tồn tại | paradigm nào hiệu quả hơn — không có so sánh định lượng thống nhất | [Paper: PDF p. 20-22, Section 4.4.1-4.4.3] |
| Table 6 | so sánh LLM trong program repair | BFP-Small / BFP-Medium, BLEU + Accuracy | CodeT5 accuracy 21.62% (Small), 13.96% (Medium); GraphCodeBERT 17.30% / 0.09%; CodeBERTER 17.75% / N.A. | BLEU cao (~77-91%) không đi kèm accuracy cao | xếp hạng mô hình tổng quát — không rõ nguồn, cấu hình, độ bất định | [Paper: PDF p. 21, Table 6] |
| Section 5 | các vấn đề tích hợp | mô tả | data leakage, attack, PEFT, continual learning, Compressor nén xuống 3 MB | các khía cạnh này đã được nghiên cứu | mức độ nghiêm trọng định lượng của data leakage trên toàn lĩnh vực | [Paper: PDF p. 24-28, Section 5] |
| Figure 3 (Appendix B) | ánh xạ chi tiết bài → tác vụ | danh sách trích dẫn | ví dụ Requirement Engineering có 7 trích dẫn [478]-[484] | cho phép truy vết | khớp với Table 5 — Table 5 ghi Requirement Engineering (1) | [Paper: PDF p. 58, Figure 3; PDF p. 12, Table 5] |

## 11 Diễn giải đúng các kết luận

- **Phạm vi tác vụ:** chỉ các Code LLM; general-purpose LLM (PaLM, Qwen, LLaMA, Gemini) bị loại khỏi RQ1 [Paper: PDF p. 5, footnote 1]. Tuy nhiên RQ2 vẫn đếm các nghiên cứu dùng ChatGPT/GPT-4 → hai trục có phạm vi "LLM" khác nhau `[Analysis]`.
- **Định nghĩa "LLM":** bao gồm mô hình 60M-220M (XFT, CodeT5) [Paper: PDF p. 6, Table 2], nên kết luận về "LLM" trộn lẫn PLM cỡ nhỏ và mô hình tỷ tham số.
- **Không có đánh giá chất lượng:** bài không báo cáo tiêu chí chất lượng cụ thể, kappa, hay risk of bias [Paper: PDF p. 3, Section 2.3]; mọi so sánh là đếm tần suất.
- **Phụ thuộc thời điểm:** cắt 08/2024; năm 2024 chỉ tính ~8 tháng [Paper: PDF p. 2, Comparison with Existing Surveys; PDF p. 3, Section 2.2].
- **Độ bất định số liệu:** các tổng (1009/947/211) không khớp hoàn toàn với tổng cộng từ Figure 1 và Table 5 (xem Section 10).
- **Vùng thưa:** Requirements & Design và Management ít bài có thể do thiếu ứng dụng thật hoặc do từ khóa tìm kiếm (danh sách SE keyword thiên về code/testing/repair) `[Analysis]` [Paper: PDF p. 3, Section 2.2].
- **Phát biểu lại có giới hạn:** Trong tập 1009 bài được thu thập bằng chuỗi từ khóa và lọc của tác giả tới 08/2024, các nghiên cứu LLM-based SE tập trung vào development, testing và maintenance (đặc biệt code generation, vulnerability detection, program repair), trong khi requirements/design và management ít được đại diện; bài không đánh giá hiệu quả tương đối của các kỹ thuật.

## 12 Hạn chế được tác giả thừa nhận rõ ràng

No explicit author-acknowledged limitation was found in the supplied source. Bài không có mục "Threats to Validity" hoặc "Limitations" cho chính survey (đã rà Section 1-7, PDF p. 1-30).

### Ràng buộc liên quan được tác giả ghi nhận (không được trình bày như hạn chế chính thức)

| Ràng buộc | Biểu hiện cụ thể | Hướng tương lai tác giả nêu | Nguồn |
|---|---|---|---|
| Table 1 chỉ hiển thị top-30 venue | "due to page limitations" | — | [Paper: PDF p. 4, Section 2.4] |
| Table 4 chỉ liệt kê LLM có link artifact | "due to limited space" | — | [Paper: PDF p. 10, Section 3.4] |
| General-purpose LLM nằm ngoài phạm vi RQ1 | đã được review ở cộng đồng NLP/AI | tham chiếu [84], [85] | [Paper: PDF p. 5, footnote 1] |
| Lo ngại bỏ sót của tìm kiếm tự động | dùng snowballing để giảm | — | [Paper: PDF p. 3, Section 2.3] |

## 13 Phân tích phản biện

| `[Analysis]` Quan sát | Vấn đề tiềm ẩn hoặc giải thích thay thế | Vì sao quan trọng | Cách kiểm tra | Cơ sở |
|---|---|---|---|---|
| Tổng cột Total trong Table 5 = 43+341+240+211+5 = 840, khác 947 | có thể một bài thuộc nhiều tác vụ (nhưng khi đó tổng phải ≥ 947), hoặc bảng thiếu nhóm, hoặc số 947 lỗi thời | mọi tỷ lệ phân bố dựa trên con số này | đối chiếu Table 5 với Figure 3 / repository; đếm lại trích dẫn Appendix B | [Paper: PDF p. 12, Table 5; PDF p. 10, Section 4] |
| Figure 1 cộng ra 1008 (62 + 946), văn bản 1009 (62 + 947); 912 + 36 = 948 | sai số nhập liệu nhỏ | ảnh hưởng tính tái lập của quy trình chọn | yêu cầu danh sách PRISMA-style từ repo | [Paper: PDF p. 3, Figure 1, Section 2.3; PDF p. 4, Section 2.4] |
| Số downstream task: Abstract "16", Section 3.3 "15", Figure 2 liệt kê 11 | taxonomy RQ1.3 chưa ổn định | mâu thuẫn nội bộ làm giảm độ tin cậy của mapping | đếm lại theo CodeXGLUE | [Paper: PDF p. 1, Abstract; PDF p. 9, Section 3.3; PDF p. 5, Figure 2] |
| Requirement Engineering: Table 5 ghi 1, Figure 3 có 7 trích dẫn | gán nhãn không nhất quán giữa hai bảng | kết luận "Req & Design thưa" có thể bị đánh giá thấp | so sánh từng tác vụ giữa Table 5 và Figure 3 | [Paper: PDF p. 12, Table 5; PDF p. 58, Figure 3] |
| Từ khóa SE không có "requirement", "agent", "repository-level", "management" chi tiết | thiên lệch truy hồi về code/test/repair | vùng "thưa" có thể là artifact của truy vấn | chạy lại tìm kiếm với từ khóa bổ sung và so sánh số bài thêm vào | [Paper: PDF p. 3, Section 2.2] |
| Table 6 không ghi nguồn, GraphCodeBERT accuracy 0.09% trên BFP-Medium | có thể lỗi đơn vị hoặc lấy từ cấu hình khác nhau | đây là bằng chứng định lượng duy nhất của bài | truy nguồn số liệu (CodeXGLUE / bài gốc) | [Paper: PDF p. 21, Table 6] |
| Table 1: TOSEM gán loại "C"; ICPC được khai là "International Collegiate Programming Contest" | có thể lỗi ghi nhãn venue | ảnh hưởng nhận định "25/30 venue là hội nghị" | đối chiếu tên venue chính thức (cần [External]) | [Paper: PDF p. 4, Table 1] |
| Không có đánh giá chất lượng/risk of bias; 382 preprint | đếm tần suất ≠ sức mạnh bằng chứng | người đọc có thể hiểu "nhiều bài" = "đã giải quyết" | phân tầng lại theo peer-review và theo loại nghiên cứu (kỹ thuật/empirical) | [Paper: PDF p. 4, Section 2.4] |
| Agent-based, RAG, repository-level chỉ được nhắc một câu | taxonomy có thể đã lỗi thời so với 08/2024 | các hướng này là nơi các tác vụ phân tích chương trình đang dịch chuyển | đếm số bài agent trong Appendix B so với ước lượng ngoài | [Paper: PDF p. 14, Section 4.2.1] |

## 14 Kiến thức học được

### Agent-derived knowledge candidates

- **Ba trục phân loại Code LLM:** kiến trúc (encoder-only / encoder-decoder / decoder-only) ↔ loại tác vụ phù hợp (hiểu / seq2seq / sinh) [Paper: PDF p. 5-7, Section 3.1].
- **Bốn nhóm pre-training objective:** sequence modeling (CLM, MLM, MSP, MIP, RTD, MASS, SD), bimodal (BDG, MNG), cấu trúc (IT, EP, NA, CAP), cross-modal (MCL, CMG) [Paper: PDF p. 7, Table 3].
- **Paradigm chuyển dịch trong program repair:** downstream task → component → fine-tuning → zero-shot cloze → hybrid với template-based APR [Paper: PDF p. 20-21, Section 4.4.1]. Có thể áp dụng như khung phân tích cho các tác vụ khác (fault localization, test generation).
- **Mẫu thiết kế "generation-validation-repair"** lặp lại ở nhiều tác vụ: Self-Edit, TestPilot, ChatUniTest, UniTrans [Paper: PDF p. 14, Section 4.2.1; PDF p. 17, Section 4.3.4]. `[Analysis]` đây là motif chung: LLM sinh, công cụ thực thi/phân tích kiểm tra, phản hồi được đưa lại vào prompt.
- **Ba nguồn dữ liệu sạch để giảm data leakage:** viết tay, chương trình mới phát hành sau cutoff, dự án closed-source [Paper: PDF p. 28-29, Section 6].
- **Khoảng cách BLEU vs. Accuracy** trong Table 6: metric bề mặt cao không đảm bảo sửa đúng [Paper: PDF p. 21, Table 6].

## 15 Kết nối với kiến thức hiện có

Context mode `paper-only`: không có nguồn [External] nào được kiểm chứng; người dùng chưa cung cấp kiến thức liên quan.

- `Agent-derived candidate` — **Kết hợp với phân tích chương trình truyền thống:** bài đề xuất tích hợp LLM như một thành phần trong workflow sẵn có (ví dụ test case prioritization dựa trên tương đồng ngữ nghĩa) [Paper: PDF p. 29, Section 6 "Application on More SE Tasks"]; tương ứng các ví dụ LmPa (LLM + program analysis cho decompilation), GPTScan (GPT + static analysis), LLMAO (fault localization không cần coverage) [Paper: PDF p. 16, Section 4.3.1-4.3.3].
- `Agent-derived candidate` — **Patch overfitting** là bài toán lâu đời của APR; bài cho thấy LLM được dùng làm feature extractor, fine-tuned classifier và zero-shot (PatchZero) [Paper: PDF p. 22, Section 4.4.3] — có thể nối với lý thuyết test suite như partial specification.
- **Xung đột cần kiểm chứng:** tác giả khẳng định "larger models usually yield better performance" [Paper: PDF p. 28, Section 6] nhưng đồng thời ghi nhận Compressor đạt 3 MB "without compromising performance" [Paper: PDF p. 27, Section 5.4] — hai nhận định chỉ tương thích khi giới hạn theo tác vụ; cần nguồn ngoài để kết luận.

## 16 Ý tưởng nghiên cứu

### Agent-derived research candidates

**Ý tưởng 1 — Kiểm toán thiên lệch truy hồi của survey LLM4SE (candidate idea)**

- **Tên:** Keyword-induced sparsity audit cho bản đồ LLM-based SE.
- **Hạn chế / quan sát gốc:** danh sách từ khóa SE thiên về code/testing/repair và Req & Design (43), Management (5) được kết luận là "relatively unexplored"; đồng thời Table 5 và Figure 3 mâu thuẫn ở Requirement Engineering (1 vs 7) [Paper: PDF p. 3, Section 2.2; PDF p. 12, Table 5; PDF p. 24, Answer to RQ2; PDF p. 58, Figure 3].
- **Giả thuyết cốt lõi (hypothesis):** Khi bổ sung từ khóa đặc thù của requirements/design/management (ví dụ "user story", "requirements elicitation", "effort estimation", "architecture") vào cùng quy trình lọc, tỷ lệ bài thuộc Req & Design + Management tăng ít nhất gấp đôi so với 48/840 trong Table 5. Bị bác bỏ nếu tỷ lệ tăng không đáng kể (< 20% tương đối).
- **Delta so với bài:** thay đổi *evaluation* của chính quy trình survey (truy hồi), không thay đổi taxonomy.
- **Phương pháp ban đầu:** tái tạo truy vấn gốc trên cùng 3 database với cùng mốc 08/2024; chạy biến thể từ khóa mở rộng; dùng lại tiêu chí lọc (năm ≥ 2017, ≥ 7 trang, hai người gán nhãn + kappa).
- **Kiểm chứng (validation):** so sánh số bài mới theo từng SE phase; biến kiểm soát: database, mốc thời gian, tiêu chí lọc; metric: recall tương đối theo phase, Cohen's kappa; tập đối chứng: danh sách AwesomeLLM4SE.
- **Possible failure mode / failure modes:** (1) truy vấn mở rộng kéo về nhiều bài không phải LLM (precision thấp) khiến chi phí lọc thủ công quá lớn; (2) số bài thật sự ít — khi đó vùng thưa là thật chứ không phải artifact; (3) không tái tạo được truy vấn gốc vì Google Scholar không ổn định theo thời gian.
- **Innovation status:** unverified — prior-art search required.

**Ý tưởng 2 — Đánh giá có kiểm soát data leakage cho tác vụ phân tích chương trình (possible extension)**

- **Tên:** Leakage-stratified benchmark cho fault localization / program repair.
- **Hạn chế / quan sát gốc:** bài nêu data leakage (Defects4J trong CodeSearchNet) và đề xuất 3 nguồn dữ liệu sạch nhưng không định lượng mức ảnh hưởng; Table 6 cho thấy BLEU cao nhưng accuracy thấp và không có độ bất định [Paper: PDF p. 28-29, Section 6 "Clean Evaluation Datasets"; PDF p. 21, Table 6; PDF p. 25, Section 5.1.2].
- **Giả thuyết cốt lõi (hypothesis):** Với cùng một LLM, hiệu năng program repair / fault localization trên bug phát hành sau training cutoff thấp hơn đáng kể (ví dụ ≥ 10 điểm % về số bug sửa đúng) so với bug lịch sử có khả năng bị lộ; mức chênh tương quan với tín hiệu memorization (ví dụ khả năng tái sinh nguyên văn bản vá). Bị bác bỏ nếu chênh lệch không có ý nghĩa thống kê.
- **Delta so với bài:** *data* + *evaluation*: biến đề xuất định tính của bài thành thí nghiệm có nhóm đối chứng.
- **Phương pháp ban đầu:** chia bug thành ba tầng (lịch sử/đã công khai, mới sau cutoff, closed-source hoặc viết tay) theo đúng ba nguồn bài đề xuất; đo memorization bằng prompt chỉ chứa định danh bug.
- **Kiểm chứng (validation):** so sánh giữa các tầng với cùng mô hình, prompt, budget sampling; metric: correct patch rate, Top-1 fault localization, khoảng tin cậy bootstrap; kiểm soát độ khó bug bằng số hunk / độ dài vá.
- **Possible failure mode / failure modes:** (1) bug mới có phân bố độ khó khác (confounding) nên chênh lệch không quy được cho leakage; (2) thiếu dữ liệu closed-source; (3) chi phí truy vấn mô hình đóng lớn và mô hình thay đổi phiên bản trong quá trình thí nghiệm.
- **Innovation status:** unverified — prior-art search required (bài tự nêu EvalGPTFix, HumanEval-Java, ConDefects, HITS là các benchmark liên quan [Paper: PDF p. 25, Section 5.1.2]).
