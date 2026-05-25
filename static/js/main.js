/* ==========================================================================
   MAIN.JS - FRONTEND BUSINESS LOGIC & INTERACTION ENGINE
   C.P. VIETNAM - CHI NHÁNH BÌNH DƯƠNG
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide Icons
    lucide.createIcons();

    // ----------------------------------------------------------------------
    // 1. STATE & GLOBAL CONFIGURATION
    // ----------------------------------------------------------------------
    const state = {
        currentView: 'dashboard',
        activeCategory: null,
        dataSourcesStatus: {},
        
        // Data Details Table Pagination & Filtering State
        tableData: [],
        filteredData: [],
        currentPage: 1,
        rowsPerPage: 50,
        
        // Walkin Orders State
        walkinOrders: [],
        
        // Adjustments Editing State
        adjustments: {
            additions: [],
            cancellations: [],
            substitutions: [],
            bag_substitutions: []
        }
    };

    // Human-friendly mapping of categories to display titles
    const categoryInfo = {
        'forecast': { title: 'Dự Báo Bán Hàng (Forecast)', filename: 'SALES_FORECAST.xlsx' },
        'silo_plan': { title: 'Kế Hoạch Xuất Bồn Silo', filename: 'KE_HOACH_SILO.xlsx' },
        'bacang': { title: 'Kế Hoạch Silo Bá Căng', filename: 'KE_HOACH_CANG.xlsx' },
        'ffstock': { title: 'Stock Đầu Ngày', filename: 'FFSTOCK.xlsx', subtitle: 'Stock(N) = StockOld(N-2) + Packing(N-1) - Sale(N-1)' },
        'tonbon': { title: 'Tồn Bồn Đóng Bao (Batching)', filename: 'TON_BON.xlsx' },
        'empty_bag': { title: 'Tồn Kho Bao Bì Rỗng (Empty Bag)', filename: 'EMPTY_BAG.xlsx' },
        'congsuat': { title: 'Bảng Công Suất & Cấu Hình Specs', filename: 'Plan.xlsm' },
        'feedcode': { title: 'Bản Đồ Định Biên Máy Đóng Bao', filename: 'KHSX THANG 5-20261.xlsm' },
        'khangsinh': { title: 'Cấu Hình Kháng Sinh Theo Cám', filename: 'KHSX THANG 5-20261.xlsm' },
        'yesterday_plan': { title: 'Kế Hoạch & Thực Tế Ngày Hôm Qua', filename: 'KHSX THANG 5-20261.xlsm' },
        'adjustments': { title: 'Bảng Cấu Hình Điều Chỉnh Nhanh KHSX', filename: 'DIEU_CHINH_NHANH.xlsx' }
    };

    // ----------------------------------------------------------------------
    // 2. DOM ELEMENTS CACHE
    // ----------------------------------------------------------------------
    const elements = {
        sidebarItems: document.querySelectorAll('.nav-item'),
        viewPanels: document.querySelectorAll('.view-panel'),
        viewTitle: document.getElementById('view-title'),
        viewSubtitle: document.getElementById('view-subtitle'),
        liveDatetime: document.getElementById('live-datetime'),
        btnGlobalExportExcel: document.getElementById('btn-global-export-excel'),
        
        // Dashboard
        sourcesStatusGrid: document.getElementById('sources-status-grid'),
        statRecordCount: document.getElementById('stat-record-count'),
        dbMixerSequenceTbody: document.getElementById('db-mixer-sequence-tbody'),
        dbPelletLinesGrid: document.getElementById('db-pellet-lines-grid'),
        dbPackagingMatrixTbody: document.getElementById('db-packaging-matrix-tbody'),
        dashboardPlanCard: document.getElementById('dashboard-plan-card'),
        dashboardPlanTitle: document.getElementById('dashboard-plan-title'),
        dashboardPlanFilename: document.getElementById('dashboard-plan-filename'),
        btnDashboardExportExcel: document.getElementById('btn-dashboard-export-excel'),
        
        // Details View
        viewDataDetails: document.getElementById('view-data-details'),
        detailsTitle: document.getElementById('details-title'),
        detailsFilename: document.getElementById('details-filename'),
        detailsLastmod: document.getElementById('details-lastmod'),
        detailsFilesize: document.getElementById('details-filesize'),
        detailFileInput: document.getElementById('detail-file-input'),
        detailUploaderForm: document.getElementById('detail-uploader-form'),
        uploadProgressContainer: document.getElementById('upload-progress-container'),
        uploadProgressFill: document.getElementById('upload-progress-fill'),
        uploadProgressText: document.getElementById('upload-progress-text'),
        tableSearchInput: document.getElementById('table-search-input'),
        tableRowCount: document.getElementById('table-row-count'),
        detailedTableThead: document.getElementById('detailed-table-thead'),
        detailedTableTbody: document.getElementById('detailed-table-tbody'),
        btnPrevPage: document.getElementById('btn-prev-page'),
        btnNextPage: document.getElementById('btn-next-page'),
        paginationLabel: document.getElementById('pagination-label'),
        
        // Adjustments View
        adjustTabs: document.querySelectorAll('.adjust-tab'),
        adjustTabPanels: document.querySelectorAll('.tab-panel'),
        btnSaveAdjustments: document.getElementById('btn-save-adjustments'),
        btnAddAdditionRow: document.getElementById('btn-add-addition-row'),
        btnAddCancellationRow: document.getElementById('btn-add-cancellation-row'),
        btnAddSubstitutionRow: document.getElementById('btn-add-substitution-row'),
        btnAddBagSubRow: document.getElementById('btn-add-bag-sub-row'),
        tableAdjustAdditions: document.querySelector('#table-adjust-additions tbody'),
        tableAdjustCancellations: document.querySelector('#table-adjust-cancellations tbody'),
        tableAdjustSubstitutions: document.querySelector('#table-adjust-substitutions tbody'),
        tableAdjustBagSubs: document.querySelector('#table-adjust-bag-subs tbody'),
        
        // Generator View
        planTargetDate: document.getElementById('plan-target-date'),
        walkinOrdersList: document.getElementById('walkin-orders-list'),
        btnAddWalkinRow: document.getElementById('btn-add-walkin-row'),
        btnRunSolver: document.getElementById('btn-run-solver'),
        planTerminalConsole: document.getElementById('plan-terminal-console'),
        btnClearTerminal: document.getElementById('btn-clear-terminal'),
        planResultSummary: document.getElementById('plan-result-summary'),
        solveResultTitle: document.getElementById('solve-result-title'),
        solveResultFilename: document.getElementById('solve-result-filename'),
        btnDownloadPlanXlsx: document.getElementById('btn-download-plan-xlsx'),
        resTotalTons: document.getElementById('res-total-tons'),
        resTotalBatches: document.getElementById('res-total-batches'),
        resProductCount: document.getElementById('res-product-count'),
        resWarningStatus: document.getElementById('res-warning-status'),
        resWarningDesc: document.getElementById('res-warning-desc'),
        resWarningsListContainer: document.getElementById('res-warnings-list-container'),
        resWarningsUl: document.getElementById('res-warnings-ul'),
        planResultSequence: document.getElementById('plan-result-sequence'),
        mixerSequenceTbody: document.getElementById('mixer-sequence-tbody'),
        
        // Pellet Line View
        pelletLinesMainGrid: document.getElementById('pellet-lines-main-grid'),
        plMetaInfo: document.getElementById('pl-meta-info'),
        
        // Packaging View
        packagingMatrixTbody: document.getElementById('packaging-matrix-tbody')
    };

    // Set default target date to tomorrow
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    elements.planTargetDate.value = tomorrow.toISOString().split('T')[0];

    // ----------------------------------------------------------------------
    // 3. UTILITIES & WIDGETS
    // ----------------------------------------------------------------------
    
    // Live ticking clock in topbar
    function updateClock() {
        const now = new Date();
        const d = String(now.getDate()).padStart(2, '0');
        const m = String(now.getMonth() + 1).padStart(2, '0');
        const y = now.getFullYear();
        const h = String(now.getHours()).padStart(2, '0');
        const min = String(now.getMinutes()).padStart(2, '0');
        const s = String(now.getSeconds()).padStart(2, '0');
        elements.liveDatetime.textContent = `${d}-${m}-${y} ${h}:${min}:${s}`;
    }
    setInterval(updateClock, 1000);
    updateClock();

    // Create customized notification toasts
    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `glass-card toast-box type-${type}`;
        toast.style.position = 'fixed';
        toast.style.bottom = '30px';
        toast.style.right = '30px';
        toast.style.padding = '1rem 1.5rem';
        toast.style.zIndex = '9999';
        toast.style.borderLeft = `4px solid ${type === 'success' ? 'var(--emerald)' : (type === 'error' ? 'var(--rose)' : 'var(--amber)')}`;
        toast.style.animation = 'slideUp 0.3s ease-out';
        toast.style.background = 'rgba(15, 20, 34, 0.9)';
        toast.style.backdropFilter = 'var(--glass-blur)';
        
        toast.innerHTML = `
            <div style="display:flex; align-items:center; gap:0.75rem;">
                <i data-lucide="${type === 'success' ? 'check-circle' : 'alert-triangle'}" style="color:${type === 'success' ? 'var(--emerald)' : 'var(--amber)'};"></i>
                <span style="font-size:0.875rem; font-weight:600; color:var(--text-primary);">${message}</span>
            </div>
        `;
        document.body.appendChild(toast);
        lucide.createIcons();
        
        setTimeout(() => {
            toast.style.animation = 'fadeOut 0.3s ease-out forwards';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }

    // ----------------------------------------------------------------------
    // 4. NAVIGATION SYSTEM (SPA ROUTER)
    // ----------------------------------------------------------------------
    elements.sidebarItems.forEach(item => {
        item.addEventListener('click', () => {
            const targetView = item.getAttribute('data-view');
            
            // Handle active classes on sidebar
            elements.sidebarItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            
            // Adjust title and subtitles
            if (targetView.startsWith('data-')) {
                const category = targetView.replace('data-', '');
                if (category === 'adjustments') {
                    switchView('data-adjustments');
                    loadAdjustmentsData();
                } else {
                    switchView('data-details');
                    loadCategoryDetails(category);
                }
            } else {
                switchView(targetView);
            }
        });
    });

    function switchView(viewName) {
        state.currentView = viewName;
        
        // Hide all panels
        elements.viewPanels.forEach(panel => {
            panel.classList.remove('active');
        });
        
        // Show target panel
        const activePanel = document.getElementById(`view-${viewName}`);
        if (activePanel) {
            activePanel.classList.add('active');
        }
        
        // Set dynamic titles
        if (viewName === 'dashboard') {
            elements.viewTitle.textContent = 'Bảng Tổng Quan Hệ Thống';
            elements.viewSubtitle.textContent = 'Trạng thái 10 nguồn dữ liệu phục vụ lập kế hoạch';
        } else if (viewName === 'data-adjustments') {
            elements.viewTitle.textContent = 'Bảng Điều Chỉnh Nhanh KHSX';
            elements.viewSubtitle.textContent = 'Đồng bộ trực tiếp thay đổi sang file cấu hình DIEU_CHINH_NHANH.xlsx';
        } else if (viewName === 'plan-generator') {
            elements.viewTitle.textContent = 'Trình Lập Kế Hoạch Sản Xuất Tự Động';
            elements.viewSubtitle.textContent = 'Chạy thuật toán Mixer Sequence tối ưu và an toàn sinh học';
        } else if (viewName === 'plan-pellet-lines') {
            elements.viewTitle.textContent = 'Phân Bổ Kế Hoạch Máy Ép Pellet Lines';
            elements.viewSubtitle.textContent = 'Trực quan hóa lịch ép của 7 line máy Pellet và Mash theo an toàn kháng sinh';
        } else if (viewName === 'plan-packaging') {
            elements.viewTitle.textContent = 'Ma Trận Phân Bổ Bao Bì Đại Lý & Trại';
            elements.viewSubtitle.textContent = 'Khoa học, đầy đủ, hiển thị chi tiết số lượng bao bì thương hiệu đại lý và trại';
        }
    }

    // ----------------------------------------------------------------------
    // 5. DASHBOARD: RETRIEVE 10 DATA SOURCES STATUS
    // ----------------------------------------------------------------------
    async function loadDataSourcesStatus() {
        try {
            const res = await fetch('/api/data-status');
            const json = await res.json();
            
            if (json.success) {
                state.dataSourcesStatus = json.status;
                renderDashboardStatus(json.status);
            } else {
                showToast(`Lỗi lấy dữ liệu: ${json.message}`, 'error');
            }
        } catch (err) {
            console.error(err);
            showToast('Không thể kết nối đến Flask server!', 'error');
        }
    }

    function renderDashboardStatus(status) {
        elements.sourcesStatusGrid.innerHTML = '';
        let okCount = 0;
        let totalRecords = 0;
        
        const categories = Object.keys(status).filter(c => c !== 'adjustments');
        
        categories.forEach(cat => {
            const fileInfo = status[cat];
            const displayInfo = categoryInfo[cat] || { title: cat, filename: 'unknown' };
            const exists = fileInfo.exists;
            if (exists) okCount++;
            
            const card = document.createElement('div');
            card.className = `source-card glass-card ${exists ? '' : 'border-danger'}`;
            
            // Format dynamic status badge
            const badgeClass = exists ? 'badge-success' : 'badge-danger';
            const badgeText = exists ? 'Sẵn sàng' : 'Thiếu file';
            
            card.innerHTML = `
                <div class="source-card-header">
                    <span class="source-name">${displayInfo.title}</span>
                    <span class="badge ${badgeClass}">${badgeText}</span>
                </div>
                <div class="source-card-body">
                    <div class="source-meta-row"><strong>File:</strong> ${fileInfo.filename}</div>
                    <div class="source-meta-row"><strong>Cập nhật:</strong> ${fileInfo.last_modified}</div>
                    <div class="source-meta-row"><strong>Dung lượng:</strong> ${fileInfo.size}</div>
                </div>
                <div class="source-card-footer">
                    <span class="text-muted" style="font-size: 0.65rem;">Nhấp xem bảng &gt;</span>
                    <button class="btn-view-detail" data-cat="${cat}">Chi tiết</button>
                </div>
            `;
            
            // Wire click events
            card.addEventListener('click', () => {
                switchView('data-details');
                loadCategoryDetails(cat);
                
                // Highlight sidebar
                elements.sidebarItems.forEach(i => i.classList.remove('active'));
                const sidebarItem = document.querySelector(`.nav-item[data-view="data-${cat}"]`);
                if (sidebarItem) sidebarItem.classList.add('active');
            });
            
            elements.sourcesStatusGrid.appendChild(card);
        });
        
        // Update stats card numbers
        document.getElementById('stat-excel-count').textContent = `${okCount} / ${categories.length}`;
        elements.statRecordCount.textContent = `${categories.length * 10} Cấu hình`;
        
        lucide.createIcons();
    }

    // ----------------------------------------------------------------------
    // 6. DETAIL VIEW & DRAG-AND-DROP FILE UPLOADER
    // ----------------------------------------------------------------------
    async function loadCategoryDetails(category) {
        state.activeCategory = category;
        state.currentPage = 1;
        
        const display = categoryInfo[category];
        elements.detailsTitle.textContent = display.title;
        
        // Hiển thị subtitle nếu có (VD: công thức Stock đầu ngày)
        const subtitleEl = document.getElementById('details-subtitle');
        if (subtitleEl) {
            subtitleEl.textContent = display.subtitle || '';
            subtitleEl.style.display = display.subtitle ? 'block' : 'none';
        }
        
        // Quản lý animal filter bar
        let filterBar = document.getElementById('stock-animal-filter');
        if (category === 'ffstock') {
            if (!filterBar) {
                const tableContainer = elements.detailedTableThead?.closest('.table-scroll-container')?.parentElement;
                if (tableContainer) {
                    const bar = document.createElement('div');
                    bar.id = 'stock-animal-filter';
                    bar.className = 'animal-filter-bar';
                    bar.style.marginBottom = '0.5rem';
                    bar.innerHTML = `
                        <span style="font-size: 0.75rem; color: var(--text-secondary); margin-right: 8px;">🐾 Vật nuôi:</span>
                        <button class="animal-btn active" data-animal="all" style="--animal-color: var(--primary)">Tất cả</button>
                        <button class="animal-btn" data-animal="H" style="--animal-color: #FF6B6B">HEO</button>
                        <button class="animal-btn" data-animal="G" style="--animal-color: #4ECDC4">GÀ</button>
                        <button class="animal-btn" data-animal="B" style="--animal-color: #45B7D1">BÒ</button>
                        <button class="animal-btn" data-animal="V" style="--animal-color: #96CEB4">VỊT</button>
                        <button class="animal-btn" data-animal="C" style="--animal-color: #FFEAA7">CÚT</button>
                        <button class="animal-btn" data-animal="D" style="--animal-color: #DDA0DD">DÊ</button>
                    `;
                    const scrollContainer = elements.detailedTableThead?.closest('.table-scroll-container');
                    tableContainer.insertBefore(bar, scrollContainer);
                }
                filterBar = document.getElementById('stock-animal-filter');
            }
            if (filterBar) {
                filterBar.style.display = 'flex';
                // Reset filter
                filterBar.querySelectorAll('.animal-btn').forEach(b => b.classList.remove('active'));
                filterBar.querySelector('[data-animal="all"]')?.classList.add('active');
            }
        } else {
            if (filterBar) filterBar.style.display = 'none';
        }
        
        // Show skeleton loader
        elements.detailedTableThead.innerHTML = '<tr><th>Đang tải...</th></tr>';
        elements.detailedTableTbody.innerHTML = '<tr><td style="text-align:center;"><i class="loading-icon animate-spin"></i> Đang đọc file Excel từ hệ thống...</td></tr>';
        
        try {
            const res = await fetch(`/api/data/${category}`);
            const json = await res.json();
            
            if (json.success) {
                // Update file headers metadata
                const info = json.file_info;
                elements.detailsFilename.textContent = `Tên file: ${info.filename || 'Không có'}`;
                elements.detailsLastmod.textContent = `Cập nhật: ${info.last_modified || '-'}`;
                elements.detailsFilesize.textContent = `Dung lượng: ${info.size || '-'}`;
                
                state.tableData = json.data;
                state.filteredData = [...json.data];
                
                renderDetailedTable();
                
                // Setup animal filter events cho ffstock
                if (category === 'ffstock' && filterBar) {
                    filterBar.querySelectorAll('.animal-btn').forEach(btn => {
                        btn.onclick = function() {
                            filterBar.querySelectorAll('.animal-btn').forEach(b => b.classList.remove('active'));
                            this.classList.add('active');
                            const animal = this.dataset.animal;
                            if (animal === 'all') {
                                state.filteredData = [...state.tableData];
                            } else {
                                state.filteredData = state.tableData.filter(r => r.animal_type === animal);
                            }
                            state.currentPage = 1;
                            renderDetailedTable();
                        };
                    });
                }
            } else {
                elements.detailedTableTbody.innerHTML = `<tr><td style="text-align:center; color:var(--rose);">Lỗi đọc Excel: ${json.message}</td></tr>`;
            }
        } catch (err) {
            elements.detailedTableTbody.innerHTML = '<tr><td style="text-align:center; color:var(--rose);">Không kết nối được API Server.</td></tr>';
        }
    }

    // Dynamic columns renderer based on active category
    function renderDetailedTable() {
        const category = state.activeCategory;
        const start = (state.currentPage - 1) * state.rowsPerPage;
        const end = start + state.rowsPerPage;
        const pageData = state.filteredData.slice(start, end);
        
        elements.tableRowCount.textContent = `Tổng cộng: ${state.filteredData.length} dòng`;
        
        // 1. Render Headers
        let headHTML = '<tr>';
        if (category === 'forecast') {
            headHTML += `
                <th>Mã Cám</th><th>Bao/Silo</th><th>Kích khuôn</th>
                <th>Higro 25</th><th>CP 25</th><th>Star 25</th><th>Nuvo 25</th><th>Nasa 25</th><th>Tổng DL</th>
                <th>Swine Farm</th><th>Integrate Farm</th><th>Tổng Trại</th><th>Tổng Tấn</th><th>Tấn Silo</th><th>Tổng + Silo</th>
            `;
        } else if (category === 'silo_plan' || category === 'bacang') {
            headHTML += `<th>Mã Cám</th><th>Ngày 1 (Thứ 2)</th><th>Ngày 2 (Thứ 3)</th><th>Ngày 3 (Thứ 4)</th><th>Ngày 4 (Thứ 5)</th><th>Ngày 5 (Thứ 6)</th><th>Ngày 6 (Thứ 7)</th><th>Tổng Tấn</th>`;
        } else if (category === 'ffstock') {
            headHTML += `<th style="width:4%">Stt</th><th style="width:10%">Code</th><th style="width:12%">Tên</th><th style="width:5%">Vật nuôi</th><th style="width:9%">Stock</th><th style="width:9%">Aver</th><th style="width:6%">DOH</th><th style="width:9%">Plan</th><th style="width:8%">Day5</th><th style="width:8%">KQ GC2</th><th>Ghi chú</th>`;
        } else if (category === 'tonbon') {
            headHTML += `<th>Mã Cám</th><th>Khối lượng Tồn Bồn (Tấn)</th>`;
        } else if (category === 'empty_bag') {
            headHTML += `<th>Mã Cám</th><th>HIGRO (Cái)</th><th>C.P. (Cái)</th><th>STAR (Cái)</th><th>NASA (Cái)</th><th>NUVO (Cái)</th><th>FARM (Cái)</th>`;
        } else if (category === 'congsuat') {
            headHTML += `<th>Mã Cám</th><th>Mã Công Thức</th><th>Kích Khuôn</th><th>Tấn/Mẻ Trộn</th><th>Mixer Line</th><th>Line Đóng Bao</th><th>Kháng Sinh</th>`;
        } else if (category === 'feedcode') {
            headHTML += `<th>Mã Cám</th><th>Line Trộn (Mixer)</th><th>Line Đóng Bao</th>`;
        } else if (category === 'khangsinh') {
            headHTML += `<th>Mã Cám</th><th>Mã Cấu Hình Kháng Sinh</th>`;
        } else if (category === 'yesterday_plan') {
            headHTML += `<th>Mã Cám</th><th>Kế hoạch (Mẻ)</th><th>Thực tế (Mẻ)</th><th>Kế hoạch (Tấn)</th><th>Thực tế (Tấn)</th><th>Tình trạng</th>`;
        }
        headHTML += '</tr>';
        elements.detailedTableThead.innerHTML = headHTML;
        
        // 2. Render Rows
        if (pageData.length === 0) {
            elements.detailedTableTbody.innerHTML = '<tr><td colspan="15" style="text-align:center; padding: 2rem;">Không tìm thấy kết quả phù hợp!</td></tr>';
            elements.btnPrevPage.disabled = true;
            elements.btnNextPage.disabled = true;
            elements.paginationLabel.textContent = 'Trang 0 / 0';
            return;
        }
        
        let bodyHTML = '';
        pageData.forEach(row => {
            bodyHTML += '<tr>';
            if (category === 'forecast') {
                bodyHTML += `
                    <td><strong>${row.product_code}</strong></td><td>${row.packing_size}</td><td>${row.die_size}</td>
                    <td>${row.dealer_higro || '-'}</td><td>${row.dealer_cp || '-'}</td><td>${row.dealer_star || '-'}</td>
                    <td>${row.dealer_nuvo || '-'}</td><td>${row.dealer_nasa || '-'}</td><td>${row.dealer_total || '-'}</td>
                    <td>${row.farm_swine || '-'}</td><td>${row.farm_integrate || '-'}</td><td>${row.farm_total || '-'}</td>
                    <td><strong class="text-cyan">${row.grand_total_tons}</strong></td><td>${row.silo_tons || '-'}</td><td><strong>${row.total_with_silo}</strong></td>
                `;
            } else if (category === 'silo_plan' || category === 'bacang') {
                bodyHTML += `
                    <td><strong>${row.product_code}</strong></td>
                    <td>${row.day_1 || '-'}</td><td>${row.day_2 || '-'}</td><td>${row.day_3 || '-'}</td>
                    <td>${row.day_4 || '-'}</td><td>${row.day_5 || '-'}</td><td>${row.day_6 || '-'}</td>
                    <td><strong class="text-cyan">${row.total}</strong></td>
                `;
            } else if (category === 'ffstock') {
                const dohVal = row.doh !== null && row.doh !== undefined ? Number(row.doh) : null;
                let dohHtml = '-';
                if (dohVal !== null) {
                    let dohClass = 'doh-safe';
                    if (dohVal < 1) dohClass = 'doh-critical';
                    else if (dohVal < 3) dohClass = 'doh-warning';
                    dohHtml = `<span class="doh-badge ${dohClass}">${dohVal.toFixed(1)}</span>`;
                }
                const animalColor = row.animal_color || '#FF6B6B';
                const animalLabel = row.animal_label || 'HEO';
                const petChip = `<span class="animal-chip" style="--chip-color: ${animalColor}">${animalLabel}</span>`;
                const sttIdx = pageData.indexOf(row) + 1 + ((state.currentPage - 1) * state.rowsPerPage);
                bodyHTML += `
                    <td>${sttIdx}</td>
                    <td><strong>${row.product_code}</strong></td>
                    <td style="font-size:0.72rem;">${row.product_name || ''}</td>
                    <td>${petChip}</td>
                    <td><strong>${row.stock_tons}</strong></td>
                    <td>${row.daily_sales_tons}</td>
                    <td>${dohHtml}</td>
                    <td>${row.plan || 0}</td>
                    <td>${row.day5 || 0}</td>
                    <td><strong>${row.kq_gc2 || 0}</strong></td>
                    <td style="font-size:0.7rem;">${row.ghi_chu || ''}</td>
                `;
            } else if (category === 'tonbon') {
                bodyHTML += `<td><strong>${row.product_code}</strong></td><td><strong class="text-cyan">${row.tons}</strong></td>`;
            } else if (category === 'empty_bag') {
                bodyHTML += `
                    <td><strong>${row.product_code}</strong></td>
                    <td>${row.HIGRO || '-'}</td><td>${row.CP || '-'}</td><td>${row.STAR || '-'}</td>
                    <td>${row.NASA || '-'}</td><td>${row.NUVO || '-'}</td><td>${row.FARM || '-'}</td>
                `;
            } else if (category === 'congsuat') {
                bodyHTML += `
                    <td><strong>${row.product_code}</strong></td>
                    <td>${row.formular_code || ''}</td>
                    <td>${row.die_size || ''}</td>
                    <td><strong>${row.ton_per_batch}</strong></td>
                    <td>${row.line_cv || ''}</td>
                    <td>${row.line_pk || ''}</td>
                    <td style="color:${row.ks_code && row.ks_code !== 'Sạch không KS' ? 'var(--purple)' : 'var(--emerald)'};"><strong>${row.ks_code || ''}</strong></td>
                `;
            } else if (category === 'feedcode') {
                bodyHTML += `
                    <td><strong>${row.product_code}</strong></td>
                    <td>${row.line_cv}</td>
                    <td>${row.line_pk}</td>
                `;
            } else if (category === 'khangsinh') {
                bodyHTML += `
                    <td><strong>${row.product_code}</strong></td>
                    <td style="color:${row.ks_code && row.ks_code !== 'Sạch không KS' ? 'var(--purple)' : 'var(--emerald)'};"><strong>${row.ks_code}</strong></td>
                `;
            } else if (category === 'yesterday_plan') {
                const planned_tons = Number(row.planned_tons || 0);
                const actual_tons = Number(row.actual_tons || 0);
                const isWarning = actual_tons < planned_tons * 0.95;
                bodyHTML += `
                    <td><strong>${row.product_code}</strong></td>
                    <td>${row.planned_batches}</td><td>${row.actual_batches}</td>
                    <td>${planned_tons}</td><td>${actual_tons}</td>
                    <td style="color:${isWarning ? 'var(--amber)' : 'var(--emerald)'};"><strong>${row.status || ''}</strong></td>
                `;
            }
            bodyHTML += '</tr>';
        });
        
        elements.detailedTableTbody.innerHTML = bodyHTML;
        
        // 3. Client Pagination Calculations
        const totalPages = Math.ceil(state.filteredData.length / state.rowsPerPage);
        elements.btnPrevPage.disabled = state.currentPage <= 1;
        elements.btnNextPage.disabled = state.currentPage >= totalPages;
        elements.paginationLabel.textContent = `Trang ${state.currentPage} / ${totalPages}`;
    }

    // Client-side instant filter search
    elements.tableSearchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();
        state.currentPage = 1;
        
        if (query === '') {
            state.filteredData = [...state.tableData];
        } else {
            state.filteredData = state.tableData.filter(row => {
                return Object.values(row).some(val => 
                    String(val).toLowerCase().includes(query)
                );
            });
        }
        renderDetailedTable();
    });

    elements.btnPrevPage.addEventListener('click', () => {
        if (state.currentPage > 1) {
            state.currentPage--;
            renderDetailedTable();
        }
    });

    elements.btnNextPage.addEventListener('click', () => {
        const totalPages = Math.ceil(state.filteredData.length / state.rowsPerPage);
        if (state.currentPage < totalPages) {
            state.currentPage++;
            renderDetailedTable();
        }
    });

    // ----------------------------------------------------------------------
    // 7. DRAG-AND-DROP FILE UPLOADER ENGINE
    // ----------------------------------------------------------------------
    const zone = elements.detailUploaderForm;
    
    zone.addEventListener('click', () => {
        elements.detailFileInput.click();
    });
    
    // Drag/Drop Visual Highlight triggers
    ['dragenter', 'dragover'].forEach(eventName => {
        zone.addEventListener(eventName, (e) => {
            e.preventDefault();
            zone.classList.add('dragover');
        }, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        zone.addEventListener(eventName, (e) => {
            e.preventDefault();
            zone.classList.remove('dragover');
        }, false);
    });
    
    zone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length) {
            handleFileUpload(files[0]);
        }
    });
    
    elements.detailFileInput.addEventListener('change', (e) => {
        const files = e.target.files;
        if (files.length) {
            handleFileUpload(files[0]);
        }
    });

    // Async AJAX file upload with dynamic percentage progress bar
    function handleFileUpload(file) {
        const cat = state.activeCategory;
        if (!cat) return;
        
        const formData = new FormData();
        formData.append('file', file);
        
        elements.uploadProgressContainer.style.display = 'block';
        elements.uploadProgressFill.style.width = '0%';
        elements.uploadProgressText.textContent = '0%';
        
        const xhr = new XMLHttpRequest();
        xhr.open('POST', `/api/upload/${cat}`, true);
        
        xhr.upload.onprogress = (e) => {
            if (e.lengthComputable) {
                const percent = Math.round((e.loaded / e.total) * 100);
                elements.uploadProgressFill.style.width = `${percent}%`;
                elements.uploadProgressText.textContent = `${percent}%`;
            }
        };
        
        xhr.onload = () => {
            elements.uploadProgressContainer.style.display = 'none';
            if (xhr.status === 200) {
                const resp = JSON.parse(xhr.responseText);
                if (resp.success) {
                    showToast(resp.message, 'success');
                    
                    // Reload data status list and update table view instantly
                    loadDataSourcesStatus();
                    loadCategoryDetails(cat);
                } else {
                    showToast(resp.message, 'error');
                }
            } else {
                showToast('Lỗi server khi upload file!', 'error');
            }
        };
        
        xhr.onerror = () => {
            elements.uploadProgressContainer.style.display = 'none';
            showToast('Không thể kết nối đến server để upload!', 'error');
        };
        
        xhr.send(formData);
    }

    // ----------------------------------------------------------------------
    // 8. QUICK ADJUSTMENT EDITABLE SHEETS (DIEU_CHINH_NHANH)
    // ----------------------------------------------------------------------
    elements.adjustTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            elements.adjustTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            const targetPanelId = tab.getAttribute('data-tab');
            elements.adjustTabPanels.forEach(p => p.classList.remove('active'));
            document.getElementById(targetPanelId).classList.add('active');
        });
    });

    async function loadAdjustmentsData() {
        try {
            const res = await fetch('/api/data/adjustments');
            const json = await res.json();
            
            if (json.success) {
                state.adjustments = json.data;
                renderAdjustmentTables();
            } else {
                showToast(`Lỗi lấy cấu hình: ${json.message}`, 'error');
            }
        } catch (err) {
            showToast('Không kết nối được server cấu hình!', 'error');
        }
    }

    function renderAdjustmentTables() {
        // Clear all tables
        elements.tableAdjustAdditions.innerHTML = '';
        elements.tableAdjustCancellations.innerHTML = '';
        elements.tableAdjustSubstitutions.innerHTML = '';
        elements.tableAdjustBagSubs.innerHTML = '';
        
        // 1. THEM_MOI_HOAC_SUA Row items
        state.adjustments.additions.forEach((item, idx) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><input type="text" class="cell-prod" value="${item.product_code || ''}" placeholder="566"></td>
                <td><input type="number" step="0.1" class="cell-tons" value="${item.tons || 0}"></td>
                <td>
                    <select class="cell-packing">
                        <option value="25" ${item.packing_size == '25' ? 'selected' : ''}>Bao 25kg</option>
                        <option value="40" ${item.packing_size == '40' ? 'selected' : ''}>Bao 40kg</option>
                        <option value="50" ${item.packing_size == '50' ? 'selected' : ''}>Bao 50kg (Trại)</option>
                        <option value="M" ${item.packing_size == 'M' ? 'selected' : ''}>Bồn Silo</option>
                    </select>
                </td>
                <td>
                    <select class="cell-priority">
                        <option value="NORMAL" ${item.priority == 'NORMAL' ? 'selected' : ''}>Normal (Bình thường)</option>
                        <option value="HIGH" ${item.priority == 'HIGH' ? 'selected' : ''}>High (Ưu tiên cao)</option>
                        <option value="FORCE" ${item.priority == 'FORCE' ? 'selected' : ''}>Force (Bắt buộc chạy)</option>
                    </select>
                </td>
                <td><input type="number" class="cell-batches" value="${item.force_batches || ''}"></td>
                <td><input type="number" step="0.1" class="cell-tpb" value="${item.force_tpb || ''}"></td>
                <td><input type="text" class="cell-note" value="${item.note || ''}" placeholder="Ghi chú"></td>
                <td><button class="btn-delete-row" data-action="delete-add" data-index="${idx}"><i data-lucide="trash-2"></i></button></td>
            `;
            elements.tableAdjustAdditions.appendChild(tr);
        });

        // 2. HUY_KHSX Row items
        state.adjustments.cancellations.forEach((item, idx) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><input type="text" class="cell-prod" value="${item.product_code || ''}" placeholder="566"></td>
                <td>
                    <select class="cell-cancel-type">
                        <option value="HỦY HẾT" ${item.cancel_type == 'HỦY HẾT' ? 'selected' : ''}>HỦY HẾT (Hủy cả Silo & Đóng bao)</option>
                        <option value="HỦY BAO" ${item.cancel_type == 'HỦY BAO' ? 'selected' : ''}>HỦY BAO (Không đóng bao bì)</option>
                        <option value="HỦY SILO" ${item.cancel_type == 'HỦY SILO' ? 'selected' : ''}>HỦY SILO (Hủy đơn đổ bồn)</option>
                    </select>
                </td>
                <td><input type="text" class="cell-note" value="${item.note || ''}" placeholder="Ghi chú"></td>
                <td><button class="btn-delete-row" data-action="delete-cancel" data-index="${idx}"><i data-lucide="trash-2"></i></button></td>
            `;
            elements.tableAdjustCancellations.appendChild(tr);
        });

        // 3. THAY_THE_MA_CAM Row items
        state.adjustments.substitutions.forEach((item, idx) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><input type="text" class="cell-old" value="${item.old_code || ''}" placeholder="Mã cám cũ"></td>
                <td><input type="text" class="cell-new" value="${item.new_code || ''}" placeholder="Mã cám thay thế"></td>
                <td><input type="text" class="cell-note" value="${item.note || ''}" placeholder="Ghi chú"></td>
                <td><button class="btn-delete-row" data-action="delete-sub" data-index="${idx}"><i data-lucide="trash-2"></i></button></td>
            `;
            elements.tableAdjustSubstitutions.appendChild(tr);
        });

        // 4. THAY_THE_BAO_BI Row items
        state.adjustments.bag_substitutions.forEach((item, idx) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><input type="text" class="cell-prod" value="${item.product_code || ''}" placeholder="566"></td>
                <td><input type="text" class="cell-old-bag" value="${item.old_bag || ''}" placeholder="Mã bao bì cũ"></td>
                <td><input type="text" class="cell-new-bag" value="${item.new_bag || ''}" placeholder="Mã bao bì thay thế"></td>
                <td><input type="text" class="cell-note" value="${item.note || ''}" placeholder="Ghi chú"></td>
                <td><button class="btn-delete-row" data-action="delete-bag-sub" data-index="${idx}"><i data-lucide="trash-2"></i></button></td>
            `;
            elements.tableAdjustBagSubs.appendChild(tr);
        });

        // Register trash delete triggers
        document.querySelectorAll('.btn-delete-row').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const target = e.currentTarget;
                const action = target.getAttribute('data-action');
                const idx = parseInt(target.getAttribute('data-index'), 10);
                
                // Read current grid values first to prevent data loss on click
                pullAdjustmentsDataFromUI();
                
                if (action === 'delete-add') state.adjustments.additions.splice(idx, 1);
                else if (action === 'delete-cancel') state.adjustments.cancellations.splice(idx, 1);
                else if (action === 'delete-sub') state.adjustments.substitutions.splice(idx, 1);
                else if (action === 'delete-bag-sub') state.adjustments.bag_substitutions.splice(idx, 1);
                
                renderAdjustmentTables();
            });
        });

        lucide.createIcons();
    }

    // Pull edited values in table inputs back to JS state
    function pullAdjustmentsDataFromUI() {
        // 1. Additions
        state.adjustments.additions = [];
        elements.tableAdjustAdditions.querySelectorAll('tr').forEach(tr => {
            const prod = tr.querySelector('.cell-prod').value.trim();
            if (!prod) return;
            state.adjustments.additions.push({
                product_code: prod,
                tons: Number(tr.querySelector('.cell-tons').value || 0),
                packing_size: tr.querySelector('.cell-packing').value,
                priority: tr.querySelector('.cell-priority').value,
                force_batches: tr.querySelector('.cell-batches').value ? Number(tr.querySelector('.cell-batches').value) : '',
                force_tpb: tr.querySelector('.cell-tpb').value ? Number(tr.querySelector('.cell-tpb').value) : '',
                note: tr.querySelector('.cell-note').value
            });
        });

        // 2. Cancellations
        state.adjustments.cancellations = [];
        elements.tableAdjustCancellations.querySelectorAll('tr').forEach(tr => {
            const prod = tr.querySelector('.cell-prod').value.trim();
            if (!prod) return;
            state.adjustments.cancellations.push({
                product_code: prod,
                cancel_type: tr.querySelector('.cell-cancel-type').value,
                note: tr.querySelector('.cell-note').value
            });
        });

        // 3. Substitutions
        state.adjustments.substitutions = [];
        elements.tableAdjustSubstitutions.querySelectorAll('tr').forEach(tr => {
            const old = tr.querySelector('.cell-old').value.trim();
            const newVal = tr.querySelector('.cell-new').value.trim();
            if (!old || !newVal) return;
            state.adjustments.substitutions.push({
                old_code: old,
                new_code: newVal,
                note: tr.querySelector('.cell-note').value
            });
        });

        // 4. Bag substitutions
        state.adjustments.bag_substitutions = [];
        elements.tableAdjustBagSubs.querySelectorAll('tr').forEach(tr => {
            const prod = tr.querySelector('.cell-prod').value.trim();
            const old = tr.querySelector('.cell-old-bag').value.trim();
            const newVal = tr.querySelector('.cell-new-bag').value.trim();
            if (!prod || !old || !newVal) return;
            state.adjustments.bag_substitutions.push({
                product_code: prod,
                old_bag: old,
                new_bag: newVal,
                note: tr.querySelector('.cell-note').value
            });
        });
    }

    // Save adjustments to DIEU_CHINH_NHANH.xlsx
    elements.btnSaveAdjustments.addEventListener('click', async () => {
        pullAdjustmentsDataFromUI();
        
        elements.btnSaveAdjustments.disabled = true;
        elements.btnSaveAdjustments.innerHTML = '<i class="loading-icon animate-spin"></i> Đang lưu...';
        
        try {
            const res = await fetch('/api/adjustments/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(state.adjustments)
            });
            const json = await res.json();
            
            if (json.success) {
                showToast(json.message, 'success');
                loadAdjustmentsData(); // Refresh UI values
            } else {
                showToast(`Lỗi lưu: ${json.message}`, 'error');
            }
        } catch (err) {
            showToast('Không kết nối được server để ghi đè Excel!', 'error');
        } finally {
            elements.btnSaveAdjustments.disabled = false;
            elements.btnSaveAdjustments.innerHTML = '<i class="save"></i> Lưu và áp dụng vào Excel';
            lucide.createIcons();
        }
    });

    // Add empty rows triggers
    elements.btnAddAdditionRow.addEventListener('click', () => {
        pullAdjustmentsDataFromUI();
        state.adjustments.additions.push({ product_code: '', tons: 0, packing_size: '25', priority: 'NORMAL', force_batches: '', force_tpb: '', note: '' });
        renderAdjustmentTables();
    });

    elements.btnAddCancellationRow.addEventListener('click', () => {
        pullAdjustmentsDataFromUI();
        state.adjustments.cancellations.push({ product_code: '', cancel_type: 'HỦY HẾT', note: '' });
        renderAdjustmentTables();
    });

    elements.btnAddSubstitutionRow.addEventListener('click', () => {
        pullAdjustmentsDataFromUI();
        state.adjustments.substitutions.push({ old_code: '', new_code: '', note: '' });
        renderAdjustmentTables();
    });

    elements.btnAddBagSubRow.addEventListener('click', () => {
        pullAdjustmentsDataFromUI();
        state.adjustments.bag_substitutions.push({ product_code: '', old_bag: '', new_bag: '', note: '' });
        renderAdjustmentTables();
    });

    // ----------------------------------------------------------------------
    // 9. PLAN GENERATOR ENGINE & SSE LIVE STREAM LOGS
    // ----------------------------------------------------------------------
    
    // Add walkin orders
    elements.btnAddWalkinRow.addEventListener('click', () => {
        const index = state.walkinOrders.length;
        
        const row = document.createElement('div');
        row.className = 'walkin-row-item';
        row.id = `walkin-row-${index}`;
        row.innerHTML = `
            <input type="text" class="walkin-prod" placeholder="Cám (VD: 566)" style="text-transform:uppercase;">
            <input type="number" step="0.1" class="walkin-tons" placeholder="Tấn" min="0">
            <select class="walkin-packing">
                <option value="25">Bao 25</option>
                <option value="40">Bao 40</option>
                <option value="50">Bao 50</option>
                <option value="M">Silo</option>
            </select>
            <button class="btn-delete-row walkin-delete" data-index="${index}"><i data-lucide="x-circle" style="color:var(--rose); width:16px;"></i></button>
        `;
        
        // Remove no walkin label
        const noLabel = elements.walkinOrdersList.querySelector('.no-walkin-label');
        if (noLabel) noLabel.remove();
        
        elements.walkinOrdersList.appendChild(row);
        
        // Wire delete walkin row event
        row.querySelector('.walkin-delete').addEventListener('click', (e) => {
            const idx = e.currentTarget.getAttribute('data-index');
            document.getElementById(`walkin-row-${idx}`).remove();
            
            if (elements.walkinOrdersList.children.length === 0) {
                elements.walkinOrdersList.innerHTML = `
                    <div class="no-walkin-label text-muted text-center py-3">Chưa thêm đơn vãng lai</div>
                `;
            }
        });
        
        lucide.createIcons();
    });

    elements.btnClearTerminal.addEventListener('click', () => {
        elements.planTerminalConsole.innerHTML = '<div class="terminal-line text-muted">> Terminal cleared. Sẵn sàng...</div>';
    });

    // Solve engine dispatcher
    elements.btnRunSolver.addEventListener('click', async () => {
        const targetDate = elements.planTargetDate.value;
        if (!targetDate) {
            showToast('Vui lòng chọn ngày chạy kế hoạch!', 'error');
            return;
        }

        // Pull walkin orders array
        const walkinOrders = [];
        elements.walkinOrdersList.querySelectorAll('.walkin-row-item').forEach(row => {
            const prod = row.querySelector('.walkin-prod').value.trim().toUpperCase();
            const tons = parseFloat(row.querySelector('.walkin-tons').value);
            const packing = row.querySelector('.walkin-packing').value;
            
            if (prod && !isNaN(tons) && tons > 0) {
                walkinOrders.push({
                    product: prod,
                    tons: tons,
                    packing_size: packing
                });
            }
        });

        // Interface adjustments: lock button state
        elements.btnRunSolver.disabled = true;
        elements.btnRunSolver.querySelector('.spinner-hidden').style.display = 'none';
        elements.btnRunSolver.querySelector('.spinner-shown').style.display = 'inline-block';
        
        // Clear terminal & prepare stream
        elements.planTerminalConsole.innerHTML = '';
        appendTerminalLine(`🚀 Đang chuẩn bị dữ liệu và kết nối đến solver cho ngày KHSX: ${targetDate}...`, 'text-success');
        



        try {
            // Modern POST streaming with Fetch ReadableStream
            const response = await fetch('/api/generate-plan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    date: targetDate,
                    walkin_orders: walkinOrders
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');
            let buffer = '';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                buffer = lines.pop(); // Keep incomplete chunk line in buffer

                for (const line of lines) {
                    const lineTrimmed = line.trim();
                    if (lineTrimmed.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(lineTrimmed.slice(6));
                            if (data.type === 'log') {
                                appendTerminalLine(data.text);
                            } else if (data.type === 'complete') {
                                if (data.success) {
                                    appendTerminalLine(`\n${data.message}`, 'text-success');
                                    showToast(data.message, 'success');
                                    
                                    // Parse and load result UI
                                    const d = new Date(targetDate);
                                    const formattedDateStr = `${String(d.getDate()).padStart(2, '0')}-${String(d.getMonth()+1).padStart(2, '0')}-${d.getFullYear()}`;
                                    loadPlanResults(formattedDateStr);
                                } else {
                                    appendTerminalLine(`\n${data.message}`, 'text-error');
                                    showToast(data.message, 'error');
                                }
                            }
                        } catch (e) {
                            console.error('Failed to parse SSE JSON:', e);
                        }
                    }
                }
            }

        } catch (err) {
            console.error(err);
            appendTerminalLine(`❌ Đã xảy ra lỗi hệ thống nghiêm trọng: ${err.message}`, 'text-error');
            showToast('Lỗi chạy solver!', 'error');
        } finally {
            elements.btnRunSolver.disabled = false;
            elements.btnRunSolver.querySelector('.spinner-hidden').style.display = 'inline-block';
            elements.btnRunSolver.querySelector('.spinner-shown').style.display = 'none';
        }
    });

    function appendTerminalLine(text, className = '') {
        const line = document.createElement('div');
        line.className = `terminal-line ${className}`;
        line.textContent = text;
        elements.planTerminalConsole.appendChild(line);
        
        // Auto scroll console
        elements.planTerminalConsole.scrollTop = elements.planTerminalConsole.scrollHeight;
    }

    // ----------------------------------------------------------------------
    // 10. PLAN RESULTS DETAILS DISPLAY (SEQUENCE, PL TIMELINE, PACKAGING)
    // ----------------------------------------------------------------------
    async function loadPlanResults(dateStr) {
        try {
            const res = await fetch(`/api/plan-details/${dateStr}`);
            const json = await res.json();
            
            if (json.success) {
                // RENDER BẢNG KẾ HOẠCH SẢN XUẤT (CHÍNH)
                renderProductionPlanTable(json.sequence, dateStr, 'production-plan-container');
                renderProductionPlanTable(json.sequence, dateStr, 'dashboard-excel-plan-container');
                
                // RENDER TABLE 2: Pellet line timelines
                renderPelletLinesTimeline(json.pl_plans, dateStr, json.pl_rich_plans, json.mash_plan_rich, json.mixer_summary_rich, json.khpl_raw_grid);
                
                // RENDER TABLE 3: Packaging Matrix
                renderPackagingMatrix(json.packaging);
                
                // Show dashboard bento card & populate titles
                if (elements.dashboardPlanCard) {
                    elements.dashboardPlanCard.style.display = 'block';
                }
                if (elements.dashboardPlanTitle) {
                    elements.dashboardPlanTitle.textContent = `Kế Hoạch Sản Xuất Tự Động Ngày ${dateStr}`;
                }
                if (elements.dashboardPlanFilename) {
                    elements.dashboardPlanFilename.textContent = `File KHSX đầu ra: ${json.filename}`;
                }
                if (elements.btnDashboardExportExcel) {
                    elements.btnDashboardExportExcel.onclick = () => {
                        window.location.href = `/api/download-plan/${json.filename}`;
                    };
                }

                // Show global export button and set click handler
                if (elements.btnGlobalExportExcel) {
                    elements.btnGlobalExportExcel.style.display = 'inline-flex';
                    elements.btnGlobalExportExcel.onclick = () => {
                        window.location.href = `/api/download-plan/${json.filename}`;
                    };
                }
                
                // Alert completion
                appendTerminalLine(`🏁 Dữ liệu chi tiết cho Ngày ${dateStr} đã được vẽ và cập nhật đầy đủ lên giao diện web!`, 'text-success');
                
            } else {
                showToast(`Không đọc được file kết quả: ${json.message}`, 'error');
                if (elements.btnGlobalExportExcel) {
                    elements.btnGlobalExportExcel.style.display = 'none';
                }
                if (elements.dashboardPlanCard) {
                    elements.dashboardPlanCard.style.display = 'none';
                }
            }
        } catch (err) {
            console.error(err);
            showToast('Lỗi nạp chi tiết kế hoạch!', 'error');
            if (elements.btnGlobalExportExcel) {
                elements.btnGlobalExportExcel.style.display = 'none';
            }
            if (elements.dashboardPlanCard) {
                elements.dashboardPlanCard.style.display = 'none';
            }
        }
    }

    function renderMixerSequence(seq) {
        let html = '';
        seq.forEach((item, idx) => {
            const isMedicated = item.ks_code && item.ks_code !== 'Sạch không KS' && item.ks_code !== 'SẠCH (KHÔNG KS)';
            const rowClass = isMedicated ? 'medicated-row' : 'clean-row';
            const ksColor = isMedicated ? 'var(--purple)' : 'var(--emerald)';
            
            // Xây dựng hiển thị Quy cách với phân bổ tấn chi tiết cho người Mixer
            const siloT = Number(item.silo_tons) || 0;
            const bag25T = Number(item.bag_25_tons) || 0;
            const bag40T = Number(item.bag_40_tons) || 0;
            const bag50T = Number(item.bag_50_tons) || 0;
            
            const chips = [];
            if (siloT > 0) chips.push(`<span class="packing-chip packing-chip-silo">Silo <strong>${siloT}T</strong></span>`);
            if (bag25T > 0) chips.push(`<span class="packing-chip packing-chip-bag25">Bao 25 <strong>${bag25T}T</strong></span>`);
            if (bag40T > 0) chips.push(`<span class="packing-chip packing-chip-bag40">Bao 40 <strong>${bag40T}T</strong></span>`);
            if (bag50T > 0) chips.push(`<span class="packing-chip packing-chip-bag50">Bao 50 <strong>${bag50T}T</strong></span>`);
            
            let packingHtml;
            if (chips.length > 0) {
                packingHtml = `<div class="packing-breakdown">${chips.join('')}</div>`;
            } else {
                // Fallback khi chưa có dữ liệu phân bổ chi tiết từ Excel
                let packingText = item.packing_size;
                if (packingText === 'M') packingText = 'Silo';
                else if (packingText === '25' || packingText === '40' || packingText === '50') packingText = 'Bao ' + packingText;
                const chipClass = packingText.includes('Silo') ? 'packing-chip-silo' :
                                  packingText.includes('50') ? 'packing-chip-bag50' :
                                  packingText.includes('40') ? 'packing-chip-bag40' : 'packing-chip-bag25';
                packingHtml = `<span class="packing-chip ${chipClass}">${packingText} <strong>${item.tons}T</strong></span>`;
            }
            
            // DOH badge với color coding
            let dohHtml = '-';
            if (item.doh !== null && item.doh !== undefined) {
                const dohVal = Number(item.doh);
                let dohClass = 'doh-safe';     // Xanh (DOH >= 3)
                if (dohVal < 1) dohClass = 'doh-critical';   // Đỏ (DOH < 1)
                else if (dohVal < 3) dohClass = 'doh-warning'; // Vàng (DOH < 3)
                dohHtml = `<span class="doh-badge ${dohClass}" title="Tồn kho: ${item.stock || 0}T | TB bán: ${item.daily_avg || 0}T/ngày">${dohVal.toFixed(1)}</span>`;
            }
            
            // Badge cho Mixer Line
            const cvBadge = (item.line_cv && item.line_cv !== 'None') 
                ? `<span class="badge badge-success">${item.line_cv}</span>` 
                : '-';
            
            // Badge cho Line Đóng Bao
            let pkBadge = '-';
            if (item.line_pk && item.line_pk !== 'None') {
                if (item.line_pk.toUpperCase() === 'SILO') {
                    pkBadge = `<span class="badge badge-danger">SILO</span>`;
                } else {
                    pkBadge = `<span class="badge badge-warning">Line ${item.line_pk}</span>`;
                }
            }
            
            html += `
                <tr class="${rowClass}">
                    <td><strong>${idx + 1}</strong></td>
                    <td><strong>${item.product_code}</strong></td>
                    <td><strong>${item.batches}</strong></td>
                    <td><strong>${item.tons}T</strong></td>
                    <td>${packingHtml}</td>
                    <td>${dohHtml}</td>
                    <td style="color:${ksColor};"><strong>${item.ks_code || 'Sạch không KS'}</strong></td>
                    <td>${cvBadge}</td>
                    <td>${pkBadge}</td>
                </tr>
            `;
        });
        
        if (elements.mixerSequenceTbody) {
            elements.mixerSequenceTbody.innerHTML = html;
        }
        if (elements.dbMixerSequenceTbody) {
            elements.dbMixerSequenceTbody.innerHTML = html;
        }
        
        // Kích hoạt filter vật nuôi
        initAnimalFilters();
    }
    
    // ============================================================
    // FILTER VẬT NUÔI - Lọc bảng Mixer Sequence theo loại vật nuôi
    // ============================================================
    function initAnimalFilters() {
        document.querySelectorAll('.animal-filter-bar').forEach(bar => {
            bar.querySelectorAll('.animal-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    // Toggle active
                    bar.querySelectorAll('.animal-btn').forEach(b => b.classList.remove('active'));
                    this.classList.add('active');
                    
                    const animal = this.dataset.animal;
                    
                    // Tìm bảng tbody gần nhất (cùng panel)
                    const panel = bar.closest('.dashboard-subtab-panel, .result-details-card, .glass-card');
                    if (!panel) return;
                    const tbody = panel.querySelector('tbody');
                    if (!tbody) return;
                    
                    tbody.querySelectorAll('tr').forEach(row => {
                        if (animal === 'all') {
                            row.style.display = '';
                        } else {
                            row.style.display = row.dataset.animal === animal ? '' : 'none';
                        }
                    });
                });
            });
        });
    }

    // ============================================================
    // BẢNG KẾ HOẠCH SẢN XUẤT - Giống Excel KHSX
    // ============================================================
    function renderProductionPlanTable(seq, dateStr, containerId = 'production-plan-container') {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        // Tính tổng
        let totalBatches = 0, totalTons = 0;
        let sum_higro_25 = 0, sum_higro_40 = 0;
        let sum_cp_25 = 0, sum_cp_40 = 0;
        let sum_star_25 = 0, sum_star_40 = 0;
        let sum_nuvo_25 = 0, sum_nuvo_40 = 0;
        let sum_bell_25 = 0, sum_bell_40 = 0;
        let sum_nasa_25 = 0, sum_nasa_40 = 0;
        let sum_white_25 = 0, sum_white_40 = 0, sum_white_50 = 0;
        let sum_silo = 0;

        seq.forEach(it => { 
            totalBatches += Number(it.batches) || 0; 
            totalTons += Number(it.tons) || 0; 
            sum_higro_25 += Number(it.higro_25) || 0;
            sum_higro_40 += Number(it.higro_40) || 0;
            sum_cp_25 += Number(it.cp_25) || 0;
            sum_cp_40 += Number(it.cp_40) || 0;
            sum_star_25 += Number(it.star_25) || 0;
            sum_star_40 += Number(it.star_40) || 0;
            sum_nuvo_25 += Number(it.nuvo_25) || 0;
            sum_nuvo_40 += Number(it.nuvo_40) || 0;
            sum_bell_25 += Number(it.bell_25) || 0;
            sum_bell_40 += Number(it.bell_40) || 0;
            sum_nasa_25 += Number(it.nasa_25) || 0;
            sum_nasa_40 += Number(it.nasa_40) || 0;
            sum_white_25 += Number(it.white_25) || 0;
            sum_white_40 += Number(it.white_40) || 0;
            sum_white_50 += Number(it.white_50) || 0;
            sum_silo += Number(it.silo_truck) || 0;
        });
        
        // Helper: hiển thị số, bỏ qua 0, làm tròn 1 chữ số thập phân
        const n = (v) => { const x = Number(v) || 0; return x > 0 ? parseFloat(x.toFixed(1)) : ''; };
        
        let html = `
        <div class="khsx-excel-wrapper">
            <div class="khsx-excel-header">
                <div class="khsx-company">CÔNG TY CỔ PHẦN CHĂN NUÔI C.P. VIỆT NAM<br><small>Chi Nhánh Tại Bình Dương - Phòng Sản Xuất</small></div>
                <div class="khsx-title">KẾ HOẠCH SẢN XUẤT</div>
                <div class="khsx-date">Ngày: ${dateStr}</div>
            </div>
            <div class="table-scroll-container" style="max-height: none;">
                <table class="khsx-excel-table">
                    <thead>
                        <tr class="khsx-group-header">
                            <th rowspan="2" style="width:3%">STT</th>
                            <th rowspan="2" style="width:7%">TÊN CÁM</th>
                            <th rowspan="2" style="width:3%">KH<br>MẺ</th>
                            <th rowspan="2" style="width:4%">TỔNG<br>TẤN</th>
                            <th colspan="2">HIGRO</th>
                            <th colspan="2">CP</th>
                            <th colspan="2">STAR FEED</th>
                            <th colspan="2">NUVO</th>
                            <th colspan="2">BELL</th>
                            <th colspan="2">NASA</th>
                            <th colspan="3">WHITE BAG</th>
                            <th rowspan="2" style="width:3%">SILO<br>TRUCK</th>
                            <th rowspan="2" style="width:11%">KHÁNG SINH (KS)<br>HOẠT CHẤT (HC)</th>
                            <th rowspan="2" style="width:4%">CÁM VIÊN<br>(LINE SỐ)</th>
                            <th rowspan="2" style="width:4%">ĐÓNG BAO<br>(LINE SỐ)</th>
                        </tr>
                        <tr class="khsx-sub-header">
                            <th>25KG</th><th>40KG</th>
                            <th>25KG</th><th>40KG</th>
                            <th>25KG</th><th>40KG</th>
                            <th>25KG</th><th>40KG</th>
                            <th>25KG</th><th>40KG</th>
                            <th>25KG</th><th>40KG</th>
                            <th>25KG</th><th>40KG</th><th>50KG</th>
                        </tr>
                    </thead>
                    <tbody>`;
        
        seq.forEach((item, idx) => {
            const isMedicated = item.ks_code && item.ks_code !== 'Sạch không KS' && item.ks_code !== 'SẠCH (KHÔNG KS)';
            const ksClass = isMedicated ? 'khsx-medicated' : '';
            
            let cvText = item.line_cv || '';
            if (cvText === 'None') cvText = '';
            let pkText = item.line_pk || '';
            if (pkText === 'None') pkText = '';
            
            html += `
                <tr class="${ksClass}">
                    <td class="khsx-stt">${idx + 1}</td>
                    <td class="khsx-code"><strong>${item.product_code}</strong></td>
                    <td class="khsx-num">${item.batches}</td>
                    <td class="khsx-num"><strong>${parseFloat(Number(item.tons).toFixed(1))}</strong></td>
                    <td class="khsx-num">${n(item.higro_25)}</td>
                    <td class="khsx-num">${n(item.higro_40)}</td>
                    <td class="khsx-num">${n(item.cp_25)}</td>
                    <td class="khsx-num">${n(item.cp_40)}</td>
                    <td class="khsx-num">${n(item.star_25)}</td>
                    <td class="khsx-num">${n(item.star_40)}</td>
                    <td class="khsx-num">${n(item.nuvo_25)}</td>
                    <td class="khsx-num">${n(item.nuvo_40)}</td>
                    <td class="khsx-num">${n(item.bell_25)}</td>
                    <td class="khsx-num">${n(item.bell_40)}</td>
                    <td class="khsx-num">${n(item.nasa_25)}</td>
                    <td class="khsx-num">${n(item.nasa_40)}</td>
                    <td class="khsx-num">${n(item.white_25)}</td>
                    <td class="khsx-num">${n(item.white_40)}</td>
                    <td class="khsx-num">${n(item.white_50)}</td>
                    <td class="khsx-num khsx-silo">${n(item.silo_truck)}</td>
                    <td class="khsx-ks" style="color:${isMedicated ? '#c084fc' : '#34d399'};">${item.ks_code || 'Sạch'}</td>
                    <td class="khsx-line">${cvText}</td>
                    <td class="khsx-line">${pkText || (Number(item.silo_truck) > 0 ? 'SILO' : '')}</td>
                </tr>`;
        });
        
        html += `
                        <tr class="khsx-total-row">
                            <td colspan="2"><strong>TỔNG (TOTAL)</strong></td>
                            <td class="khsx-num"><strong>${totalBatches}</strong></td>
                            <td class="khsx-num"><strong>${parseFloat(totalTons.toFixed(1))}</strong></td>
                            <td class="khsx-num"><strong>${n(sum_higro_25)}</strong></td>
                            <td class="khsx-num"><strong>${n(sum_higro_40)}</strong></td>
                            <td class="khsx-num"><strong>${n(sum_cp_25)}</strong></td>
                            <td class="khsx-num"><strong>${n(sum_cp_40)}</strong></td>
                            <td class="khsx-num"><strong>${n(sum_star_25)}</strong></td>
                            <td class="khsx-num"><strong>${n(sum_star_40)}</strong></td>
                            <td class="khsx-num"><strong>${n(sum_nuvo_25)}</strong></td>
                            <td class="khsx-num"><strong>${n(sum_nuvo_40)}</strong></td>
                            <td class="khsx-num"><strong>${n(sum_bell_25)}</strong></td>
                            <td class="khsx-num"><strong>${n(sum_bell_40)}</strong></td>
                            <td class="khsx-num"><strong>${n(sum_nasa_25)}</strong></td>
                            <td class="khsx-num"><strong>${n(sum_nasa_40)}</strong></td>
                            <td class="khsx-num"><strong>${n(sum_white_25)}</strong></td>
                            <td class="khsx-num"><strong>${n(sum_white_40)}</strong></td>
                            <td class="khsx-num"><strong>${n(sum_white_50)}</strong></td>
                            <td class="khsx-num khsx-silo"><strong>${n(sum_silo)}</strong></td>
                            <td colspan="3"></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>`;
        
        container.innerHTML = html;
    }

    function renderPelletLinesTimeline(plPlans, dateStr, plRichPlans = null, mashPlanRich = null, mixerSummaryRich = null, khplRawGrid = null) {
        elements.plMetaInfo.textContent = `Hiển thị phân bổ Pellet Lines cho kế hoạch ngày ${dateStr}`;
        
        if (khplRawGrid && khplRawGrid.length > 0) {
            // Render exact-match Excel-style table
            const renderTable = (gridEl, isForDashboard) => {
                if (!gridEl) return;
                gridEl.innerHTML = '';
                
                const wrapper = document.createElement('div');
                wrapper.className = 'khsx-excel-wrapper w-100 col-span-3';
                
                const headerDiv = document.createElement('div');
                headerDiv.className = 'khsx-excel-header';
                headerDiv.innerHTML = `
                    <div class="khsx-company">CÔNG TY CỔ PHẦN CHĂN NUÔI C.P. VIỆT NAM<br><small>Chi Nhánh Tại Bình Dương - Lập kế hoạch Pellet Lines</small></div>
                    <div class="khsx-title" style="letter-spacing:1px; font-size:1.1rem;">KẾ HOẠCH MÁY ÉP PELLET MILL & MASH</div>
                    <div class="khsx-date">Ngày: ${dateStr}</div>
                `;
                wrapper.appendChild(headerDiv);
                
                const scrollContainer = document.createElement('div');
                scrollContainer.className = 'table-scroll-container x-scrollable';
                
                const table = document.createElement('table');
                table.className = 'khsx-excel-table premium-table compact';
                
                let tbodyHtml = '';
                
                khplRawGrid.forEach((row, rowIdx) => {
                    const rowNum = rowIdx + 1;
                    let rowClass = '';
                    let rowLabel = row[0] ? String(row[0]).toUpperCase() : '';
                    
                    if (rowNum === 1) {
                        rowClass = 'khpl-row-title';
                    } else if (rowNum === 2) {
                        rowClass = 'khpl-row-header';
                    } else if (rowLabel.includes('TỒN ĐẦU') || rowNum === 3 || rowNum === 4) {
                        rowClass = 'khpl-row-tondau';
                    } else if (rowLabel.includes('CA 1') || (rowNum >= 5 && rowNum <= 8)) {
                        rowClass = 'khpl-row-ca1';
                    } else if (rowLabel.includes('CA 2') || (rowNum >= 9 && rowNum <= 12)) {
                        rowClass = 'khpl-row-ca2';
                    } else if (rowLabel.includes('CA 3') || (rowNum >= 13 && rowNum <= 16)) {
                        rowClass = 'khpl-row-ca3';
                    } else if (rowLabel.includes('LOSS') || rowLabel.includes('NGƯNG') || rowNum === 17 || rowNum === 18) {
                        rowClass = 'khpl-row-loss';
                    } else if (rowLabel.includes('NEXT') || rowNum === 19 || rowNum === 20) {
                        rowClass = 'khpl-row-next';
                    } else if (rowLabel.includes('TARGET') || rowNum === 21 || rowNum === 22) {
                        rowClass = 'khpl-row-target';
                    } else if (rowLabel.includes('PLAN PL') || rowNum === 23 || rowNum === 24) {
                        rowClass = 'khpl-row-plan';
                    } else {
                        rowClass = 'khpl-row-mx';
                    }
                    
                    tbodyHtml += `<tr class="${rowClass}">`;
                    
                    row.forEach((cellVal, colIdx) => {
                        let displayVal = cellVal !== null && cellVal !== undefined ? String(cellVal) : '';
                        
                        if (displayVal !== '' && !isNaN(displayVal)) {
                            const num = Number(displayVal);
                            displayVal = num % 1 === 0 ? num.toString() : num.toFixed(1);
                        }
                        
                        if (displayVal === 'C.DIE' || displayVal === 'LOSS') {
                            displayVal = `<span class="badge badge-danger" style="font-size:0.6rem; padding: 0.1rem 0.25rem;">${displayVal}</span>`;
                        }
                        
                        const isProductCode = /^[1-9][0-9]{2}[A-Z0-9]*$/.test(displayVal) || ['550SF', '552F', '552SF', '540F', '566F', '567SF', '6924', '511', '511L', '550SFS31', '567SFS25', '552FS90', '552S', '511NFP35', '6995', '553MF', '552E', '991-18', '513F', '524A', '551FS31', '551GPFS13', '511ANFP92', '6952', '553', 'GT12AS', '567SFS31', '552M', '502', '551', '521SNPRO', '521SPRO', '510S', 'GT11S', '510', '552SXS88', 'BS07TA'].includes(displayVal);
                        if (isProductCode) {
                            const isMed = displayVal.includes('F') || displayVal.includes('SF') || displayVal.includes('S') || displayVal.includes('MF') || displayVal.includes('M') || displayVal.includes('PRO');
                            const medColor = isMed ? 'var(--purple)' : 'var(--cyan)';
                            displayVal = `<strong style="color:${medColor}; font-size:0.75rem;">${displayVal}</strong>`;
                        }
                        
                        let alignClass = 'text-center';
                        if (colIdx === 0) {
                            alignClass = 'text-left font-bold font-display';
                        }
                        
                        tbodyHtml += `<td class="${alignClass}">${displayVal}</td>`;
                    });
                    
                    tbodyHtml += `</tr>`;
                });
                
                table.innerHTML = `<tbody>${tbodyHtml}</tbody>`;
                scrollContainer.appendChild(table);
                wrapper.appendChild(scrollContainer);
                gridEl.appendChild(wrapper);
            };
            
            renderTable(elements.pelletLinesMainGrid, false);
            if (elements.dbPelletLinesGrid) {
                renderTable(elements.dbPelletLinesGrid, true);
            }
        } else {
            // Render original timeline cards as fallback
            const renderGrid = (gridEl, isForDashboard) => {
                if (!gridEl) return;
                gridEl.innerHTML = '';
                
                const lines = Object.keys(plPlans);
                
                lines.forEach(lineName => {
                    const items = plPlans[lineName];
                    const totalTons = items.reduce((sum, it) => sum + Number(it.tons), 0).toFixed(1);
                    const totalBatches = items.reduce((sum, it) => sum + Number(it.batches), 0);
                    
                    const card = document.createElement('div');
                    const colSpan = isForDashboard ? 'col-span-1' : 'col-span-3';
                    card.className = `bento-card ${colSpan} glass-card pl-card`;
                    
                    const rowDiv = document.createElement('div');
                    rowDiv.className = 'pl-row';
                    
                    const laneDiv = document.createElement('div');
                    laneDiv.className = 'pl-lane';
                    
                    laneDiv.innerHTML = `
                        <div class="pl-lane-header">
                            <span class="pl-lane-name">${lineName}</span>
                            <span class="pl-lane-summary">${totalTons} Tấn / ${totalBatches} Mẻ</span>
                        </div>
                    `;
                    
                    const blocksContainer = document.createElement('div');
                    blocksContainer.className = 'pl-blocks-container';
                    
                    if (items.length === 0) {
                        blocksContainer.innerHTML = `
                            <span class="text-muted" style="font-size: 0.75rem; padding-left: 1rem; font-style: italic;">Trống (Không chạy sản phẩm)</span>
                        `;
                    } else {
                        items.forEach(it => {
                            const block = document.createElement('div');
                            const isMedicated = it.ks_code && it.ks_code !== 'Sạch không KS';
                            block.className = `pl-item-block ${isMedicated ? 'ks-medicated' : 'ks-clean'}`;
                            block.title = `Sản phẩm: ${it.product_code}\nSản lượng: ${it.tons} tấn / ${it.batches} mẻ\nKháng sinh: ${it.ks_code || 'Sạch'}`;
                            
                            block.innerHTML = `
                                <span class="pl-block-prod">${it.product_code}</span>
                                <div class="pl-block-meta">
                                    <span>${it.tons}T</span>
                                    <span>${it.batches}M</span>
                                </div>
                            `;
                            blocksContainer.appendChild(block);
                        });
                    }
                    
                    laneDiv.appendChild(blocksContainer);
                    rowDiv.appendChild(laneDiv);
                    card.appendChild(rowDiv);
                    gridEl.appendChild(card);
                });
            };
            
            renderGrid(elements.pelletLinesMainGrid, false);
            if (elements.dbPelletLinesGrid) {
                renderGrid(elements.dbPelletLinesGrid, true);
            }
        }
    }

    function renderPackagingMatrix(packList) {
        let html = '';
        
        if (packList.length === 0) {
            html = `
                <tr>
                    <td colspan="13" class="text-center py-5 text-muted">Không có dữ liệu phân bổ đóng bao nào trong ngày này.</td>
                </tr>
            `;
        } else {
            packList.forEach(row => {
                const size = row.packing_size;
                
                // Map Brand bag allocation dynamically based on the current product packaging size (25kg vs 40kg)
                const is40 = (size && size.includes('40'));
                const higro = is40 ? (row.higro_40 || 0) : (row.higro_25 || 0);
                const cp = is40 ? (row.cp_40 || 0) : (row.cp_25 || 0);
                const star = is40 ? (row.star_40 || 0) : (row.star_25 || 0);
                const nuvo = is40 ? (row.nuvo_40 || 0) : (row.nuvo_25 || 0);
                const nasa = is40 ? (row.nasa_40 || 0) : (row.nasa_25 || 0);
                const bell = is40 ? (row.bell_40 || 0) : (row.bell_25 || 0);
                
                const w25 = row.white_25 || 0;
                const w40 = row.white_40 || 0;
                const w50 = row.white_50 || 0;
    
                const formatCell = (val, isWhite = false) => {
                    if (val === 0) return '<td class="zero-val">-</td>';
                    const cls = isWhite ? 'active-val-white' : 'active-val';
                    return `<td class="${cls}"><strong>${val.toLocaleString('vi-VN')}</strong></td>`;
                };

                // Xử lý hiển thị Quy cách đóng gói thông minh
                let packingText = size;
                let badgeClass = 'badge-success';
                if (packingText === 'M') {
                    packingText = 'Silo';
                    badgeClass = 'badge-warning';
                } else if (packingText === '25' || packingText === '40' || packingText === '50') {
                    packingText = 'Bao ' + packingText;
                    if (packingText === 'Bao 50') {
                        badgeClass = 'badge-warning';
                    }
                } else {
                    badgeClass = 'badge-info'; // Quy cách ghép "Silo + Bao 50"
                }

                // Badge cho Line Đóng Bao
                let pkBadge = '-';
                if (row.line_pk && row.line_pk !== 'None') {
                    if (row.line_pk.toUpperCase() === 'SILO') {
                        pkBadge = `<span class="badge badge-danger">SILO</span>`;
                    } else {
                        pkBadge = `<span class="badge badge-warning">Line ${row.line_pk}</span>`;
                    }
                }
    
                html += `
                    <tr>
                        <td><strong>${row.product_code}</strong></td>
                        <td><strong>${row.tons}</strong></td>
                        <td><span class="badge ${badgeClass}">${packingText}</span></td>
                        <td>${pkBadge}</td>
                        
                        ${formatCell(higro)}
                        ${formatCell(cp)}
                        ${formatCell(star)}
                        ${formatCell(nuvo)}
                        ${formatCell(nasa)}
                        ${formatCell(bell)}
                        
                        ${formatCell(w25, true)}
                        ${formatCell(w40, true)}
                        ${formatCell(w50, true)}
                    </tr>
                `;
            });
        }
        
        if (elements.packagingMatrixTbody) {
            elements.packagingMatrixTbody.innerHTML = html;
        }
        if (elements.dbPackagingMatrixTbody) {
            elements.dbPackagingMatrixTbody.innerHTML = html;
        }
    }

    async function initAutoPlanDetection() {
        try {
            appendTerminalLine("🔍 Đang quét dữ liệu để tự động tìm ngày KHSX tiếp theo...", "text-muted");
            const res = await fetch('/api/latest-target-date');
            const json = await res.json();
            
            if (json.success) {
                // Gán ngày mục tiêu (YYYY-MM-DD) vào ô input
                elements.planTargetDate.value = json.target_date_iso;
                
                if (json.has_existing_plan) {
                    appendTerminalLine(`📅 Phát hiện file kế hoạch sẵn có: ${json.existing_plan_filename} cho ngày mục tiêu ${json.target_date}.`, 'text-success');
                    appendTerminalLine(`🔄 Đang tự động nạp kế hoạch lên giao diện...`, 'text-success');
                    
                    // Nạp dữ liệu hiển thị
                    await loadPlanResults(json.target_date);
                    
                    showToast(`Tự động nạp thành công kế hoạch ngày ${json.target_date}!`, 'success');
                } else {
                    if (elements.btnGlobalExportExcel) {
                        elements.btnGlobalExportExcel.style.display = 'none';
                    }
                    appendTerminalLine(`⚠️ Chưa lập kế hoạch sản xuất cho ngày mục tiêu ${json.target_date} (sau ngày dữ liệu ${json.data_date} 1 ngày).`, 'text-warning');
                    appendTerminalLine(`👉 Vui lòng nhấn nút "BẮT ĐẦU TÍNH KHSX TỰ ĐỘNG" để khởi tạo kế hoạch.`, 'text-warning');
                }
            } else {
                console.error("latest-target-date error:", json.message);
                appendTerminalLine(`⚠️ Không thể tự động phát hiện ngày lập kế hoạch: ${json.message}`, 'text-warning');
            }
        } catch (err) {
            console.error("initAutoPlanDetection failed:", err);
            appendTerminalLine(`❌ Lỗi kết nối hệ thống khi kiểm tra ngày lập kế hoạch tự động.`, 'text-error');
        }
    }

    // ----------------------------------------------------------------------
    // 11. INGEST & STARTUP TRIGGER
    // ----------------------------------------------------------------------
    // Dashboard plan subtabs navigation switching logic
    const subtabBtns = document.querySelectorAll('.subtab-btn');
    const subtabPanels = document.querySelectorAll('.dashboard-subtab-panel');
    subtabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = btn.getAttribute('data-dashboard-tab');
            subtabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            subtabPanels.forEach(p => {
                if (p.id === `${target}-panel`) {
                    p.classList.add('active');
                    p.style.display = 'block';
                } else {
                    p.classList.remove('active');
                    p.style.display = 'none';
                }
            });
        });
    });

    loadDataSourcesStatus();
    initAutoPlanDetection();
});
