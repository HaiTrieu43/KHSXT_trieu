"""Test tìm file FFStock và Empty Bag từ OneDrive"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import os
import glob

# Khai báo thuật toán detect thông minh trực tiếp trong test để chạy thử trước
base_dir = r'C:\Users\haitr\OneDrive - Cong Ty Co Phan Chan Nuoi C.P. Viet Nam'

def detect_category(category):
    import unicodedata
    def _strip_accents(s):
        nfkd = unicodedata.normalize('NFKD', s.lower())
        return ''.join(c for c in nfkd if not unicodedata.combining(c))

    if not os.path.isdir(base_dir):
        return ''
        
    for name in os.listdir(base_dir):
        full = os.path.join(base_dir, name)
        if not os.path.isdir(full):
            continue
            
        if category == 'ffstock':
            # Chứa "FFSTOCK" trong tên file con
            matches = glob.glob(os.path.join(full, '**', '*FFSTOCK*'), recursive=True)
            if matches:
                # Phải chứa thư mục "FFSTOCK THANG"
                matches_ascii = [_strip_accents(m) for m in matches]
                if any('ffstock thang' in m for m in matches_ascii):
                    return full
                    
        elif category == 'empty_bag':
            # Chứa "EMPTY BAG" trong tên file con
            matches = glob.glob(os.path.join(full, '**', '*EMPTY BAG*'), recursive=True)
            if matches:
                return full
                
        elif category == 'forecast':
            matches = glob.glob(os.path.join(full, '**', '*FORECAST*'), recursive=True)
            if matches or 'sale packing' in name.lower():
                return full
                
        elif category == 'tonbon':
            matches = glob.glob(os.path.join(full, '**', '*ton bon*'), recursive=True)
            matches2 = glob.glob(os.path.join(full, '**', '*ton bin*'), recursive=True)
            if matches or matches2 or 'ton bin' in _strip_accents(name) or 'ton bon' in _strip_accents(name):
                return full
                
    return ''

print("=" * 60)
print("KẾT QUẢ TỰ ĐỘNG PHÂN LOẠI THƯ MỤC ONEDRIVE:")
ff_dir = detect_category('ffstock')
bag_dir = detect_category('empty_bag')
fc_dir = detect_category('forecast')
tb_dir = detect_category('tonbon')

print(f"  -> FFStock Folder:   {ff_dir}")
print(f"  -> Empty Bag Folder: {bag_dir}")
print(f"  -> Forecast Folder:  {fc_dir}")
print(f"  -> Ton Bon Folder:   {tb_dir}")
print("=" * 60)

import data_loader

if ff_dir:
    f_ff = data_loader._find_latest_file(ff_dir, '*FFSTOCK*.xls*')
    print(f"Latest FFStock file found: {f_ff}")
if bag_dir:
    f_bag = data_loader._find_latest_file(bag_dir, '*EMPTY BAG*.xls*')
    print(f"Latest Empty Bag file found: {f_bag}")
print("=" * 60)

