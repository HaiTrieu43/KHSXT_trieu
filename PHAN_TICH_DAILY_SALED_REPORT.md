# PHÂN TÍCH FILE DAILY SALED REPORT - C.P. VIETNAM (Bình Dương)

> **File**: `DAILY SALED REPORT THANG 5.2026.xlsm`
> **Ngày phân tích**: 19/05/2026
> **Đơn vị**: C.P. Vietnam Corporation - Binh Duong Sales Department
> **Loại file**: Excel Macro-Enabled (.xlsm) - chứa VBA Macro tự động

---

## 1. TỔNG QUAN FILE

### 1.1. Mục đích sử dụng
File này là **hệ thống báo cáo bán hàng hàng ngày** (Daily Saled Report) của nhà máy thức ăn chăn nuôi CP Vietnam - Bình Dương cho tháng 5/2026. File ghi nhận **từng đơn hàng giao cho khách** theo ngày, dùng để:

1. **Theo dõi doanh số bán hàng thực tế theo ngày** (so với Forecast)
2. **Phân tích tỷ lệ bán hàng** theo kênh: Đại lý / Trại / Silo
3. **Quản lý khách hàng**: Theo dõi doanh số từng đại lý/trại
4. **Tổng hợp sản lượng SILO** giao hàng xá
5. **Kiểm soát công thức sản xuất**: Theo dõi mã công thức nào bán được mỗi ngày
6. **Hỗ trợ lập kế hoạch sản xuất**: So sánh Actual vs Forecast để điều chỉnh kế hoạch

### 1.2. Cấu trúc tổng thể
- **37 sheet** tổng cộng
- **6 sheet tổng hợp** (summary) + **31 sheet dữ liệu ngày** (1 sheet = 1 ngày trong tháng)

---

## 2. CHI TIẾT TỪNG SHEET

---

### SHEET 1: `hoanchinh` (306 dòng × 39 cột)
**Mục đích**: Bảng tổng hợp hoàn chỉnh - **Summary toàn bộ tháng theo sản phẩm**

| Cột | Ý nghĩa |
|-----|---------|
| E (C5) | CODE BRAND - Mã thức ăn (VD: 510, 551, 552S...) |
| F (C6) | SPECIAL - Mã đặc biệt (nếu có) |
| G (C7) | PACKING TYPE - Loại đóng gói (25 kgs., 50 kgs., Silo...) |
| H (C8) | CODE FORMULAS - Mã công thức (VD: 112001, 314001...) |
| I-AM (C9-C39) | Ngày 1-31: Sản lượng bán (kg) của từng ngày |

- Dòng 3: **Tổng sản lượng theo ngày** (VD: ngày 2 = 1,449,710 kg)
- Dòng 4 trở đi: Chi tiết từng sản phẩm
- Đơn vị: **kg** (kilogram)

---

### SHEET 2: `MONTH SOLD` (1514 dòng × 42 cột)
**Mục đích**: **Báo cáo bán hàng tháng phân theo thương hiệu** - Là bảng chi tiết nhất

| Cột | Ý nghĩa |
|-----|---------|
| A (C1) | GROUP BRAND - Nhóm thương hiệu |
| B (C2) | CODE BRAND - Mã sản phẩm |
| C (C3) | SPECIAL |
| D (C4) | PACKING TYPE - Quy cách đóng gói |
| E (C5) | CODE FORMULAS - Mã công thức |
| F-AJ (C6-C36) | Ngày 1-31: Sản lượng bán (kg) |
| AK (C37) | TỔNG - Tổng cả tháng |
| AL (C38) | Key ghép (Code+Packing) |
| AM (C39) | Số tháng |

**Phân nhóm thương hiệu** (merged cells cột A):
| Dòng bắt đầu | Nhóm | Mô tả |
|---------------|-------|-------|
| 8 | HIGRO | Thương hiệu HIGRO - dòng 8-22 |
| 24 | CHICKEN | Gà (thương hiệu HIGRO) - dòng 24-44 |
| 47 | BIG FEED | Thức ăn heo lớn - dòng 47-86 |
| 90 | BEEF FEED | Thức ăn bò - dòng 90-101 |
| 103 | DUCK FEED | Thức ăn vịt - dòng 103-112 |
| 114 | CP FEED | Thương hiệu CP - dòng 114-138 |
| 140 | NUVO FEED | Thương hiệu NUVO - dòng 140-149 |
| 151 | BELL FEED | Thương hiệu NASA/BELL - dòng 151-161 |
| 184 | STAR FEED | Thương hiệu STAR - dòng 184-202 |
| 205 | NASA | Thương hiệu NASA - dòng 205-218 |
| 222 | CHICKEN FARM | Gà trại nội bộ - dòng 222-418 |
| 430 | BIG FARM FEED | Heo trại nội bộ - dòng 430-606 |
| 610 | DUCK FEED (Farm) | Vịt trại - dòng 610-641 |
| 672 | KHÁNG SINH | Kháng sinh/phụ gia - dòng 672-690 |

- Dòng 6: **Tổng toàn bộ** = 32,022,270 kg (~32,022 tấn tháng 5)
- Đơn vị: **kg**

---

### SHEET 3: `customer` (1004 dòng × 43 cột)
**Mục đích**: **Báo cáo bán hàng theo khách hàng** - Mỗi dòng = 1 khách hàng

| Cột | Ý nghĩa |
|-----|---------|
| B (C2) | Customer code - Mã khách hàng (VD: 2000052689, 2000073501...) |
| C (C3) | - |
| D (C4) | Name description - Tên khách hàng (VD: "Hộ Kinh Doanh Phú Khang") |
| E (C5) | Tổng cả tháng (kg) |
| F-AJ (C6-C36) | Ngày 1-31: Sản lượng bán cho khách đó (kg) |

- Dòng 3: Tổng toàn bộ = 32,022,270 kg
- ~1000 khách hàng được liệt kê
- Bao gồm cả đại lý cá nhân ("Hộ Kinh Doanh...") và trang trại CP ("Chi Nhánh Công Ty...")

---

### SHEET 4: `TY LE BAN TRONG NGAY` (28 dòng × 39 cột)
**Mục đích**: **Phân tích tỷ lệ bán hàng theo loại đóng gói mỗi ngày**

| Dòng | Loại | Ý nghĩa |
|------|------|---------|
| 3 | Cám đại lý (25 kgs.) | Tổng bán bao 25kg cho đại lý |
| 4 | Cám đại lý (40 kgs.) | Tổng bán bao 40kg cho đại lý |
| 5 | Cám trại (50 kgs.) | Tổng bán bao 50kg cho trại nội bộ |
| 6 | Silo | Tổng bán hàng xá (Silo) |
| 7 | Cám đại lý (10 kgs.) | Tổng bán bao 10kg |
| 8 | Kháng sinh (1 kgs.) | Tổng bán kháng sinh |
| 9 | 550SF | Riêng sản phẩm 550SF |
| 13-15 | Cám đại lý/trại/Silo (Kg) | Tổng hợp lại theo kg |
| 17-19 | Cám đại lý/trại/Silo (%) | **Tỷ lệ phần trăm** |

**Tỷ lệ trung bình tháng 5**:
| Kênh | Tỷ lệ |
|------|--------|
| Cám đại lý (Dealer) | **14.8%** |
| Cám trại (Farm) | **61.4%** |
| Silo | **23.8%** |

**Tổng hợp cuối sheet**:
| Metric | Giá trị |
|--------|---------|
| TOTAL FARM | 19,576,850 kg (61.1%) |
| TOTAL CUSTOMER (Dealer) | 4,844,790 kg (15.1%) |
| TOTAL SILO | 7,600,630 kg (23.7%) |
| **TOTAL FEED SALED IN MONTH** | **32,022,270 kg** |

---

### SHEET 5: `SILO` (263 dòng × 48 cột)
**Mục đích**: **Chi tiết bán hàng Silo (hàng xá)** - Chỉ gồm sản phẩm giao bằng xe bồn

| Cột | Ý nghĩa |
|-----|---------|
| A (C1) | Tên sản phẩm SILO |
| B (C2) | CODE BRAND |
| C (C3) | SPECIAL (mã trại, VD: P32, P33...) |
| D (C4) | CODE FEED - Mã công thức |
| E (C5) | Loại = "Silo" |
| G-AK (C7-C37) | Ngày 1-31: Sản lượng (kg) |
| AL (C38) | TỔNG cả tháng |
| AM (C39) | Key ghép |

- Dòng 4: Tổng SILO = 7,600,630 kg
- ~259 mã sản phẩm SILO
- Mã SPECIAL (P32, P33...) = mã trại/điểm giao hàng

---

### SHEET 6: `CONG` (257 dòng × 40 cột)
**Mục đích**: **Bảng tổng hợp SILO theo số thứ tự** (đánh STT + tên cám + mã công thức)

| Cột | Ý nghĩa |
|-----|---------|
| B (C2) | STT |
| C (C3) | FEED NAME - Tên cám |
| D (C4) | CODE FOMULLA - Mã công thức |
| E-AI (C5-C35) | Ngày 1-31: Sản lượng (kg) |
| AJ (C36) | Tổng cả tháng |

- Dòng 3: Tổng SILO theo ngày
- Dòng cuối (248-257): Bảng tra cứu mã (lookup table cho HT13S, 552F, 552SF, 566F, 567S...)

---

### SHEET 7-37: `1` đến `31` (mỗi sheet ~1004 dòng × 30 cột)
**Mục đích**: **Dữ liệu giao hàng chi tiết từng ngày** - Mỗi sheet = 1 ngày trong tháng

#### Cấu trúc mỗi dòng (1 dòng = 1 đơn hàng):

| Cột | Ý nghĩa |
|-----|---------|
| A (C1) | Key ghép: "{Mã cám}{Packing}" (VD: "55125 kgs.", "552SFS90Silo") |
| C (C3) | Ngày đặt hàng (Sales Order date) |
| D (C4) | Mã đơn hàng (Sales Order number) |
| E (C5) | Mã sản phẩm / Feed Code |
| F (C6) | SPECIAL code (nếu có, VD: S90, S54...) |
| G (C7) | Loại đóng gói ("25 kgs.", "50 kgs.", "Silo") |
| H (C8) | Mã khách hàng (Customer code) |
| I (C9) | Tên khách hàng |
| J (C10) | Số lượng bao (bags) |
| K (C11) | Số lượng bao (duplicate - xác nhận) |
| L (C12) | Luôn = 0 |
| M (C13) | Trọng lượng (kg) |
| N (C14) | Mã sản phẩm SAP |
| O (C15) | SPECIAL (nếu có) |
| P (C16) | Ngày giao hàng (Delivery date) |
| Y (C25) | Mã tháng × 8 hoặc 32 |
| Z (C26) | = 1 (flag) |
| AA (C27) | Số tháng hoặc "Customer" (header) |

**Dòng đặc biệt**:
- Dòng 2: C13 = Tổng SILO ngày, C14 = Tổng tất cả ngày
- Dòng 4: C13 = Tổng toàn bộ ngày đó

**Ví dụ đọc 1 dòng (Sheet '2', Row 5)**:
```
Key: 54825 kgs.
Ngày đặt: 25/04/2026
Mã đơn: 10004126103792
Sản phẩm: 548
Đóng gói: 25 kgs.
Khách hàng: 2000083551 - Hệ Kinh Doanh Tó Liên
Số bao: 86
Trọng lượng: 2,150 kg
Ngày giao: 02/05/2026
```

---

## 3. LUỒNG DỮ LIỆU TRONG FILE

```
Sheet 1-31 (Dữ liệu ngày)
    ↓ Macro VBA tổng hợp
Sheet "MONTH SOLD" (Tổng hợp theo sản phẩm × thương hiệu)
Sheet "customer" (Tổng hợp theo khách hàng)
Sheet "SILO" (Tổng hợp riêng hàng xá)
Sheet "CONG" (Tổng hợp SILO đánh STT)
Sheet "hoanchinh" (Tổng hợp hoàn chỉnh)
Sheet "TY LE BAN TRONG NGAY" (Phân tích tỷ lệ %)
```

---

## 4. THỐNG KÊ THÁNG 5/2026 (tính đến ngày 16/05)

### 4.1. Tổng sản lượng bán
| Metric | Giá trị |
|--------|---------|
| **Tổng sản lượng bán** | **32,022,270 kg = ~32,022 tấn** |
| Ngày bán cao nhất | Ngày 11: 2,797,905 kg (~2,798 tấn) |
| Ngày bán thấp nhất | Ngày 3: 2,025,450 kg (~2,025 tấn) |
| Trung bình/ngày (14 ngày làm việc) | ~2,287 tấn/ngày |

### 4.2. Phân theo kênh
| Kênh | Sản lượng (kg) | Tỷ lệ |
|------|---------------|--------|
| Cám trại (Farm 50kg) | 19,576,850 | 61.1% |
| Silo (hàng xá) | 7,600,630 | 23.7% |
| Cám đại lý (25kg) | 4,629,350 | 14.5% |
| Cám đại lý (10kg) | 167,040 | 0.5% |
| Cám đại lý (40kg) | 48,400 | 0.2% |

### 4.3. Ngày không bán hàng
- Ngày 1, 10, 17 = 0 (Chủ nhật hoặc ngày nghỉ)
- Ngày 18-31 = chưa có dữ liệu (chưa đến)

---

## 5. MỐI LIÊN HỆ VỚI FILE FORECAST

| Đặc điểm | FORECAST | DAILY SALED REPORT |
|-----------|----------|-------------------|
| Mục đích | Dự báo bán hàng **tuần tới** | Ghi nhận bán hàng **thực tế ngày** |
| Đơn vị | **Tấn** | **Kg** (×1000 = tấn) |
| Phân loại | Theo loài (HOG/BROILER/DUCK...) | Theo thương hiệu (HIGRO/CP/STAR...) |
| Kênh | DEALER + FARM (Swine/Integrate) | Đại lý (25/40kg) + Trại (50kg) + Silo |
| Thời gian | 1 tuần | 1 tháng (31 ngày) |
| Chi tiết | Theo mã công thức + packing | Theo đơn hàng + khách hàng cụ thể |

**Cách so sánh**: 
- Forecast W21 tổng = 11,903 tấn/tuần → kỳ vọng ~1,984 tấn/ngày (6 ngày)
- Actual trung bình = ~2,287 tấn/ngày → Bán vượt forecast ~15%

---

## 6. LƯU Ý KỸ THUẬT

### 6.1. Lỗi trong file
- **#VALUE!** ở cột C27 sheet "hoanchinh" - lỗi công thức
- **#REF!** ở nhiều cột trong sheet ngày (C31-C36) - tham chiếu bị mất
- **#N/A** ở một số ô lookup - không tìm thấy mã sản phẩm
- Một số ô bị đánh dấu date sai (serial value ngoài giới hạn)

### 6.2. VBA Macro
- File .xlsm chứa macro tự động tổng hợp dữ liệu từ 31 sheet ngày
- Macro tính tổng vào các sheet tổng hợp (MONTH SOLD, customer, SILO, hoanchinh)

### 6.3. Đơn vị dữ liệu
- **Tất cả số liệu trong file này đều tính bằng KG** (kilogram)
- Khác với file Forecast tính bằng TẤN
- Quy đổi: 1 tấn = 1,000 kg

---

*Tài liệu này được tạo tự động bởi AI dựa trên phân tích dữ liệu file Excel gốc.*
