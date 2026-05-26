"""Test tìm file FFStock từ OneDrive"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import config
import data_loader

print("=" * 60)
print(f"FFStock dir: {config.FSTOCK_DIR_FFSTOCK}")
print()

# Test tìm file FFSTOCK
f = data_loader._find_latest_file(config.FSTOCK_DIR_FFSTOCK, '*FFSTOCK*.xls*')
print(f"FFStock file found: {f}")

# Test get_file_info  
info = data_loader.get_file_info(config.FSTOCK_DIR_FFSTOCK, '*FFSTOCK*.xls*')
print(f"FFStock info: {info}")
print("=" * 60)
