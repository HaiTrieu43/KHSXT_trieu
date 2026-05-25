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
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'cp@123456')

