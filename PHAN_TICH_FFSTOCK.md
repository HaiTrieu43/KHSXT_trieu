# PHÂN TÍCH FILE FFSTOCK - BÁO CÁO TỒN KHO THÀNH PHẨM

> **File**: `FFSTOCK 17 -05-2026.xlsm`  
> **Thư mục**: `D:\Kê hoạch sản xuât\FSTOCK-BAG\`  
> **Ngày báo cáo**: 17/05/2026  
> **Đơn vị**: CÔNG TY CỔ PHẦN CHĂN NUÔI C.P VIỆT NAM - Chi Nhánh Tại Bình Dương  
> **Bộ phận**: Kho thành phẩm  
> **Người gửi**: Mrs. Nguyen  
> **Gửi đến**: Mr. Peeraphol Puapunt / Mrs. Thanh Thu / Mrs. Le Thi Y / Mr. Ánh

---

## 1. TỔNG QUAN FILE

### 1.1. Mục đích sử dụng
File này là **BÁO CÁO TỒN KHO CÁM THÀNH PHẨM HÀNG NGÀY** (Finished Feed Daily Report / FFSTOCK), ghi nhận:

1. **Tồn kho đầu ngày** (REMAIN) - số bao còn trong kho
2. **Nhận trong ngày** (RECEIVE) - sản xuất mới + nhận chuyển kho
3. **Xuất trong ngày** (USAGE) - bán hàng + điều chỉnh + chuyển kho
4. **Tồn kho cuối ngày** (BALANCE) - số bao còn lại
5. **Tổng bán cả tháng** (Total Sale) - tổng sản lượng bán tích lũy
6. **Trung bình bán/ngày** (Sales Average) - để tính Day On Hand
7. **Số ngày tồn bán hàng** (Day On Hand) - Balance ÷ Sales Average

### 1.2. Cấu trúc file
- **15 sheets** tổng cộng
- **4 sheet báo cáo chính** (PRO-NASA, BRAN, INTGRATE, REMIX)
- **6 sheet dữ liệu/tra cứu** (Map, data, pro, Sheet3, Sheet6, Sheet4)
- **4 sheet hỗ trợ** (CBOUT, CBIN, AJOUT - điều chỉnh kho)
- **1 sheet virus** (XL4Poppy - tàn dư virus Excel macro cũ, đã bị Kaspersky xử lý)

---

## 2. CHI TIẾT TỪNG SHEET CHÍNH

---

### SHEET 2: `PRO-NASA` (88 dòng × 149 cột)
**Mục đích**: Tồn kho thương hiệu **HIGRO (dòng PRO)** và **NASA/BELL**

#### Phần 1: HI-GRO FEED (Thương hiệu HIGRO) - Dòng 9-34

| Cột | Ý nghĩa |
|-----|---------|
| A (C1) | STT |
| B (C2) | FEED CODE - Mã sản phẩm (VD: 550Pro, 551Pro, 552Pro...) |
| C (C3) | Pellet Size - Kích cỡ viên (dạng mm) |
| D (C4) | PACK SIZE - Cỡ bao (25kg, 50kg, 5*5, silo) |
| E (C5) | REMAIN - Tồn đầu (bao) |
| F (C6) | Produce - Sản xuất (bao) |
| G (C7) | Adj in - Điều chỉnh thêm (bao) |
| H (C8) | Trans in - Nhận chuyển (bao) |
| I (C9) | Sell out - Bán hàng (bao) |
| J (C10) | Bán hàng (Kg) |
| K (C11) | Adj out - Điều chỉnh giảm (bao) |
| L (C12) | Trans out - Chuyển (bao) |
| M (C13) | BALANCE - Tồn cuối (bao) |
| N (C14) | Tồn cuối (Kg) |
| O (C15) | Total Sale - Tổng bán tháng (Kg) |
| R (C18) | Sales Average - TB bán/ngày (Kg/ngày) |
| S (C19) | Day On Hand - Số ngày tồn |
| T (C20) | REMARK - Ghi chú |
| U (C21) | NOT SALE - Ngừng bán (bao) |
| X-AW (C24-C49) | Lịch sử bán ngày 1-26 (Kg) |

**Tổng hợp HIGRO PRO**:
| Metric | Giá trị |
|--------|---------|
| TOTAL BAG (Tổng bao tồn) | 4,128 bao |
| TOTAL KG (Tổng kg tồn) | 103,200 kg |
| Total Sale tháng | 296,460 kg |
| Sales Average | 19,764 kg/ngày |
| Day On Hand trung bình | ~27 ngày |

#### Phần 2: NASA - FEED (Thương hiệu NASA/BELL) - Dòng 37-63

**Tổng hợp NASA/BELL**:
| Metric | Giá trị |
|--------|---------|
| TOTAL BAG | 3,315 bao |
| TOTAL KG | 82,875 kg |
| Total Sale tháng | 225,600 kg |
| Day On Hand | ~68 ngày |

---

### SHEET 3: `BRAN` (363 dòng × 151 cột)
**Mục đích**: Tồn kho thương hiệu **HIGRO (đại lý)**, **CP**, **STAR**, **NUVO** - **Bán lẻ đại lý**

Chia thành nhiều phần (mỗi phần là 1 thương hiệu):

#### Phần 1: HI-GRO FEED (Đại lý) - Dòng 10-158
Gồm tất cả sản phẩm bán cho đại lý: 150S, 151, 157M, 301, 302, 510, 511, 512, 551, 552, 553, 566, 567, 384...

**Thêm 2 cột đặc biệt (chỉ có ở BRAN)**:
| Cột | Ý nghĩa |
|-----|---------|
| P (C16) | Tồn kho viên 2.5mm |
| Q (C17) | Tổng bán viên 2.5mm |

**Tổng hợp HIGRO BRAN**:
| Metric | Giá trị |
|--------|---------|
| TOTAL 5*5 KG | 36 bao (900 kg) |
| TOTAL 25 KG | 49,600 bao (1,240,000 kg) |
| TOTAL BAG | 49,725 bao |
| TOTAL KG | **1,241,790 kg** |
| Total Sale tháng | **5,211,365 kg** |
| TOTAL SILO | 718,250 kg |

#### Phần 2: CP FEED - Dòng 163-199
**Tổng hợp CP**:
| Metric | Giá trị |
|--------|---------|
| TOTAL BAG | 3,369 bao |
| TOTAL KG | **84,225 kg** |
| Total Sale tháng | 319,550 kg |

#### Phần 3: STAR FEED - (Tiếp theo)
#### Phần 4: NUVO FEED - (Tiếp theo)

---

### SHEET 4: `INTGRATE` (416 dòng × 108 cột)
**Mục đích**: Tồn kho **cám trại** (Integrate) - Gà & Vịt nội bộ (Farm feed)

Tên đầy đủ: **INTEGRATE (CHICKEN & DUCK FEED) - TRẠI (CÁM GÀ VÀ VỊT)**

Chia 2 phần lớn:

#### Phần 1: Chicken Feed (Cám Gà Trại) - Dòng 7-108
Sản phẩm bao 50kg + Silo cho trại gà: 510F, 510NF, 511F, 511NF, 513F, 532NF, 534NF, 540F, 550SF, 551F, 551GPF, 552F, 552SF, 553MF, 562PF, 566F, 567SF...

**Tổng hợp Chicken Farm**:
| Metric | Giá trị |
|--------|---------|
| TOTAL 50 KG | 6,825 bao (341,250 kg) |
| Total Sale tháng | 1,518,890 kg |
| TOTAL SILO | 177,940 kg |

#### Phần 2: Duck & Swine Feed (Cám Vịt + Heo) - Dòng 115-266
GD04, GD14, GT11, GT12, GT12A, HT11, HT12, HT12S, HG16, HG17, VT11, VT12, BS07TA, BS09TA...

**Tổng hợp Phần 2**:
| Metric | Giá trị |
|--------|---------|
| TOTAL 10 KG | 7,864 bao (78,640 kg) |
| TOTAL 50 KG | 46,755 bao (2,337,750 kg) |
| Total Sale tháng | 23,577,070 kg |
| TOTAL SILO | 6,347,920 kg |

**Tổng INTGRATE**:
| Metric | Giá trị |
|--------|---------|
| TOTAL BAG | 61,444 bao |
| TOTAL KG | **2,757,640 kg** |

#### Bảng tổng hợp cuối sheet (Dòng 293+):
| Thông tin | Giá trị |
|-----------|---------|
| Số ngày sản xuất | 15.5 ngày |
| Số ngày bán hàng | 15 ngày |

| Thương hiệu | Sản xuất (kg) | Tổng bán (kg) |
|-------------|---------------|---------------|
| HIGRO | 718,250 | 4,485,590 |
| CP | - | 319,550 |
| STAR | - | - |
| NUVO | - | - |
| NASA/BELL | - | 225,600 |

---

### SHEET 5: `REMIX` (28 dòng × 254 cột)
**Mục đích**: **Cám chờ Remix** - Sản phẩm cần xay lại (quá ngày tuổi hoặc lỗi chất lượng)

| Cột | Ý nghĩa |
|-----|---------|
| B (C2) | FEED CODE |
| C (C3) | Pellet Size |
| D (C4) | PACK SIZE |
| E (C5) | REMAIN - Tồn đầu (bao chờ remix) |
| F (C6) | Produce date - Ngày sản xuất |
| G (C7) | Trans in - Nhận thêm |
| I (C9) | Remix out - Đã remix xong |
| N (C14) | BALANCE - Còn chờ |
| P (C16) | Total Remix (Kg) |
| Q (C17) | Location - Lô chất |
| R (C18) | REMARK - Ghi chú |

**Hiện tại**: 1 sản phẩm chờ remix
- **GT12S** (P3.5, 25kg) - Sản xuất ngày 14/04/2026 - Lý do: **QUÁ NGÀY TUỔI**
- Vị trí: D3.1
- Tổng: 15,550 kg

---

## 3. CÁC SHEET HỖ TRỢ

### SHEET 6: `Map` (768 dòng × 10 cột)
**Mục đích**: **Bảng mapping mã sản phẩm SAP** ↔ Mã nội bộ
- Cột B: Mã SAP (VD: 21115100000125)
- Cột D: Tên đầy đủ (VD: "TA# 510 (25Kg)")
- Cột E: Mã brand (VD: 510, 551, HT12S...)
- Cột F: Loại đóng gói (25, 50, Silo, 5*5...)
- **768 mã sản phẩm** được mapping

### SHEET 8: `pro` (180 dòng × 28 cột)
**Mục đích**: **Dữ liệu sản xuất ngày** - Pivot từ hệ thống SAP
- Brand Code, Size, Product Name, Medicine
- Quantity/Weight phân theo ca sản xuất
- Grand Total ngày 17/05: **791,275 kg** (17,127 bao)

### SHEET 12: `Sheet3` (330 dòng × 21 cột)
**Mục đích**: **Master Data sản phẩm** - Bảng tra cứu chính
- TYPE: CAM_DAI_LY, CAM_TUI, CAM_TRAI
- CODE, PACKAGING, FORMULAR, PRODUCT
- Dùng cho VBA Macro tự động phân loại

### SHEET 14: `Sheet6` (159 dòng × 13 cột)
**Mục đích**: **Master Data bao bì** - Mapping mã bao → thông số kỹ thuật
- VD: "BagO25- 510- 54x90-99-B-000-H" = Bao 25kg, 510, kích thước 54×90mm

### SHEET 15: `Sheet4` (622 dòng × 15 cột)
**Mục đích**: **Dữ liệu đơn hàng** (PK_w) - Tracking số xe giao hàng

### SHEET 1: `XL4Poppy` ⚠️ VIRUS
**Lưu ý**: Đây là **tàn dư virus Excel macro XF.Classic** (Narkotic Network 1998). Đã bị **Kaspersky Lab AV** vô hiệu hóa. Không ảnh hưởng đến dữ liệu nhưng cần lưu ý khi mở file.

---

## 4. CÔNG THỨC TÍNH TOÁN CHÍNH

```
BALANCE = REMAIN + Produce + Adj_in + Trans_in - Sell_out - Adj_out - Trans_out

Day On Hand = BALANCE (kg) ÷ Sales Average (kg/ngày)

Sales Average = Total Sale (kg) ÷ Số ngày bán hàng (15 ngày)
```

---

## 5. TỔNG HỢP TỒN KHO NGÀY 17/05/2026

| Phân khúc | Sheet | Tồn kho (Kg) | Tổng bán tháng (Kg) |
|-----------|-------|--------------|---------------------|
| HIGRO PRO (đại lý cao cấp) | PRO-NASA | 103,200 | 296,460 |
| NASA/BELL (đại lý) | PRO-NASA | 82,875 | 225,600 |
| HIGRO BRAN (đại lý) | BRAN | 1,241,790 | 5,211,365 |
| CP FEED (đại lý) | BRAN | 84,225 | 319,550 |
| STAR + NUVO (đại lý) | BRAN | *(trong BRAN)* | *(trong BRAN)* |
| Cám trại (INTGRATE) | INTGRATE | 2,757,640 | 23,577,070 |
| Cám chờ Remix | REMIX | 15,550 | - |
| **TỔNG ƯỚC TÍNH** | | **~4,285,280 kg** | **~29,630,045 kg** |

---

## 6. MỐI LIÊN HỆ VỚI CÁC FILE KHÁC

| File | Mối quan hệ |
|------|------------|
| **FORECAST** | Forecast dự báo → FFSTOCK kiểm tra tồn kho có đủ đáp ứng không |
| **DAILY SALED REPORT** | Sell out trong FFSTOCK = Dữ liệu bán hàng trong Daily Saled Report |
| **DAILY STOCK EMPTY BAG** | Quản lý bao rỗng → Khi sản xuất, tiêu thụ bao rỗng → thêm vào FFSTOCK |
| **Kế hoạch sản xuất** | FFSTOCK cung cấp tồn kho hiện tại → Input cho lập kế hoạch ngày mai |

### Luồng dữ liệu:
```
FORECAST (dự báo tuần)
    ↓
Kế hoạch sản xuất (plan ngày)
    ↓ Produce
FFSTOCK (tồn kho thành phẩm) ← DAILY STOCK BAG (bao rỗng)
    ↓ Sell out
DAILY SALED REPORT (thực tế bán)
```

---

## 7. LƯU Ý KỸ THUẬT

- **⚠️ Virus XL4Poppy**: File chứa tàn dư macro virus cũ (đã bị Kaspersky xử lý)
- **#REF!** errors: Một số ô tổng bị lỗi tham chiếu
- **#DIV/0!** trong sheet AJOUT: Do chia cho 0 (chưa có dữ liệu)
- **Đơn vị kép**: Cả BAO (bags) và KG đều được theo dõi song song
- **Quy đổi**: 1 bao 25kg = 25 kg, 1 bao 50kg = 50 kg
- File .xlsm chứa VBA Macro để tự động pull dữ liệu từ SAP và tính toán

---

*Tài liệu phân tích tự động - Ngày 19/05/2026*
