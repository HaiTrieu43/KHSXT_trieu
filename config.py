"""
config.py - Cấu hình đường dẫn file và hằng số
"""
import os

# ============================================
# THƯ MỤC GỐC
# ============================================
DATA_DIR = r'D:\Kê hoạch sản xuât'

# ============================================
# ĐƯỜNG DẪN FILE INPUT
# ============================================
FORECAST_DIR = os.path.join(DATA_DIR, 'FORECAST')
SILO_DIR = os.path.join(DATA_DIR, 'SILO')
BACANG_DIR = os.path.join(DATA_DIR, 'BACANG')
FSTOCK_DIR = os.path.join(DATA_DIR, 'FSTOCK-BAG')
TONBON_DIR = os.path.join(DATA_DIR, 'BATCHING-TONBON')
PLAN_DIR = os.path.join(DATA_DIR, 'plan')

# File cố định (ít thay đổi)
KHSX_FILE = os.path.join(DATA_DIR, 'KHSX THANG 5-20261.xlsm')
PLAN_FILE = os.path.join(PLAN_DIR, 'Plan.xlsm')
QUICK_ADJUST_FILE = os.path.join(DATA_DIR, 'DIEU_CHINH_NHANH.xlsx')


# ============================================
# HẰNG SỐ SẢN XUẤT
# ============================================
MIN_DAILY_TONS = 2100    # Công suất tối thiểu (tấn/ngày)
MAX_DAILY_TONS = 2500    # Công suất tối đa (tấn/ngày)
TARGET_DAILY_TONS = 2250 # Mục tiêu (tấn/ngày)

# Trọng lượng mẻ mặc định
DEFAULT_TON_PER_BATCH = 8.4
SMALL_DIE_TON_PER_BATCH = 8.0  # Cho sản phẩm DIE nhỏ (55x)
CDIE_TON_PER_BATCH = 5.0       # Chuyển khuôn

# Ngưỡng hoàn thành (%) để không cần bù
COMPLETION_THRESHOLD = 95

# Số ngày làm việc trong tuần (Thứ 2 → Thứ 7)
WORKING_DAYS_PER_WEEK = 6

# ============================================
# THƯ MỤC OUTPUT
# ============================================
OUTPUT_DIR = os.path.join(DATA_DIR, 'laptrinh vao', 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================
# CẤU HÌNH DATABASE CLOUD (NEON TECH)
# ============================================
USE_POSTGRESQL = True
DB_URI = os.environ.get('DATABASE_URL') or os.environ.get('DB_URI') or "postgresql://neondb_owner:npg_ITvYDxe34qWl@ep-ancient-waterfall-aonnt7nf-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# ============================================
# CẤU HÌNH TÀI KHOẢN ADMIN ĐĂNG NHẬP APP
# ============================================
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', '123456')

# ============================================
# CẤU HÌNH ONEDRIVE ĐỒNG BỘ CỤC BỘ
# ============================================
# Khi nhấn "Add shortcut to OneDrive" trên SharePoint, OneDrive tạo thư mục
# với tên rút gọn (không giữ nguyên cấu trúc SharePoint gốc).
# Đường dẫn thực tế đã xác minh ngày 26/05/2026.

ONEDRIVE_BASE_DIR = r'C:\Users\haitr\OneDrive - Cong Ty Co Phan Chan Nuoi C.P. Viet Nam'

def _find_onedrive_shortcut(base_dir, keyword):
    """Tìm thư mục OneDrive shortcut chứa keyword (không phân biệt hoa/thường, bỏ dấu).
    
    OneDrive tạo shortcut với tên có dấu VN (VD: 'CPV Document - NĂM 2026').
    Dùng Unicode NFKD normalize để bỏ dấu trước khi so sánh.
    """
    import unicodedata
    
    def _strip_accents(s):
        nfkd = unicodedata.normalize('NFKD', s.lower())
        return ''.join(c for c in nfkd if not unicodedata.combining(c))
    
    if not os.path.isdir(base_dir):
        return ''
    keyword_ascii = _strip_accents(keyword)
    for name in os.listdir(base_dir):
        full = os.path.join(base_dir, name)
        if os.path.isdir(full) and keyword_ascii in _strip_accents(name):
            return full
    return ''

# --- FFStock (Tồn kho thành phẩm hàng ngày) ---
# Thực tế: CPV Document - NAM 2026\FFSTOCK THANG 05-2026\FFSTOCK 22-05-2026.xlsm
# Shortcut chứa keyword "NAM 2026" thuộc mục BÁO CÁO TỒN KHO CÁM
ONEDRIVE_FFSTOCK_DIR = _find_onedrive_shortcut(ONEDRIVE_BASE_DIR, 'NAM 2026')

# --- Empty Bag (Bao bì hàng ngày) ---  
# Sẽ có shortcut riêng sau khi sync, chứa keyword tương ứng
ONEDRIVE_EMPTY_BAG_DIR = _find_onedrive_shortcut(ONEDRIVE_BASE_DIR, 'BAO BI')

# --- Sale Packing Daily (Forecast) ---
ONEDRIVE_FORECAST_DIR = _find_onedrive_shortcut(ONEDRIVE_BASE_DIR, 'sale packing')

# --- Tồn Bồn (Bin Report) ---
ONEDRIVE_TONBON_DIR = _find_onedrive_shortcut(ONEDRIVE_BASE_DIR, 'TON BIN')

def _pick_dir(onedrive_dir, fallback_dir):
    """Ưu tiên thư mục OneDrive nếu tồn tại, nếu không dùng fallback."""
    if onedrive_dir and os.path.isdir(onedrive_dir):
        return onedrive_dir
    return fallback_dir

# Override thư mục đầu vào: ưu tiên OneDrive, fallback về ổ D:
FORECAST_DIR = _pick_dir(ONEDRIVE_FORECAST_DIR, FORECAST_DIR)
FSTOCK_DIR_FFSTOCK = _pick_dir(ONEDRIVE_FFSTOCK_DIR, FSTOCK_DIR)     # Riêng FFStock
FSTOCK_DIR_EMPTYBAG = _pick_dir(ONEDRIVE_EMPTY_BAG_DIR, FSTOCK_DIR)  # Riêng Empty Bag
TONBON_DIR = _pick_dir(ONEDRIVE_TONBON_DIR, TONBON_DIR)


# Ghi log thư mục đang sử dụng khi khởi chạy
def _log_active_dirs():
    """In ra console thư mục dữ liệu đang dùng (OneDrive hay fallback)"""
    import sys
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
    
    try:
        print("=" * 60)
        print("[DIRS] CAU HINH THU MUC DU LIEU DANG SU DUNG:")
        print(f"   Forecast:  {FORECAST_DIR}")
        print(f"   FFStock:   {FSTOCK_DIR_FFSTOCK}")
        print(f"   Empty Bag: {FSTOCK_DIR_EMPTYBAG}")
        print(f"   Ton Bon:   {TONBON_DIR}")
        print(f"   Silo:      {SILO_DIR}")
        print(f"   Ba Cang:   {BACANG_DIR}")
        
        onedrive_active = any([
            os.path.isdir(ONEDRIVE_FFSTOCK_DIR),
            os.path.isdir(ONEDRIVE_EMPTY_BAG_DIR),
            os.path.isdir(ONEDRIVE_FORECAST_DIR),
            os.path.isdir(ONEDRIVE_TONBON_DIR),
        ])
        if onedrive_active:
            print("   [OK] OneDrive dang hoat dong - doc du lieu tu SharePoint tu dong!")
        else:
            print("   [!] OneDrive chua duoc dong bo - dang dung thu muc cuc bo o D:")
        print("=" * 60)
    except Exception:
        pass

_log_active_dirs()


# ============================================
# CẤU HÌNH SHAREPOINT URL (Dự phòng - chỉ dùng khi không có OneDrive)
# ============================================
SHAREPOINT_FORECAST_URL = os.environ.get('SHAREPOINT_FORECAST_URL', '')
SHAREPOINT_SILO_URL = os.environ.get('SHAREPOINT_SILO_URL', '')
SHAREPOINT_BACANG_URL = os.environ.get('SHAREPOINT_BACANG_URL', '')
SHAREPOINT_FFSTOCK_URL = os.environ.get('SHAREPOINT_FFSTOCK_URL', '')
SHAREPOINT_EMPTY_BAG_URL = os.environ.get('SHAREPOINT_EMPTY_BAG_URL', '')
SHAREPOINT_TONBON_URL = os.environ.get('SHAREPOINT_TONBON_URL', '')
SHAREPOINT_PLAN_URL = os.environ.get('SHAREPOINT_PLAN_URL', '')


