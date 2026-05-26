@echo off
chcp 65001 >nul
title C.P. Binh Duong - KHSX Tu Dong
color 0B
echo =====================================================================
echo    C.P. VIET NAM - CHI NHANH BINH DUONG
echo    HE THONG LAP KE HOACH SAN XUAT TU DONG (KHSX WEB APP)
echo =====================================================================
echo.
echo  [*] Dang dong bo du lieu len Neon Tech Cloud...
cd /d "D:\Kê hoạch sản xuât\laptrinh vao"
py auto_sync_onedrive.py
echo.
echo  [*] Dang khoi dong Server Flask...
start cmd /k "cd /d "D:\Kê hoạch sản xuât\laptrinh vao" && py app.py"
echo  [*] Dang cho Server san sang trong 3 giay...
timeout /t 3 /nobreak >nul
echo  [*] Dang tu dong mo trinh duyet web: http://127.0.0.1:5000
start http://127.0.0.1:5000
echo.
echo  [+] He thong da duoc khoi chay thanh cong!
echo  [+] Ban co the thu nho cua so nay va su dung Web tren trinh duyet.
echo.
echo =====================================================================
timeout /t 5 >nul
exit
