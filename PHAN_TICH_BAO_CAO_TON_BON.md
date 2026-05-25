# PHÂN TÍCH FILE BÁO CÁO CÁM TỒN BỒN THÀNH PHẨM

> **File**: `Bao cao ton bon thanh pham 05.2026.xlsx`  
> **Thư mục**: `D:\Kê hoạch sản xuât\BATCHING-TONBON\`  
> **Đơn vị**: CÔNG TY CỔ PHẦN CHĂN NUÔI C.P VIỆT NAM - Chi Nhánh Tại Bình Dương  
> **Bộ phận**: Phòng Sản Xuất  
> **Mã biểu mẫu**: QT-SX-01/BM13 (Lần ban hành: 01, Ngày hiệu lực: 15/06/2017)

---

## 1. TỔNG QUAN

### 1.1. Mục đích sử dụng
Đây là **BÁO CÁO CÁM TỒN BỒN** - ghi lại trạng thái cám còn tồn lại trong các **bồn chứa** (silo/bin) tại nhà máy sau mỗi **ca sản xuất cuối ngày (Ca 3)**. 

**Ý nghĩa thực tiễn**: Cuối mỗi ca sản xuất, cám đã trộn xong nhưng chưa kịp đóng bao sẽ nằm lại trong bồn. File này ghi lại:
- **Bồn nào** chứa cám (số bồn)
- **Loại cám gì** (mã số cám)
- **Bao nhiêu kg** còn tồn

### 1.2. Cấu trúc file
- **32 sheets** tổng cộng
- **Sheet '1'**: Template rỗng (ngày 01/12/2025 - mẫu cũ)
- **Sheet '2' đến '17'**: Dữ liệu ngày 02/05/2026 đến 17/05/2026
- **Sheet '18' đến '31'**: Template rỗng (chưa có dữ liệu, dùng cho ngày 18-31/05/2026)
- **Sheet 'Sheet1'**: Template mẫu cũ (07/2024)

---

## 2. CẤU TRÚC MỖI SHEET (1 ngày)

### 2.1. Header
- Dòng 1-4: Tên công ty, chi nhánh, phòng ban
- Dòng 5-6: Tiêu đề "BÁO CÁO CÁM TỒN BỒN"
- Dòng 7: **Ca: 3** + **Ngày** (báo cáo cuối ca 3 = cuối ngày sản xuất)

### 2.2. Phần 1: BỒN CÁM BÁN THÀNH PHẨM (Dòng 8-17)
Bồn chứa cám **bán thành phẩm** (cám đã trộn nhưng CHƯA viên/CHƯA ép):

| Cột | Ý nghĩa |
|-----|---------|
| A (C1) | Số bồn (86-92) |
| B (C2) | Mã số cám |
| C (C3) | Khối Lượng (Kg) |
| E (C5) | Số bồn (93-98) |
| F (C6) | Mã số cám |
| G (C7) | Khối Lượng (Kg) |

**Tổng: 13 bồn** (bồn 86 → 98)

### 2.3. Phần 2: BỒN CÁM THÀNH PHẨM (Dòng 19-38)
Bồn chứa cám **thành phẩm** (đã viên/ép, sẵn sàng đóng bao):

| Cột | Ý nghĩa |
|-----|---------|
| A (C1) | Số bồn (99-116) |
| B (C2) | Mã số cám |
| C (C3) | Khối Lượng (Kg) |
| E (C5) | Số bồn (117-134) |
| F (C6) | Mã số cám |
| G (C7) | Khối Lượng (Kg) |

**Tổng: 36 bồn** (bồn 99 → 134)

### 2.4. Tổng hệ thống bồn: **49 bồn**
- 13 bồn bán thành phẩm (86-98)
- 36 bồn thành phẩm (99-134)

---

## 3. DỮ LIỆU MẪU - Ngày 02/05/2026 (Sheet '2')

### Bồn cám bán thành phẩm:
| Bồn | Mã cám | Khối lượng (kg) |
|-----|--------|-----------------|
| 88 | 32110890 | 21,616 |
| 89 | 112001 | 24,025 |
| 90 | 112001 | 13,236 |
| 91 | 367101 | 23,548 |
| 92 | 367101 | 16,366 |
| 93 | 32010890 | 6,077 |
| 94 | 32010890 | 4,828 |
| 95 | 32010890 | 23,618 |
| 97 | 367101 | 24,059 |
| 98 | 31210831 | 7,254 |

### Bồn cám thành phẩm:
| Bồn | Mã cám | Khối lượng (kg) |
|-----|--------|-----------------|
| 99 | 312001 | 9,652 |
| 102 | 320001 | 16,404 |
| 105 | 36630831 | 3,919 |
| 106 | 32110890 | 3,842 |
| 107 | 36730831 | 2,900 |
| 108 | 114601 | 9,202 |
| 110 | 366201 | 7,209 |
| 111 | 314001 | 7,704 |
| 114 | 332101 | 38,472 |
| 115 | 332211 | 18,281 |
| 116 | 203501 | 6,011 |
| 117 | 204501 | 16,884 |
| 120 | 36730825 | 18,255 |
| 121 | 32010890 | 2,889 |
| 122 | 32010890 | 19,227 |
| 123 | 321001 | 2,474 |
| 124 | 367101 | 6,788 |
| 125 | 31411831 | 1,258 |
| 129 | 114001B | 9,619 |
| 130 | 423001 | 45,639 |
| 131 | 433779 | 4,832 |
| 132 | 433780 | 11,585 |

---

## 4. MÃ SỐ CÁM THƯỜNG XUẤT HIỆN

| Mã cám | Nhóm sản phẩm (ước đoán) |
|--------|--------------------------|
| 312001 | Cám 512 (HIGRO - Đại lý) |
| 320001/320101 | Cám 520/521 (HIGRO) |
| 321001/321101 | Cám 521/511 (HIGRO/STAR) |
| 332101/332211 | Cám 552/552M (HIGRO) |
| 367101/367301 | Cám 567/573 (HIGRO) |
| 366201/366301 | Cám 562/563 (HIGRO) |
| 314001 | Cám 514 (HIGRO) |
| 204501 | Cám 545 (HIGRO) |
| 112001 | Cám 120 (CP) |
| 113601 | Cám 136 (CP) |
| 114601 | Cám 146 (CP) |
| 423001 | Cám Farm (Trại) |
| 433779/433780 | Cám Farm (Trại) |
| 31411831/31410831 | Cám Farm silo (50kg) |
| 32010890/32110890 | Cám trộn sẵn (Premix) |
| 546001 | Cám đặc biệt |
| BS07TA | Cám STAR bao 40kg |

---

## 5. Ý NGHĨA TRONG QUY TRÌNH SẢN XUẤT

```
Nguyên liệu → BATCHING (trộn)
    ↓
BỒN BÁN THÀNH PHẨM (86-98) ← Cám đã trộn, chưa viên
    ↓ Pelleting (ép viên)
BỒN THÀNH PHẨM (99-134) ← Cám đã viên, chờ đóng bao
    ↓ Packing (đóng bao)
KHO THÀNH PHẨM (FFSTOCK)
```

### Luồng thông tin:
1. **Cuối Ca 3** → Ghi nhận cám tồn bồn → File này
2. **Sáng Ca 1 hôm sau** → Cám tồn bồn cần được đóng bao/xử lý trước → Ảnh hưởng kế hoạch SX
3. **Tồn bồn nhiều** = Sản xuất nhanh hơn đóng bao = Cần tăng công suất packing
4. **Tồn bồn ít** = Đóng bao nhanh hơn sản xuất = Có thể giảm ca đóng bao

---

## 6. CÁC FILE CSV BỔ SUNG

Trong cùng thư mục có **16 file CSV** tên `PRODUCTION X.csv` (X = 2-17) và `PRO9.csv`:
- Đây là dữ liệu **production** hàng ngày export từ hệ thống batching
- Tương ứng với dữ liệu trong các sheet ngày 2-17/05/2026
- Dùng để nhập liệu tự động hoặc đối chiếu

---

## 7. MỐI LIÊN HỆ VỚI CÁC FILE KHÁC

| File | Mối quan hệ |
|------|------------|
| **FFSTOCK** | Cám tồn bồn → Đóng bao → Thành phẩm (FFSTOCK) |
| **DAILY STOCK EMPTY BAG** | Cám tồn bồn cần bao để đóng gói |
| **FORECAST** | Kế hoạch SX → Cám sẽ trộn → Dự kiến tồn bồn |
| **DAILY SALED REPORT** | Bán hàng → Cần đóng bao → Giải phóng bồn |

---

## 8. LƯU Ý QUAN TRỌNG

> ⚠️ **Sheet '1'** có ngày 01/12/2025 (template cũ), KHÔNG PHẢI ngày 01/05/2026!  
> Dữ liệu thực tế bắt đầu từ **Sheet '2' = Ngày 02/05/2026**.

> ⚠️ **Sheet '18' đến '31'** đều trống - Dữ liệu chỉ có đến **ngày 17/05/2026** (tương ứng thời điểm báo cáo).

> ⚠️ Khối lượng tồn bồn dao động **rất lớn**: từ vài trăm kg đến **47,000+ kg** mỗi bồn. Bồn lớn nhất chứa ~47 tấn cám.

---

*Tài liệu phân tích tự động - Ngày 19/05/2026*
