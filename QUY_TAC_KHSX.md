# QUY TẮC LẬP KẾ HOẠCH SẢN XUẤT (KHSX)

> Phân tích từ dữ liệu thực tế KHSX THÁNG 5-2026 (19 ngày)
> File: KHSX THANG 5-20261.xlsm

---

## 1. MỖI MÃ CÁM CHỈ XUẤT HIỆN 1 DÒNG DUY NHẤT

Đây là quy tắc **quan trọng nhất**. Dù sản phẩm có nhu cầu từ nhiều nguồn (SILO + Forecast + Bù thiếu), 
tất cả phải **gộp thành 1 dòng duy nhất** trong bảng KHSX.

**Ví dụ ngày 19:**
```
552SF  | 50 mẻ | 420 tấn | WH50kg=170 | SILO TRUCK=250
552F   | 40 mẻ | 336 tấn | WH50kg=236 | SILO TRUCK=100
552    | 12 mẻ | 100.8 tấn | HIGRO25=35.8 | START25=15 | SILO TRUCK=50
552S   |  6 mẻ |  50.4 tấn | HIGRO25=20.4 | SILO TRUCK=30
```

**Quy tắc phân bổ trong 1 dòng:**
- `TỔNG TẤN = Tấn đóng bao (các brand) + Tấn SILO TRUCK`
- Tấn SILO lấy từ Silo Plan
- Phần còn lại đóng bao theo tỷ lệ brand trong Forecast

---

## 2. SỐ MÃ CÁM TỐI ĐA: 31-35 mã/ngày

| Ngày | Mã cám | Mẻ  | Tấn    |
|------|--------|-----|--------|
| 12   | 33     | 269 | 2,239  |
| 13   | 31     | 253 | 2,099  |
| 14   | 33     | 277 | 2,296  |
| 15   | 31     | 282 | 2,294  |
| 16   | 31     | 380 | 3,146  |
| 18   | 35     | 312 | 2,580  |
| 19   | 33     | 294 | 2,446  |

→ Mặc định giới hạn **35 mã cám/ngày**

---

## 3. SẮP XẾP THEO LINE CÁM VIÊN (CỘT V)

Sản phẩm được **nhóm theo LINE CV**, theo thứ tự:

```
LINE 1 → LINE 2 → LINE 3 → LINE 4 → LINE 5 → LINE 6 → LINE 7 → LINE M
```

- Trong cùng LINE, SP SILO (mẻ lớn) thường xếp trước
- LINE "M" (Mixer đặc biệt: 385S, BS07TA) luôn **cuối cùng**
- Mỗi SP có LINE CV cố định (lấy từ sheet FEEDCODE)

---

## 4. LINE ĐÓNG BAO (CỘT W)

| Trường hợp | Cột W ghi | Ví dụ |
|------------|-----------|-------|
| 100% SILO (không đóng bao) | `SILO` | 550SX54PRO, 566XS34 |
| Có đóng bao | Số line (1-8) | 552M → W=5 |
| Vừa SILO vừa đóng bao | Số line đóng bao | 552SF → W=1 (SILO tự động) |

---

## 5. CÔNG SUẤT NGÀY

- **Tối thiểu:** ~2,100 tấn/ngày
- **Mục tiêu:** ~2,250 tấn/ngày
- **Tối đa:** ~2,500 tấn/ngày
- Ngoại lệ: Ngày 16 đạt 3,146 tấn (có thể do tích lũy cuối tuần)

---

## 6. TẤN/MẺ CỐ ĐỊNH CHO TỪNG SẢN PHẨM

- Đa số: **8.4 tấn/mẻ**
- Một số đặc biệt: 8.0 (550SX, 550PRO, 551GP...), 6.0 (522, GT11)
- Giá trị lấy từ sheet **CONG SUAT** trong file Plan.xlsm
- Tấn/mẻ KHÔNG thay đổi giữa các ngày

---

## 7. THỨ TỰ ƯU TIÊN KHI CHỌN SẢN PHẨM

```
Ưu tiên 1: SILO xe bồn + Bá Cang     → BẮT BUỘC, không cắt
Ưu tiên 2: Khách vãng lai              → BẮT BUỘC, không cắt
Ưu tiên 3: Bù hàng thiếu hôm qua      → Ưu tiên giữ, cắt nếu quá 35 mã
Ưu tiên 4: Forecast tuần               → Cắt nếu quá 35 mã (giữ SP tấn lớn)
```

Khi cần cắt để không vượt 35 mã:
1. Giữ tất cả ưu tiên 1 + 2
2. Giữ ưu tiên 3 (sắp xếp theo tấn giảm dần)
3. Lấp đầy slot còn lại bằng ưu tiên 4 (tấn lớn trước)

---

## 8. KHÁNG SINH (CỘT U)

Format chuẩn: `KS/ HC (mã1)/(mã2)`

Các biến thể:
- `KS/ HC (1)/(2)` — phổ biến nhất
- `KS/ HC (1)/(24)` — dòng 510, 510M
- `KS/ HC (4),(6)/(2)|S31` — có suffix S31
- `KS/ HC (4)(8)/(2)|S34` — có suffix S34
- `#N/A` — không có thông tin

---

## 9. CẤU TRÚC FILE KHSX

### Header (Dòng 1-6):
```
A1: CÔNG TY CỔ PHẦN CHĂN NUÔI C.P. VIỆT NAM
A2: Chi Nhánh Tại Bình Dương
A3: Phòng Sản Xuất
A4: KẾ HOẠCH TRỘN          | E4: KẾ HOẠCH ĐÓNG BAO
A5: STT | B5: TÊN CÁM | C5: KẾ HOẠCH (MẺ) | D5: TỔNG (TẤN)
E5-F5: HIGRO 25/40 | G5-H5: CP 25/40 | I5-J5: START 25/40 
K5-L5: NUVO 25/40 | M5-N5: BELL 25/40 | O5-P5: NASA 25/40
Q5-S5: WHITE BAG 25/40/50 | T5: SILO TRUCK
U5: KHÁNG SINH | V5: CÁM VIÊN (LINE SỐ) | W5: ĐÓNG BAO (LINE SỐ)
```

### Data (Dòng 7-41):
- Tối đa 35 dòng sản phẩm
- Mỗi dòng: STT, TÊN CÁM, MẺ, TẤN, phân bổ bao bì, SILO, KS, LINE

### Footer (Dòng 42+):
```
A42: TỔNG (TOTAL) | C42: Tổng mẻ | D42: Tổng tấn
```

### Cột theo dõi thực hiện (Z-AB):
```
Z: THỰC HIỆN (MẺ)
AA: HOÀN THÀNH (%)
AB: LÝ DO CHI TIẾT NẾU KHÔNG ĐẠT 95%
```

---

## 10. CÁC BRAND BAO BÌ

| Cột | Brand | Quy cách |
|-----|-------|----------|
| E   | HIGRO | 25kg |
| F   | HIGRO | 40kg |
| G   | CP    | 25kg |
| H   | CP    | 40kg |
| I   | START FEED | 25kg |
| J   | START FEED | 40kg |
| K   | NUVO  | 25kg |
| L   | NUVO  | 40kg |
| M   | BELL  | 25kg |
| N   | BELL  | 40kg |
| O   | NASA  | 25kg |
| P   | NASA  | 40kg |
| Q   | WHITE BAG | 25kg |
| R   | WHITE BAG | 40kg |
| S   | WHITE BAG | 50kg |
| T   | SILO TRUCK | - |
