import sys
import json
import os
import psutil
from datetime import datetime

print("[GUI] 正在初始化 PyQt6...", file=sys.stderr)

try:
    from PyQt6 import QtWidgets, QtCore, QtGui
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    import matplotlib
    matplotlib.rcParams['font.family'] = 'sans-serif'
    matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    matplotlib.rcParams['axes.unicode_minus'] = False
    print("[GUI] ✅ PyQt6 和 Matplotlib 載入成功", file=sys.stderr)
except ImportError as e:
    print(f"[GUI] ❌ 缺少依賴: {e}", file=sys.stderr)
    print(f"[GUI] 請執行: pip install PyQt6 matplotlib psutil", file=sys.stderr)
    sys.exit(1)

PROJECT_DIR = os.path.dirname(__file__)
USER_DATA = os.path.join(PROJECT_DIR, 'user_data.json')
LOG_DIR = os.path.join(PROJECT_DIR, 'logs')


class MonitorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        print("[GUI] 正在創建主視窗...", file=sys.stderr)
        super().__init__()
        self.setWindowTitle('subaso 🤖 管理監控面板')
        self.resize(1400, 900)
        self.start_time = datetime.now()
        print("[GUI] ✅ 主視窗基礎設置完成", file=sys.stderr)
        
        # 設置樣式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 9pt;
                border: 1px solid #ccc;
            }
        """)

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        
        # 建立 Tab 頁面
        self.tabs = QtWidgets.QTabWidget()
        layout.addWidget(self.tabs)
        
        # Tab 1: 概況儀錶板
        self.tab_dashboard = self.create_dashboard_tab()
        self.tabs.addTab(self.tab_dashboard, '📊 概況')
        
        # Tab 2: 用戶統計
        self.tab_stats = self.create_stats_tab()
        self.tabs.addTab(self.tab_stats, '📈 統計')
        
        # Tab 3: 系統信息
        self.tab_system = self.create_system_tab()
        self.tabs.addTab(self.tab_system, '⚙️ 系統')
        
        # Tab 4: 日誌
        self.tab_logs = self.create_logs_tab()
        self.tabs.addTab(self.tab_logs, '📝 日誌')
        
        # 底部按鈕
        btn_layout = QtWidgets.QHBoxLayout()
        
        self.refresh_btn = QtWidgets.QPushButton('🔄 重新整理')
        self.refresh_btn.clicked.connect(self.refresh)
        self.refresh_btn.setFixedWidth(120)
        btn_layout.addWidget(self.refresh_btn)
        
        self.open_logs_btn = QtWidgets.QPushButton('📂 開啟日誌資料夾')
        self.open_logs_btn.clicked.connect(self.open_log_folder)
        self.open_logs_btn.setFixedWidth(150)
        btn_layout.addWidget(self.open_logs_btn)
        
        btn_layout.addStretch()
        
        self.auto_refresh = QtWidgets.QCheckBox('自動重新整理 (5秒)')
        self.auto_refresh.stateChanged.connect(self.toggle_auto_refresh)
        btn_layout.addWidget(self.auto_refresh)
        
        layout.addLayout(btn_layout)
        
        # 計時器用於自動刷新
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.refresh)
        
        self.refresh()
        print("[GUI] ✅ 視窗初始化完成，準備顯示", file=sys.stderr)

    def create_dashboard_tab(self):
        """建立概況儀錶板"""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        
        # 統計卡片區
        cards_layout = QtWidgets.QHBoxLayout()
        
        self.card_users = self.create_stat_card('👥 活躍用戶', '0', '#4CAF50')
        self.card_personalities = self.create_stat_card('🎭 角色', '0', '#2196F3')
        self.card_languages = self.create_stat_card('🌍 語言', '0', '#FF9800')
        self.card_uptime = self.create_stat_card('⏱️ 運行時間', '--:--:--', '#9C27B0')
        
        cards_layout.addWidget(self.card_users)
        cards_layout.addWidget(self.card_personalities)
        cards_layout.addWidget(self.card_languages)
        cards_layout.addWidget(self.card_uptime)
        
        layout.addLayout(cards_layout)
        
        # 圖表區
        charts_layout = QtWidgets.QHBoxLayout()
        
        # 角色分佈圓餅圖
        self.figure_pie = Figure(figsize=(4, 3), dpi=100)
        self.canvas_pie = FigureCanvas(self.figure_pie)
        charts_layout.addWidget(self.canvas_pie)
        
        # 語言分佈長條圖
        self.figure_bar = Figure(figsize=(4, 3), dpi=100)
        self.canvas_bar = FigureCanvas(self.figure_bar)
        charts_layout.addWidget(self.canvas_bar)
        
        layout.addLayout(charts_layout)
        
        return widget

    def create_stats_tab(self):
        """建立統計頁面"""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        
        # 詳細統計表格
        self.stats_table = QtWidgets.QTableWidget()
        self.stats_table.setColumnCount(3)
        self.stats_table.setHorizontalHeaderLabels(['統計項目', '值', '備註'])
        self.stats_table.horizontalHeader().setStretchLastSection(True)
        self.stats_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #ddd;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                border: none;
            }
        """)
        layout.addWidget(self.stats_table)
        
        return widget

    def create_system_tab(self):
        """建立系統信息頁面"""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        
        # 系統信息標籤
        self.system_label = QtWidgets.QLabel('載入中...')
        self.system_label.setStyleSheet("""
            QLabel {
                font-family: 'Consolas', monospace;
                font-size: 10pt;
                background-color: white;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.system_label)
        
        # CPU 和記憶體圖表
        chart_layout = QtWidgets.QHBoxLayout()
        
        self.figure_cpu = Figure(figsize=(4, 3), dpi=100)
        self.canvas_cpu = FigureCanvas(self.figure_cpu)
        chart_layout.addWidget(self.canvas_cpu)
        
        self.figure_mem = Figure(figsize=(4, 3), dpi=100)
        self.canvas_mem = FigureCanvas(self.figure_mem)
        chart_layout.addWidget(self.canvas_mem)
        
        layout.addLayout(chart_layout)
        
        return widget

    def create_logs_tab(self):
        """建立日誌頁面"""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        
        # 日誌篩選
        filter_layout = QtWidgets.QHBoxLayout()
        filter_layout.addWidget(QtWidgets.QLabel('篩選級別:'))
        
        self.log_filter = QtWidgets.QComboBox()
        self.log_filter.addItems(['全部', 'INFO', 'WARNING', 'ERROR', 'DEBUG'])
        self.log_filter.currentTextChanged.connect(self.refresh)
        filter_layout.addWidget(self.log_filter)
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)
        
        # 日誌顯示
        self.log_text = QtWidgets.QPlainTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text, 1)
        
        return widget

    def create_stat_card(self, title, value, color):
        """建立統計卡片"""
        card = QtWidgets.QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        card.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet('color: white; font-size: 12pt; font-weight: bold;')
        
        value_label = QtWidgets.QLabel(value)
        value_label.setStyleSheet('color: white; font-size: 24pt; font-weight: bold;')
        value_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        card.value_label = value_label  # 保存引用方便更新
        return card

    def toggle_auto_refresh(self):
        if self.auto_refresh.isChecked():
            self.timer.start(5000)  # 每 5 秒刷新
        else:
            self.timer.stop()

    def refresh(self):
        """刷新所有數據"""
        # 加載用戶數據
        users = {}
        personalities = {}
        languages = {}
        lang_counts = {}
        
        if os.path.exists(USER_DATA):
            try:
                with open(USER_DATA, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    users = data.get('personalities', {})
                    personalities = {v: list(users.values()).count(v) for v in set(users.values()) if v}
                    languages = data.get('languages', {})
                    lang_counts = {v: list(languages.values()).count(v) for v in set(languages.values()) if v}
            except Exception as e:
                print(f'讀取數據失敗: {e}')
        
        # 更新概況卡片
        self.card_users.value_label.setText(str(len(users)))
        self.card_personalities.value_label.setText(str(len(personalities)))
        self.card_languages.value_label.setText(str(len(lang_counts)))
        
        # 計算運行時間
        uptime = datetime.now() - self.start_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        self.card_uptime.value_label.setText(f'{hours:02d}:{minutes:02d}:{seconds:02d}')
        
        # 更新圖表
        self.update_charts(personalities, lang_counts)
        
        # 更新統計表格
        self.update_stats_table(users, personalities, languages)
        
        # 更新系統信息
        self.update_system_info()
        
        # 更新日誌
        self.update_logs()

    def update_charts(self, personalities, languages):
        """更新圖表"""
        # 角色分佈圓餅圖
        self.figure_pie.clear()
        ax_pie = self.figure_pie.add_subplot(111)
        
        if personalities:
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
            ax_pie.pie(personalities.values(), labels=personalities.keys(), autopct='%1.1f%%',
                      colors=colors[:len(personalities)], startangle=90)
            ax_pie.set_title('🎭 角色分佈', fontsize=12, fontweight='bold')
        else:
            ax_pie.text(0.5, 0.5, '沒有數據', ha='center', va='center')
        
        self.canvas_pie.draw()
        
        # 語言分佈長條圖
        self.figure_bar.clear()
        ax_bar = self.figure_bar.add_subplot(111)
        
        if languages:
            ax_bar.bar(languages.keys(), languages.values(), color='#4CAF50', alpha=0.8)
            ax_bar.set_ylabel('用戶數', fontweight='bold')
            ax_bar.set_title('🌍 語言分佈', fontsize=12, fontweight='bold')
            ax_bar.tick_params(axis='x', rotation=45)
        else:
            ax_bar.text(0.5, 0.5, '沒有數據', ha='center', va='center')
        
        self.figure_bar.tight_layout()
        self.canvas_bar.draw()

    def update_stats_table(self, users, personalities, languages):
        """更新統計表格"""
        self.stats_table.setRowCount(0)
        
        stats = [
            ('總用戶數', len(users), ''),
            ('已配置角色', len(personalities), f"{', '.join(personalities.keys()) if personalities else '無'}"),
            ('已配置語言', len(languages), f"{', '.join(set(languages.values())) if languages else '無'}"),
        ]
        
        for i, (item, value, remark) in enumerate(stats):
            self.stats_table.insertRow(i)
            self.stats_table.setItem(i, 0, QtWidgets.QTableWidgetItem(item))
            self.stats_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(value)))
            self.stats_table.setItem(i, 2, QtWidgets.QTableWidgetItem(remark))

    def update_system_info(self):
        """更新系統信息"""
        try:
            import platform
            cpu_percent = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            process = psutil.Process(os.getpid())
            proc_mem = process.memory_info().rss / 1024 / 1024  # MB
            
            info = f"""
系統信息 (GUI 進程):

• 操作系統: {platform.system()} {platform.release()}
• Python 版本: {platform.python_version()}
• 處理器: {platform.processor()}

資源使用:
• CPU 使用率: {cpu_percent}%
• 系統記憶體: {mem.percent}% ({mem.used // (1024**3)}GB / {mem.total // (1024**3)}GB)
• GUI 進程記憶體: {proc_mem:.2f} MB
• GUI 進程 CPU: {process.cpu_percent(interval=0.1):.2f}%

更新時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            self.system_label.setText(info)
            
            # 更新 CPU 和內存圖表
            self.figure_cpu.clear()
            ax_cpu = self.figure_cpu.add_subplot(111)
            ax_cpu.barh(['CPU'], [cpu_percent], color='#FF6B6B', alpha=0.8)
            ax_cpu.set_xlim(0, 100)
            ax_cpu.set_xlabel('使用率 (%)', fontweight='bold')
            ax_cpu.set_title('CPU 使用率', fontsize=11, fontweight='bold')
            ax_cpu.text(cpu_percent + 2, 0, f'{cpu_percent:.1f}%', va='center')
            self.canvas_cpu.draw()
            
            self.figure_mem.clear()
            ax_mem = self.figure_mem.add_subplot(111)
            ax_mem.barh(['記憶體'], [mem.percent], color='#4CAF50', alpha=0.8)
            ax_mem.set_xlim(0, 100)
            ax_mem.set_xlabel('使用率 (%)', fontweight='bold')
            ax_mem.set_title('記憶體使用率', fontsize=11, fontweight='bold')
            ax_mem.text(mem.percent + 2, 0, f'{mem.percent:.1f}%', va='center')
            self.canvas_mem.draw()
        except Exception as e:
            self.system_label.setText(f'讀取系統信息失敗: {e}')

    def update_logs(self):
        """更新日誌顯示"""
        if not os.path.isdir(LOG_DIR):
            self.log_text.setPlainText('日誌目錄不存在')
            return
        
        files = [os.path.join(LOG_DIR, f) for f in os.listdir(LOG_DIR) if f.endswith('.log')]
        if not files:
            self.log_text.setPlainText('找不到日誌檔')
            return
        
        latest = max(files, key=os.path.getmtime)
        
        try:
            with open(latest, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
                
            filter_level = self.log_filter.currentText()
            if filter_level != '全部':
                lines = [l for l in lines if filter_level in l]
            
            tail = '\n'.join(lines[-300:])
            self.log_text.setPlainText(tail)
        except Exception as e:
            self.log_text.setPlainText(f'讀取日誌失敗: {e}')

    def open_log_folder(self):
        """打開日誌資料夾"""
        if os.path.isdir(LOG_DIR):
            path = os.path.abspath(LOG_DIR)
            if sys.platform.startswith('win'):
                os.startfile(path)
            elif sys.platform.startswith('darwin'):
                subprocess.Popen(['open', path])
            else:
                subprocess.Popen(['xdg-open', path])


def main():
    print("[GUI] 正在啟動應用程式...", file=sys.stderr)
    try:
        app = QtWidgets.QApplication(sys.argv)
        print("[GUI] ✅ QApplication 創建成功", file=sys.stderr)
        
        w = MonitorWindow()
        print("[GUI] ✅ 視窗創建成功", file=sys.stderr)
        
        w.show()
        print("[GUI] ✅ 視窗已顯示", file=sys.stderr)
        print("[GUI] 🎉 subaso GUI 監控面板已啟動！", file=sys.stderr)
        
        sys.exit(app.exec())
    except Exception as e:
        print(f"[GUI] ❌ GUI 啟動失敗: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
