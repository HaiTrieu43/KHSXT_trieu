# CÁC CÂU HỎI QUAN TRỌNG ĐỂ XÂY DỰNG THUẬT TOÁN LẬP KẾ HOẠCH PL (ÉP VIÊN)
**C.P. Vietnam - Chi nhánh Bình Dương**

Tài liệu này được tạo ra để lưu trữ các câu hỏi nghiệp vụ và làm rõ các ràng buộc thực tế trong vận hành 7 máy ép viên tại nhà máy. Phản hồi từ người vận hành/điều độ sản xuất sẽ giúp thuật toán tối ưu hóa thời gian chạy máy ép viên, thời gian thay khuôn và an toàn kháng sinh đạt độ hoàn hảo cao nhất.

---

### 1. Quy tắc thay cỡ khuôn (`C.DIE`) và cỡ hạt của từng máy
*   **Các cỡ khuôn mặc định hiện tại:**
    *   **PL1, PL5, PL7:** Cỡ khuôn hạt nhỏ **2.8 mm** (chuyên chạy cám heo con sữa, cám gà con).
    *   **PL2, PL3, PL4:** Cỡ khuôn hạt to **4.0 mm** (chuyên cám heo thịt lớn, cám nái).
    *   **PL6:** Cỡ khuôn hạt nhỡ **3.5 mm**.
*   **Câu hỏi làm rõ:**
    *   *Có trường hợp nào nhà máy chủ động thay đổi cỡ khuôn vật lý của một máy khác với mặc định không?* (Ví dụ: Đổi khuôn của máy PL3 từ 4.0mm sang 2.8mm để phụ tải cho PL1).
    *   *Nếu có thay khuôn giữa ngày, thời gian thay khuôn (`C.DIE`) thực tế của từng máy là bao nhiêu giờ cố định?* (Trong công thức Excel thường cộng thêm từ **1.5 đến 2.5 giờ**).

---

### 2. Quy tắc chuyển mã cám (`LOSS CHUYỂN CÁM`)
*   **Khái niệm:** Khi chạy mã cám mới trên cùng một cỡ khuôn (không cần thay khuôn vật lý), máy vẫn cần thời gian vệ sinh, đuổi cám cũ để tránh lẫn lộn.
*   **Câu hỏi làm rõ:**
    *   *Thời gian hao hụt chuyển mã cám (`LOSS CHUYỂN CÁM`) thực tế giữa hai mã cám khác nhau là bao nhiêu?* (Trong sheet hiện tại đang gán từ **1.0 đến 1.5 giờ**).
    *   *Quy tắc gom mẻ chạy liên tiếp:* Thuật toán sẽ ưu tiên gom các mẻ cùng mã chạy liên tục trên một line để chỉ chịu 1 lần `LOSS CHUYỂN CÁM`. Tuy nhiên, nếu hai mã cám khác nhau nhưng **cùng một nhóm sản phẩm** (ví dụ: `550S` và `550SF` cùng nhóm heo con) thì có cần tính `LOSS CHUYỂN CÁM` hay không, hay chỉ tính khi chuyển đổi giữa các nhóm khác hẳn nhau?

---

### 3. Silo chứa bán thành phẩm (Silo chờ ép viên) và An toàn kháng sinh
*   **Bối cảnh:** Ở Mixer, chúng ta có quy tắc an toàn sinh học nghiêm ngặt: cám sạch (không thuốc) trộn trước, cám thuốc trộn sau, cấp độ kháng sinh tăng dần.
*   **Câu hỏi làm rõ:**
    *   *Tại khu vực ép viên, chúng ta có các Silo trung gian để chứa bột cám đã trộn trước khi đưa vào máy ép viên không? Nếu có, dung tích của các silo này là bao nhiêu mẻ và mỗi line có bao nhiêu silo chờ ép viên?*
    *   *Thứ tự chạy máy ép viên có bắt buộc phải trùng khớp 100% với thứ tự trộn của Mixer ở thượng nguồn không?* Hay máy ép viên có thể chạy linh hoạt hơn (ví dụ: Mixer trộn cám sạch -> cám thuốc, nhưng máy ép viên có thể đợi gom đủ cám thuốc trong silo trung gian rồi mới ép viên liên tục để tối ưu hóa thời gian chạy)?

---

### 4. Quy tắc phân bổ mẻ vào 3 ca (Ca 1, Ca 2, Ca 3)
*   **Bối cảnh:** Mỗi ca làm việc kéo dài 8 tiếng (Ca 1: 06h-14h, Ca 2: 14h-22h, Ca 3: 22h-06h sáng hôm sau).
*   **Câu hỏi làm rõ:**
    *   *Khi thời gian chạy của một mã cám vượt quá ranh giới ca, quy tắc chia nhỏ mẻ là gì?* (Ví dụ: Mã cám X cần chạy 5 giờ, nhưng Ca 1 chỉ còn 2 giờ là hết ca. Thuật toán có nên phân bổ 2 giờ (tương đương ~2.4 mẻ) vào Ca 1 và 3 giờ (tương đương ~3.6 mẻ) vào Ca 2 không?)
    *   *Ý nghĩa của dòng `TARGET` (dòng 7, 11, 15):* Trong mỗi ca có một dòng ghi chữ "TARGET" ở cột A, nhưng các cột PL vẫn ghi mã cám và số mẻ như một mẻ chạy bình thường. Dòng `TARGET` này có ý nghĩa nghiệp vụ gì đặc biệt, hay chỉ đơn thuần là dòng chạy thứ 3 trong ca của máy?

---

### 5. Kế thừa trạng thái đầu ngày (`TỒN ĐẦU` & `NEXT`)
*   **Câu hỏi làm rõ:**
    *   *Thông tin ở dòng `TỒN ĐẦU` (dòng 3) của ngày hôm nay có bắt buộc phải trùng khớp với dòng `NEXT` (dòng 19) của ngày hôm trước không?*
    *   *Số tấn và số giờ của `TỒN ĐẦU` có được tính vào tổng sản lượng và tổng giờ chạy máy thực tế của hôm nay không?* (Trong công thức Excel: `PLAN PL HOURS = SUM(E5:E18)`, tức là giờ của Ca 1 dòng 5 lấy trực tiếp từ dòng 3 `TỒN ĐẦU`, có nghĩa là giờ tồn đầu được tính vào tổng giờ chạy máy hôm nay).

---

### 6. Phân bổ ca cho dây chuyền cám bột (`MASH FEED`)
*   **Bối cảnh:** Cám bột `MASH FEED` (cột AD - AE) xả thẳng ra phễu đóng bao PK3 hoặc nạp silo mà không qua ép viên.
*   **Câu hỏi làm rõ:**
    *   *Quy tắc phân bổ ca (Ca 1, Ca 2, Ca 3) cho cám bột dựa trên tiêu chí nào? Có cần tối ưu hóa chuyển mã cám hay thay đổi gì cho cám bột không, hay chỉ cần xếp mẻ đều theo tiến độ Mixer?*

---

**Ngày tạo:** 2026-05-21  
**Nơi lưu:** `D:\Kê hoạch sản xuât\laptrinh vao\CAU_HOI_XAY_DUNG_THUAT_TOAN_PL.md`
