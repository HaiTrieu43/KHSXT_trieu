"""
pellet_planner.py - Phân hệ Lập Kế Hoạch Pellet (PL) chi tiết theo Ca
C.P. Vietnam - Chi nhánh Bình Dương
"""
import os
import sys
from models import DemandItem, Priority

# Định nghĩa các hằng số hao hụt thời gian
STARTUP_TIME = 5 / 60.0      # 5 phút khởi động máy pellet (giờ)
CHANGEOVER_TIME = 15 / 60.0  # 15 phút chuyển cám không thay khuôn (giờ)

# Hao hụt thay khuôn (C.DIE) theo từng máy (giờ)
DIE_CHANGE_TIME = {
    'PL1': 30 / 60.0,
    'PL2': 90 / 60.0,
    'PL3': 90 / 60.0,
    'PL4': 90 / 60.0,
    'PL5': 45 / 60.0,
    'PL6': 45 / 60.0,
    'PL7': 45 / 60.0
}

# Ánh xạ bồn bán thành phẩm tới các máy PL
SILO_MAPPING = {
    'PL1': [96, 98],
    'PL2': [93, 94, 95],
    'PL3': [91, 92, 97],
    'PL4': [86, 87, 88],
    'PL5': [89, 90],
    'PL6': [129, 130],
    'PL7': [129, 130]
}


def get_die_size(product_code, congsuat_dict, fix_code_pellet_dict):
    """
    Lấy kích thước khuôn (die size) của sản phẩm.
    Tra cứu từ bảng _die_mapping trong fix_code_pellet_dict (Bảng 2 của Fix code pellet).
    Fallback về congsuat_dict.die_size nếu không tìm thấy.
    """
    p_code = str(product_code).strip().upper().replace(' ', '')
    
    # 1. Tra trong _die_mapping (source of truth từ Fix code pellet Bảng 2)
    die_mapping = fix_code_pellet_dict.get('_die_mapping', {})
    
    # Thử khớp chính xác
    if p_code in die_mapping:
        ds = die_mapping[p_code].get('die_size', 0)
        if ds > 0:
            return ds
    
    # Thử khớp gần đúng (loại bỏ hậu tố FS, S, F, ...)
    for name in sorted(die_mapping.keys(), key=len, reverse=True):
        name_norm = name.replace(' ', '')
        if p_code.startswith(name_norm) and len(name_norm) >= 3:
            ds = die_mapping[name_norm].get('die_size', 0)
            if ds > 0:
                return ds
    
    # 2. Fallback: tra trong congsuat_dict
    if p_code in congsuat_dict:
        spec = congsuat_dict[p_code]
        if hasattr(spec, 'die_size') and spec.die_size > 0:
            return spec.die_size
    
    # 3. Fallback mặc định = 4.0mm (die phổ biến nhất)
    return 4.0


def get_tph(product_code, line_cv, congsuat_dict, fix_code_pellet_dict):
    """
    Lấy năng suất Tấn/Giờ (T/h) của sản phẩm trên máy cụ thể.
    """
    p_code = str(product_code).strip().upper()
    line = str(line_cv).strip().upper()
    
    # 1. Thử tra trong fix_code_pellet từ Plan.xlsm
    # Tìm config phù hợp với product_code
    for key, cfg in fix_code_pellet_dict.items():
        if key.startswith(p_code):
            # Kiểm tra nếu máy này có trong priorities và có tph tương ứng
            if line in cfg.get('priorities', []):
                idx = cfg['priorities'].index(line)
                # Đôi khi bảng fix_code_pellet chứa tph tương ứng cho từng ưu tiên
                tph_list = cfg.get('tph_list', [])
                if idx < len(tph_list) and tph_list[idx] > 0:
                    return tph_list[idx]
            
            # Kiểm tra default_line
            if cfg.get('default_line') == line and cfg.get('default_tph', 0) > 0:
                return cfg['default_tph']
                
    # 2. Thử tra trong bảng công suất chung (congsuat_dict)
    if p_code in congsuat_dict:
        spec = congsuat_dict[p_code]
        # Nếu dòng khớp với mặc định và có tph
        if spec.line_cv == line and hasattr(spec, 'tph') and spec.tph > 0:
            return spec.tph
            
    # 3. Fallback mặc định theo máy
    default_machine_tph = {
        'PL1': 13.0, 'PL2': 25.0, 'PL3': 20.0, 'PL4': 22.0,
        'PL5': 10.0, 'PL6': 5.0, 'PL7': 5.0
    }
    return default_machine_tph.get(line, 15.0)


def plan_pellet_shifts(demand_list, tonbon_detail, congsuat_dict, fix_code_pellet_dict, khangsinh_dict, target_date, feedcode_dict=None, code_mapping=None):
    """
    Thuật toán chính lập kế hoạch Pellet chi tiết theo ca và Mixer cám bột.
    """
    print("\n" + "="*50)
    print("🔮 BẮT ĐẦU LẬP KẾ HOẠCH PELLET CHI TIẾT THEO CA")
    print("="*50)
    
    # Xây dựng bản đồ quy đổi mã SAP thành tên cám dân dã từ FEEDCODE và code_mapping
    sap_to_colloquial = {}
    if code_mapping:
        for raw_code, colloquial_name in code_mapping.items():
            if raw_code and colloquial_name:
                sap_to_colloquial[str(raw_code).strip().upper()] = str(colloquial_name).strip().upper()
    if feedcode_dict:
        for colloquial_name, info in feedcode_dict.items():
            raw_code = info.get('feed_code')
            if raw_code:
                sap_to_colloquial[str(raw_code).strip().upper()] = str(colloquial_name).strip().upper()
    # Bổ sung từ congsuat_dict (đảm bảo mọi digit_code→colloquial_name đều có)
    if congsuat_dict:
        for key, spec in congsuat_dict.items():
            if hasattr(spec, 'product_code') and hasattr(spec, 'product_name'):
                pc = str(spec.product_code).strip().upper()
                pn = str(spec.product_name).strip().upper()
                if pc and pn and pc != pn:
                    sap_to_colloquial[pc] = pn  # congsuat override Code sheet

                
    def _translate_sap_code(raw_code):
        if not raw_code:
            return ''
        c = str(raw_code).strip().upper().replace(' ', '')
        
        # 1. Khớp chính xác
        if c in sap_to_colloquial:
            return sap_to_colloquial[c]
            
        # 2. Loại bỏ đuôi .0 nếu Excel đọc dạng float
        if c.endswith('.0'):
            c_no_dot = c[:-2]
            if c_no_dot in sap_to_colloquial:
                return sap_to_colloquial[c_no_dot]
                
        # 3. Khớp gần đúng (loại bỏ hậu tố chữ cái hoặc tìm tiền tố tương đương)
        for sap, colloquial in sap_to_colloquial.items():
            if c.startswith(sap) or sap.startswith(c):
                return colloquial
                
        # 4. Quy tắc tiền tố hệ thống mặc định của nhà máy (fallback từ demand_calculator)
        if c.startswith('96') and len(c) >= 4:
            return '5' + c[2:]
        if c.startswith('94') and len(c) >= 4:
            return '3' + c[2:]
        if c.startswith('9') and len(c) == 3:
            return '5' + c[1:]
        if c.startswith('8') and len(c) == 3:
            return '3' + c[1:]
            
        return c

    # 1. Tách riêng cám bột (Mash Feed) và cám viên (Pellet)
    pellet_demands = []
    mash_demands = []
    
    for item in demand_list:
        line = str(item.line_cv).strip().upper()
        if line == 'M' or line == 'MASH' or not line:
            mash_demands.append(item)
        else:
            pellet_demands.append(item)
            
    print(f"  📝 Phân loại: {len(pellet_demands)} cám viên (PL), {len(mash_demands)} cám bột (Mash)")
    
    # 2. Xác định Tồn Đầu (Carry-over) của các máy từ Báo cáo tồn bồn
    ton_dau_by_machine = {f"PL{i}": [] for i in range(1, 8)}
    
    # Duyệt qua các bồn để phân bổ tồn đầu cho máy PL tương ứng
    # Đối với PL6 & PL7 dùng chung bồn 129 và 130
    pl6_7_silos = {}
    for silo_num_key, data_item in tonbon_detail.items():
        try:
            silo_num = int(silo_num_key)
        except (ValueError, TypeError):
            continue
        prod_raw = data_item.get('product', data_item.get('product_code', ''))
        prod = _translate_sap_code(prod_raw)
        tons = data_item['tons']
        if silo_num in (129, 130):
            pl6_7_silos[silo_num] = {'product': prod, 'tons': tons}
            continue
            
        # Ánh xạ bồn khác tới PL1-PL5
        for machine, silos in SILO_MAPPING.items():
            if machine not in ('PL6', 'PL7') and silo_num in silos:
                ton_dau_by_machine[machine].append({
                    'product_code': prod,
                    'tons': tons,
                    'silo': silo_num
                })
                
    # Phân bổ tối ưu bồn 129, 130 cho PL6 và PL7
    # Nếu bồn 129 có cám, ưu tiên xếp cho PL6 làm tồn đầu
    if 129 in pl6_7_silos:
        ton_dau_by_machine['PL6'].append({
            'product_code': pl6_7_silos[129]['product'],
            'tons': pl6_7_silos[129]['tons'],
            'silo': 129
        })
    # Nếu bồn 130 có cám, ưu tiên xếp cho PL7 làm tồn đầu
    if 130 in pl6_7_silos:
        ton_dau_by_machine['PL7'].append({
            'product_code': pl6_7_silos[130]['product'],
            'tons': pl6_7_silos[130]['tons'],
            'silo': 130
        })
        
    for m, items in ton_dau_by_machine.items():
        if items:
            for item in items:
                print(f"  📥 TỒN ĐẦU {m}: Cám {item['product_code']} - Bồn {item['silo']} ({item['tons']:.2f} tấn)")
                
    # 3. Phân bổ nhu cầu sản xuất ngày hôm nay vào các máy
    machine_jobs = {f"PL{i}": [] for i in range(1, 8)}
    
    # Gán các sản phẩm Pellet vào các máy tương ứng theo thuộc tính line_cv
    for item in pellet_demands:
        line = str(item.line_cv).strip().upper()
        if line in machine_jobs:
            machine_jobs[line].append(item)
            
    # 4. Kiểm tra tải và thực hiện "Đá cám" tự động khi tổng thời gian vượt quá 22 giờ
    # Định nghĩa cấu hình để đá cám chéo
    def calculate_machine_time(machine, jobs, ton_daus):
        total_time = 0.0
        
        # 1. Thời gian tồn đầu (nếu có chạy tiếp)
        current_die = None
        
        # Lấy die_size cuối cùng từ tồn đầu
        if ton_daus:
            for td in ton_daus:
                current_die = get_die_size(td['product_code'], congsuat_dict, fix_code_pellet_dict)
                tph = get_tph(td['product_code'], machine, congsuat_dict, fix_code_pellet_dict)
                total_time += td['tons'] / tph
                total_time += CHANGEOVER_TIME  # cộng hao hụt chuyển cám
        
        # 2. Thời gian chạy các job trong ngày
        is_first = True
        for job in jobs:
            die_size = get_die_size(job.product_code, congsuat_dict, fix_code_pellet_dict)
            
            # Thời gian khởi động máy pellet đầu ngày
            if is_first and not ton_daus:
                total_time += STARTUP_TIME
                is_first = False
                
            # Đổi khuôn (C.DIE) nếu die_size thay đổi
            if current_die is not None and current_die != die_size:
                total_time += DIE_CHANGE_TIME.get(machine, 0.75)
            # Chuyển cám không thay khuôn nếu sản phẩm khác
            elif current_die is not None:
                total_time += CHANGEOVER_TIME
                
            tph = get_tph(job.product_code, machine, congsuat_dict, fix_code_pellet_dict)
            run_hours = job.tons / tph
            total_time += run_hours
            
            current_die = die_size
            
        return total_time

    # Thuật toán đá cám vòng lặp cân bằng tải
    print("\n⚖️ Đang kiểm tra cân bằng tải và đá cám chéo tự động...")
    has_moved = True
    iteration = 0
    
    while has_moved and iteration < 5:
        has_moved = False
        iteration += 1
        
        # Sắp xếp các máy theo tổng giờ chạy giảm dần
        loads = {}
        for m in machine_jobs.keys():
            loads[m] = calculate_machine_time(m, machine_jobs[m], ton_dau_by_machine[m])
            
        # Tìm máy quá tải (> 22 giờ)
        overloaded_machines = [m for m, hours in loads.items() if hours > 22.0]
        if not overloaded_machines:
            break
            
        # Ưu tiên giải quyết máy quá tải nhất
        overloaded_machines.sort(key=lambda x: loads[x], reverse=True)
        m_from = overloaded_machines[0]
        
        # Thử chuyển 1 job của máy m_from sang máy khác có giờ chạy thấp
        jobs = machine_jobs[m_from]
        if not jobs:
            continue
            
        # Lựa chọn job có mức độ ưu tiên thấp nhất (FORECAST hoặc URGENT_STOCKOUT) để chuyển
        jobs_candidates = [j for j in jobs if j.priority in (Priority.FORECAST, Priority.URGENT_STOCKOUT, Priority.SHORTFALL)]
        if not jobs_candidates:
            # Nếu không có job thường, thử cả job vãng lai
            jobs_candidates = [j for j in jobs if j.priority == Priority.WALKIN]
            
        if not jobs_candidates:
            continue
            
        # Sắp xếp job có dung lượng lớn để chuyển hiệu quả nhất
        jobs_candidates.sort(key=lambda x: x.tons, reverse=True)
        job_to_move = jobs_candidates[0]
        
        # Tìm xem máy nào khác chạy được sản phẩm này
        p_code = job_to_move.product_code
        compatible_machines = []
        
        # Lấy danh sách máy từ fix_code_pellet
        for key, cfg in fix_code_pellet_dict.items():
            if key.startswith(p_code):
                for p_line in cfg.get('priorities', []):
                    norm_line = str(p_line).strip().upper()
                    if norm_line.isdigit():
                        norm_line = f"PL{norm_line}"
                    if norm_line != m_from and norm_line in machine_jobs:
                        compatible_machines.append(norm_line)
                if cfg.get('default_line'):
                    def_line = str(cfg['default_line']).strip().upper()
                    if def_line.isdigit():
                        def_line = f"PL{def_line}"
                    if def_line != m_from and def_line in machine_jobs and def_line not in compatible_machines:
                        compatible_machines.append(def_line)
                        
        # Fallback các máy PL2, PL3, PL4 thường xuyên chạy chéo cho nhau
        if m_from in ('PL2', 'PL3', 'PL4'):
            for fall_m in ('PL2', 'PL3', 'PL4'):
                if fall_m != m_from and fall_m not in compatible_machines:
                    compatible_machines.append(fall_m)
                    
        # Loại trừ PL2 cho 566 và 567S cưỡng chế
        if p_code.startswith('566') or p_code.startswith('567S'):
            compatible_machines = [m for m in compatible_machines if m != 'PL2']
            
        # Lọc các máy Y còn khả dụng (< 22 giờ)
        candidates = []
        for m_to in compatible_machines:
            h_to = loads[m_to]
            # Tính thử giờ chạy nếu thêm job
            tph_to = get_tph(p_code, m_to, congsuat_dict, fix_code_pellet_dict)
            added_hours = job_to_move.tons / tph_to
            if h_to + added_hours < 22.0:
                candidates.append((m_to, h_to + added_hours))
                
        if candidates:
            # Chọn máy có thời gian chạy dự kiến thấp nhất sau khi thêm job
            candidates.sort(key=lambda x: x[1])
            m_to_best = candidates[0][0]
            
            # Thực hiện đá cám chéo!
            machine_jobs[m_from].remove(job_to_move)
            job_to_move.line_cv = m_to_best
            machine_jobs[m_to_best].append(job_to_move)
            
            print(f"  🔀 ĐÁ CÁM: Chuyển {job_to_move.product_code} ({job_to_move.tons:.1f}T) từ {m_from} ({loads[m_from]:.2f}h) "
                  f"sang máy {m_to_best} ({loads[m_to_best]:.2f}h) thành công!")
            has_moved = True

    # 5. Phân ca (Ca 1, Ca 2, Ca 3) và Sắp xếp sinh học (Kháng sinh tăng dần)
    final_pl_plan = {f"PL{i}": [] for i in range(1, 8)}
    loss_by_machine = {f"PL{i}": 0.0 for i in range(1, 8)}
    
    print("\n🧬 Sắp xếp an toàn sinh học kháng sinh và chia 3 ca cho từng máy Pellet...")
    
    for m in machine_jobs.keys():
        jobs = machine_jobs[m]
        ton_daus = ton_dau_by_machine[m]
        
        # Sắp xếp các job trong ngày theo quy tắc tối ưu (từ kinh nghiệm Mixer):
        # 1. Cám Silo ưu tiên lên trước (xe bồn đang chờ)
        # 2. GOM CÙNG DIE SIZE chạy liên tiếp (giảm C.DIE - loss lớn nhất)
        # 3. Trong cùng die → sắp xếp kháng sinh tăng dần (sạch → bẩn)
        # 4. Trong cùng KS level → tons lớn chạy trước để ổn định máy
        from data_loader import resolve_antibiotic_for_product
        from config import DEFAULT_TON_PER_BATCH
        
        # Tính toán cấp độ kháng sinh và die_size cho mỗi job
        for j in jobs:
            ks_code, ks_level = resolve_antibiotic_for_product(j.product_code, khangsinh_dict)
            j.ks_level = ks_level
            j._die_size = get_die_size(j.product_code, congsuat_dict, fix_code_pellet_dict)
        
        # Xác định die_size của tồn đầu để ưu tiên chạy cùng die trước
        carryover_die = None
        if ton_daus:
            carryover_die = get_die_size(ton_daus[0]['product_code'], congsuat_dict, fix_code_pellet_dict)
            
        jobs.sort(key=lambda x: (
            0 if (x.packing_size == 'SILO' or x.silo_truck) else 1,
            # Ưu tiên sản phẩm cùng die với tồn đầu (không cần thay khuôn)
            0 if (carryover_die and x._die_size == carryover_die) else 1,
            x._die_size,       # Gom cùng die size liên tiếp
            x.ks_level,        # Trong cùng die → sạch trước bẩn sau
            -x.tons            # Volume lớn trước
        ))
        
        # Tạo chuỗi chạy hoàn chỉnh bắt đầu bằng Tồn Đầu
        all_runs = []
        
        # Thêm Tồn Đầu vào đầu ngày
        if ton_daus:
            for td in ton_daus:
                die_size = get_die_size(td['product_code'], congsuat_dict, fix_code_pellet_dict)
                all_runs.append({
                    'product_code': td['product_code'],
                    'tons': td['tons'],
                    'batches': max(1, int(td['tons'] / 8.4)),
                    'is_carryover': True,
                    'die_size': die_size
                })
                
        # Thêm các job trong ngày
        for j in jobs:
            die_size = get_die_size(j.product_code, congsuat_dict, fix_code_pellet_dict)
            all_runs.append({
                'product_code': j.product_code,
                'tons': j.tons,
                'batches': j.batches,
                'is_carryover': False,
                'die_size': die_size
            })
            
        # Chia Ca thực tế dựa trên thời gian chạy cộng dồn
        accumulated_time = 0.0
        current_die = None
        is_first = True
        
        for run in all_runs:
            run_time = 0.0
            die_size = run['die_size']
            
            # Phí khởi động máy pellet đầu ngày
            if is_first and not ton_daus:
                run_time += STARTUP_TIME
                is_first = False
                
            # Đổi khuôn (C.DIE)
            change_type = None
            if current_die is not None and current_die != die_size:
                c_time = DIE_CHANGE_TIME.get(m, 0.75)
                run_time += c_time
                loss_by_machine[m] += c_time
                change_type = 'C.DIE'
            # Chuyển cám không đổi khuôn
            elif current_die is not None:
                run_time += CHANGEOVER_TIME
                loss_by_machine[m] += CHANGEOVER_TIME
                change_type = 'LOSS'
                
            tph = get_tph(run['product_code'], m, congsuat_dict, fix_code_pellet_dict)
            run_hours = run['tons'] / tph
            run_time += run_hours
            
            # Gán ca dựa trên thời gian cộng dồn (Ca 1: 0-8h, Ca 2: 8-16h, Ca 3: 16-24h)
            start_hour = accumulated_time
            end_hour = accumulated_time + run_time
            
            # Quyết định Ca chạy chính
            if start_hour < 8.0:
                shift_name = 'CA 1'
            elif start_hour < 16.0:
                shift_name = 'CA 2'
            else:
                shift_name = 'CA 3'
                
            # Tạo các bản ghi kế hoạch
            final_pl_plan[m].append({
                'product_code': run['product_code'],
                'tons': run['tons'],
                'batches': run['batches'],
                'hours': run_hours,
                'total_hours': run_time,
                'shift': shift_name,
                'change_type': change_type,
                'is_carryover': run['is_carryover'],
                'start_hour': start_hour,
                'end_hour': end_hour
            })
            
            accumulated_time = end_hour
            current_die = die_size
            
    print("  ✅ Đã phân chia ca và sắp xếp sinh học hoàn tất.")
    
    # 6. Trả về kết quả phân bổ Pellet và Cám bột đóng bao
    return {
        'pellet_plan': final_pl_plan,
        'mash_plan': mash_demands,
        'loss_by_machine': loss_by_machine,
        'ton_dau_by_machine': ton_dau_by_machine
    }
