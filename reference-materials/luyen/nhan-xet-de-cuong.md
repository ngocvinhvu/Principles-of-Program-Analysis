# Nhận xét đề cương của Luyen

> Tài liệu này là nhận xét / phản biện có đối chiếu đề cương `IT5440_5KH_PhanTich_va_DeCuong.pdf`
> (nhóm KHMT 2, Đề tài 5 / Chương 13) với **kết quả thực nghiệm đã hiệu chỉnh** của nhóm (12/11/2026).
> Mục đích: xác định phần nào của đề cương còn theo được, phần nào phải điều chỉnh / bác bỏ, và đề
> xuất con đường khả thi nhất cho hạn báo cáo **30/11**.

---

## 1. Tóm tắt đề cương (cốt lõi thiết kế)

- **RQ1 (H1):** với ít nhất hai trong ba mô hình, ở L=16k trên SemTrace 4 chữ số, biên độ vị trí
  **A ≥ 15 điểm %** (mã đích ở giữa) trong khi lexical ≥ 95%. Bác bỏ nếu cận trên CI 95% của A < 5pp.
- **RQ2 (H2):** ở 16k, vị trí giữa, **Acc(C3) − Acc(C1) ≥ 15 điểm %** cho ≥ 2 mô hình; phân rã
  (C2−C1)/(C3−C1). C0–C4 là các điều kiện chọn ngữ cảnh: C0 oracle, C1 ngữ cảnh thô, C2 giảm độ dài,
  C3 bao đóng đồ thị gọi hàm tĩnh, C4a truy xuất nhúng. SemTrace-Dep = bộ sinh mã nhiều hàm phụ thuộc.
- **RQ3 (H3):** kiểm chứng bằng thực thi phát hiện ≥ 15% dự đoán sai so với giám khảo LLM không thực
  thi. Đề cương tự đánh giá "gần như tầm thường", ưu tiên thấp.
- **Đóng góp 1–4:** (1) bộ dữ liệu SemTrace-Dep; (2) phân rã sắp xếp/độ dài/chọn mã; (3) kiểm tra lại
  hiệu ứng vị trí — **rõ ràng ghi "kết quả dương hay âm đều là đóng góp"**; (4) gói tái lập.

---

## 2. Kết quả thực nghiệm hiệu chỉnh của nhóm (đã sửa confound, 12/11)

Thiết kế: filler layout-independent, n=40/cell, 1 run/item/layout, lengths oracle/4k/16k/32k,
task semantic, 2 mô hình (DeepSeek-V4-Flash, Qwen3.6-27B). Dataset `toolz_final_clean` (304 mục:
176 k=1 + 128 k=3). Chi tiết: `experiments/results/pilot-12-11-2026.md`.

- **Lost-in-the-middle KHÔNG tái hiện:** mọi McNemar start-vs-middle p ≥ 0.6 (4k/16k/32k). Con −12pp ở
  pass đầu là **artefact của confound** (RNG-seed-theo-layout làm filler khác nhau mỗi vị trí), đã sửa.
- **Recency đều đặn:** end ≥ start ở 10/10 ô, trung bình ~+7pp (cần kiểm chứng bằng pooled stats, và
  kiểm tra khả năng "end" chỉ vì sát câu hỏi).
- **Gap k1→k3 chủ yếu là độ khó item** (oracle-by-k: k1 100% cả 2 model; k3 87.5% DeepSeek / 70% Qwen),
  residual aggregation/context-dilution chỉ cỡ 5–9pp (một run n=40, CI ~±12–15pp).

---

## 3. Đối chiếu: phần nào còn theo được, phần nào phải sửa

### 3.1 RQ1 (H1, hiệu ứng vị trí ≥ 15pp) — KHÔNG được hỗ trợ
Kết quả hiệu chỉnh cho A thực tế ~ 0–2.5pp (start-vs-middle), có ô đảo dấu. H1 không đạt. **Nhưng điều
này KHÔNG phá vỡ đề cương**: chính đóng góp 3 của đề cương cho phép kết quả âm tính. Với n=40, MDE
~15–25pp nên **chưa thể khẳng định "không có hiệu ứng"**; chỉ có thể nói "không có hiệu ứng ≥ 15pp",
cần pooled n=304 + báo CI (hoặc TOST với margin khai báo trước) để chặt.

→ **Điều chỉnh:** viết lại RQ1 thành *kiểm tra lại có giới hạn* (bounded re-test), báo CI và giới hạn
phát hiện (MDE), không kỳ vọng 15pp.

### 3.2 RQ2 (H2, C3−C1 ≥ 15pp) — bất khả thi về số học trên item hiện có
Headroom giữa at-context và oracle chỉ ~5–9.5pp (k3), trung bình k1+k3 ~3–5pp (k1 ở trần ~93%).
H2 cần 15pp nên **không đạt được trên toolz** — chạy full C0–C4 để test H2 sẽ chỉ xác nhận H2 thất bại.
SemTrace-Dep (benchmark khó hơn, sâu hơn) là tình huống duy nhất H2 sống được, nhưng **không thực tế
để sinh/lọc/kiểm chứng trong ~3 tuần còn lại**.

→ **Điều chỉnh:** no-go full C0–C4 và SemTrace-Dep. Thay bằng **phép đo headroom có giới hạn**.

### 3.3 RQ3 (H3) — cắt
Đề cương tự đánh giá "gần như tầm thường", ưu tiên thấp. → Cắt, ghi là future work.

### 3.4 Đóng góp 2 (phân rã) và 4 (tái lập) — giữ nguyên giá trị
Đúng hướng, giữ.

### 3.5 Phát hiện mới chưa có trong đề cương — nên bổ sung
- **Methodology contribution:** bug harness (RNG-seed-theo-layout → filler khác nhau mỗi vị trí) +
  cách sửa, trình bày như **sensitivity analysis** kèm noise floor từ filler-seed (không tự nhận "có
  bug" như một lỗi, mà là một dạng lỗi harness có thể tồn tại ở nhiều benchmark).
- **Dấu hiệu recency** (end ≥ start) — khám phá thêm, cần pooled stats để claim.
- **Cảnh báo đọc số liệu "nhiều hàm kém hơn"**: phần lớn gap là độ khó item chứ không phải aggregation.

---

## 4. Đề xuất con đường khả thi nhất cho 30/11

**Hướng chính — "bounded re-test + headroom"** (đóng khung theo RQ1/đóng góp 3 của đề cương):

1. **Thí nghiệm bổ sung (chốt ≤ 18/11, ≤ 5 ngày):**
   - Chạy **C0 / C1 / C3 tại 16k trên toàn bộ 304 mục**, 2 mô hình, 3 filler-seeds → đóng khung là
     **ceiling/headroom**: context selection có thể phục hồi tối đa bao nhiêu, kèm CI (KHÔNG phải
     hypothesis test H2). n=304 cắt MDE xuống ~6–9pp.
   - **Chạy lại harness buggy cũ trên cùng 304 mục** → biến con −12pp thành minh chứng có kiểm soát.
   - Measure noise floor từ filler-seed replicates.
2. **Viết bài (19–28/11):** cấu trúc gợi ý (xem mục 5). Freeze 18/11; buffer 29–30/11.

**Dự phòng (quyết định 18/11):** cùng bài nhưng bỏ phần headroom, dùng đúng dữ liệu đã có, tái phân tích
pooled — đóng khung negative-result + methodology note (workshop/short paper).

**Không làm:** chạy full C0–C4; xây SemTrace-Dep; chạy 64k; thêm điều kiện H-ret distractor.

---

## 5. Cấu trúc claim đề xuất (abstract)

1. Context — nhiều claim lost-in-the-middle cho code; đề cương nhóm dự đoán hiệu ứng ≥ 15pp.
2. Gap — hầu hết nghiên cứu vị trí không khống chế sự biến thiên filler giữa các layout, không báo power.
3. Method — harness filler layout-independent; 304 mục toolz; 2 mô hình; start/middle/end tại 4k/16k/32k;
   filler-seed replicates.
4. Result 1 (confound) — filler-seed-theo-layout tạo hiệu ứng giả −12pp; sau khi sửa, start-vs-middle
   pooled = Xpp [CI], loại trừ ≥15pp.
5. Result 2 (recency) — end hơn start ~7pp [CI], nhất quán giữa mô hình và độ dài.
6. Result 3 (headroom) — context oracle đóng trần lợi ích của chọn ngữ cảnh ~5–10pp; gap k1→k3 phần lớn
   tồn tại ngay cả khi không có ngữ cảnh nhiễu.
7. Limits — một repo, một họ tác vụ, 2 mô hình, giới hạn power.
8. Contribution — re-test theo phong cách pre-registered (đúng tinh thần đóng góp 3), kèm gói tái lập.

Cắt RQ3, nêu là future work. Mô tả trung thực sự lệch khỏi đề cương: H1/H2 như đã nêu không được hỗ trợ
hoặc không khả thi để kiểm trên item hiện có; đề cương tự cho phép null là kết quả chấp nhận được.

---

## 6. Kết luận

Theo đề cương **nguyên trạng** là không khả thi: H1 (hiệu ứng vị trí ≥ 15pp) và H2 (C3−C1 ≥ 15pp) đều
không đạt được trên dữ liệu hiệu chỉnh của nhóm. Nhưng theo **đề cương đã hiệu chỉnh** (bounded re-test
+ headroom + methodology + recency, cắt RQ3) là khả thi và là con đường duy nhất còn đủ sức cho 30/11,
đồng thời nhất quán với triết lý "dương hay âm đều là đóng góp" mà chính đề cương đã nêu.

---

*Ngày: 12/11/2026. Người soạn: nhóm KHMT 2. Tham khảo: kết quả thí nghiệm tại
`experiments/results/pilot-12-11-2026.md`; phân tích/phản biện: Claude Code (analyst), mô hình benchmark:
DeepSeek-V4-Flash, Qwen3.6-27B.*
