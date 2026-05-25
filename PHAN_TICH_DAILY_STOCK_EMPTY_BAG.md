# PHÂN TÍCH FILE DAILY STOCK EMPTY BAG REPORT - C.P. VIETNAM

> **File**: `DAILY STOCK EMPTY BAG REPORT  17-05-2026 .xlsm`  
> **Thư mục**: `D:\Kê hoạch sản xuât\FSTOCK-BAG\`  
> **Ngày báo cáo**: 17/05/2026  
> **Đơn vị**: CÔNG TY CỔ PHẦN CHĂN NUÔI C.P VIỆT NAM - Chi Nhánh Tại Bình Dương  
> **Bộ phận**: Kho thành phẩm  
> **Người gửi**: Mr Thái  
> **Gửi đến**: Peeraphol Puapunt / Mr Ánh / Mr Hiển / Mr Thông

---

## 1. TỔNG QUAN FILE

### 1.1. Mục đích sử dụng
File này là **BÁO CÁO TỒN KHO BAO BÌ RỖNG HÀNG NGÀY** (Empty Bags Stock Daily Report). Bao bì là vật tư quan trọng cho nhà máy - mỗi loại cám cần loại bao riêng. File theo dõi:

1. **Tồn kho bao rỗng** (REMAIN/BALANCE) - Số bao còn trong kho chưa sử dụng
2. **Nhập bao mới** (RECEIVED) - Bao mua về từ nhà cung cấp
3. **Sử dụng bao** (USAGE) - Bao được dùng để đóng gói cám thành phẩm
4. **Day On Hand** - Số ngày bao tồn kho đủ dùng (= Balance ÷ Avg Usage/ngày)
5. **Forecast Usage** - Dự kiến sử dụng bao theo kế hoạch sản xuất
6. **On The Way** - Bao đang trên đường giao (đã đặt, chưa nhận)

### 1.2. Cấu trúc file
- **9 sheets** tổng cộng
- **4 sheet báo cáo chính** theo thương hiệu bao
- **1 sheet tổng hợp** (TOTAL)
- **4 sheet hỗ trợ/dữ liệu** (MAP, Bao Trắng, SUMPK, USAGE)

---

## 2. CHI TIẾT TỪNG SHEET

---

### SHEET 1: `HIGRO` (105 dòng × 234 cột)
**Mục đích**: Tồn kho bao thương hiệu **HIGRO** - dùng cho cám bán đại lý

#### Cấu trúc cột chính:
| Cột | Ý nghĩa |
|-----|---------|
| A (C1) | STT |
| B (C2) | PRODUCT CODE - Mã bao bì (VD: 1290D203010025) |
| C (C3) | PRODUCT NAME - Tên bao + kích thước (VD: BagO25- 301- 52x87-93-B-000-H) |
| D (C4) | SIZE - Cỡ bao (5, 25, 40kg) |
| E (C5) | REMAIN - Tồn đầu mẫu cũ (Old Market) |
| F (C6) | REMAIN - Tồn đầu mẫu mới (New Market) |
| G (C7) | RECEIVED - Nhập mẫu cũ |
| H (C8) | RECEIVED - Nhập mẫu mới |
| I (C9) | USAGE - Sử dụng mẫu cũ |
| J (C10) | USAGE - Sử dụng mẫu mới |
| K (C11) | BALANCE - Tồn cuối mẫu cũ |
| L (C12) | BALANCE - Tồn cuối mẫu mới |
| M (C13) | TOTAL - Tổng tồn cuối |
| N (C14) | ACTUAL BAGS/DAY - Thực tế sử dụng bao/ngày |
| O (C15) | DAY ON HAND (Actual) - Số ngày tồn theo thực tế |
| P (C16) | EST.USAGE BAGS/WEEKLY - Ước tính sử dụng bao/tuần |
| Q (C17) | DAY ON HAND (Weekly) |
| R (C18) | DAY ON HAND (Forecast) |
| S (C19) | EST.USAGE BAGS/DAY - Ước tính forecast/ngày |
| T (C20) | ON THE WAY - Bao đang trên đường |
| U (C21) | D.O.H TO - DOH bao gồm hàng đang về |
| V (C22) | - |
| W (C23) | D.O.H TO (tổng) |
| X (C24) | REMARKS (% NEW MARKET) - Tỷ lệ mẫu mới |
| Y (C25) | TOTAL DAYS OF USAGE |
| Z-AW (C26-C49+) | Lịch sử sử dụng theo tuần (6 ngày/tuần × nhiều tuần) |

**Đặc biệt**: Phân biệt **OLD MARKET** (mẫu cũ) và **NEW MARKET** (mẫu mới) - Hiện 100% bao mẫu mới

#### Danh sách sản phẩm bao HIGRO (61 loại):
Bao 25kg: 301, 302, 352, 384, 385S, 502, 510, 510S, 510M, 511, 511B, 511L, 511M, 511S, 511AS, 521, 521Pro, 521SPro, 522, 522Pro, 524(viên), 524(mảnh), 540, 544, 545, 548, 549, 550S, 550SX, 550Pro, 551, 551X, 551Pro, 551GP, 551GPX, 552, 552E, 552Pro, 552M, 552MX, 552S, 552SX, 552SPro, 553, 553S, 562, 566, 567, 584, 585, 594, 595, 596  
Bao 5kg: 550S, 550P

#### Tổng hợp:
| Loại | Tồn kho (bao) |
|------|----------------|
| **Bao 25kg** | 187,409 |
| **Bao 5kg** | 4,570 |
| **Thread (chỉ)** | *(phần cuối sheet)* |

#### Phụ lục cuối sheet (Dòng 80+): **THREAD COLOUR STOCK**
Theo dõi tồn kho chỉ may bao - 4 loại sản phẩm

---

### SHEET 2: `CP&STAR` (76 dòng × 4088 cột)
**Mục đích**: Tồn kho bao thương hiệu **CP** và **STAR** (2 brand trên cùng 1 sheet)

#### Phần 1: CP BRAND (Dòng 4-23) - 16 loại bao
Bao 25kg: 884, 885S, 940, 949, 944, 951, 952, 952S, 952SX, 953, 953S, 966, 967, 967S, 984, 991-18

**Tổng CP**: 19,532 bao (sau sử dụng 335 bao ngày hôm đó)

#### Phần 2: STAR BRAND (Dòng 28-64) - 32 loại bao
Bao 25kg: BS04, BS04A, BS05S, BS14, HT11, HT11GP, HT12, HT12S, HT12SX, HT13, HT13S, HG16, HG17, HG17S, VT11, VT12, GD04, GD14(viên), GD14(mảnh), GT11, GT11S, GT12, GT12A(viên), GT12A(mảnh), GT12S, GT12AS(viên), GT12AS(mảnh), GT12BS, GT12B  
Bao 40kg: BS06TA, BS10TA, BS06LD, BS10LD

**Tổng STAR**:  
| Loại | Tồn kho (bao) |
|------|----------------|
| Bao 25kg | 65,565 |
| Bao 40kg | 7,210 |

---

### SHEET 3: `NASA & NUVO` (47 dòng × 3750 cột)
**Mục đích**: Tồn kho bao thương hiệu **NASA** và **NUVO**

#### Phần 1: NASA BRAND (Dòng 4-17) - 10 loại bao
Bao 25kg: 6884, 6895, 6911, 6924, 6949, 6951, 6952, 6953, 6991, 6995

**Tổng NASA**: 19,949 bao

#### Phần 2: NUVO BRAND (Dòng 22-30) - 5 loại bao
Bao 25kg: 9651, 9652, 9652S, 9666, 9667

**Tổng NUVO**: 4,930 bao

---

### SHEET 4: `FARM` (48 dòng × 4105 cột)
**Mục đích**: Tồn kho bao **FARM INTEGRATE** - dùng cho cám trại (bao 50kg)

17 loại bao 50kg: 510NF, 511ANF, 511NF, 513F, 540F, 548F, 549F, 550SF, 551F, 551GPF, 552F, 552WDF, 552SF, 553MF, 562PF, 566F, 567SF

**Tổng FARM**:
| Metric | Giá trị |
|--------|---------|
| BALANCE (tồn cuối) | **163,875 bao** |
| USAGE (sử dụng ngày) | 14,524 bao |
| REMAIN (tồn đầu) | 178,399 bao |

**Bao tiêu thụ nhiều nhất**: 552SF (29,313 bao tồn), 552F (23,938), 511NF (16,744), 550SF (14,694)

---

### SHEET 5: `TOTAL` (39 dòng × 13 cột)
**Mục đích**: **BẢNG TỔNG HỢP TẤT CẢ THƯƠNG HIỆU**

| Thương hiệu | Cỡ bao | Tồn đầu | Nhập | Sử dụng | Tồn cuối |
|-------------|--------|---------|------|---------|---------|
| HI-GRO | 5 kg | 4,570 | 0 | 0 | **4,570** |
| HI-GRO | 25 kg | 189,677 | 0 | 2,268 | **187,409** |
| CP | 25 kg | 19,867 | 0 | 335 | **19,532** |
| STAR | 25 kg | 65,565 | 0 | 0 | **65,565** |
| STAR | 40 kg | 7,210 | 0 | 0 | **7,210** |
| NUVO | 25 kg | 4,930 | 0 | 0 | **4,930** |
| NASA | 25 kg | 19,949 | 0 | 0 | **19,949** |
| FARM | 50 kg | 178,399 | 0 | 14,524 | **163,875** |
| **GRAND TOTAL** | | **490,167** | **0** | **17,127** | **473,040** |

**Chỉ số quan trọng**:
| Metric | Giá trị |
|--------|---------|
| **DAY ON HAND (Actual)** | **27.6 ngày** |
| **DAY ON HAND (Forecast)** | **12.9 ngày** |

**Forecast bao bì theo tháng**:
| Tháng | Bao dự kiến | Bao/ngày |
|-------|------------|----------|
| Tháng 5 | 953,960 | 36,691 |
| Tháng 6 | 954,060 | 36,695 |
| Tháng 7 | 945,860 | 36,379 |

**Tỷ lệ mẫu bao**: 100% NEW MARKET (mẫu mới)

---

### SHEET 6: `MAP` (288 dòng × 20 cột)
**Mục đích**: **Bảng mapping bao bì ↔ Forecast** - So sánh tồn kho bao vs nhu cầu

| Cột | Ý nghĩa |
|-----|---------|
| A-G | Thông tin bao: Mã, tên, code bao bì, size, tồn kho |
| L (C12) | Mã bao tồn kho |
| M (C13) | Số lượng bao tồn hàng ngày |
| N (C14) | Code cám forecast đặt hàng |
| O (C15) | Số lượng bao đặt hàng forecast |
| P (C16) | **So sánh** (Tồn - Forecast) → Âm = thiếu bao |
| Q (C17) | Code cám (nhóm 2) |
| R (C18) | Số lượng bao forecast (nhóm 2) |
| S (C19) | **Số lượng bao cần bổ sung** |
| T (C20) | Ngày nhập dự kiến |

**Ví dụ thiếu bao**:
- 552SF50: Forecast 36,600 bao → Thiếu **-7,287 bao** → Nhập dự kiến 18.5/05
- 552F50: Forecast 33,200 bao → Thiếu **-9,262 bao** → Nhập dự kiến 18.5/05
- 553MF50: Forecast 11,400 bao → Thiếu **-5,373 bao** → Nhập dự kiến 19.5/05
- 553S25: Forecast 5,600 bao → Thiếu **-2,869 bao** → Nhập dự kiến 18.5/05

---

### SHEET 7: `Bao Trắng` (11 dòng × 28 cột)
**Mục đích**: Tồn kho **bao trắng** (plain bags) - bao không in thương hiệu, dùng tạm

| Sản phẩm | Size | Tồn (bao) |
|----------|------|-----------|
| 513F (bao trắng Farm) | 25 | 3,408 |
| Bao Trắng thường | 25 | 0 |
| Bao Trắng (Túi Nylon) | 40 | 0 |
| Bao Trắng thường | 40 | 458 |

---

### SHEET 8: `SUMPK` (160 dòng × 18 cột)
**Mục đích**: **Dữ liệu sản xuất** - Bao bì sử dụng cho sản xuất ngày 17/05

Gồm cột trạng thái: **ĐÃ CẮT** (đã cắt bao để đóng gói) / **CHƯA CẮT** (chưa xử lý)

| Sản phẩm | Trạng thái | Bao SX | Kg |
|----------|-----------|--------|-----|
| 510 (25kg) | ĐÃ CẮT | 1,572 | 39,300 |
| 552F (50kg) | ĐÃ CẮT | 4,249 | 212,450 |
| 552SF (50kg) | ĐÃ CẮT | 2,700 | 135,000 |
| 551GPF (50kg) | ĐÃ CẮT | 2,538 | 126,900 |
| 550SF (50kg) | ĐÃ CẮT | 2,430 | 121,500 |
| 540F (50kg) | CHƯA CẮT | 1,497 | 74,850 |
| **Grand Total** | | **17,127** | **791,275 kg** |

---

### SHEET 9: `USAGE` (134 dòng × 11 cột)
**Mục đích**: **Chi tiết xuất bao** - So sánh bao lấy từ kho vs bao thực sử dụng

| Cột | Ý nghĩa |
|-----|---------|
| B | Product Code (mã bao) |
| C | Product Name |
| E (C5) | Quantity - Số bao lấy ra từ kho |
| G (C7) | SUMPK - Số bao thực sử dụng (= cắt đóng gói) |
| H (C8) | CẮT WF THÊM - Chênh lệch (dư/thiếu) |

**Tổng**: 38,492 bao lấy ra, 17,127 bao sử dụng → 21,365 bao dư chưa cắt (lưu kho sản xuất)

---

## 3. LUỒNG DỮ LIỆU

```
Nhà cung cấp bao bì
    ↓ RECEIVED (nhập)
Kho bao bì rỗng (DAILY STOCK EMPTY BAG)
    ↓ USAGE (xuất dùng)
Nhà máy sản xuất (SUMPK - cắt bao)
    ↓ Đóng gói thành phẩm
Kho thành phẩm (FFSTOCK)
    ↓ Bán hàng
DAILY SALED REPORT
```

---

## 4. CÔNG THỨC TÍNH

```
BALANCE = REMAIN + RECEIVED - USAGE

DAY ON HAND (Actual) = BALANCE ÷ ACTUAL BAGS/DAY

DAY ON HAND (Forecast) = BALANCE ÷ EST.USAGE BAGS/DAY

D.O.H TO = (BALANCE + ON THE WAY) ÷ EST.USAGE BAGS/DAY
```

---

## 5. TỔNG HỢP TỒN KHO BAO BÌ NGÀY 17/05/2026

### Tổng tồn kho: **473,040 bao**
### Sử dụng trong ngày: **17,127 bao** (= 791,275 kg cám)
### Day On Hand: **27.6 ngày** (thực tế) / **12.9 ngày** (theo forecast)

| Thương hiệu | Tồn kho (bao) | DOH (ngày) |
|-------------|---------------|------------|
| HIGRO 25kg | 187,409 | ~14-27 |
| STAR 25kg | 65,565 | ~15-150 |
| CP 25kg | 19,532 | ~18-44 |
| NASA 25kg | 19,949 | ~7-175 |
| NUVO 25kg | 4,930 | ~11-200 |
| **FARM 50kg** | **163,875** | ~3-41 |
| STAR 40kg | 7,210 | N/A |
| HIGRO 5kg | 4,570 | ~69-73 |

### ⚠️ Cảnh báo bao thiếu (từ sheet MAP):
| Loại bao | Thiếu (bao) | Ngày nhập dự kiến |
|----------|-------------|-------------------|
| 552SF 50kg | -7,287 | 18-19/05 |
| 552F 50kg | -9,262 | 18-19/05 |
| 553MF 50kg | -5,373 | 19-20/05 |
| 553S 25kg | -2,869 | 18-19/05 |

---

## 6. MỐI LIÊN HỆ VỚI CÁC FILE KHÁC

| File | Mối quan hệ |
|------|------------|
| **FFSTOCK** | Bao rỗng → SX → Thành phẩm (FFSTOCK) |
| **FORECAST** | Forecast sản xuất → Tính nhu cầu bao bì |
| **DAILY SALED REPORT** | Bán hàng → Tiêu thụ bao bì gián tiếp |
| **Kế hoạch sản xuất** | SX theo kế hoạch → Cần đủ bao bì đúng loại |

---

*Tài liệu phân tích tự động - Ngày 19/05/2026*
