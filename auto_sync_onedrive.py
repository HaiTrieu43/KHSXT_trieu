"""
auto_sync_onedrive.py - Tự động quét thư mục OneDrive/cục bộ và đẩy dữ liệu lên Neon Tech Cloud DB

Chạy script này khi khởi động để đồng bộ tất cả dữ liệu Excel mới nhất lên Cloud.
"""
import sys
import os
import time

# Đảm bảo encoding UTF-8
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# Thêm thư mục dự án vào path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config

def main():
    print("=" * 60)
    print("[AUTO-SYNC] Bat dau dong bo du lieu len Neon Tech Cloud...")
    print("=" * 60)
    
    start_time = time.time()
    
    if not getattr(config, 'USE_POSTGRESQL', False):
        print("[!] PostgreSQL chua duoc bat (USE_POSTGRESQL=False). Bo qua.")
        return
    
    try:
        import db_manager
        
        # Khởi tạo database nếu chưa có
        db_manager.init_db(getattr(config, 'DB_URI', db_manager.DB_URI))
        
        # Đồng bộ toàn bộ dữ liệu Excel cục bộ lên Cloud
        print("\n[*] Dang doc file Excel tu thu muc cuc bo...")
        db_manager.sync_local_to_db(config, getattr(config, 'DB_URI', db_manager.DB_URI))
        
        elapsed = time.time() - start_time
        print(f"\n[OK] Dong bo thanh cong trong {elapsed:.1f} giay!")
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n[LOI] Dong bo that bai sau {elapsed:.1f} giay: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)


if __name__ == '__main__':
    main()
