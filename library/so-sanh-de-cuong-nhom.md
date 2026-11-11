# So sánh: đề cương nhóm KHMT 2 (`references/`) với khảo sát hiện tại của workspace

- **Ngày:** 2026-11-08
- **Tài liệu A (đề cương nhóm):** `references/IT5440_5KH_PhanTich_va_DeCuong.pdf`, 43 trang, "Bản nháp 1", 07/11/2026, nhóm trưởng Nguyễn Tiến Luyện. Phần I phân tích công trình liên quan; Phần II đề cương nghiên cứu (SemTrace-Dep, RQ1–RQ3).
- **Tài liệu B (workspace):** 6 card trong `cards/`, `library/expanded-reading.md`, `library/novelty-audit.md` (Topic Card C1′-mini), `experiments/README.md` (kết quả pilot G1, 06/11).
- **Mức đọc:** đọc toàn văn A. Đối chiếu tài liệu tham khảo bằng tìm chuỗi trong `library/` và `cards/`.

---

## 1. Phạm vi tài liệu

| Tiêu chí | A (đề cương nhóm) | B (workspace) |
|---|---|---|
| Bài gốc đọc sâu | 4 bài [1]–[4], có bảng "mức đã đọc" | 4 bài như A, thêm 2 card RepoMirage và Dolce. Đọc có mục tiêu toàn văn RepoReason |
| Tra cứu bổ sung | Khoảng 9 truy vấn web, 9 bài [6]–[14], chỉ đọc abstract | Khoảng 32 truy vấn trên OpenAlex và Semantic Scholar, cộng trích dẫn xuôi; 38 + khoảng 40 bài, có BibTeX |
| Ánh xạ vào mục 13.1–13.11 của đề cương môn | **Có** (Bảng 6) | **Không có** |
| Bảng xếp loại bằng chứng theo E1–E4 của [3] | **Có** (Bảng 7) | Chỉ có trong từng card |

**Bài có trong A nhưng B chưa có hoặc chỉ nằm trong file tìm kiếm thô:**
- RepoGraph (2410.14684) và SWEzze/OCD (2603.28119): **không có** trong B.
- Trace Gadgets, Program Slices → Causal Clarity (EASE '26), Completion semantics (2607.12490), TraceEval (2605.11006): chỉ có trong `library/search/*.json`, chưa được đưa vào `expanded-reading.md` hay `expanded.bib`.

**Bài có trong B nhưng A thiếu (quan trọng cho kiểm tra tính mới của A):**
- **RepoReason (2601.03731, ACL 2026):** công trình gần nhất. Dùng dynamic slicing, oracle thực thi, repository thật. A không nhắc tới.
- CORE (NeurIPS 2025): phân tích tĩnh làm oracle.
- RepoMirage, Dolce (B đã có card).
- "LLMs Lean on Priors", "How Robustly Do LLMs Understand Execution Semantics?", CoRE: cùng câu hỏi "mẹo tắt hay ngữ nghĩa thật".
- LONGCODEU, RepoQA, Michelangelo, "Positional Biases Shift…", "Found in the Middle".
- Dataflow-Guided Retrieval, GraphCoder, RepoScope: dựng ngữ cảnh theo đồ thị hoặc luồng dữ liệu, sát điều kiện C3 của A.

→ Tuyên bố (b) ở mục I.3.2 của A ("chưa thấy công trình nào cùng lúc…") vẫn có thể đúng, nhưng phải định vị so với RepoReason và nhóm RepoScope/Dataflow-guided trước khi viết vào bài.

## 2. Chỗ hai bên lệch về dữ kiện

| Điểm | A | B | Cần làm |
|---|---|---|---|
| Tình trạng bình duyệt của [2] | "Không xác minh được" | Semantic Scholar ghi **ACL 2025** | Kiểm tra trên ACL Anthology rồi sửa A |
| Hạn nộp | Báo cáo 18–19/11 và 25–26/11; sản phẩm cuối **tháng 12** (chưa rõ ngày) | Giả định **30/11** | Chốt lại một mốc. Nếu là tháng 12 thì kế hoạch của B dư thời gian |
| Mô hình | ≥3 mô hình, ít nhất 1 mô hình trong danh sách của [2]; "không xác minh được mô hình nào sẵn có" | Đã thử endpoint FPT: có **Llama-3.3-70B** và **gemma-3-27b-it**, cả hai đều nằm trong danh sách của [2] | Dùng 1 trong 2 làm mốc tái lập (mục II.11.1 của A). Chưa kiểm tra độ dài ngữ cảnh tối đa của các mô hình này trên endpoint |
| Ngân sách | Khoảng 160 triệu token đầu vào cho 3 mô hình; giá chưa rõ | Giá FPT: UNKNOWN; có prefix cache (khoảng 50k token được cache ở lời gọi thứ hai) | Đo chi phí thật trên một ô pilot |

## 3. Hai hướng đề tài

| Khía cạnh | A: SemTrace-Dep (can thiệp) | B: C1′-mini (chẩn đoán) |
|---|---|---|
| Câu hỏi chính | Dựng ngữ cảnh bằng phân tích chương trình (sắp xếp lại, bao đóng call graph, retrieval) có **khôi phục** semantic recall không; tách phần đóng góp của thứ tự, độ dài và chọn mã | Suy giảm theo vị trí là do **không định vị được** mã (H-ret) hay **không tổng hợp được** nhiều mảnh (H-agg) |
| Dữ liệu | Tổng hợp: hàm cộng/trừ hằng số 3 chữ số, tên ngẫu nhiên, distractor giống cấu trúc | Code thật (toolz), đổi tên alpha, đột biến input, cộng chuỗi ghép từ hàm thật |
| Phân tích chương trình | Call graph tĩnh (AST) cho C3; thực thi làm oracle | Vết gọi hàm động (`sys.setprofile`), backward slice tĩnh cho setup, đổi tên alpha bằng AST, thực thi làm oracle |
| Điều kiện đối chứng đặc trưng | C0 (oracle), C2 (gom về cuối), C4a/b (retrieval nhúng), K1–K5 có hiệu chỉnh Holm | Lexical control trên cùng mảnh; retrieve-then-trace (RTT); no-context; phản thực tế xóa hàm trong và ngoài vết |
| Kiểm chứng thực thi (RQ3) | Có, nhưng A tự nhận RQ3 "gần như tầm thường" | Không có RQ riêng |
| Thống kê | Ngưỡng ghi trước, n = 200 mỗi ô, McNemar, bootstrap, Holm | Hồi quy logistic với hiệu ứng ngẫu nhiên theo mục, bootstrap |
| Phạm vi kết luận | Mức E2, Python, mã tổng hợp | Một hoặc hai mô hình, Python, mức hàm, ngữ cảnh 8k–64k |

**Phần giao nhau:** cả hai cùng xây trên [2]; cùng dùng lexical control; cùng dùng thực thi làm oracle; cùng có điều kiện oracle (C0 của A ≈ `--lengths 0` của B); cùng biến "gom hay rải" (C1 rải rác của A ≈ `spread` của B).

**Phần bổ sung cho nhau:**
- RTT của B là thứ A thiếu để giải thích *vì sao* C2 hay C3 có hiệu quả.
- C2 và C4 của A là thứ B thiếu để nói *nên làm gì*.

## 4. Kết quả pilot của B ảnh hưởng trực tiếp tới thiết kế của A

1. **Chưa thấy suy giảm theo vị trí** với DeepSeek-V4-Flash ở 16k, 32k, 64k (n = 10, nhiễu lớn).
   - H1 của A (A ≥ 15 điểm phần trăm ở 16k) có nguy cơ bị bác bỏ với mô hình hiện hành.
   - Nếu C1 không suy giảm thì RQ2 của A không còn gì để "khôi phục".
   - A đã có R2 cho trường hợp này. Nên chạy pilot RQ1 **trước** khi dựng C2–C4.
2. **Thinking bật sẵn trên endpoint và sửa được lỗi semantic.**
   - A chỉ xem chain-of-thought là biến thể P1.
   - Cần ghi vào phương pháp của A: mọi lời gọi chính gửi `"thinking": {"type": "disabled"}` tường minh.
3. **Hiệu ứng sàn với chuỗi nhiều hàm khi tắt thinking.**
   - Ở B, k = 3 chỉ đạt 0,10–0,22 ngay ở điều kiện oracle.
   - SemTrace-Dep của A dùng k ∈ {3, 5}, d ∈ {1, 2}, m = 3, hằng số 3 chữ số, có thể chạm sàn tương tự.
   - Cần hiệu chỉnh độ khó bằng C0 trước khi đóng băng tham số. A đã có C0, nhưng chưa có bước hiệu chỉnh.
4. **Không tất định ở T = 0:** một số ô chênh tới 0,2 giữa các lần chạy. A đã dự trù chạy lặp trên tập con; với mức chênh này, nên lặp toàn bộ hoặc dùng mô hình hiệu ứng ngẫu nhiên.
5. **Đoán được mà không cần code:** 66% khi giữ tên thật, 5% sau khi đổi tên. A dùng tên ngẫu nhiên nên đã tránh được. Đây là bằng chứng thực nghiệm để A dẫn vào phần mối đe dọa tính hợp lệ.
6. **Lexical chạm trần (1,00)** ở mọi ô. Điều này khớp với điều kiện "lexical ≥ 95%" trong H1 của A, nhưng làm phép so sánh tương tác vị trí × tác vụ mất tác dụng.

## 5. Đề xuất hợp nhất (để nhóm quyết định)

- **Phương án 1: theo A, lấy hạ tầng của B.** Dùng lại `run_eval.py`, cách tắt thinking, `nocontext_filter.py`, quy trình hiệu chỉnh oracle. Bổ sung RTT làm điều kiện phụ trong RQ2. Thêm RepoReason, RepoScope và Dataflow-guided retrieval vào Phần I.
- **Phương án 2: theo B, lấy khung của A.** Giữ câu hỏi H-ret/H-agg trên code thật; thêm C2 (gom về cuối) và C3 (bao đóng call graph) làm biến can thiệp; mượn Bảng 6 (ánh xạ 13.x), Bảng 7 (E1–E4), ngưỡng ghi trước và K1–K5.
- **Việc làm ngay, không phụ thuộc phương án:**
  - Chạy pilot RQ1 với n lớn hơn (≥ 40 mục) ở 16k–64k, cùng một mô hình mốc của [2] (Llama-3.3-70B hoặc Gemma-3-27B), để biết hiệu ứng vị trí còn tồn tại hay không.
  - Chốt ngày nộp cuối.

Chọn phương án là quyết định của nhóm và giảng viên. Mục II.15.1–2 của A cũng đang chờ đúng câu hỏi này.

---

## 6. Cập nhật sau pilot so sánh (09/11)

Số liệu và giới hạn nằm ở `experiments/README.md`, mục "Lượt 3".

**Sửa điểm 4.1 ở trên:** hiệu ứng vị trí **có** xuất hiện với DeepSeek-V4-Flash. Pilot trước không thấy vì chỉ có n = 10, và các mục chưa được lọc theo độ giải được.

| Điểm cần kiểm tra | Kết quả pilot | Hệ quả |
|---|---|---|
| H1 của A (A ≥ 15 điểm phần trăm ở 16k, SemTrace 4 chữ số, ≥ 2 mô hình) | DeepSeek: A = 0,30 ở 16k và 0,53 ở 32k. Gemma: chạm sàn (0–3%), không đánh giá được | Đạt với 1 mô hình. Cần một mô hình thứ hai không chạm sàn, ví dụ Qwen3.6-27B hoặc gemma-4-31B |
| Kiểm tra tái lập II.11.1 (sai lệch ≤ 10 điểm phần trăm so với Bảng 3) | Gemma SemTrace không độn: **50%**, trong khi [2] báo 12,25% | **Không đạt.** Có thể do prompt (không prefill), cách phục vụ mô hình trên FPT hoặc khoảng giá trị x. Phải báo cáo, không được coi là đã tái lập |
| RQ2 của A có còn gì để "khôi phục" | semtrace4, 32k: middle 0,23 so với oracle 0,83 | Còn khoảng 60 điểm phần trăm để khôi phục. RQ2 có ý nghĩa |
| Nhánh code thật của B | DeepSeek: D ≈ +0,10–0,12 (CI sát 0). Gemma: D = +0,31 [+0,15; +0,47] | Có hiệu ứng, nhưng với DeepSeek nhỏ hơn SemTrace. Phù hợp với luận điểm "độ nhạy" của [2] |
| Lexical control | DeepSeek 1,00. Gemma 1,00 (SemTrace) nhưng 0,83 (toolz) | Với Gemma trên code thật, lexical không chạm trần. Điều kiện "lexical ≥ 95%" trong H1 của A không đạt |

**Nhận xét:**
- Hai bộ đo bổ sung cho nhau. SemTrace-4 nhạy hơn với mô hình mạnh, nhưng chạm sàn với mô hình yếu. Mục toolz đo được cả hai mô hình.
- Nếu gộp hai hướng, nên giữ cả hai bộ dữ liệu và chọn độ khó theo từng mô hình dựa trên oracle.

