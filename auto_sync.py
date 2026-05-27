# -*- coding: utf-8 -*-
"""
AUTO SYNC - Tự động đồng bộ dữ liệu từ OneDrive lên Cloud Database (Neon Tech)
================================================================================
Chạy script này trên máy có OneDrive (máy văn phòng).
Nó sẽ tự kiểm tra file mới mỗi 10 phút và đẩy lên PostgreSQL.

Cách dùng:
  - Click đúp auto_sync.bat  (hoặc)
  - Task Scheduler chạy tự động khi bật máy
"""

import os
import sys
import time
import datetime
import hashlib
import json
import traceback

# Fix encoding cho Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Thêm thư mục hiện tại vào path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

# ============================================================
# CẤU HÌNH
# ============================================================
SYNC_INTERVAL_MINUTES = 10   # Kiểm tra mỗi 10 phút
LOG_FILE = os.path.join(SCRIPT_DIR, 'auto_sync.log')
STATE_FILE = os.path.join(SCRIPT_DIR, '.sync_state.json')

# ============================================================
# LOGGING
# ============================================================
def log(msg, level='INFO'):
    """Ghi log ra console và file"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{timestamp}] [{level}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(line + '\n')
    except:
        pass

def log_separator():
    log('=' * 60)

# ============================================================
# THEO DÕI THAY ĐỔI FILE
# ============================================================
def get_file_hash(filepath):
    """Tính hash nhanh: mtime + size (không cần đọc nội dung)"""
    try:
        stat = os.stat(filepath)
        return f"{stat.st_mtime:.2f}_{stat.st_size}"
    except:
        return None

def load_state():
    """Đọc trạng thái lần sync trước"""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {'file_hashes': {}, 'last_sync': None}

def save_state(state):
    """Lưu trạng thái sync"""
    try:
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except:
        pass

def scan_files(cfg):
    """Quét tất cả file Excel đầu vào, trả về dict {category: filepath}"""
    import glob
    
    files = {}
    
    # Daily reports
    categories = {
        'ffstock': (getattr(cfg, 'FSTOCK_DIR_FFSTOCK', cfg.FSTOCK_DIR), '*FFSTOCK*.xls*'),
        'empty_bag': (getattr(cfg, 'FSTOCK_DIR_EMPTYBAG', cfg.FSTOCK_DIR), '*EMPTY BAG*.xls*'),
        'tonbon': (cfg.TONBON_DIR, '*ton bon*.xlsx'),
        'forecast': (cfg.FORECAST_DIR, '*FORECAST*.xlsx'),
        'silo_plan': (cfg.SILO_DIR, '*SILO*.xlsx'),
        'bacang': (cfg.BACANG_DIR, '*CANG*.xlsx'),
    }
    
    for cat, (directory, pattern) in categories.items():
        if not directory or not os.path.isdir(directory):
            continue
        
        search = os.path.join(directory, '**', pattern)
        found = glob.glob(search, recursive=True)
        found = [f for f in found if not os.path.basename(f).startswith('~$')]
        
        if found:
            # Lấy file mới nhất
            latest = max(found, key=os.path.getmtime)
            files[cat] = latest
    
    # Static files
    for cat, attr in [('congsuat', 'PLAN_FILE'), ('feedcode', 'KHSX_FILE'), ('khangsinh', 'KHSX_FILE')]:
        path = getattr(cfg, attr, None)
        if path and os.path.isfile(path):
            files[cat] = path
    
    return files

def check_changes(current_files, state):
    """So sánh file hiện tại với lần sync trước, trả về danh sách thay đổi"""
    changed = []
    old_hashes = state.get('file_hashes', {})
    
    for cat, filepath in current_files.items():
        current_hash = get_file_hash(filepath)
        old_hash = old_hashes.get(cat)
        
        if current_hash != old_hash:
            changed.append({
                'category': cat,
                'filepath': filepath,
                'filename': os.path.basename(filepath),
                'hash': current_hash,
                'is_new': old_hash is None
            })
    
    return changed

# ============================================================
# ĐỒNG BỘ
# ============================================================
def sync_all(cfg):
    """Đồng bộ toàn bộ dữ liệu lên cloud"""
    import db_manager
    db_uri = getattr(cfg, 'DB_URI', db_manager.DB_URI)
    db_manager.sync_local_to_db(cfg, db_uri)

def sync_single(cfg, category):
    """Đồng bộ 1 danh mục"""
    import db_manager
    db_uri = getattr(cfg, 'DB_URI', db_manager.DB_URI)
    result = db_manager.sync_category_to_db(cfg, category, db_uri)
    return result

# ============================================================
# VÒNG LẶP CHÍNH
# ============================================================
def run_once():
    """Chạy 1 lần kiểm tra và sync nếu có thay đổi"""
    import config as cfg
    
    state = load_state()
    current_files = scan_files(cfg)
    changes = check_changes(current_files, state)
    
    if not changes:
        log('✅ Không có file nào thay đổi — bỏ qua sync.')
        return False
    
    log(f'📦 Phát hiện {len(changes)} file thay đổi:')
    for c in changes:
        status = '🆕 MỚI' if c['is_new'] else '🔄 CẬP NHẬT'
        log(f'   {status} [{c["category"].upper()}] {c["filename"]}')
    
    # Sync toàn bộ (vì các file có thể liên quan nhau)
    log('☁️ Bắt đầu đồng bộ lên Neon Tech Cloud Database...')
    try:
        sync_all(cfg)
        log('✅ Đồng bộ thành công!')
        
        # Cập nhật state
        new_hashes = {}
        for cat, filepath in current_files.items():
            new_hashes[cat] = get_file_hash(filepath)
        
        state['file_hashes'] = new_hashes
        state['last_sync'] = datetime.datetime.now().isoformat()
        state['last_sync_changes'] = len(changes)
        save_state(state)
        
        return True
    except Exception as e:
        log(f'❌ LỖI ĐỒNG BỘ: {e}', 'ERROR')
        traceback.print_exc()
        return False

def run_loop():
    """Vòng lặp chính — chạy liên tục, kiểm tra mỗi N phút"""
    log_separator()
    log('🚀 AUTO SYNC - Khởi động hệ thống đồng bộ tự động')
    log(f'   Chu kỳ kiểm tra: mỗi {SYNC_INTERVAL_MINUTES} phút')
    log(f'   Log file: {LOG_FILE}')
    log_separator()
    
    # Sync ngay lần đầu khi khởi động
    log('🔍 Kiểm tra lần đầu...')
    run_once()
    
    cycle = 0
    while True:
        try:
            # Chờ N phút
            next_check = datetime.datetime.now() + datetime.timedelta(minutes=SYNC_INTERVAL_MINUTES)
            log(f'⏳ Lần kiểm tra tiếp theo: {next_check.strftime("%H:%M:%S")}')
            time.sleep(SYNC_INTERVAL_MINUTES * 60)
            
            cycle += 1
            log_separator()
            log(f'🔍 Kiểm tra lần #{cycle}...')
            run_once()
            
        except KeyboardInterrupt:
            log('⏹️ Dừng auto-sync theo yêu cầu (Ctrl+C)')
            break
        except Exception as e:
            log(f'❌ Lỗi không mong đợi: {e}', 'ERROR')
            traceback.print_exc()
            time.sleep(60)  # Chờ 1 phút rồi thử lại

# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == '__main__':
    # Nếu truyền tham số --once thì chỉ chạy 1 lần
    if '--once' in sys.argv:
        log_separator()
        log('🔍 Chạy kiểm tra 1 lần (--once)')
        run_once()
    else:
        run_loop()
