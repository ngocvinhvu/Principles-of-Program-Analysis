# Đề tài 5 — Chương 13 · LLM cho hiểu code & phân tích chương trình

> File này là nơi **cập nhật kết quả mới nhất** của thí nghiệm. Mỗi lần chạy/lần phân tích mới,
> cập nhật phần "KẾT QUẢ MỚI NHẤT". Xem thêm báo cáo chi tiết theo ngày trong
> `experiments/results/` và mô tả pipeline trong `experiments/README.md`.

---

## KẾT QUẢ MỚI NHẤT — corrected benchmark (12/11/2026)

**Thiết kế:** filler layout-independent (đã sửa confound), n=40/k-group, 1 run/item/layout,
lengths oracle/4k/16k/32k, task semantic (thinking off, T=0).

**Dữ liệu:** `toolz_final_clean` — **304 mục** (176 k_core=1 + 128 k_core=3), alpha-renamed,
oracle-solvable 3/3, nocontext-filtered.

**Mô hình:** DeepSeek-V4-Flash (target), Qwen3.6-27B (positive control).

### 1. Oracle accuracy
| Model | oracle | 95% CI |
|---|---|---|
| DeepSeek-V4-Flash | 93.8% | [86.2, 97.3] |
| Qwen3.6-27B | 85.0% | [75.6, 91.2] |

### 2. Semantic accuracy theo vị trí (%)
**DeepSeek** — 4k: k1 90/92.5/97.5, k3 72.5/72.5/80/82.5 · 16k: k1 92.5/92.5/92.5, k3 75/72.5/87.5/77.5 ·
32k: k1 90/95/95, k3 70/80/82.5/82.5
**Qwen** — 4k: k1 95/90/95, k3 60/72.5/72.5/67.5 · 16k: k1 90/90/92.5, k3 65/72.5/70/52.5 ·
32k: k1 87.5/87.5/92.5, k3 62.5/65/65/62.5

### 3. Phát hiện chính
- **Lost-in-the-middle KHÔNG tái hiện** — mọi McNemar start-vs-middle p ≥ 0.6 (null; MDE ~15–25pp).
- **Recency đều đặn** — end ≥ start ở **10/10 ô** (cả 2 model, mọi length), trung bình ~+7pp.
- **Gap k1→k3 chủ yếu là độ khó nội tại** — oracle k3 (DeepSeek 87.5%, Qwen 70.0%) đã thấp hơn k1
  (100%); phần aggregation-under-context còn lại nhỏ.
- Con −12pp ở pass đầu (16k cũ) là **artefact của confound filler** (RNG-seed-theo-layout), đã sửa.

### 4. Định hướng bài báo
Pivot sang **methodology (bug harness confound + validity control) + null result + recency**.
Không power-up n≈200 / không 64k / không H-ret distractor.

**Báo cáo chi tiết:** `experiments/results/pilot-12-11-2026.md`

---

## Nhật ký cập nhật
- **12/11/2026** — Đăng kết quả corrected benchmark đầu tiên: null LITM, recency 10/10, oracle-by-k.
  (Từ đây mỗi kết quả mới sẽ được thay thế vào mục "KẾT QUẢ MỚI NHẤT".)
