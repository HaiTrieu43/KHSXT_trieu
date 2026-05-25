# PHÂN TÍCH FILE KẾ HOẠCH CÁM SILO TUẦN 21

> **File**: `SILO W21-18-23-05-2026.xlsx`  
> **Thư mục**: `D:\Kê hoạch sản xuât\SILO\`  
> **Đơn vị**: CTY CỔ PHẦN CHĂN NUÔI C.P VIỆT NAM - Chi Nhánh Tại Bình Dương  
> **Tuần hiện tại**: Tuần 21 (18/05 → 23/05/2026)

---

## 1. TỔNG QUAN

### 1.1. Mục đích sử dụng
Đây là **KẾ HOẠCH CÁM SILO** - lịch giao cám rời bằng **xe bồn (bulk)** cho khách hàng trại chăn nuôi (FARM) và đại lý lớn. Cám silo **KHÔNG đóng bao** mà bơm trực tiếp từ nhà máy lên xe bồn → giao đến silo tại trại.

### 1.2. Tại sao file này quan trọng?
**Cám silo chiếm ~60-70% tổng sản lượng nhà máy** - đây là kênh phân phối lớn nhất. File này quyết định trực tiếp:
- Kế hoạch sản xuất hàng ngày (FORECAST)
- Lịch vận chuyển xe bồn
- Thứ tự ưu tiên sản xuất trên dây chuyền

### 1.3. Cấu trúc file
- **21 sheets** = 21 tuần (Tuần 01/2026 → Tuần 21/2026)
- Mỗi sheet = 1 tuần (Thứ 2 → Thứ 7, 6 ngày)
- Sheet đặt tên theo ngày: `18-23-05-2026` (tuần 21)

---

## 2. CẤU TRÚC MỖI SHEET

### 2.1. Header (Dòng 1-4)
- Dòng 3: `KẾ HOẠCH CÁM SILO TUẦN XX`
- Dòng 4: `Từ ngày DD/MM/YYYY => DD/MM/YYYY`

### 2.2. Phần CÁM FARM - Trại chăn nuôi (Dòng 5-36)

Cám giao cho **trại chăn nuôi** (Farm) - khối lượng lớn nhất:

| Cột | Ý nghĩa |
|-----|---------|
| A (C1) | Tên sản phẩm cám |
| B (C2) | PELLET SIZE - Kích cỡ viên (mm) |
| C-H/I (C3-C8/C9) | Sản lượng kế hoạch từng ngày (Thứ 2→7) - đơn vị **KG** |
| Cuối | TOTAL - Tổng tuần |

**Đặc biệt**: Mỗi sản phẩm có **2 dòng**:
- **Dòng lẻ**: Kế hoạch (PLAN) - số lượng dự kiến
- **Dòng chẵn**: Thực tế (ACTUAL) - số lượng giao thực tế

#### Danh sách cám Farm:

| Mã cám | Pellet Size | Loại | Ghi chú |
|--------|-------------|------|---------|
| **549F** | 4mm | Cám heo Farm | |
| **540F** | 4mm | Cám heo Farm | |
| **548F** | 2.5mm | Cám heo Farm | |
| **550SF** | 2.8mm | Cám gà Farm (viên nhỏ) | |
| **550SFS31** | 2.8mm | Cám gà Farm silo 31 | |
| **551FS54** | 2.8mm | Cám gà Farm silo 54 | |
| **551GPFS13/31/54** | 4mm | Cám gà GP Farm | |
| **566F / 566FS25/31** | 4mm | Cám vịt Farm | **Sản lượng RẤT LỚN** |
| **567SF / 567SFS25/31** | 4mm | Cám vịt Farm đặc biệt | **Sản lượng RẤT LỚN** |
| **552SF / 552SFS90** | 4mm | Cám heo Farm | **SẢN PHẨM CHỦ LỰC #1** |
| **552F / 552FS90** | 4mm | Cám heo Farm | **SẢN PHẨM CHỦ LỰC #2** |
| **553MF** | 4mm | Cám heo mẹ Farm | |
| **562PF** | 4mm | Cám vịt Farm | |

**Dòng tổng hợp**: `SỐ LƯỢNG XE FARM` - Tính tổng số xe bồn cần cho Farm mỗi ngày

### 2.3. Phần CÁM ĐẠI LÝ - Silo (Dòng 37-57)

Cám giao cho **đại lý** bằng xe bồn:

| Mã cám | Pellet Size | Loại |
|--------|-------------|------|
| **GD14AP32** | 4mm | Cám gà đại lý (GD14) - **giao mỗi ngày 14 tấn** |
| **502** | MC (mash) | Cám bột |
| **GT11S / GT12 / GT12A** | 2.5-3.5mm | Cám gà tây |
| **511S** | 3.5mm | Cám gà |
| **550S / 550SX / 550XPRO** | 2.5mm | Cám gà đại lý |
| **551PRO / 551GP** | 2.8mm | Cám gà cao cấp |
| **HT11** | 2.8mm | Cám heo thịt 11 |
| **HT12S / HT12SX** | 2.8mm | Cám heo thịt 12 |
| **552 / 552S** | 4mm / 2.8mm | Cám heo |
| **553 / 553S** | 2.8mm | Cám heo |
| **HT13S** | 4mm | Cám heo thịt 13 |
| **562P / 562PXS72** | 4mm | Cám vịt đại lý |
| **HG16 / HG16XS74** | 4mm | Cám heo giống 16 |
| **HG17S / HG17SXS74** | 4mm | Cám heo giống 17 |

**Dòng tổng hợp**: `SỐ LƯỢNG XE ĐL` - Số xe bồn cần cho Đại lý

### 2.4. Dòng TỔNG CỘNG
`TỔNG CỘNG SỐ LƯỢNG XE` = XE FARM + XE ĐẠI LÝ

### 2.5. Ghi chú khách hàng
- **BÁ CANG** - Đại lý Võ Bá Cang (liên kết với file KẾ HOẠCH BA CANG)
- **CÔNG DỰ** - Đại lý khác
- **VIÊTSSWAN - MAI THI THƯỚC** - Đại lý/trại

---

## 3. DỮ LIỆU MẪU - TUẦN 09 (23-28/02/2026)

### Top sản phẩm Farm theo sản lượng:

| Sản phẩm | KẾ HOẠCH (kg) | THỰC TẾ (kg) | % Đạt |
|----------|---------------|--------------|-------|
| **552SF** | 1,410,000 | 728,390 | 51.7% |
| **552F** | 500,000 | 245,190 | 49.0% |
| **567SF** | 512,000 | 440,510 | 86.0% |
| **566F** | 376,000 | 342,990 | 91.2% |
| **540F** | 84,000 | 14,240 | 17.0% |

### Số lượng xe bồn/ngày (Tuần 09):
- **Xe Farm**: 27-41 xe/ngày
- **Xe Đại lý**: 3-5 xe/ngày  
- **Tổng**: ~30-46 xe/ngày

---

## 4. PHÂN TÍCH SẢN LƯỢNG

### 4.1. Sản phẩm chủ lực (chiếm >80% tổng sản lượng Farm):

| Sản phẩm | Sản lượng/tuần | Tỷ trọng |
|----------|---------------|----------|
| **552SF/552SFS90** | 1,100,000 - 1,500,000 kg | **~40%** |
| **566F/566FS25/31** | 300,000 - 500,000 kg | **~15%** |
| **567SF/567SFS25/31** | 300,000 - 500,000 kg | **~15%** |
| **552F/552FS90** | 100,000 - 500,000 kg | **~12%** |

### 4.2. Tổng sản lượng silo ước tính/tuần:
- **Farm**: 2,500,000 - 4,000,000 kg (**2,500 - 4,000 tấn**)
- **Đại lý**: 300,000 - 500,000 kg (**300 - 500 tấn**)
- **TỔNG SILO**: **~3,000 - 4,500 tấn/tuần** (500-750 tấn/ngày)

### 4.3. Pellet Size phân bố:
| Size | Sản phẩm | Tỷ trọng |
|------|----------|----------|
| **4mm** | 552SF, 552F, 566F, 567SF, GD14AP... | **~80%** |
| **2.8mm** | 550SF, 551FS, HT11, HT12S... | **~15%** |
| **2.5mm** | 550S, GT11S, 502... | **~5%** |

---

## 5. SO SÁNH KẾ HOẠCH vs THỰC TẾ

Mỗi sản phẩm có 2 dòng (Plan/Actual). Kết quả:

| Sản phẩm | Xu hướng |
|----------|----------|
| **552SF** | Thực tế thường **thấp hơn** kế hoạch (50-80%) |
| **566F** | Thực tế **gần đạt** kế hoạch (80-100%) |
| **567SF** | Thực tế **gần đạt** hoặc vượt kế hoạch |
| **552F** | Biến động lớn (30-100%) |
| **GD14AP** | Giao đều **14 tấn/ngày** (ổn định nhất) |

> ⚠️ **552SF thường sản xuất không kịp kế hoạch** → Đây là bottleneck chính cần cải thiện trong kế hoạch SX

---

## 6. MỐI LIÊN HỆ VỚI CÁC FILE KHÁC

```
KẾ HOẠCH CÁM SILO (File này)  ←──→  KẾ HOẠCH BA CANG
         ↓                                    ↓
    FORECAST (Sale Forecast) ←── Tổng hợp tất cả
         ↓
    KẾ HOẠCH SẢN XUẤT (Plan)
         ↓
    TỒN BỒN (Batching) → Cám SX xong chờ trong bồn
         ↓                         ↓
    FFSTOCK (đóng bao)        GIAO SILO (xe bồn)
         ↓
    DAILY SALED (bán hàng) ← Xuất kho
```

### Phân bổ sản lượng nhà máy:
| Kênh | Sản lượng/ngày | Tỷ trọng |
|------|---------------|----------|
| **Cám Silo (Farm + ĐL)** | 500-750 tấn | **~30-35%** |
| **Cám Bao (FFSTOCK)** | 1,400-1,800 tấn | **~65-70%** |
| **TỔNG** | 2,100-2,500 tấn | 100% |

---

## 7. LƯU Ý QUAN TRỌNG

> ⚠️ **Cám silo KHÔNG đi qua EMPTY BAG** - giao trực tiếp bằng xe bồn → Không tiêu thụ bao bì

> ⚠️ **552SF là sản phẩm lớn nhất** (~1.2-1.5 triệu kg/tuần) nhưng thường xuyên **không đạt kế hoạch** → Cần ưu tiên trong lịch sản xuất

> ⚠️ **GD14AP32 giao cố định 14 tấn/ngày, 6 ngày/tuần = 84 tấn/tuần** → Đây là đơn hàng contract, phải đảm bảo

> ⚠️ **Số xe bồn/ngày = 30-50 xe** → Ảnh hưởng logistics, cần điều phối bến xuất hàng

> ⚠️ **Khách hàng lớn**: BÁ CANG, CÔNG DỰ, VIÊTSSWAN-MAI THI THƯỚC được ghi nhận trực tiếp trong file

---

*Tài liệu phân tích tự động - Ngày 19/05/2026*
