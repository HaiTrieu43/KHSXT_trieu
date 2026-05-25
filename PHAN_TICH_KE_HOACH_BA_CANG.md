# PHÂN TÍCH FILE KẾ HOẠCH CÁM TUẦN VÕ BÁ CANG 2026

> **File**: `KẾ HOẠCH CÁM TUẦN VÕ BÁ CANG 2026 (1).xlsx`  
> **Thư mục**: `D:\Kê hoạch sản xuât\BACANG\`  
> **Đại lý**: Võ Bá Cang và Lê Thị Bích Thủy  
> **MSKH**: 2000004656  
> **Địa chỉ**: Vĩnh Tân - Tân Uyên - Bình Dương

---

## 1. TỔNG QUAN

### 1.1. Mục đích sử dụng
Đây là **DỰ KIẾN LỊCH LẤY CÁM TRONG TUẦN** - kế hoạch đặt hàng cám theo tuần của **đại lý Võ Bá Cang**. File ghi lại:

1. **Cám bao** (đóng bao 25kg) - Lịch lấy cám theo ngày trong tuần
2. **Cám silo** (cám rời, xe bồn) - Lịch giao cám silo theo ngày

### 1.2. Tại sao file này quan trọng?
Đại lý Võ Bá Cang là **khách hàng lớn** của nhà máy - đặt hàng cố định hàng tuần. Kế hoạch này là **đầu vào trực tiếp** cho kế hoạch sản xuất (FORECAST).

### 1.3. Cấu trúc file
- **22 sheets** = 22 tuần (Tuần 52@ cuối 2025 → Tuần 21 tháng 05/2026)
- Sắp xếp **mới nhất trước** (Tuần 21 ở đầu)

---

## 2. CẤU TRÚC MỖI SHEET

### Phần 1: LỊCH LẤY CÁM BAO (Dòng 6-20)

| Cột | Ý nghĩa |
|-----|---------|
| A (C1) | Tên sản phẩm cám (550P, 552S, 567S...) |
| B-G (C2-C7) | Số bao lấy mỗi ngày (Thứ 2 → Thứ 7) |
| H (C8) | TOTAL BAG - Tổng bao trong tuần |
| I (C9) | TON - Tổng tấn (= BAG × 25kg ÷ 1000) |

### Phần 2: LỊCH GIAO CÁM SILO (Dòng 22-34)

| Cột | Ý nghĩa |
|-----|---------|
| A (C1) | Thứ trong tuần |
| B (C2) | Ngày cụ thể |
| C (C3) | Mã cám silo |
| D (C4) | Số lượng (kg) |

---

## 3. DANH SÁCH SẢN PHẨM CÁM BAO (25kg)

| Mã cám | Loại | Ghi chú |
|--------|------|---------|
| **550P** | Cám 550 bao 5kg | Ít đặt |
| **550S** / **550SX** | Cám 550S / 550SX | Cám chủ lực |
| **551** / **551X** | Cám 551 | Cám gà |
| **551GP** / **551GPX** | Cám 551GP | Cám gà cao cấp |
| **552** | Cám 552 | Cám heo |
| **552S** | Cám 552S | Cám heo đặc biệt |
| **553S** | Cám 553S | Cám heo siêu |
| **562** / **562P** | Cám 562 | Cám vịt |
| **566** | Cám 566 | Cám vịt |
| **567S** | Cám 567S | Cám vịt đặc biệt |

---

## 4. TỔNG HỢP ĐẶT HÀNG THEO TUẦN (2026)

### Cám Bao (25kg):

| Tuần | Thời gian | Tổng BAO | Tổng TẤN |
|------|-----------|----------|----------|
| 21 | 18-23/05 | 9,888 | **247.2** |
| 20 | 11-16/05 | 7,712 | **192.8** |
| 19 | 04-09/05 | 9,536 | **238.4** |
| 18 | 27/04-02/05 | 7,544 | **188.6** |
| 17 | 20-25/04 | 7,008 | **175.2** |
| 16 | 13-18/04 | 6,792 | **169.8** |
| 15 | 06-11/04 | 13,536 | **338.4** |
| 14 | 30/03-04/04 | 13,536 | **338.4** |
| 13 | 23-28/03 | 13,760 | **344.0** |
| 12 | 16-21/03 | 12,784 | **319.6** |
| 11 | 09-14/03 | 10,920 | **273.0** |
| 10 | 02-07/03 | 11,584 | **289.6** |
| 09 | 23-28/02 | 7,952 | **198.8** |
| 08 | 16-21/02 | 2,176 | **54.4** |
| 07 | 09-14/02 | 15,848 | **396.2** |
| 06 | 02-07/02 | 15,712 | **392.8** |

### Cám Silo (rời, xe bồn):
Mỗi tuần giao **2-3 chuyến silo**, mỗi chuyến 14,000-28,000 kg.

Các sản phẩm silo chủ yếu: **550S, 551GP, 552S, 553S, 550SX, 562P**

Tổng silo mỗi tuần: **28,000 - 161,000 kg** (28-161 tấn)

---

## 5. PHÂN TÍCH NHU CẦU

### Top 5 sản phẩm bao được đặt nhiều nhất:

| Sản phẩm | Đặc điểm |
|----------|----------|
| **552S** | Đặt hàng gần như mỗi tuần, 500-6,124 bao/tuần |
| **552** | Đặt thường xuyên, 976-5,107 bao/tuần |
| **567S** | Đặt đều, 940-3,060 bao/tuần |
| **553S** | Đặt không đều, 0-3,320 bao/tuần |
| **562** | Đặt đều, 640-1,952 bao/tuần |

### Quy luật đặt hàng:
- **Thứ 2**: Thường đặt nhiều (1,864-2,840 bao)
- **Thứ 3**: Đặt vừa (1,200-2,840 bao)
- **Thứ 7**: Ít nhất hoặc không đặt
- **Tổng tuần**: Dao động **170-396 tấn** (trung bình ~250 tấn/tuần)

### Xu hướng: 
- Tháng 2-3/2026: Đặt **nhiều** (270-396 tấn/tuần) → Mùa cao điểm
- Tháng 4-5/2026: Đặt **giảm** (170-250 tấn/tuần) → Mùa bình thường

---

## 6. MỐI LIÊN HỆ VỚI CÁC FILE KHÁC

```
KẾ HOẠCH BA CANG (File này)
    ↓ Đơn hàng đại lý lớn nhất
FORECAST (Sale Forecast)
    ↓ Tổng hợp tất cả đơn hàng + dự báo
KẾ HOẠCH SẢN XUẤT
    ↓ Sản xuất theo kế hoạch
TỒN BỒN → FFSTOCK → DAILY SALED → BÁO CÁO
```

### Vai trò trong hệ thống:
| Khía cạnh | Chi tiết |
|-----------|---------|
| **Input** | Đơn đặt hàng → Nhập vào Forecast |
| **Cám Bao** | Ảnh hưởng nhu cầu bao bì (EMPTY BAG) |
| **Cám Silo** | Giao xe bồn trực tiếp, không qua đóng bao |
| **Tần suất** | Cập nhật hàng tuần, trước tuần sản xuất |

---

## 7. LƯU Ý QUAN TRỌNG

> ⚠️ **Đại lý Võ Bá Cang chiếm ~10-15% tổng sản lượng nhà máy** (250 tấn/tuần trên tổng ~2,100-2,500 tấn/ngày × 6 ngày = 12,600-15,000 tấn/tuần)

> ⚠️ **Cám Silo** (xe bồn) không sử dụng bao bì → Không ảnh hưởng EMPTY BAG REPORT nhưng **ảnh hưởng trực tiếp** FFSTOCK (sản lượng sản xuất)

> ⚠️ **Sheet Tuần 08** có lượng đặt rất thấp (54.4 tấn) - có thể là tuần nghỉ Tết Nguyên Đán

---

*Tài liệu phân tích tự động - Ngày 19/05/2026*
