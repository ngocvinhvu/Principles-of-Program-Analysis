# experiments/ — dựng dữ liệu và chạy đánh giá cho C1′-mini

Thiết kế nghiên cứu nằm trong `library/novelty-audit.md`, mục Step 7–8. Mọi lệnh đều chạy từ thư mục gốc của dự án bằng `.venv/bin/python`. Thư viện dùng để dựng dữ liệu: `toolz==1.0.0`, cài trong `.venv`.

| File | Vai trò |
|---|---|
| `build_items.py` | Lấy ví dụ trong docstring (doctest) → kiểm tra ví dụ chạy ra đúng kết quả ghi trong docstring → đột biến hằng số theo một ánh xạ nhất quán → cắt phần setup bằng **backward slice tĩnh** (quan hệ def-use) → chạy và ghi **vết gọi hàm động** (`sys.setprofile`), quy mỗi lời gọi về đơn vị là hàm hoặc class cấp module → kiểm tra lại trong một namespace sạch, chỉ chứa những gì mô hình nhìn thấy. Đầu ra: `data/<lib>_items.jsonl` và `data/<lib>_units.json` (mã nguồn các đơn vị, đã xóa docstring) |
| `build_contexts.py` | Đặt các mảnh vào ngữ cảnh theo bố cục (`start`/`middle`/`end`; `cluster_*`/`spread`) và độ dài mục tiêu. Phần độn lấy từ các hàm khác của toolz trước, rồi đến stdlib. Dựng câu hỏi cho 4 tác vụ: `semantic`, `lexical`, `rtt`, `nocontext` |
| `run_eval.py` | Gọi endpoint tương thích API OpenAI (`LLM_BASE_URL`/`LLM_API_KEY`), **tắt thinking một cách tường minh**, chấm điểm, ghi kết quả ra `results/*.jsonl` |
| `nocontext_filter.py` | Hỏi mọi mục mà không đưa code (3 lần lặp) để tìm các mục đoán được hoặc mô hình đã học thuộc |
| `rename.py` | **(A)** Đổi tên alpha mọi hàm và class của thư viện thành `fn_NNN`/`Cls_NNN`, cả trong các đơn vị code lẫn trong setup và biểu thức của mục. **Kiểm chứng bằng cách chạy thật**: dựng một namespace phẳng gồm toàn bộ code đã đổi tên, chạy lại từng mục, chỉ giữ mục có cùng đáp án và cùng tập mảnh lõi. Đầu ra: `data/<lib>_anon_*` |
| `summarize.py` | Bảng độ chính xác và điểm chép lại theo tác vụ × bố cục, kèm các kiểm tra: thinking có lọt không, số token thật so với ước tính |

```bash
.venv/bin/python experiments/build_items.py --lib toolz --out experiments/data/toolz
.venv/bin/python experiments/run_eval.py --n 5 --lengths 16000 --out experiments/results/pilot_16k.jsonl
.venv/bin/python experiments/summarize.py experiments/results/pilot_16k.jsonl
.venv/bin/python experiments/nocontext_filter.py --reps 3

# A + C (06/11)
.venv/bin/python experiments/build_items.py --lib toolz --synth 400 --out experiments/data/toolz
.venv/bin/python experiments/rename.py --data experiments/data/toolz --out experiments/data/toolz_anon
.venv/bin/python experiments/nocontext_filter.py --data experiments/data/toolz_anon --label "an internal utility library (identifiers anonymised)" --reps 2
.venv/bin/python experiments/run_eval.py --data experiments/data/toolz_anon --n 10 --k-groups 1,3 \
  --lengths 32000,64000 --tasks semantic,lexical,rtt \
  --exclude-guessable experiments/results/toolz_anon_nocontext.jsonl --out experiments/results/pilot_anon_32k64k.jsonl
# --lengths 0 = điều kiện oracle: chỉ đưa các mảnh, không có phần độn
```

## Kết quả bước thử G1 (06/11/2026, DeepSeek-V4-Flash, tắt thinking)

**Dựng dữ liệu (toolz 1.0.0):**
- Có 159 ví dụ doctest ứng viên, giữ lại được **116 mục**; 98 mục đã đột biến được hằng số.
- Số mảnh lõi mỗi mục (k_core): k=1 có 88 mục; k=2 có 19; k=3 có 7; k=4 có 2.
- Kiểm tra bằng mắt 21 mục có k≥2 đã đột biến: vết gọi hàm đúng ở cả 21.

**Chạy thử ở 16k** (10 mục, 100 lời gọi, `results/pilot_16k.jsonl`):
- Không có lỗi API, không có token thinking nào lọt ra.
- Số token thật bằng 0,99–1,05 lần số ước tính (`CHARS_PER_TOKEN = 3.9`).
- **Lexical đạt 1,00 ở mọi ô**: tác vụ chép lại chạm trần ở 16k.
- Semantic đạt 0,6–0,8; rtt đạt 0,8. **Ở 16k chưa thấy chênh lệch theo vị trí.** Với n = 5, kết quả này không có giá trị thống kê.

**Mô hình không cho cùng kết quả mỗi lần chạy:**
- Chạy lại cùng các prompt với `temperature=0` (`results/pilot_16k_v1b_repeat.jsonl` so với `results/pilot_16k_v1_prompt-bug.jsonl`) thì một số ô chênh tới 0,2.
- Vì vậy cần lặp lại mỗi ô nhiều lần, hoặc đưa mục vào mô hình thống kê như hiệu ứng ngẫu nhiên.

**Lỗi câu hỏi đã sửa:**
- Ở bản v1, mô hình có lúc trả lời nguyên văn chuỗi "repr(result)" thay vì giá trị.
- Từ bản này, mọi tác vụ đều phải trả lời theo dạng `ANSWER: <output>`.

**Phát hiện chặn: phần lớn mục đoán được mà không cần code.**
- `nocontext_filter.py` (3 lần lặp, `results/toolz_nocontext.jsonl`): **77/116 mục trả lời đúng mà không cần code**.
- Số mục còn dùng được (đã đột biến và không đoán được): **k=1 có 27 mục; k≥2 chỉ có 8 mục**.
- Nguyên nhân có khả năng nhất: tên hàm của toolz quá dễ hiểu (`take`, `merge`, `get`…), và mô hình đã biết thư viện này. Nguyên nhân này **chưa được kiểm chứng**.

**Hệ quả:** chỉ dùng toolz thì không đủ 40 mục k≥2. Các hướng xử lý được đề xuất trong `library/novelty-audit.md`.

## Lượt 2: A + C (06/11/2026)

**C: chuỗi ghép từ hàm thật** (`build_items.py --synth 400`):
- 1–3 phép biến đổi dãy (take, drop, unique, accumulate, pluck∘sliding_window…), cộng một phép kết thúc (frequencies, groupby, count…).
- Input là list số nguyên ngẫu nhiên.
- Kết quả: 400 ứng viên, giữ được 389 mục. Phân bố k_core: k=2 có 57, k=3 có 92, k≥4 có 232.

**A: đổi tên** (`rename.py`):
- 497/503 mục có cùng đáp án và cùng mảnh lõi khi chạy trên code đã đổi tên.
- 6 mục lỗi, đều do `toolz.curried` không còn trong namespace.
- Tên gốc còn lộ ra qua thuộc tính, ví dụ `_sigs._has_varargs` trong các hàm hạ tầng của curry, và `itertools.count`. Đây là một giới hạn đã biết.

**Đoán được mà không cần code**, sau khi đổi tên (2 lần lặp):
- Tổng cộng **25/497 (5%)**, so với 66% trước khi đổi tên.
- Theo nguồn: doctest 21/108; chuỗi ghép 4/389.

**Chạy thử ở 32k/64k** (10 mục k=1 và 10 mục k=3, 360 lời gọi, khoảng 16,7 triệu token prompt, trong đó 9 triệu được cache; `results/pilot_anon_32k64k.jsonl`):
- Lexical: **1,00 ở mọi ô**, kể cả 64k với tên đã đổi.
- Semantic: k=1 đạt 0,5–0,7; k=3 đạt 0,1–0,4. RTT (k=3) đạt 0,1–0,7.
- Không thấy xu hướng theo vị trí. Với n=10, các khác biệt giữa ô đều nằm trong mức nhiễu.

**Điều kiện oracle**, chỉ đưa các mảnh và không có phần độn (`results/pilot_anon_oracle.jsonl`):
- Semantic k=1: **0,50**. Semantic k=3: **0,10**. RTT k=3: 0,10.
- Diễn giải: **mục k=3 đã chạm sàn ngay cả khi không có ngữ cảnh dài.** Độ khó nằm ở việc tính nhẩm chuỗi hàm khi tắt thinking, không nằm ở ngữ cảnh. Với các mục như vậy, thiết kế không thể đo được ảnh hưởng của vị trí.

**Hiệu chỉnh độ giải được**: chạy oracle 3 lần cho mọi mục k=1–3 không đoán được (`results/toolz_anon_oracle_calib.jsonl`, 678 lời gọi ngắn):

| k | nguồn | số mục | độ chính xác oracle | giải đúng 3/3 |
|---|---|---|---|---|
| 1 | doctest / chuỗi ghép | 58 / 6 | 0,56 / 0,83 | 31 / 5 |
| 2 | doctest / chuỗi ghép | 11 / 57 | 0,45 / 0,33 | 5 / 17 |
| 3 | doctest / chuỗi ghép | 3 / 91 | 0,44 / 0,22 | 1 / 17 |

Số mục giải đúng 3/3 ở oracle: **k=1 có 36, k=2 có 22, k=3 có 18.** Vẫn chưa đủ 40 mục mỗi nhóm.

## Lượt 3: pilot so sánh hai hướng (09/11/2026)

- **Script:** `compare_pilot.py` (chạy tiếp được: chỉ gọi lại các ô lỗi hoặc còn thiếu); tổng hợp bằng `summarize_compare.py`.
- **Kết quả:** `results/compare_deepseek.jsonl`, `results/compare_gemma.jsonl`.
- **Hai nhánh, cùng mẫu prompt, cùng phần độn (toolz đã đổi tên + stdlib), cùng cách chấm:**
  - `semtrace2` / `semtrace4`: SemTrace cài đặt lại theo Listing 1 của 2505 (k ∈ [4,10] phần tử; |y| có 2 hoặc 4 chữ số), mỗi loại 30 mục. Đây là D1 trong đề cương nhóm.
  - `toolz`: 36 mục toolz đã đổi tên, k_core = 1, giải đúng 3/3 ở oracle khi calib bằng **DeepSeek**. Đây là hướng C1′-mini.
- **Mô hình và độ dài:**
  - DeepSeek-V4-Flash: oracle, 16k, 32k.
  - gemma-3-27b-it (có trong danh sách của [2]): oracle, 16k.
- **Bố cục:** start / middle / end. Lexical chỉ chạy ở middle.
- **Endpoint:**
  - Llama-3.3-70B **bị cắt ngầm ở 8.196 token** (dù khai báo ngữ cảnh 32k), nên không dùng được.
  - Gemma bị giới hạn TPM (HTTP 429); lời gọi lỗi được chạy lại với `--workers 1`.
  - Tokenizer của Gemma đếm nhiều hơn ước tính 1,16–1,31 lần.

| Mô hình | Nhánh | Len | oracle | start | middle | end | D = TB(đầu,cuối) − giữa [CI95] |
|---|---|---|---|---|---|---|---|
| DeepSeek | semtrace2 | 16k | 0,90 | 0,87 | 0,80 | 0,90 | +0,08 [−0,02; +0,20] |
| DeepSeek | semtrace2 | 32k | | 0,87 | 0,77 | 0,97 | +0,15 [+0,02; +0,30] |
| DeepSeek | semtrace4 | 16k | 0,83 | 0,50 | 0,43 | 0,73 | +0,18 [+0,03; +0,35] |
| DeepSeek | semtrace4 | 32k | | 0,63 | **0,23** | 0,77 | **+0,47 [+0,28; +0,63]** |
| DeepSeek | toolz | 16k | 1,00 | 0,94 | 0,81 | 0,92 | +0,12 [+0,01; +0,25] |
| DeepSeek | toolz | 32k | | 0,94 | 0,86 | 0,97 | +0,10 [−0,01; +0,22] |
| Gemma 3 27B | semtrace2 | 16k | 0,50 | 0,07 | 0,00 | 0,17 | +0,12 [+0,05; +0,20] |
| Gemma 3 27B | semtrace4 | 16k | 0,13 | 0,00 | 0,00 | 0,03 | sàn |
| Gemma 3 27B | toolz | 16k | 0,72 | 0,61 | **0,31** | 0,61 | **+0,31 [+0,15; +0,47]** |

- **Lexical:** DeepSeek 1,00 ở mọi ô. Gemma 1,00 trên SemTrace nhưng **0,83 trên toolz**.
- **Partial match của Gemma, semtrace2 16k:** 0,49 / 0,26 / 0,68.
- **Giới hạn:**
  - n = 30–36, mỗi ô chỉ chạy 1 lần; trước đây đã thấy mức không tất định tới 0,2 mỗi ô.
  - Chỉ 3 vị trí.
  - Mục toolz được chọn theo calib của DeepSeek, nên thiên vị DeepSeek.
  - Prompt khác [2]: không đặt câu hỏi trước code, không prefill.
  - Phần độn không phải CodeSearchNet như [2].
