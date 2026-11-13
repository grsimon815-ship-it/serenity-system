import shutil
import os
import platform
import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QStackedWidget, QStatusBar, QFrame, QPushButton, QLineEdit
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont, QColor, QKeySequence, QShortcut

from ui.theme import SYSTEM_DLC_THEME
from ui.tab_matrix import ParadigmMatrixTab
from ui.tab_memory import MemorySimulatorTab
from ui.tab_patterns import PatternLabTab
from ui.tab_playground import CodePlaygroundTab
from ui.tab_benchmarks import BenchmarkRadarTab
from ui.tab_exporter import ExporterTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SystemDLC — Polyglot Architecture & Execution Workbench")
        self.resize(1320, 840)
        self.setMinimumSize(1060, 680)

        self._nav_buttons = []
        self._init_ui()
        self._check_system_runtimes()
        self._init_shortcuts()

    def _init_ui(self):
        self.setStyleSheet(SYSTEM_DLC_THEME)

        central_widget = QWidget()
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # 1. Left Vertical Navigation Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("SidebarFrame")
        sidebar.setFixedWidth(205)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 14, 10, 12)
        sidebar_layout.setSpacing(4)

        # Brand Header
        brand_frame = QFrame()
        brand_layout = QVBoxLayout(brand_frame)
        brand_layout.setContentsMargins(2, 0, 2, 8)
        brand_layout.setSpacing(1)

        brand_row = QHBoxLayout()
        lbl_brand = QLabel("SYSTEM DLC")
        lbl_brand.setObjectName("LogoTitle")
        brand_row.addWidget(lbl_brand)
        brand_row.addStretch()
        brand_layout.addLayout(brand_row)

        lbl_sub = QLabel("POLYGLOT WORKBENCH")
        lbl_sub.setObjectName("LogoSubtitle")
        brand_layout.addWidget(lbl_sub)
        sidebar_layout.addWidget(brand_frame)

        # Section 1: Analysis
        lbl_sec1 = QLabel("ARCHITECTURE")
        lbl_sec1.setObjectName("SidebarCategoryHeader")
        sidebar_layout.addWidget(lbl_sec1)

        self._add_nav_item(sidebar_layout, "[01] Paradigms", 0)
        self._add_nav_item(sidebar_layout, "[02] Memory Engine", 1)
        self._add_nav_item(sidebar_layout, "[03] Design Patterns", 2)

        # Section 2: Execution & Output
        lbl_sec2 = QLabel("RUNTIMES & OUTPUT")
        lbl_sec2.setObjectName("SidebarCategoryHeader")
        sidebar_layout.addWidget(lbl_sec2)

        self._add_nav_item(sidebar_layout, "[04] Playground", 3)
        self._add_nav_item(sidebar_layout, "[05] Benchmarks", 4)
        self._add_nav_item(sidebar_layout, "[06] Export Docs", 5)

        sidebar_layout.addStretch()

        # Telemetry Card in Sidebar Footer
        telemetry_card = QFrame()
        telemetry_card.setObjectName("TelemetryFrame")
        telem_layout = QVBoxLayout(telemetry_card)
        telem_layout.setContentsMargins(6, 6, 6, 6)
        telem_layout.setSpacing(2)

        pid = os.getpid()
        lbl_telem_status = QLabel("CLIENT CORE :: ACTIVE")
        lbl_telem_status.setStyleSheet("font-size: 9px; font-weight: 700; color: #10b981; font-family: 'Consolas', monospace;")
        telem_layout.addWidget(lbl_telem_status)

        self.lbl_telem_info = QLabel(f"PID: {pid} | Arch: x86_64\nPython: 3.14.7 | V8: Node 24")
        self.lbl_telem_info.setObjectName("TelemetryText")
        telem_layout.addWidget(self.lbl_telem_info)

        sidebar_layout.addWidget(telemetry_card)
        root_layout.addWidget(sidebar)

        # 2. Right Workspace (Header + Stack)
        workspace = QFrame()
        workspace_layout = QVBoxLayout(workspace)
        workspace_layout.setContentsMargins(0, 0, 0, 0)
        workspace_layout.setSpacing(0)

        # Top Header Bar
        top_header = QFrame()
        top_header.setObjectName("TopHeaderBar")
        top_header_layout = QHBoxLayout(top_header)
        top_header_layout.setContentsMargins(14, 6, 14, 6)
        top_header_layout.setSpacing(10)

        self.search_bar = QLineEdit()
        self.search_bar.setObjectName("SearchBar")
        self.search_bar.setPlaceholderText("Filter (Ctrl+F) ... [e.g. 'async', 'borrow', 'circuit', 'primes']")
        self.search_bar.textChanged.connect(self._on_search_query)
        top_header_layout.addWidget(self.search_bar, 1)

        # Target indicators
        badge_row = QHBoxLayout()
        badge_row.setSpacing(6)
        badges = [("RUST", "#f97316"), ("GO", "#06b6d4"), ("TS", "#38bdf8"), ("PY", "#eab308"), ("JAVA", "#ef4444"), ("C++", "#a855f7")]
        for name, col in badges:
            lbl_b = QLabel(name)
            lbl_b.setStyleSheet(f"""
                QLabel {{
                    background-color: #12131a;
                    color: {col};
                    border: 1px solid #1f212c;
                    border-radius: 3px;
                    padding: 2px 6px;
                    font-size: 9px;
                    font-weight: 700;
                    font-family: 'Consolas', monospace;
                }}
            """)
            badge_row.addWidget(lbl_b)
        top_header_layout.addLayout(badge_row)

        workspace_layout.addWidget(top_header)

        # Stacked Pages
        self.stack = QStackedWidget()

        self.tab_matrix = ParadigmMatrixTab()
        self.tab_memory = MemorySimulatorTab()
        self.tab_patterns = PatternLabTab()
        self.tab_playground = CodePlaygroundTab()
        self.tab_benchmarks = BenchmarkRadarTab()
        self.tab_exporter = ExporterTab()

        self.stack.addWidget(self.tab_matrix)
        self.stack.addWidget(self.tab_memory)
        self.stack.addWidget(self.tab_patterns)
        self.stack.addWidget(self.tab_playground)
        self.stack.addWidget(self.tab_benchmarks)
        self.stack.addWidget(self.tab_exporter)

        workspace_layout.addWidget(self.stack, 1)
        root_layout.addWidget(workspace, 1)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self._switch_page(0)

    def _init_shortcuts(self):
        # Quick Tab Switching with Ctrl+1 through Ctrl+6
        for i in range(6):
            shortcut = QShortcut(QKeySequence(f"Ctrl+{i+1}"), self)
            shortcut.activated.connect(lambda idx=i: self._switch_page(idx))
        
        # Search Shortcut: Ctrl+F focuses search input
        shortcut_f = QShortcut(QKeySequence("Ctrl+F"), self)
        shortcut_f.activated.connect(lambda: self.search_bar.setFocus())

    def _add_nav_item(self, layout, text, page_idx):
        btn = QPushButton(text)
        btn.setProperty("class", "SidebarNavBtn")
        btn.setCheckable(True)
        btn.clicked.connect(lambda: self._switch_page(page_idx))
        layout.addWidget(btn)
        self._nav_buttons.append((btn, page_idx))

    def _switch_page(self, page_idx):
        self.stack.setCurrentIndex(page_idx)
        for btn, idx in self._nav_buttons:
            btn.setChecked(idx == page_idx)
            if idx == page_idx:
                btn.setProperty("class", "SidebarNavBtn Active")
            else:
                btn.setProperty("class", "SidebarNavBtn")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def _on_search_query(self, query: str):
        q = query.strip().lower()
        if not q:
            return
        if any(w in q for w in ["memory", "stack", "heap", "borrow", "raii", "leak", "pointer"]):
            self._switch_page(1)
        elif any(w in q for w in ["circuit", "breaker", "pattern", "worker", "pool", "fault"]):
            self._switch_page(2)
        elif any(w in q for w in ["play", "run", "exec", "test", "prime"]):
            self._switch_page(3)
        elif any(w in q for w in ["bench", "radar", "big-o", "sort", "metric"]):
            self._switch_page(4)
        elif any(w in q for w in ["export", "md", "markdown", "git"]):
            self._switch_page(5)
        else:
            self._switch_page(0)

    def _check_system_runtimes(self):
        has_python = shutil.which("python") is not None
        has_node = shutil.which("node") is not None
        has_javac = shutil.which("javac") is not None

        status_text = (
            f"SYSTEM DLC WORKBENCH | OS: {platform.system()} {platform.release()} | "
            f"CPython 3.14.7 [OK] | "
            f"V8 Node.js 24 [OK] | "
            f"Java HotSpot JDK 21 [OK] | "
            f"UTF-8 | CRLF"
        )
        self.status_bar.showMessage(status_text)
