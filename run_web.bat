@echo off
chcp 65001 >nul
title C.P. Bình Dương - Lập Kế Hoạch Sản Xuất Tự Động
color 0B
echo =====================================================================
echo    C.P. VIỆT NAM - CHI NHÁNH BÌNH DƯƠNG
echo    HỆ THỐNG LẬP KẾ HOẠCH SẢN XUẤT TỰ ĐỘNG (KHSX WEB APP)
echo =====================================================================
echo.
echo  [*] Đang khởi động Server Flask...
start cmd /k "cd /d D:\Kê hoạch sản xuât\laptrinh vao && py app.py"
echo  [*] Đang chờ Server sẵn sàng trong 3 giây...
timeout /t 3 /nobreak >nul
echo  [*] Đang tự động mở trình duyệt web: http://127.0.0.1:5000
start http://127.0.0.1:5000
echo.
echo  [+] Hệ thống đã được khởi chạy thành công!
echo  [+] Bạn có thể thu nhỏ cửa sổ này và sử dụng Web trên trình duyệt.
echo.
echo =====================================================================
timeout /t 5 >nul
exit
