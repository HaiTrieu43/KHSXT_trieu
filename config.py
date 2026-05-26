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
# OneDrive doanh nghiệp tự động tải file SharePoint về thư mục này.
# Hệ thống sẽ ưu tiên đọc từ thư mục OneDrive, nếu không có sẽ fallback về ổ D:.

ONEDRIVE_BASE_DIR = r'C:\Users\haitr\OneDrive - Cong Ty Co Phan Chan Nuoi C.P. Viet Nam'

# Đường dẫn các thư mục OneDrive đã đồng bộ từ SharePoint (sẽ tự phát hiện sau khi sync)
# Khi bạn nhấn "Sync" trên SharePoint, OneDrive sẽ tạo thư mục tương ứng.
# Cấu hình bên dưới sẽ được cập nhật sau khi bạn sync xong.

# --- FFStock (Tồn kho thành phẩm hàng ngày) ---
ONEDRIVE_FFSTOCK_DIR = os.path.join(
    ONEDRIVE_BASE_DIR,
    r'BDG AgroFeed Public\04. Phòng Kho Thành Phẩm\HỒ SƠ ONLINE\11. BÁO CÁO TỒN KHO CÁM HÀNG NGÀY (QT-TP-02.BM08)\NĂM 2026'
)

# --- Empty Bag (Bao bì hàng ngày) ---
ONEDRIVE_EMPTY_BAG_DIR = os.path.join(
    ONEDRIVE_BASE_DIR,
    r'BDG AgroFeed Public\04. Phòng Kho Thành Phẩm\HỒ SƠ ONLINE\15. BÁO CÁO TỒN KHO BAO BÌ HÀNG NGÀY (QT-TP-02.BM12)\NĂM 2026'
)

# --- Sale Packing Daily (Forecast) ---
ONEDRIVE_FORECAST_DIR = os.path.join(
    ONEDRIVE_BASE_DIR,
    r'BDG AgroFeed Production\File dùng chung\BỘ PHẬN HÀNH CHÁNH\MR NHO\sale packing daily'
)

# --- Tồn Bồn (Bin Report) ---
ONEDRIVE_TONBON_DIR = os.path.join(
    ONEDRIVE_BASE_DIR,
    r'BDG AgroFeed Production\File dùng chung\BÁO CÁO VẬN HÀNH SẢN XUẤT\BÁO CÁO BIN-QC\BÁO CÁO TỒN BIN\2026'
)

def _pick_dir(onedrive_dir, fallback_dir):
    """Ưu tiên thư mục OneDrive nếu tồn tại, nếu không dùng fallback."""
    if os.path.isdir(onedrive_dir):
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


