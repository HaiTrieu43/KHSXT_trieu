# THUẬT TOÁN LẬP KẾ HOẠCH SẢN XUẤT TỰ ĐỘNG
## Tóm tắt cho Người lập kế hoạch xem xét

---

### MỤC TIÊU
Thay thế việc lập KHSX thủ công mỗi sáng bằng chương trình tự động.
Chương trình sẽ đọc các file báo cáo hiện có → tính toán → xuất ra bảng kế hoạch sản xuất.

---

### DỮ LIỆU ĐẦU VÀO (chương trình tự đọc)

| Dữ liệu | Lấy từ đâu |
|----------|-----------|
| Nhu cầu tuần | File Sale Forecast |
| Lịch xe bồn | File SILO Plan |
| Đơn hàng Bá Cang | File KH Cám tuần Bá Cang |
| Tồn kho thành phẩm | File FFSTOCK |
| Tồn bồn | File Báo cáo tồn bồn |
| Bao bì còn | File Empty Bag Report |
| Trọng lượng mẻ | File Plan → Sheet CONG SUAT |
| Line máy | File KHSX → Sheet FEEDCODE |
| Kháng sinh | File KHSX → Sheet KHÁNG SINH |
| KH hôm qua | File KHSX → Sheet ngày trước |
| Đơn khách vãng lai | Mixer nhập tay |

---

### CÁCH TÍNH - TỪNG BƯỚC

#### BƯỚC 1: Xác định phải sản xuất gì

Chương trình xếp theo **4 mức ưu tiên**:

**Ưu tiên 1 - SILO xe bồn + Bá Cang (ngày mai)**
- Đọc lịch xe bồn NGÀY MAI → cần bao nhiêu tấn gì
- Đọc đơn Bá Cang NGÀY MAI → cần bao nhiêu tấn gì
- Kiểm tra tồn kho: nếu đã có đủ hàng trong kho thì KHÔNG sản xuất thêm
- Nếu thiếu → tính số mẻ = (tấn thiếu) ÷ (tấn/mẻ), làm tròn lên

**Ưu tiên 2 - Khách vãng lai**
- Mixer nhập đơn hàng mới nhận
- Kiểm tra tồn kho: thiếu bao nhiêu → tính số mẻ

**Ưu tiên 3 - Bù hàng thiếu hôm qua**
- Đọc KHSX hôm qua: sản phẩm nào hoàn thành dưới 95%?
- Tính số mẻ thiếu = mẻ kế hoạch - mẻ thực hiện

**Ưu tiên 4 - Theo Forecast tuần**
- Forecast tuần nói cần 500 tấn 552S trong tuần
- Đã SX được 200 tấn, còn thiếu 300 tấn
- Còn 3 ngày nữa trong tuần → hôm nay cần 100 tấn
- Tính số mẻ = 100 ÷ 8.4 = 12 mẻ

---

#### BƯỚC 2: Kiểm tra có hợp lý không

**Kiểm tra tổng sản lượng:**
- Cộng tất cả → nếu dưới 2,100 tấn → tăng thêm mẻ cho sản phẩm forecast
- Cộng tất cả → nếu trên 2,500 tấn → giảm mẻ sản phẩm ưu tiên thấp nhất trước

**Kiểm tra bao bì:**
- Đối chiếu số bao cần dùng với tồn kho bao bì
- Nếu thiếu → cảnh báo

---

#### BƯỚC 3: Phân bổ bao bì

- Đọc tỷ lệ thương hiệu (HIGRO/CP/STAR/NUVO/NASA) từ file Forecast
- Chia sản lượng theo đúng tỷ lệ đó
- Sản phẩm Farm (50kg) → WHITE BAG
- Sản phẩm SILO → ghi vào cột xe bồn

---

#### BƯỚC 4: Gán thông tin còn lại

- LINE cám viên → theo bảng FEEDCODE (cố định)
- LINE đóng bao → theo bảng FEEDCODE (cố định)
- Mã kháng sinh → theo bảng KHÁNG SINH (cố định)

---

#### BƯỚC 5: Xuất kế hoạch

Xuất ra file Excel giống bảng KHSX hiện tại:

| STT | Tên cám | KH (Mẻ) | Tổng (Tấn) | HIGRO | CP | START | ... | WH 50kg | SILO | KS | Line CV | Line PK |
|-----|---------|---------|-----------|-------|-----|-------|-----|---------|------|----|---------|---------|

---

### VÍ DỤ MINH HỌA

Giả sử hôm nay là Thứ 4, tuần 21:

```
Ưu tiên 1 - SILO ngày mai (Thứ 5):
  → 552SF: 100 tấn xe bồn → 100 ÷ 8.4 = 12 mẻ
  → 566F:  60 tấn xe bồn  →  60 ÷ 8.4 =  8 mẻ
  → 567SF: 40 tấn xe bồn  →  40 ÷ 8.4 =  5 mẻ

Ưu tiên 1 - Bá Cang ngày mai:
  → 552S: 20 tấn, tồn kho 5 tấn → thiếu 15 → 15 ÷ 8.4 = 2 mẻ
  → 553S: 10 tấn, tồn kho 0     → thiếu 10 → 10 ÷ 8.4 = 2 mẻ

Ưu tiên 3 - Bù thiếu hôm qua:
  → 553MF: KH 20 mẻ, thực 17 mẻ → bù 3 mẻ

Ưu tiên 4 - Forecast:
  → 552SF bao 50kg: FC tuần 1620 tấn, đã SX 800, còn 3 ngày → 273 tấn/ngày = 33 mẻ
  → 552F bao 50kg: FC tuần 1540 tấn, đã SX 700, còn 3 ngày → 280 tấn/ngày = 34 mẻ
  → 552S bao 25kg: FC tuần 160 tấn, đã SX 80 → 27 tấn/ngày = 4 mẻ
  → 566 bao 25kg: FC tuần 168 tấn, đã SX 90 → 26 tấn/ngày = 4 mẻ
  → ... (các sản phẩm khác)

Tổng kiểm tra: ~2,250 tấn ✅ (nằm trong 2,100-2,500)
```

---

### CÂU HỎI CHO NGƯỜI LẬP KẾ HOẠCH

1. Logic trên có đúng với cách anh/chị đang làm thủ công không?
2. Có trường hợp đặc biệt nào mà thuật toán chưa tính đến không?
3. Khi thiếu bao bì, anh/chị xử lý như thế nào? (giảm sản lượng? chuyển thương hiệu bao?)
4. Có sản phẩm nào KHÔNG BAO GIỜ được giảm mẻ không? (VD: đơn hàng xuất khẩu?)
