@echo off
chcp 65001 >nul
title AUTO SYNC - KHSX Cloud Database

echo ============================================================
echo   AUTO SYNC - Tu dong dong bo du lieu len Cloud Neon Tech
echo   C.P. Viet Nam - Chi Nhanh Binh Duong
echo ============================================================
echo.
echo   [!] Dang chay... KHONG DONG CUA SO NAY
echo   [!] Nhan Ctrl+C de dung
echo.

cd /d "D:\Kê hoạch sản xuât\laptrinh vao"
py auto_sync.py

pause
