# PHÂN TÍCH FILE SALE FORECAST - C.P. VIETNAM (Bình Dương)

> **File**: `W21.(18-23-05-) SALEFORECAST 2026.xlsx`
> **Ngày phân tích**: 19/05/2026
> **Đơn vị**: C.P. Vietnam Corporation - Binh Duong Sales Department

---

## 1. TỔNG QUAN FILE

### 1.1. Cấu trúc file
- **21 sheet** (W1 → W21), mỗi sheet tương ứng **1 tuần** trong năm 2026
- Tên sheet theo format: `W{số tuần}.{ngày bắt đầu}-{ngày kết thúc}-2026`
- Mỗi sheet có cấu trúc **giống hệt nhau**: ~700 dòng, 31 cột (A-AE)
- Sheet cuối cùng (W21): tuần 18/05 - 23/05/2026

### 1.2. Thông tin header (Dòng 1-6)
| Dòng | Nội dung |
|------|----------|
| 1 | C.P. VIETNAM CORPORATION |
| 2 | BINH DUONG SALES DEPARTMENT |
| 3 | SALES FORECAST |
| 4 | From DD/MM/YYYY to DD/MM/YYYY (khoảng thời gian tuần) |
| 5 | ATTN: Danh sách người nhận (Mr. PEERAPHOL PUAPUNT, Mr. LOC, Mr. VINH, Mr. THÔNG, Mr. ÁNH, Mrs. Oanh, Mrs. Luynh) |
| 6 | From: Mr Tuan (người gửi forecast) |

### 1.3. Mã biểu mẫu
- **QT-KD-01/BM01** - Biểu mẫu quản lý chất lượng
- Lần ban hành: 03
- Ngày ban hành: 15/06/2017

---

## 2. CẤU TRÚC CỘT (31 cột)

### 2.1. Thông tin sản phẩm (Cột A-I, dòng 7-9)

| Cột | Header Dòng 8 | Header Dòng 9 | Ý nghĩa |
|-----|---------------|---------------|---------|
| **A** (C1) | FORMULAR CODE | - | Mã công thức sản phẩm (VD: 312001, 314001...) |
| **B** (C2) | DIE (Size) | - | Kích thước khuôn ép viên (mm): 2.5, 2.8, 3.5, 4, M, C, SC, BC, MC |
| **C** (C3) | PACKING SIZE (kg) | - | Quy cách đóng gói: 1, 5, 25, 30, 40, 50 kg hoặc "SILO" (hàng xá/rời) |
| **D** (C4) | FEED CODE | HIGRO | Mã thức ăn thương hiệu HIGRO |
| **E** (C5) | FEED CODE | CP | Mã thức ăn thương hiệu CP |
| **F** (C6) | FEED CODE | STAR | Mã thức ăn thương hiệu STAR |
| **G** (C7) | FEED CODE | NUVO | Mã thức ăn thương hiệu NUVO |
| **H** (C8) | FEED CODE | NASA | Mã thức ăn thương hiệu NASA |
| **I** (C9) | FEED CODE | FARM | Mã thức ăn cho trang trại nội bộ (FARM) |

### 2.2. Số lượng FEED - tấn (Cột J-W)

| Cột | Sub-group | Header | Ý nghĩa |
|-----|-----------|--------|---------|
| **J** (C10) | DEALER | HIGRO | Số tấn bán qua đại lý - thương hiệu HIGRO |
| **K** (C11) | DEALER | CP | Số tấn bán qua đại lý - thương hiệu CP |
| **L** (C12) | DEALER | STAR | Số tấn bán qua đại lý - thương hiệu STAR |
| **M** (C13) | DEALER | NUVO | Số tấn bán qua đại lý - thương hiệu NUVO |
| **N** (C14) | DEALER | NASA | Số tấn bán qua đại lý - thương hiệu NASA |
| **O** (C15) | DEALER | **TOTAL** | **Tổng tấn DEALER** = C10+C11+C12+C13+C14 |
| **P** (C16) | FARM | SWINE | Số tấn cho trại heo nội bộ (SWINE FARM) |
| **Q** (C17) | FARM | INTEGRATE | Số tấn cho trang trại tích hợp (INTEGRATE) |
| **R** (C18) | FARM | **TOTAL** | **Tổng tấn FARM** = C16+C17 |
| **S** (C19) | GRAND TOTAL | TONS | **Tổng tấn đóng bao** (Dealer + Farm - Silo) |
| **T** (C20) | GRAND TOTAL | SILO | **Tổng tấn hàng xá/SILO** (rời, không đóng bao) |
| **U** (C21) | GRAND TOTAL | **TOTAL** | **TỔNG CỘNG TẤT CẢ** = C19 + C20 |
| **V** (C22) | - | - | (Cột trống, thường = 0) |
| **W** (C23) | REMARK | - | Ghi chú (VD: "Chờ đại lý đặt thêm", "Chờ hết tồn kho mới SX") |

### 2.3. Số lượng BAG - đơn vị bao (Cột X-AE)

| Cột | Sub-group | Header | Ý nghĩa |
|-----|-----------|--------|---------|
| **X** (C24) | DEALER | HIGRO | Số bao đại lý - HIGRO |
| **Y** (C25) | DEALER | CP | Số bao đại lý - CP |
| **Z** (C26) | DEALER | STAR | Số bao đại lý - STAR |
| **AA** (C27) | DEALER | NUVO | Số bao đại lý - NUVO |
| **AB** (C28) | DEALER | NASA | Số bao đại lý - NASA |
| **AC** (C29) | DEALER | **TOTAL** | Tổng bao DEALER |
| **AD** (C30) | FARM | - | Tổng bao FARM |
| **AE** (C31) | - | **GRAND TOTAL** | **Tổng bao tất cả** |

> **Quy đổi**: Số bao = Số tấn × 1000 / Packing size (kg)
> VD: 40 tấn × 1000 / 25kg = 1,600 bao

---

## 3. CẤU TRÚC DỮ LIỆU - 2 PHẦN CHÍNH

### PHẦN 1: DỮ LIỆU CHÍNH (Dòng 10 - 336)
Đây là phần **Sale Forecast chi tiết** theo loài vật nuôi, chia thành các SECTION:

#### 3.1. HOG (Heo) - Dòng 10 → 162

| Sub-section | Dòng | Tổng DEALER (tấn) | Tổng FARM (tấn) | **GRAND TOTAL (tấn)** |
|-------------|-------|-------------------|-----------------|----------------------|
| **PRE-STARTER** (Thức ăn tập ăn) | 10-51 | 216 | 1,324 | **1,540** |
| **FATTENING** (Thức ăn vỗ béo) | 52-118 | 958 | 6,149 | **7,107** |
| **BREEDER** (Thức ăn heo giống) | 119-149 | 366 | 1,295 | **1,661** |
| **LOCAL** (Sản phẩm nội địa) | 150-161 | 0 | 0 | **0** |
| **TOTAL HOG** | **162** | **1,540** | **8,768** | **10,308** |

> HOG chiếm ~87% tổng sản lượng nhà máy

#### 3.2. BROILER (Gà thịt) - Dòng 163 → 214

| Sub-section | Dòng | Tổng DEALER (tấn) | Tổng FARM (tấn) | **GRAND TOTAL (tấn)** |
|-------------|-------|-------------------|-----------------|----------------------|
| Broiler Chicken (Gà thịt công nghiệp) | 163-198 | 272 | 368 | **640** |
| Local Chicken (Gà ta) | 199-210 | 64 | 0 | **64** |
| Breeder Chicken (Gà giống) | 211-213 | 0 | 0 | **0** |
| **TOTAL BROILER** | **214** | **336** | **368** | **704** |

#### 3.3. LAYER (Gà đẻ) - Dòng 215 → 246

| **TOTAL LAYER** | **246** | **218** | **0** | **218** |

#### 3.4. DUCK (Vịt) - Dòng 247 → 277

| **TOTAL DUCK** | **277** | **153** | **200** | **353** |

#### 3.5. QUAIL (Cút) - Dòng 278 → 283

| **TOTAL QUAIL** | **283** | **76** | **0** | **76** |

#### 3.6. COW (Bò) - Dòng 284 → 330

| **TOTAL COW** | **330** | **244** | **0** | **244** |

#### 3.7. GOAT (Dê) - Dòng 331 → 335

| **TOTAL GOAT** | **335** | **0** | **0** | **0** |

#### GRAND TOTAL (Dòng 336)

| Kênh | HIGRO | CP | STAR | NUVO | NASA | **TOTAL** |
|------|-------|----|------|------|------|-----------|
| DEALER | 2,099 | 132 | 264 | 0 | 72 | **2,567** |
| FARM (Swine) | - | - | - | - | - | **5,019** |
| FARM (Integrate) | - | - | - | - | - | **4,317** |
| **FARM TOTAL** | - | - | - | - | - | **9,336** |
| **TONS (đóng bao)** | - | - | - | - | - | **8,609** |
| **SILO (hàng xá)** | - | - | - | - | - | **3,294** |
| **TỔNG SẢN LƯỢNG** | - | - | - | - | - | **11,903** |

---

### PHẦN 2: LABORATORY (Dòng 337 → 697)
Phần này là bảng phụ dùng cho **Phòng thí nghiệm / QC** (Laboratory):
- Liệt kê lại **tất cả mã công thức (FORMULAR CODE)** giống Phần 1
- Chỉ có các cột C10-C18 và C21 (chỉ có số tấn, không có số bao)
- **Không có cột DIE, PACKING SIZE, FEED CODE** (cột B, C, D-I trống)
- Mục đích: tổng hợp sản lượng theo mã công thức để phòng Lab chuẩn bị nguyên liệu/kiểm tra
- Dòng 697: **TOTAL** = kiểm chứng tổng khớp với GRAND TOTAL ở dòng 336

---

## 4. GIẢI THÍCH CÁC TRƯỜNG QUAN TRỌNG

### 4.1. Mã công thức (FORMULAR CODE - Cột A)
- Mã số (6-8 chữ số) đại diện cho **công thức phối trộn** nguyên liệu
- VD: `312001` = công thức Pre-Starter 550S, `320001` = công thức Fattening 552S
- Cùng 1 FORMULAR CODE có thể xuất hiện **nhiều dòng** với packing khác nhau (25kg, 50kg, SILO)

### 4.2. DIE Size (Cột B)
Kích thước khuôn ép viên trên máy Pellet:
| Giá trị | Ý nghĩa |
|---------|---------|
| 2.5 | Khuôn 2.5mm (viên nhỏ, chủ yếu Pre-Starter) |
| 2.8 | Khuôn 2.8mm (phổ biến nhất cho Fattening) |
| 3.5 | Khuôn 3.5mm |
| 4 | Khuôn 4mm (viên lớn, thường cho Farm/Breeder) |
| M | Mash - dạng bột (không ép viên) |
| C | Crumble - dạng mảnh vụn |
| SC | Small Crumble |
| BC | Big Crumble |
| MC | Medium Crumble |

### 4.3. Packing Size (Cột C)
| Giá trị | Ý nghĩa |
|---------|---------|
| 1 | Bao 1kg (ít dùng) |
| 5 | Bao 5kg (có loại 5×5 = combo 5 bao nhỏ) |
| 25 | Bao 25kg (phổ biến nhất cho DEALER) |
| 30 | Bao 30kg |
| 40 | Bao 40kg |
| 50 | Bao 50kg (phổ biến cho FARM) |
| SILO | Hàng xá/rời, giao bằng xe bồn (không đóng bao) |

### 4.4. Thương hiệu (Brand)
CP Vietnam bán hàng qua **5 thương hiệu** cho kênh DEALER:
| Brand | Cột Feed Code | Cột Tấn | Cột Bao |
|-------|---------------|---------|---------|
| **HIGRO** | D (C4) | J (C10) | X (C24) |
| **CP** | E (C5) | K (C11) | Y (C25) |
| **STAR** | F (C6) | L (C12) | Z (C26) |
| **NUVO** | G (C7) | M (C13) | AA (C27) |
| **NASA** | H (C8) | N (C14) | AB (C28) |

Và 1 kênh nội bộ **FARM** (cột I/C9) cho trang trại CP.

### 4.5. Kênh phân phối
- **DEALER**: Bán qua hệ thống đại lý bên ngoài (5 thương hiệu trên)
- **FARM**: Cung cấp nội bộ cho trang trại CP Vietnam
  - **SWINE** (C16): Trại heo CP
  - **INTEGRATE** (C17): Trại tích hợp (gà, vịt... do CP quản lý)

### 4.6. SILO vs TONS
- **TONS** (C19): Tổng tấn hàng **đóng bao** (25kg, 50kg...)
- **SILO** (C20): Tổng tấn hàng **xá/rời** (giao xe bồn, không đóng bao)
- **TOTAL** (C21) = TONS + SILO = Tổng sản lượng thực cần sản xuất

### 4.7. Cột REMARK (C23)
Ghi chú đặc biệt từ sales:
- "Chờ đại lý đặt thêm" → Số lượng có thể tăng
- "Chờ hết tồn kho mới SX" → Chưa cần sản xuất ngay
- "Chờ khách hàng đặt" → Đơn hàng chưa chốt

---

## 5. CÔNG THỨC TÍNH

### 5.1. Tính tổng theo kênh
```
DEALER TOTAL (C15) = HIGRO(C10) + CP(C11) + STAR(C12) + NUVO(C13) + NASA(C14)
FARM TOTAL (C18) = SWINE(C16) + INTEGRATE(C17)
```

### 5.2. Tính tổng chung
```
TONS (C19) = Tổng tấn đóng bao = DEALER TOTAL + FARM TOTAL - SILO
SILO (C20) = Tổng tấn hàng xá (lấy từ các dòng có Packing = "SILO")
GRAND TOTAL (C21) = TONS(C19) + SILO(C20)
```

### 5.3. Quy đổi tấn → bao
```
Số bao = Số tấn × 1000 / Packing Size (kg)
VD: 48 tấn bao 25kg = 48 × 1000 / 25 = 1,920 bao
```

---

## 6. THỐNG KÊ TUẦN W21 (18-23/05/2026)

### 6.1. Tổng sản lượng theo loài

| Loài | DEALER (tấn) | FARM (tấn) | SILO (tấn) | **TỔNG (tấn)** | Tỷ trọng |
|------|-------------|------------|------------|----------------|----------|
| HOG | 1,540 | 8,768 | 3,206 | **10,308** | 86.6% |
| BROILER | 336 | 368 | 0 | **704** | 5.9% |
| DUCK | 153 | 200 | 0 | **353** | 3.0% |
| COW | 244 | 0 | 60 | **244** | 2.0% |
| LAYER | 218 | 0 | 0 | **218** | 1.8% |
| QUAIL | 76 | 0 | 28 | **76** | 0.6% |
| GOAT | 0 | 0 | 0 | **0** | 0.0% |
| **TỔNG** | **2,567** | **9,336** | **3,294** | **11,903** | **100%** |

### 6.2. Tổng sản lượng theo thương hiệu (DEALER)

| Thương hiệu | Tấn | Tỷ trọng Dealer |
|-------------|------|------------------|
| HIGRO | 2,099 | 81.8% |
| STAR | 264 | 10.3% |
| CP | 132 | 5.1% |
| NASA | 72 | 2.8% |
| NUVO | 0 | 0.0% |
| **TOTAL DEALER** | **2,567** | **100%** |

### 6.3. Tổng sản lượng theo kênh

| Kênh | Tấn | Tỷ trọng |
|------|------|----------|
| FARM (Swine) | 5,019 | 42.2% |
| FARM (Integrate) | 4,317 | 36.3% |
| DEALER | 2,567 | 21.6% |
| **TỔNG** | **11,903** | **100%** |

### 6.4. Thống kê sản phẩm
- Tổng mã sản phẩm (FORMULAR CODE): **659 dòng**
- Sản phẩm có forecast > 0: **164 dòng** (24.9%)
- Sản phẩm forecast = 0: **495 dòng** (75.1%)

---

## 7. LƯU Ý ĐẶC BIỆT

### 7.1. Lỗi #REF! trong file
- Cột C24 (Bao HIGRO) và C29 (Tổng bao DEALER) tại dòng GRAND TOTAL (336) bị lỗi **#REF!**
- Nguyên nhân: có công thức tham chiếu đến ô đã bị xóa hoặc di chuyển
- Ảnh hưởng: không tính được tổng số bao DEALER chính xác

### 7.2. Dòng dữ liệu đặc biệt
- Một FORMULAR CODE có thể xuất hiện **nhiều dòng** (khác packing: 5kg, 25kg, 50kg, SILO)
- Cùng 1 dòng có thể có **nhiều FEED CODE** ở các cột brand khác nhau (cùng công thức, khác thương hiệu)
- VD: Dòng 28 (Row 28): FORMULAR=314001, có FEED CODE ở cả HIGRO(551), CP(951), STAR(HT11)

### 7.3. SILO (hàng xá)
- Sản phẩm SILO có Packing Size = "SILO" (cột C)
- Số tấn SILO được ghi vào C20 thay vì C19
- Sản phẩm SILO **không có số bao** (cột X-AE trống)

### 7.4. Sản phẩm combo
- Một số sản phẩm có packing đặc biệt: `5*5` (5 bao × 5kg = combo 25kg)
- VD: `550S(5*5)`, `551(5*5)`

---

## 8. CÁCH ĐỌC 1 DÒNG DỮ LIỆU (VÍ DỤ)

**Dòng 14** (Row 14):
```
FORMULAR CODE: 312021
DIE Size: 2.5mm
Packing: 25kg
FEED CODE: 550PRO (thương hiệu HIGRO)
DEALER HIGRO: 40 tấn
DEALER TOTAL: 40 tấn
GRAND TOTAL TONS: 40 tấn
GRAND TOTAL: 40 tấn
BAG DEALER HIGRO: 1,600 bao (= 40 × 1000 / 25)
BAG DEALER TOTAL: 1,600 bao
```

**Dòng 65** (Row 65):
```
FORMULAR CODE: 320101
DIE Size: 4mm
Packing: 50kg
FEED CODE: 552SF (FARM)
FARM SWINE: 480 tấn
FARM INTEGRATE: 1,350 tấn
FARM TOTAL: 1,830 tấn
GRAND TOTAL TONS: 1,830 tấn (đóng bao)
GRAND TOTAL: 1,830 tấn
BAG FARM: 36,600 bao (= 1,830 × 1000 / 50)
BAG GRAND TOTAL: 36,600 bao
```

---

## 9. MỤC ĐÍCH SỬ DỤNG

File SALE FORECAST này được dùng để:
1. **Lập kế hoạch sản xuất (KHSX)**: Xác định sản lượng cần sản xuất tuần tới
2. **Chuẩn bị nguyên liệu**: Phòng Lab/QC dùng Phần 2 để tính toán nguyên liệu
3. **Phân bổ máy Pellet**: Dựa vào DIE Size để phân máy ép viên phù hợp
4. **Kế hoạch đóng gói**: Dựa vào Packing Size và số bao để chuẩn bị bao bì
5. **Kế hoạch logistics**: SILO cần xe bồn, hàng đóng bao cần pallet + xe tải
6. **Quản lý tồn kho**: Kết hợp với tồn kho hiện tại để quyết định thứ tự sản xuất

---

*Tài liệu này được tạo tự động bởi AI dựa trên phân tích dữ liệu file Excel gốc.*
