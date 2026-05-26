"""
db_manager.py - Quản lý cơ sở dữ liệu PostgreSQL (Neon Tech)
Tự động khởi tạo cấu trúc bảng, đồng bộ dữ liệu Excel lên Cloud
và đọc dữ liệu trực tiếp phục vụ giải thuật KHSX mà không cần file Excel.
"""
import sys
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime, date

# Thiết lập encoding utf-8 cho console logs
if sys.platform == 'win32':
    import io
    if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from models import ForecastItem, ProductSpec, Priority

# Connection string mặc định
DB_URI = "postgresql://neondb_owner:npg_ITvYDxe34qWl@ep-ancient-waterfall-aonnt7nf-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"


def get_connection(conn_str=DB_URI):
    return psycopg2.connect(conn_str)


def init_db(conn_str=DB_URI):
    """Khởi tạo cấu trúc bảng trong PostgreSQL nếu chưa tồn tại"""
    print("⏳ Khởi tạo các bảng cơ sở dữ liệu trên Neon Tech...")
    conn = get_connection(conn_str)
    cur = conn.cursor()
    
    # 1. Bảng forecast
    cur.execute("""
    CREATE TABLE IF NOT EXISTS forecast (
        id SERIAL PRIMARY KEY,
        product_code VARCHAR(50),
        packing_size VARCHAR(50),
        die_size FLOAT,
        dealer_higro FLOAT,
        dealer_cp FLOAT,
        dealer_star FLOAT,
        dealer_nuvo FLOAT,
        dealer_nasa FLOAT,
        dealer_total FLOAT,
        farm_swine FLOAT,
        farm_integrate FLOAT,
        farm_total FLOAT,
        grand_total_tons FLOAT,
        silo_tons FLOAT,
        total_with_silo FLOAT,
        bag_higro INT,
        bag_cp INT,
        bag_star INT,
        bag_nuvo INT,
        bag_nasa INT,
        bag_dealer_total INT,
        bag_farm INT,
        bag_grand_total INT,
        feed_code_higro VARCHAR(50),
        feed_code_cp VARCHAR(50),
        feed_code_star VARCHAR(50),
        feed_code_nuvo VARCHAR(50),
        feed_code_nasa VARCHAR(50),
        feed_code_farm VARCHAR(50)
    );
    """)

    # 2. Bảng silo_plan
    cur.execute("""
    CREATE TABLE IF NOT EXISTS silo_plan (
        id SERIAL PRIMARY KEY,
        day INT,
        product_code VARCHAR(50),
        tons FLOAT
    );
    """)

    # 3. Bảng bacang
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bacang (
        id SERIAL PRIMARY KEY,
        day INT,
        product_code VARCHAR(50),
        tons FLOAT
    );
    """)

    # 4. Bảng ffstock
    cur.execute("""
    CREATE TABLE IF NOT EXISTS ffstock (
        id SERIAL PRIMARY KEY,
        product_code VARCHAR(50),
        stock_tons FLOAT
    );
    """)

    # 5. Bảng ffstock_details
    cur.execute("""
    CREATE TABLE IF NOT EXISTS ffstock_details (
        id SERIAL PRIMARY KEY,
        product_code VARCHAR(50),
        product_name VARCHAR(255),
        safety_stock_tons FLOAT,
        daily_sales_tons FLOAT,
        doh FLOAT,
        warning VARCHAR(255)
    );
    """)

    # 6. Bảng tonbon
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tonbon (
        id SERIAL PRIMARY KEY,
        product_code VARCHAR(50),
        stock_tons FLOAT
    );
    """)

    # 7. Bảng tonbon_detail
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tonbon_detail (
        id SERIAL PRIMARY KEY,
        bon_id VARCHAR(50),
        product_code VARCHAR(50),
        tons FLOAT
    );
    """)

    # 8. Bảng empty_bag
    cur.execute("""
    CREATE TABLE IF NOT EXISTS empty_bag (
        id SERIAL PRIMARY KEY,
        product_code VARCHAR(50),
        brand VARCHAR(50),
        bags INT
    );
    """)

    # 9. Bảng congsuat
    cur.execute("""
    CREATE TABLE IF NOT EXISTS congsuat (
        id SERIAL PRIMARY KEY,
        product_code VARCHAR(50),
        formular_code VARCHAR(100),
        die_size FLOAT,
        ton_per_batch FLOAT,
        line_cv VARCHAR(50),
        line_pk VARCHAR(50),
        ks_code VARCHAR(100)
    );
    """)

    # 10. Bảng stt_khangsinh (cấp độ)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS stt_khangsinh (
        id SERIAL PRIMARY KEY,
        ks_level INT,
        ks_name VARCHAR(255)
    );
    """)

    # 11. Bảng fix_code_pellet
    cur.execute("""
    CREATE TABLE IF NOT EXISTS fix_code_pellet (
        id SERIAL PRIMARY KEY,
        product_code VARCHAR(50),
        packing_size VARCHAR(50),
        die_size FLOAT,
        default_line VARCHAR(50),
        priority_1 VARCHAR(50),
        priority_2 VARCHAR(50),
        priority_3 VARCHAR(50),
        priority_4 VARCHAR(50),
        priority_5 VARCHAR(50)
    );
    """)

    # 12. Bảng feedcode
    cur.execute("""
    CREATE TABLE IF NOT EXISTS feedcode (
        id SERIAL PRIMARY KEY,
        product_code VARCHAR(50),
        line_cv VARCHAR(50),
        line_pk VARCHAR(50)
    );
    """)

    # 13. Bảng khangsinh (mã kháng sinh)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS khangsinh (
        id SERIAL PRIMARY KEY,
        product_code VARCHAR(50),
        ks_code VARCHAR(100),
        ks_level INT
    );
    """)

    # 14. Bảng khsx_yesterday
    cur.execute("""
    CREATE TABLE IF NOT EXISTS khsx_yesterday (
        id SERIAL PRIMARY KEY,
        product_code VARCHAR(50),
        planned FLOAT,
        actual FLOAT
    );
    """)

    # 15. Bảng adjustments
    cur.execute("""
    CREATE TABLE IF NOT EXISTS adjustments (
        id SERIAL PRIMARY KEY,
        adj_type VARCHAR(50), -- 'addition', 'cancellation', 'substitution', 'bag_substitution'
        product_code VARCHAR(50),
        param_1 VARCHAR(255),
        param_2 VARCHAR(255),
        param_3 VARCHAR(255),
        param_4 VARCHAR(255),
        param_5 VARCHAR(255),
        note VARCHAR(255)
    );
    """)

    # 16. Bảng lưu trữ lịch sử kế hoạch sản xuất đầu ra để có thể khôi phục không cần file Excel
    cur.execute("""
    CREATE TABLE IF NOT EXISTS plan_outputs (
        id SERIAL PRIMARY KEY,
        date_str VARCHAR(50) UNIQUE,
        filename VARCHAR(255),
        khpl_raw_grid JSONB,
        sequence JSONB,
        packaging JSONB,
        summary JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Đã tạo cấu trúc các bảng thành công trên Neon Tech!")


def clear_db(conn_str=DB_URI):
    """Xóa sạch dữ liệu trong các bảng phục vụ đồng bộ mới"""
    print("🗑️ Đang làm sạch dữ liệu cũ trong các bảng...")
    conn = get_connection(conn_str)
    cur = conn.cursor()
    tables = [
        'forecast', 'silo_plan', 'bacang', 'ffstock', 'ffstock_details',
        'tonbon', 'tonbon_detail', 'empty_bag', 'congsuat', 'stt_khangsinh',
        'fix_code_pellet', 'feedcode', 'khangsinh', 'khsx_yesterday', 'adjustments'
    ]
    for table in tables:
        cur.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Đã làm sạch các bảng!")


def sync_local_to_db(config, conn_str=DB_URI):
    """
    Đọc tất cả các file Excel cục bộ hiện tại bằng data_loader 
    và tải trực tiếp lên PostgreSQL (Neon Tech)
    """
    import data_loader
    init_db(conn_str)
    clear_db(conn_str)
    
    # Đọc dữ liệu từ file Excel cục bộ (tạm thời tắt database mode để đọc thực tế từ Excel)
    was_postgres = getattr(config, 'USE_POSTGRESQL', False)
    config.USE_POSTGRESQL = False
    try:
        data = data_loader.load_all_data(config)
    finally:
        config.USE_POSTGRESQL = was_postgres
    
    conn = get_connection(conn_str)
    cur = conn.cursor()
    
    # 1. Đồng bộ forecast
    print("📤 Đang đồng bộ Forecast...")
    fc_data = []
    for it in data.get('forecast', []):
        fc_data.append((
            it.product_code, it.packing_size, it.die_size,
            it.dealer_higro, it.dealer_cp, it.dealer_star, it.dealer_nuvo, it.dealer_nasa, it.dealer_total,
            it.farm_swine, it.farm_integrate, it.farm_total,
            it.grand_total_tons, it.silo_tons, it.total_with_silo,
            it.bag_higro, it.bag_cp, it.bag_star, it.bag_nuvo, it.bag_nasa, it.bag_dealer_total,
            it.bag_farm, it.bag_grand_total,
            it.feed_code_higro, it.feed_code_cp, it.feed_code_star, it.feed_code_nuvo, it.feed_code_nasa, it.feed_code_farm
        ))
    if fc_data:
        execute_values(cur, """
        INSERT INTO forecast (
            product_code, packing_size, die_size,
            dealer_higro, dealer_cp, dealer_star, dealer_nuvo, dealer_nasa, dealer_total,
            farm_swine, farm_integrate, farm_total,
            grand_total_tons, silo_tons, total_with_silo,
            bag_higro, bag_cp, bag_star, bag_nuvo, bag_nasa, bag_dealer_total,
            bag_farm, bag_grand_total,
            feed_code_higro, feed_code_cp, feed_code_star, feed_code_nuvo, feed_code_nasa, feed_code_farm
        ) VALUES %s
        """, fc_data)
        
    # 2. Đồng bộ silo_plan
    print("📤 Đang đồng bộ Kế hoạch Silo...")
    sp_data = []
    for day, products in data.get('silo_plan', {}).items():
        for p, tons in products.items():
            sp_data.append((day, p, tons))
    if sp_data:
        execute_values(cur, "INSERT INTO silo_plan (day, product_code, tons) VALUES %s", sp_data)

    # 3. Đồng bộ bacang
    print("📤 Đang đồng bộ Silo Bá Căng...")
    bc_data = []
    for day, products in data.get('bacang', {}).items():
        for p, tons in products.items():
            bc_data.append((day, p, tons))
    if bc_data:
        execute_values(cur, "INSERT INTO bacang (day, product_code, tons) VALUES %s", bc_data)

    # 4. Đồng bộ ffstock
    print("📤 Đang đồng bộ Stock đầu ngày...")
    ff_data = []
    for p, tons in data.get('ffstock', {}).items():
        ff_data.append((p, tons))
    if ff_data:
        execute_values(cur, "INSERT INTO ffstock (product_code, stock_tons) VALUES %s", ff_data)

    # 5. Đồng bộ ffstock_details
    print("📤 Đang đồng bộ Chi tiết DOH...")
    ffd_data = []
    for p, det in data.get('ffstock_details', {}).items():
        ffd_data.append((
            p, det.get('product_name', ''), det.get('stock_tons', 0.0),
            det.get('sales_avg_kg', 0.0), det.get('doh', None), det.get('warning', '')
        ))
    if ffd_data:
        execute_values(cur, """
        INSERT INTO ffstock_details (
            product_code, product_name, safety_stock_tons, daily_sales_tons, doh, warning
        ) VALUES %s
        """, ffd_data)

    # 6. Đồng bộ tonbon
    print("📤 Đang đồng bộ Tồn bồn...")
    tb_data = []
    for p, tons in data.get('tonbon', {}).items():
        tb_data.append((p, tons))
    if tb_data:
        execute_values(cur, "INSERT INTO tonbon (product_code, stock_tons) VALUES %s", tb_data)

    # 7. Đồng bộ tonbon_detail
    print("📤 Đang đồng bộ Chi tiết Bồn chứa...")
    tbd_data = []
    for b_id, item in data.get('tonbon_detail', {}).items():
        tbd_data.append((b_id, item.get('product', item.get('product_code', '')), item.get('tons', 0.0)))
    if tbd_data:
        execute_values(cur, "INSERT INTO tonbon_detail (bon_id, product_code, tons) VALUES %s", tbd_data)

    # 8. Đồng bộ empty_bag
    print("📤 Đang đồng bộ Kho vỏ bao bì...")
    eb_data = []
    for p, brands in data.get('empty_bag', {}).items():
        for b, qty in brands.items():
            eb_data.append((p, b, qty))
    if eb_data:
        execute_values(cur, "INSERT INTO empty_bag (product_code, brand, bags) VALUES %s", eb_data)

    # 9. Đồng bộ congsuat
    print("📤 Đang đồng bộ Công suất & Specs...")
    cs_data = []
    for p, spec in data.get('congsuat', {}).items():
        cs_data.append((
            p, spec.formular_code, spec.die_size, spec.ton_per_batch,
            spec.line_cv, spec.line_pk, spec.ks_code
        ))
    if cs_data:
        execute_values(cur, """
        INSERT INTO congsuat (
            product_code, formular_code, die_size, ton_per_batch, line_cv, line_pk, ks_code
        ) VALUES %s
        """, cs_data)

    # 10. Đồng bộ stt_khangsinh
    print("📤 Đang đồng bộ Cấp độ kháng sinh...")
    stt_ks_data = []
    for lvl, name in data.get('stt_khangsinh', {}).items():
        stt_ks_data.append((lvl, name))
    if stt_ks_data:
        execute_values(cur, "INSERT INTO stt_khangsinh (ks_level, ks_name) VALUES %s", stt_ks_data)

    # 11. Đồng bộ fix_code_pellet
    print("📤 Đang đồng bộ Ma trận Pellet...")
    fcp_data = []
    for p, cfg in data.get('fix_code_pellet', {}).items():
        pr = cfg.get('priorities', [])
        p1 = pr[0] if len(pr) > 0 else ''
        p2 = pr[1] if len(pr) > 1 else ''
        p3 = pr[2] if len(pr) > 2 else ''
        p4 = pr[3] if len(pr) > 3 else ''
        p5 = pr[4] if len(pr) > 4 else ''
        fcp_data.append((
            p, cfg.get('packing_size', ''), cfg.get('die_size', 0.0), cfg.get('default_line', ''),
            p1, p2, p3, p4, p5
        ))
    if fcp_data:
        execute_values(cur, """
        INSERT INTO fix_code_pellet (
            product_code, packing_size, die_size, default_line,
            priority_1, priority_2, priority_3, priority_4, priority_5
        ) VALUES %s
        """, fcp_data)

    # 12. Đồng bộ feedcode
    print("📤 Đang đồng bộ Định biên đóng bao...")
    fc_map_data = []
    for p, cfg in data.get('feedcode', {}).items():
        fc_map_data.append((p, cfg.get('line_cv', ''), cfg.get('line_pk', '')))
    if fc_map_data:
        execute_values(cur, "INSERT INTO feedcode (product_code, line_cv, line_pk) VALUES %s", fc_map_data)

    # 13. Đồng bộ khangsinh
    print("📤 Đang đồng bộ Cấu hình kháng sinh sản phẩm...")
    ks_map_data = []
    for p, ks_info in data.get('khangsinh', {}).items():
        ks_map_data.append((p, ks_info.get('ks_code', ''), ks_info.get('ks_level', 1)))
    if ks_map_data:
        execute_values(cur, "INSERT INTO khangsinh (product_code, ks_code, ks_level) VALUES %s", ks_map_data)

    # 14. Đồng bộ khsx_yesterday
    print("📤 Đang đồng bộ KHSX hôm qua...")
    yest_data = []
    for p, cfg in data.get('khsx_yesterday', {}).items():
        yest_data.append((p, cfg.get('planned', 0.0), cfg.get('actual', 0.0)))
    if yest_data:
        execute_values(cur, "INSERT INTO khsx_yesterday (product_code, planned, actual) VALUES %s", yest_data)

    # 15. Đồng bộ adjustments
    print("📤 Đang đồng bộ Điều chỉnh nhanh...")
    adj = data.get('adjustments', {})
    adj_data = []
    
    # additions
    for it in adj.get('additions', []):
        adj_data.append((
            'addition', it.get('product_code', ''), str(it.get('tons', 0.0)),
            it.get('packing_size', '25'), it.get('priority', 'FORECAST'),
            str(it.get('force_batches', '') if it.get('force_batches') is not None else ''), 
            str(it.get('force_tpb', '') if it.get('force_tpb') is not None else ''),
            it.get('note', '')
        ))
    # cancellations
    for p, mode in adj.get('cancellations', {}).items():
        adj_data.append(('cancellation', p, mode, '', '', '', '', ''))
        
    # substitutions
    for orig, repl in adj.get('substitutions', {}).items():
        adj_data.append(('substitution', orig, repl, '', '', '', '', ''))
        
    # bag substitutions
    for p, orig_repls in adj.get('bag_substitutions', {}).items():
        for o_brand, r_brand in orig_repls.items():
            adj_data.append(('bag_substitution', p, o_brand, r_brand, '', '', '', ''))
            
    if adj_data:
        execute_values(cur, """
        INSERT INTO adjustments (
            adj_type, product_code, param_1, param_2, param_3, param_4, param_5, note
        ) VALUES %s
        """, adj_data)

    conn.commit()
    cur.close()
    conn.close()
    print("🎉 ĐỒNG BỘ THÀNH CÔNG TOÀN BỘ DỮ LIỆU LÊN NEON TECH!")


def load_all_data_from_db(conn_str=DB_URI, target_date=None) -> dict:
    """
    Đọc toàn bộ dữ liệu trực tiếp từ PostgreSQL (Neon Tech) 
    và tái tạo cấu trúc giống hệt load_all_data của data_loader.
    """
    print("\n⚡ Đang đọc dữ liệu đầu vào trực tiếp từ PostgreSQL (Neon Tech)...")
    conn = get_connection(conn_str)
    cur = conn.cursor()
    
    data = {}
    
    # 0. Adjustments
    cur.execute("SELECT adj_type, product_code, param_1, param_2, param_3, param_4, param_5 FROM adjustments;")
    adj_rows = cur.fetchall()
    additions = []
    cancellations = {}
    substitutions = {}
    bag_substitutions = {}
    
    for r in adj_rows:
        a_type, p_code, p1, p2, p3, p4, p5 = r
        if a_type == 'addition':
            # tons, batches, tons_per_batch
            t = float(p1) if p1 else 0.0
            pack = p2 if p2 else '25'
            pri = p3 if p3 else 'FORECAST'
            b = int(p4) if p4 and p4.isdigit() else None
            tpb = float(p5) if p5 else None
            additions.append({
                'product_code': p_code,
                'tons': t,
                'packing_size': pack,
                'priority': pri,
                'force_batches': b,
                'force_tpb': tpb
            })
        elif a_type == 'cancellation':
            cancellations[p_code] = p1
        elif a_type == 'substitution':
            substitutions[p_code] = p1
        elif a_type == 'bag_substitution':
            if p_code not in bag_substitutions:
                bag_substitutions[p_code] = {}
            bag_substitutions[p_code][p1] = p2
            
    data['adjustments'] = {
        'additions': additions,
        'cancellations': cancellations,
        'substitutions': substitutions,
        'bag_substitutions': bag_substitutions
    }
    
    # 1. Forecast
    cur.execute("SELECT * FROM forecast;")
    fc_rows = cur.fetchall()
    forecast = []
    for r in fc_rows:
        # Bỏ qua column ID (r[0])
        forecast.append(ForecastItem(
            product_code=r[1], packing_size=r[2], die_size=r[3],
            dealer_higro=r[4], dealer_cp=r[5], dealer_star=r[6], dealer_nuvo=r[7], dealer_nasa=r[8], dealer_total=r[9],
            farm_swine=r[10], farm_integrate=r[11], farm_total=r[12],
            grand_total_tons=r[13], silo_tons=r[14], total_with_silo=r[15],
            bag_higro=r[16], bag_cp=r[17], bag_star=r[18], bag_nuvo=r[19], bag_nasa=r[20], bag_dealer_total=r[21],
            bag_farm=r[22], bag_grand_total=r[23],
            feed_code_higro=r[24], feed_code_cp=r[25], feed_code_star=r[26], feed_code_nuvo=r[27], feed_code_nasa=r[28], feed_code_farm=r[29]
        ))
    data['forecast'] = forecast

    # 2. Silo Plan
    cur.execute("SELECT day, product_code, tons FROM silo_plan;")
    sp_rows = cur.fetchall()
    silo_plan = {d: {} for d in range(1, 7)}
    for r in sp_rows:
        day, p, tons = r
        silo_plan[day][p] = tons
    data['silo_plan'] = silo_plan

    # 3. Ba Cang
    cur.execute("SELECT day, product_code, tons FROM bacang;")
    bc_rows = cur.fetchall()
    bacang = {d: {} for d in range(1, 7)}
    for r in bc_rows:
        day, p, tons = r
        bacang[day][p] = tons
    data['bacang'] = bacang

    # 4. FFStock
    cur.execute("SELECT product_code, stock_tons FROM ffstock;")
    ff_rows = cur.fetchall()
    ffstock = {}
    for r in ff_rows:
        p, tons = r
        ffstock[p] = tons
    data['ffstock'] = ffstock

    # 5. FFStock Details
    cur.execute("SELECT product_code, product_name, safety_stock_tons, daily_sales_tons, doh, warning FROM ffstock_details;")
    ffd_rows = cur.fetchall()
    ffstock_details = {}
    for r in ffd_rows:
        p, name, s_stock, d_sales, doh, warn = r
        ffstock_details[p] = {
            'product_code': p,
            'product_name': name,
            'stock_tons': s_stock,
            'sales_avg_kg': d_sales,
            'doh': doh,
            'warning': warn
        }
    data['ffstock_details'] = ffstock_details

    # 6. Tonbon
    cur.execute("SELECT product_code, stock_tons FROM tonbon;")
    tb_rows = cur.fetchall()
    tonbon = {}
    for r in tb_rows:
        p, tons = r
        tonbon[p] = tons
    data['tonbon'] = tonbon

    # 7. Tonbon Detail
    cur.execute("SELECT bon_id, product_code, tons FROM tonbon_detail;")
    tbd_rows = cur.fetchall()
    tonbon_detail = {}
    for r in tbd_rows:
        b_id, p, tons = r
        tonbon_detail[b_id] = {
            'bon_id': b_id,
            'product_code': p,
            'tons': tons
        }
    data['tonbon_detail'] = tonbon_detail

    # 8. Empty Bag
    cur.execute("SELECT product_code, brand, bags FROM empty_bag;")
    eb_rows = cur.fetchall()
    empty_bag = {}
    for r in eb_rows:
        p, b, qty = r
        if p not in empty_bag:
            empty_bag[p] = {}
        empty_bag[p][b] = qty
    data['empty_bag'] = empty_bag

    # 9. Congsuat
    cur.execute("SELECT product_code, formular_code, die_size, ton_per_batch, line_cv, line_pk, ks_code FROM congsuat;")
    cs_rows = cur.fetchall()
    congsuat = {}
    for r in cs_rows:
        p, f_code, d_size, tpb, l_cv, l_pk, ks = r
        congsuat[p] = ProductSpec(
            product_code=p, formular_code=f_code, die_size=d_size,
            ton_per_batch=tpb, line_cv=l_cv, line_pk=l_pk, ks_code=ks
        )
    data['congsuat'] = congsuat

    # 10. STT Khangsinh
    cur.execute("SELECT ks_level, ks_name FROM stt_khangsinh;")
    stt_ks_rows = cur.fetchall()
    stt_khangsinh = {}
    for r in stt_ks_rows:
        lvl, name = r
        stt_khangsinh[lvl] = name
    data['stt_khangsinh'] = stt_khangsinh

    # 11. Fix Code Pellet
    cur.execute("SELECT product_code, packing_size, die_size, default_line, priority_1, priority_2, priority_3, priority_4, priority_5 FROM fix_code_pellet;")
    fcp_rows = cur.fetchall()
    fix_code_pellet = {}
    for r in fcp_rows:
        p, pack, d_size, d_line, p1, p2, p3, p4, p5 = r
        pr = [p1, p2, p3, p4, p5]
        pr = [x for x in pr if x]
        fix_code_pellet[p] = {
            'product_code': p,
            'packing_size': pack,
            'die_size': d_size,
            'default_line': d_line,
            'priorities': pr
        }
    data['fix_code_pellet'] = fix_code_pellet

    # 12. Feedcode
    cur.execute("SELECT product_code, line_cv, line_pk FROM feedcode;")
    fc_rows = cur.fetchall()
    feedcode = {}
    for r in fc_rows:
        p, l_cv, l_pk = r
        feedcode[p] = {
            'line_cv': l_cv,
            'line_pk': l_pk
        }
    data['feedcode'] = feedcode

    # 13. Khangsinh
    cur.execute("SELECT product_code, ks_code, ks_level FROM khangsinh;")
    ks_rows = cur.fetchall()
    khangsinh = {}
    for r in ks_rows:
        p, ks, lvl = r
        khangsinh[p] = {
            'ks_code': ks,
            'ks_level': lvl
        }
    data['khangsinh'] = khangsinh

    # 14. KHSX Yesterday
    cur.execute("SELECT product_code, planned, actual FROM khsx_yesterday;")
    yest_rows = cur.fetchall()
    khsx_yesterday = {}
    for r in yest_rows:
        p, pl, act = r
        khsx_yesterday[p] = {
            'planned': pl,
            'actual': act
        }
    data['khsx_yesterday'] = khsx_yesterday

    cur.close()
    conn.close()
    
    print("✅ Đã nạp thành công dữ liệu đầu vào từ PostgreSQL (Neon Tech)!")
    return data


def save_plan_output_to_db(date_str, filename, khpl_raw_grid, sequence, packaging, summary, conn_str=DB_URI):
    """Lưu trữ lịch sử kết quả kế hoạch sản xuất đầu ra xuống Neon Tech"""
    import json
    from datetime import datetime, date, time
    
    class DateTimeEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (datetime, date, time)):
                return obj.isoformat()
            return super().default(obj)
            
    try:
        conn = get_connection(conn_str)
        cur = conn.cursor()
        
        cur.execute("""
        INSERT INTO plan_outputs (date_str, filename, khpl_raw_grid, sequence, packaging, summary, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        ON CONFLICT (date_str) DO UPDATE SET
            filename = EXCLUDED.filename,
            khpl_raw_grid = EXCLUDED.khpl_raw_grid,
            sequence = EXCLUDED.sequence,
            packaging = EXCLUDED.packaging,
            summary = EXCLUDED.summary,
            created_at = CURRENT_TIMESTAMP;
        """, (
            date_str, filename, 
            json.dumps(khpl_raw_grid, cls=DateTimeEncoder), 
            json.dumps(sequence, cls=DateTimeEncoder), 
            json.dumps(packaging, cls=DateTimeEncoder), 
            json.dumps(summary, cls=DateTimeEncoder)
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ Đã lưu trữ kế hoạch ngày {date_str} thành công lên PostgreSQL Cloud!")
        return True
    except Exception as e:
        print(f"⚠️ Lỗi lưu trữ kế hoạch sản xuất lên database: {e}")
        return False


def get_plan_output_from_db(date_str, conn_str=DB_URI):
    """Tải lịch sử kết quả kế hoạch sản xuất đầu ra trực tiếp từ PostgreSQL"""
    try:
        conn = get_connection(conn_str)
        cur = conn.cursor()
        
        cur.execute("SELECT filename, khpl_raw_grid, sequence, packaging, summary FROM plan_outputs WHERE date_str = %s;", (date_str,))
        row = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if row:
            return {
                'exists': True,
                'filename': row[0],
                'khpl_raw_grid': row[1],
                'sequence': row[2],
                'packaging': row[3],
                'summary': row[4]
            }
        return {'exists': False}
    except Exception as e:
        print(f"⚠️ Lỗi khi đọc kết quả kế hoạch từ database: {e}")
        return {'exists': False}


def sync_category_to_db(config, category, conn_str=DB_URI) -> dict:
    """
    Đồng bộ và cập nhật CHỈ RIÊNG 1 danh mục dữ liệu từ SharePoint -> Excel -> PostgreSQL.
    Tối ưu hóa tốc độ tải và xử lý, bỏ qua các danh mục khác.
    """
    import os
    import datetime
    import data_loader
    
    print(f"\n⚡ Bắt đầu đồng bộ danh mục: {category.upper()} từ SharePoint lên Neon Tech Cloud...")
    
    # 1. Xác định URL SharePoint và đường dẫn file cục bộ tương ứng
    url = ""
    local_path = ""
    
    if category == 'forecast':
        url = getattr(config, 'SHAREPOINT_FORECAST_URL', '')
        local_path = os.path.join(config.FORECAST_DIR, 'SharePoint_Forecast.xlsx')
    elif category == 'silo_plan':
        url = getattr(config, 'SHAREPOINT_SILO_URL', '')
        local_path = os.path.join(config.SILO_DIR, 'SharePoint_Silo.xlsx')
    elif category == 'bacang':
        url = getattr(config, 'SHAREPOINT_BACANG_URL', '')
        local_path = os.path.join(config.BACANG_DIR, 'SharePoint_BaCang.xlsx')
    elif category == 'ffstock':
        url = getattr(config, 'SHAREPOINT_FFSTOCK_URL', '')
        ffstock_dir = getattr(config, 'FSTOCK_DIR_FFSTOCK', config.FSTOCK_DIR)
        local_path = os.path.join(ffstock_dir, 'SharePoint_FFStock.xlsx')
    elif category == 'empty_bag':
        url = getattr(config, 'SHAREPOINT_EMPTY_BAG_URL', '')
        bag_dir = getattr(config, 'FSTOCK_DIR_EMPTYBAG', config.FSTOCK_DIR)
        local_path = os.path.join(bag_dir, 'SharePoint_EmptyBag.xlsx')
    elif category == 'tonbon':
        url = getattr(config, 'SHAREPOINT_TONBON_URL', '')
        local_path = os.path.join(config.TONBON_DIR, 'SharePoint_TonBon.xlsx')
    
    if not url:
        # Nếu không có SharePoint URL, kiểm tra xem có file cục bộ tương ứng không để nạp trực tiếp
        print(f"ℹ️ Không tìm thấy link SharePoint cho {category}, sử dụng file local hiện tại...")
        # Lấy file local tương ứng
        if category == 'forecast':
            info = data_loader.get_file_info(config.FORECAST_DIR, '*FORECAST*.xlsx')
        elif category == 'silo_plan':
            info = data_loader.get_file_info(config.SILO_DIR, '*SILO*.xlsx')
        elif category == 'bacang':
            info = data_loader.get_file_info(config.BACANG_DIR, '*CANG*.xlsx')
        elif category == 'ffstock':
            ffstock_dir = getattr(config, 'FSTOCK_DIR_FFSTOCK', config.FSTOCK_DIR)
            info = data_loader.get_file_info(ffstock_dir, '*FFSTOCK*.xls*')
        elif category == 'empty_bag':
            bag_dir = getattr(config, 'FSTOCK_DIR_EMPTYBAG', config.FSTOCK_DIR)
            info = data_loader.get_file_info(bag_dir, '*EMPTY BAG*.xls*')
        elif category == 'tonbon':
            info = data_loader.get_file_info(config.TONBON_DIR, '*ton bon*.*')
        else:
            info = {'exists': False}
            
        if not info['exists']:
            raise Exception(f"Không tìm thấy nguồn tệp dữ liệu nào cho {category}")
        local_path = info['path']
    else:
        # Tải từ SharePoint
        success = data_loader.download_sharepoint_file(url, local_path)
        if not success:
            raise Exception(f"Tải tệp từ SharePoint thất bại cho {category}")
            
    # 2. Đọc dữ liệu từ file Excel
    conn = get_connection(conn_str)
    cur = conn.cursor()
    
    try:
        if category == 'forecast':
            items = data_loader.load_forecast(local_path)
            # Clear & Insert
            cur.execute("TRUNCATE TABLE forecast;")
            fc_data = []
            for it in items:
                fc_data.append((
                    it.product_code, it.packing_size, it.die_size,
                    it.dealer_higro, it.dealer_cp, it.dealer_star, it.dealer_nuvo, it.dealer_nasa, it.dealer_total,
                    it.farm_swine, it.farm_integrate, it.farm_total,
                    it.grand_total_tons, it.silo_tons, it.total_with_silo,
                    it.bag_higro, it.bag_cp, it.bag_star, it.bag_nuvo, it.bag_nasa, it.bag_dealer_total,
                    it.bag_farm, it.bag_grand_total,
                    it.feed_code_higro, it.feed_code_cp, it.feed_code_star, it.feed_code_nuvo, it.feed_code_nasa, it.feed_code_farm
                ))
            if fc_data:
                execute_values(cur, """
                INSERT INTO forecast (
                    product_code, packing_size, die_size,
                    dealer_higro, dealer_cp, dealer_star, dealer_nuvo, dealer_nasa, dealer_total,
                    farm_swine, farm_integrate, farm_total,
                    grand_total_tons, silo_tons, total_with_silo,
                    bag_higro, bag_cp, bag_star, bag_nuvo, bag_nasa, bag_dealer_total,
                    bag_farm, bag_grand_total,
                    feed_code_higro, feed_code_cp, feed_code_star, feed_code_nuvo, feed_code_nasa, feed_code_farm
                ) VALUES %s
                """, fc_data)
                
        elif category == 'silo_plan':
            silo_plan = data_loader.load_silo_plan(local_path)
            cur.execute("TRUNCATE TABLE silo_plan;")
            sp_data = []
            for day, products in silo_plan.items():
                for p, tons in products.items():
                    sp_data.append((day, p, tons))
            if sp_data:
                execute_values(cur, "INSERT INTO silo_plan (day, product_code, tons) VALUES %s", sp_data)
                
        elif category == 'bacang':
            bacang = data_loader.load_bacang(local_path)
            cur.execute("TRUNCATE TABLE bacang;")
            bc_data = []
            for day, products in bacang.items():
                for p, tons in products.items():
                    bc_data.append((day, p, tons))
            if bc_data:
                execute_values(cur, "INSERT INTO bacang (day, product_code, tons) VALUES %s", bc_data)
                
        elif category == 'ffstock':
            ffstock = data_loader.load_ffstock(local_path)
            details = data_loader.load_ffstock_details(local_path)
            
            cur.execute("TRUNCATE TABLE ffstock;")
            cur.execute("TRUNCATE TABLE ffstock_details;")
            
            ff_data = [(p, tons) for p, tons in ffstock.items()]
            if ff_data:
                execute_values(cur, "INSERT INTO ffstock (product_code, stock_tons) VALUES %s", ff_data)
                
            ffd_data = []
            for p, det in details.items():
                ffd_data.append((
                    p, det.get('product_name', ''), det.get('stock_tons', 0.0),
                    det.get('sales_avg_kg', 0.0), det.get('doh', None), det.get('warning', '')
                ))
            if ffd_data:
                execute_values(cur, """
                INSERT INTO ffstock_details (
                    product_code, product_name, safety_stock_tons, daily_sales_tons, doh, warning
                ) VALUES %s
                """, ffd_data)
                
        elif category == 'empty_bag':
            empty_bag = data_loader.load_empty_bag(local_path)
            cur.execute("TRUNCATE TABLE empty_bag;")
            eb_data = []
            for p, brands in empty_bag.items():
                for b, qty in brands.items():
                    eb_data.append((p, b, qty))
            if eb_data:
                execute_values(cur, "INSERT INTO empty_bag (product_code, brand, bags) VALUES %s", eb_data)
                
        elif category == 'tonbon':
            tonbon = data_loader.load_tonbon(local_path)
            tonbon_detail = data_loader.load_tonbon_detail(local_path)
            
            cur.execute("TRUNCATE TABLE tonbon;")
            cur.execute("TRUNCATE TABLE tonbon_detail;")
            
            tb_data = [(p, tons) for p, tons in tonbon.items()]
            if tb_data:
                execute_values(cur, "INSERT INTO tonbon (product_code, stock_tons) VALUES %s", tb_data)
                
            tbd_data = []
            for b_id, item in tonbon_detail.items():
                tbd_data.append((b_id, item.get('product', item.get('product_code', '')), item.get('tons', 0.0)))
            if tbd_data:
                execute_values(cur, "INSERT INTO tonbon_detail (bon_id, product_code, tons) VALUES %s", tbd_data)
                
        conn.commit()
        print(f"🎉 Đồng bộ danh mục {category.upper()} thành công lên Neon Tech Cloud Database!")
        return {
            'success': True,
            'filename': os.path.basename(local_path),
            'last_modified': datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        }
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()
