# 🏭 PHÂN TÍCH FILE KẾ HOẠCH SẢN XUẤT (KHSX)

> **File**: `KHSX THANG 5-20261.xlsm`  
> **Thư mục**: `D:\Kê hoạch sản xuât\`  
> **Người lập**: Hồ Đăng Xuân Thành / Châu Ngọc Quang  
> **Người thẩm tra**: Phan Văn Thông (Manager)

---

## 1. TỔNG QUAN FILE

### 37 Sheets:

| Nhóm | Sheet | Mục đích |
|-------|-------|----------|
| **Tham chiếu** | `TIÊU CHUẨN HMFM` | Tiêu chuẩn lưới nghiền, phun molas |
| **Quản trị** | `Admin` | Danh sách người dùng, mật khẩu, phân quyền |
| **Kế hoạch hàng ngày** | `1` → `31` (31 sheets) | **KẾ HOẠCH SẢN XUẤT mỗi ngày** |
| **Tổng hợp** | `Summary` | Tổng hợp sản lượng cả tháng theo mã cám |
| **Danh mục** | `FEEDCODE` | Bảng mã cám ↔ Máy ép viên ↔ Máy đóng bao |
| **Mapping** | `LINE PK VÀ CV` | Bảng map LINE CÁM VIÊN ↔ LINE ĐÓNG BAO |
| **Kháng sinh** | `KHÁNG SINH` | Bảng tra KS/HC cho 280+ mã cám |

---

## 2. CẤU TRÚC MỖI SHEET NGÀY (Sheet "1" → "31")

### ĐÂY LÀ PHẦN QUAN TRỌNG NHẤT - Mỗi ngày mixer phải lập thủ công:

### 2.1. PHẦN KẾ HOẠCH TRỘN (Cột A-D)

| Cột | Tên | Ý nghĩa | Ví dụ |
|-----|-----|---------|-------|
| **A** | STT | Thứ tự sản xuất | 1, 2, 3... |
| **B** | TÊN CÁM | Mã sản phẩm | 552SF, 566F, 511B... |
| **C** | KẾ HOẠCH (MẺ) | Số mẻ trộn | 60, 50, 15... |
| **D** | TỔNG (TẤN) | = Mẻ × Trọng lượng/mẻ | 504, 420, 126... |

> ⚠️ **1 MẺ = 8.4 tấn** (mặc định) hoặc **8.0 tấn** (cám 55x)

### 2.2. PHẦN KẾ HOẠCH ĐÓNG BAO (Cột E-S)

Phân chia sản lượng theo **thương hiệu bao bì** và **loại bao**:

| Cột | Thương hiệu | Loại bao |
|-----|-------------|----------|
| E-F | **HIGRO** | 25kg / 40kg |
| G-H | **CP** | 25kg / 40kg |
| I-J | **START FEED** | 25kg / 40kg |
| K-L | **NUVO** | 25kg / 40kg |
| M-N | **BELL** | 25kg / 40kg |
| O-P | **NASA** | 25kg / 40kg |
| Q-R-S | **WHITE BAG** | 25kg / 40kg / **50kg** |

> ⚠️ **Cột S (50kg)** = Bao lớn, thường dùng cho cám Farm (552F, 552SF...)

### 2.3. PHẦN SILO TRUCK (Cột T)
Sản lượng giao bằng **xe bồn** (không đóng bao)

### 2.4. PHẦN THÔNG TIN BỔ SUNG (Cột U-X)

| Cột | Ý nghĩa |
|-----|---------|
| U | KHÁNG SINH (KS) / HOẠT CHẤT (HC) - Mã kháng sinh in lên bao |
| V | CÁM VIÊN (LINE SỐ) - Line ép viên sẽ chạy |
| W | ĐÓNG BAO (LINE SỐ) - Line đóng bao sẽ chạy |

### 2.5. PHẦN THEO DÕI THỰC TẾ (Cột Z-AD)

| Cột | Ý nghĩa |
|-----|---------|
| Z | THỰC HIỆN (MẺ) - Số mẻ thực tế chạy |
| AA | HOÀN THÀNH (%) - % hoàn thành |
| AB | LÝ DO nếu không đạt 95% |
| AC-AD | Dữ liệu thực tế pha trộn |

---

## 3. BẢNG FEEDCODE - Quy tắc phân bổ máy

> ⚠️ **ĐÂY LÀ RÀNG BUỘC CỨNG** - Mỗi mã cám chỉ chạy được trên LINE cụ thể

| LINE CÁM VIÊN | LINE ĐÓNG BAO | Sản phẩm điển hình |
|---------------|--------------|-------------------|
| **1** | **5** | 550S, 511B, 550PRO, 551PRO, GT12B |
| **2** | **1** | 552F, 552FS90, 551GPFS54, 513F, 524P |
| **3** | **4** | 552SF, 552SFS90, 562PF, 553MF |
| **4** | **2** | 566, 567S, 552, 553, 553S, 549F |
| **5** | **6** | 552S, 552M, 521SPRO, 6951 |
| **6** | **7** | *(ít dùng)* |
| **7** | **8** | 549, 594, 595 |
| **M** (Mash) | **3** | 510, 301, 384, BS04, BS09TA |
| **M** | **SILO** | Cám bột giao xe bồn |

---

## 4. DỮ LIỆU MẪU - NGÀY 3/05/2026 (Sheet '3')

| STT | Tên cám | Mẻ | Tấn | HIGRO 25 | CP 25 | START 25 | WH 50kg | SILO | Line CV | Line PK |
|-----|---------|-----|-----|----------|-------|----------|---------|------|---------|---------|
| 1 | GT12 | 4 | 33.6 | 19.6 | | | | 14 | 4 | 2 |
| 29 | 552F | 30 | 252 | | | | 152 | 100 | 2 | 1 |
| 30 | 552SF | 40 | 336 | | | | 136 | 200 | 3 | 4 |
| 31 | 552FS90 | 20 | 168 | | | | 68 | 100 | 2 | 1 |
| 32 | 552SFS90 | 30 | 252 | | | | 102 | 150 | 3 | 4 |

**Tổng ngày 3/05: 273 mẻ = 2,287.2 tấn**

### Sản lượng hàng ngày trong tháng 5:

| Ngày | Tổng Mẻ | Tổng Tấn |
|------|---------|----------|
| 2 | 272 | 2,271 |
| 3 | 273 | 2,287 |
| 4 | 275 | 2,292 |
| 5 | 294 | 2,465 |
| 6 | 277 | 2,301 |
| 7 | 282 | 2,357 |
| 8 | 281 | 2,351 |
| 9 | 273 | 2,272 |

**Trung bình: ~275 mẻ = ~2,300 tấn/ngày** (nằm trong target 2,100-2,500 tấn)

---

## 5. QUY TRÌNH HIỆN TẠI (THỦ CÔNG)

```
MIXER nhận thông tin buổi sáng:
    ├── FORECAST tuần (từ Sale)
    ├── SILO PLAN (lịch xe bồn hôm nay)  
    ├── BA CANG (đơn hàng đại lý)
    ├── TỒN BỒN (cám còn trong bồn)
    ├── FFSTOCK (tồn kho thành phẩm)
    └── EMPTY BAG (bao bì có sẵn)
        ↓
    QUYẾT ĐỊNH THỦ CÔNG:
    1. Chọn danh sách sản phẩm SX hôm nay
    2. Quyết định số mẻ mỗi sản phẩm
    3. Phân bổ bao bì (HIGRO/CP/START/NUVO...)
    4. Phân bổ SILO TRUCK
    5. Gán LINE CÁM VIÊN + LINE ĐÓNG BAO
    6. Ghi mã kháng sinh
    7. Tính tổng → đảm bảo ~2,100-2,500 tấn
        ↓
    OUTPUT: 1 sheet KẾ HOẠCH SẢN XUẤT cho ngày đó
```

---

## 6. LIÊN KẾT TOÀN BỘ HỆ THỐNG

```
┌─────────────────────────────────────────────────────────────────┐
│                     INPUT CHO THUẬT TOÁN                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FORECAST ──→ Nhu cầu sản lượng tuần (target demand)           │
│  BA CANG  ──→ Đơn hàng đại lý cụ thể (hard constraint)        │
│  SILO PLAN ─→ Lịch xe bồn (hard constraint ngày)              │
│  TỒN BỒN  ──→ Cám đang chờ trong bồn (available inventory)    │
│  FFSTOCK  ──→ Tồn kho thành phẩm (available stock)            │
│  EMPTY BAG ─→ Bao bì sẵn có (packaging constraint)            │
│  FEEDCODE ──→ Mapping sản phẩm → LINE máy (hard constraint)   │
│  KHÁNG SINH → Mã KS/HC cho mỗi sản phẩm (lookup)             │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                    THUẬT TOÁN TỐI ƯU                            │
│                                                                 │
│  Tối ưu: MIN(chi phí chuyển đổi) + MAX(đạt forecast)          │
│  Ràng buộc:                                                    │
│    - Tổng sản lượng: 2,100 - 2,500 tấn/ngày                   │
│    - Line constraint: Sản phẩm → Line cố định                 │
│    - Bao bì: ≤ Tồn kho bao bì                                 │
│    - Silo: Đúng lịch xe bồn                                   │
│    - Forecast: Đạt ≥ 95% nhu cầu tuần                         │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                        OUTPUT                                   │
│                                                                 │
│  KẾ HOẠCH SẢN XUẤT = Bảng giống Sheet ngày hiện tại           │
│  (Tên cám, Số mẻ, Tấn, phân bổ bao bì, Line, KS)            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. 🔴 CÂU HỎI QUAN TRỌNG CẦN TRẢ LỜI

> [!IMPORTANT]
> Tôi cần bạn trả lời **từng câu một** để thuật toán được chính xác nhất:

### A. VỀ SẢN LƯỢNG VÀ MẺ TRỘN

**Q1**: Mỗi mẻ trộn bao nhiêu tấn? Tôi thấy phần lớn là **8.4 tấn/mẻ**, nhưng cám 55x (550, 551) là **8.0 tấn/mẻ**. Có đúng không? Có sản phẩm nào có trọng lượng mẻ khác không?

**Q2**: Target sản lượng/ngày là **2,100-2,500 tấn**. Con số này có thay đổi theo mùa hoặc theo ngày trong tuần không? (Ví dụ: Thứ 7 sản xuất ít hơn?)

**Q3**: Tối đa mỗi LINE ép viên chạy được bao nhiêu **mẻ/ngày**? (Ví dụ: LINE 2 chạy 552F 70 mẻ + 552FS90 20 mẻ = 90 mẻ/ngày. Đây có phải giới hạn không?)

### B. VỀ PHÂN BỔ LINE MÁY

**Q4**: Có bao nhiêu LINE CÁM VIÊN tổng cộng? Tôi thấy LINE 1-7 + M (Mash). Mỗi LINE chạy **đồng thời** hay **tuần tự**? (Ví dụ: LINE 2 có thể chạy 552F rồi chuyển sang 513F trong cùng ngày không?)

**Q5**: Chi phí/thời gian **chuyển đổi** (changeover) giữa các sản phẩm trên cùng 1 LINE là bao lâu? Có mất mẻ nào không?

**Q6**: Có bao nhiêu LINE ĐÓNG BAO? Tôi thấy LINE 1-8 + SILO. Mối quan hệ giữa LINE ép viên và LINE đóng bao có phải **1:1** theo bảng FEEDCODE không?

### C. VỀ ĐƠN HÀNG VÀ ƯU TIÊN

**Q7**: Khi lên kế hoạch, **thứ tự ưu tiên** là gì? Ví dụ:
1. Đơn hàng SILO xe bồn hôm nay (vì xe đã đặt lịch)?
2. Đơn hàng đại lý Ba Cang?
3. Forecast tuần?
4. Bù hàng thiếu từ ngày hôm trước?

**Q8**: Nếu FORECAST yêu cầu 60 mẻ 552SF trong tuần, mixer có **chia đều** mỗi ngày ~10 mẻ hay tập trung sản xuất 1-2 ngày?

### D. VỀ BAO BÌ

**Q9**: Phân bổ bao bì (HIGRO, CP, START FEED, NUVO, BELL, NASA, WHITE BAG) dựa trên nguyên tắc gì? Có phải:
- Dựa trên **đơn hàng** (khách hàng A đặt bao HIGRO)?
- Hay dựa trên **tồn kho bao bì** (bao nào còn nhiều thì dùng)?
- Hay **theo tỷ lệ cố định**?

**Q10**: Bao 50kg (WHITE BAG cột S) chỉ dùng cho cám Farm (552F, 552SF, 553MF...)? Hay sản phẩm nào cũng có thể đóng 50kg?

### E. VỀ RÀNG BUỘC ĐẶC BIỆT

**Q11**: Cám có mã **FS** (FS31, FS54, FS90, FS13, FS25) - "F" là Farm, "S" là SILO number. Vậy FS90 có nghĩa là cám giao vào **silo số 90** tại trại? Hay là **công thức khác**?

**Q12**: Cám có đuôi **XS** (XS74, XS88, XS34) là gì? Khác gì với cám thường?

**Q13**: Có ngày nào trong tháng **KHÔNG sản xuất** (nghỉ lễ, bảo trì)? Hay nhà máy chạy 7 ngày/tuần?

### F. VỀ QUY TRÌNH LÊN KẾ HOẠCH

**Q14**: Mixer hiện tại lên kế hoạch cho **1 ngày** hay **cả tuần** trước? Nếu tự động hóa, bạn muốn thuật toán lên kế hoạch cho **bao nhiêu ngày** một lần?

**Q15**: Khi mixer quyết định thứ tự STT (1, 2, 3...) trong sheet, **thứ tự này có phải là thứ tự sản xuất thực tế** không? Hay chỉ là liệt kê?
