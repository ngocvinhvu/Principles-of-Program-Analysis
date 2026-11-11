# 01 Research canon

## Sự kiện từ tài liệu (nguồn: cards/, library/novelty-audit.md)
- **L1** (Štorek và cộng sự, arXiv 2505.13353, card):
  - Thí nghiệm đặt 1 hàm mục tiêu ở 11 vị trí trong 20–80 distractor (khoảng 4k–16k token), trên 10 LLM.
  - Lexical recall gần như không phụ thuộc vị trí. Semantic recall giảm theo vị trí: median Δ 53,36% trên CRUXEval, tới 92,73% trên SemTrace.
  - Xóa 50% dòng code thì CRUXEval chỉ giảm 44,15% (I) / 59,74% (O). Tác giả coi đây là dấu hiệu dùng shortcut.
  - Phạm vi: một hàm, ngữ cảnh ≤16k.
- **L2** (RepoReason, arXiv 2601.03731, ACL 2026; đọc toàn văn có mục tiêu):
  - Dùng repository thật. Oracle là môi trường thực thi, với input đã đột biến.
  - Dynamic slicing được dùng làm thước chẩn đoán độ khó (ESV, MCL, DFI). Bài nêu hiện tượng "aggregation deficit".
  - Agent tự tìm code, nên bài không kiểm soát vị trí và không có đối chứng lexical.
- **L3** (CORE, NeurIPS 2025; chỉ đọc abstract): phân tích tĩnh (data/control dependency) làm đáp án chuẩn, ở mức chương trình hoặc hàm.
- **L4** (RepoMirage, arXiv 2605.26177, card): perturbation trên SWE-Bench Verified làm resolved rate giảm từ 66,80% xuống 49,78%; số file truy cập tăng từ 4,77 lên 13,24 ("exploration drift"). Bài về agent, không kiểm soát vị trí.
- **L5** (DOLCE, arXiv 2409.06338, card): phân loại 44 task long-context thành nhóm retrieval và nhóm holistic, bằng cách lấy mẫu observation span. Không có code thực thi.
- **L6** (Code Comprehensor, arXiv 2610.30016, card): call graph tĩnh (CodeGraph), tài liệu phân cấp và retrieval đa phương thức cho repository lớn. Đây là hướng giải quyết bằng retrieval.
- **L7** (Survey 2312.15223, card; survey 2608.21107, card): điểm yếu chung của đánh giá là data leakage và benchmark cho phép shortcut. 2608.21107 đề xuất evidence ladder E1–E4.
- **L8** (chỉ biết tên và năm từ library/expanded.bib): Lost in the Middle (TACL 2024); CRUXEval (2024); RepoQA (2024); LONGCODEU (ACL 2025); RepoReasoner (PACMSE 2026); LLMs Lean on Priors, Not PL Semantics (2025); Code-QA-Bench (2026); CodeMind (TSE 2026).

## Sự kiện từ pilot của nhóm (experiments/README.md, ngày 06/11/2026; mô hình DeepSeek-V4-Flash, tắt thinking)
- **E1:**
  - Dựng được 116 mục từ doctest của toolz 1.0.0.
  - Khi hỏi không đưa code, 77/116 mục được trả lời đúng.
  - Sau khi đổi tên alpha, trên 497 mục (gồm cả mục chuỗi ghép), chỉ còn 25 mục (5%) trả lời đúng khi không có code.
- **E2:**
  - 389 mục chuỗi ghép từ hàm thật.
  - Đổi tên được kiểm chứng bằng cách chạy lại: 497/503 mục cho cùng đáp án và cùng tập mảnh.
- **E3:** pilot 32k/64k với n=10 mỗi nhóm:
  - lexical đạt 1,00 ở mọi ô;
  - semantic k=1 đạt 0,5–0,7; semantic k=3 đạt 0,1–0,4;
  - oracle (chỉ đưa các mảnh) k=3 chỉ đạt 0,10.
- **E4:**
  - Ở `temperature=0`, cùng một prompt có thể cho kết quả khác nhau (ô chênh tới 0,2).
  - Thinking bật theo mặc định; tắt được bằng `"thinking": {"type": "disabled"}`.
- **E5:** chạy oracle 3 lần, số mục giải đúng 3/3: k=1 có 36, k=2 có 22, k=3 có 18.

## Ràng buộc
- Hạn nộp 30/11/2026.
- Mô hình dùng qua API FPT Cloud (DeepSeek-V4-Flash; có thêm Qwen3.6-27B, Llama-3.3-70B, gpt-oss-120b).
- Nhóm quen Python, chưa vững tracing và AST.

## Thuật ngữ
- **lexical recall:** chép lại nguyên văn code. **semantic recall:** dự đoán hành vi khi chạy.
- **mảnh (fragment):** hàm hoặc class cấp module có trong vết gọi hàm động của mục.
- **k_core:** số mảnh, sau khi loại các hàm hạ tầng.
- **oracle condition:** chỉ đưa các mảnh, không có phần độn.
- **H-ret:** suy giảm do không định vị được mảnh. **H-agg:** suy giảm do không tổng hợp được nhiều mảnh.

## Nhận định bị cấm
- "Chưa ai nghiên cứu…" / "đề tài hoàn toàn mới".
- "Mô hình bị lost-in-the-middle ở mức repository": chưa quan sát được.
- "H-agg được xác nhận": n quá nhỏ, và oracle k=3 đã ở sàn.
- Mọi kết luận khái quát vượt ra ngoài một mô hình, Python, toolz.

## Nhận định chưa giải quyết
- N6 (Robustness & Reasoning Fidelity in Long-Context Code QA) và LoCoBench chưa đọc toàn văn.
- Chưa biết dữ liệu và code của RepoReason có công khai không.
- Giá trên FPT Cloud: chưa biết.
