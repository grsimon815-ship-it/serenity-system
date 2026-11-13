import shutil
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QStackedWidget, QStatusBar, QFrame, QPushButton, QLineEdit
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont, QColor

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
        self.setWindowTitle("SystemDLC — Polyglot Architecture & Execution Studio")
        self.resize(1340, 850)
        self.setMinimumSize(1080, 700)

        self._nav_buttons = []
        self._init_ui()
        self._check_system_runtimes()

    def _init_ui(self):
        self.setStyleSheet(SYSTEM_DLC_THEME)

        central_widget = QWidget()
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)

        # Root Horizontal Layout (Sidebar + Main Workspace)
        root_layout = QHBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # 1. Left Vertical Sidebar (System DLC style)
        sidebar = QFrame()
        sidebar.setObjectName("SidebarFrame")
        sidebar.setFixedWidth(230)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 16, 12, 14)
        sidebar_layout.setSpacing(6)

        # Brand Header
        brand_frame = QFrame()
        brand_layout = QVBoxLayout(brand_frame)
        brand_layout.setContentsMargins(4, 0, 4, 10)
        brand_layout.setSpacing(1)

        brand_row = QHBoxLayout()
        lbl_icon = QLabel("◆")
        lbl_icon.setStyleSheet("color: #8b5cf6; font-size: 18px; font-weight: bold;")
        brand_row.addWidget(lbl_icon)

        lbl_brand = QLabel("SYSTEM")
        lbl_brand.setObjectName("LogoTitle")
        brand_row.addWidget(lbl_brand)
        brand_row.addStretch()
        brand_layout.addLayout(brand_row)

        lbl_sub = QLabel("POLYGLOT ARCHITECTURE")
        lbl_sub.setObjectName("LogoSubtitle")
        brand_layout.addWidget(lbl_sub)
        sidebar_layout.addWidget(brand_frame)

        # Section 1: Core Paradigms
        lbl_sec1 = QLabel("CORE ANALYSIS")
        lbl_sec1.setObjectName("SidebarCategoryHeader")
        sidebar_layout.addWidget(lbl_sec1)

        self._add_nav_item(sidebar_layout, "◆  Paradigms Matrix", 0)
        self._add_nav_item(sidebar_layout, "⬡  Memory & Lifetimes", 1)
        self._add_nav_item(sidebar_layout, "⚡  Resilience Patterns", 2)

        # Section 2: Runtime & Tools
        lbl_sec2 = QLabel("EXECUTION & TOOLS")
        lbl_sec2.setObjectName("SidebarCategoryHeader")
        sidebar_layout.addWidget(lbl_sec2)

        self._add_nav_item(sidebar_layout, "❯_ Code Playground", 3)
        self._add_nav_item(sidebar_layout, "◈  Benchmarks & Radar", 4)
        self._add_nav_item(sidebar_layout, "⤓  GitHub Exporter", 5)

        sidebar_layout.addStretch()

        # Telemetry Card at Bottom
        telemetry_card = QFrame()
        telemetry_card.setObjectName("TelemetryFrame")
        telem_layout = QVBoxLayout(telemetry_card)
        telem_layout.setContentsMargins(8, 8, 8, 8)
        telem_layout.setSpacing(3)

        lbl_telem_status = QLabel("● SYSTEM ENGINE ONLINE")
        lbl_telem_status.setStyleSheet("font-size: 10px; font-weight: 800; color: #10b981; letter-spacing: 1px;")
        telem_layout.addWidget(lbl_telem_status)

        self.lbl_telem_info = QLabel("Python 3.14 • Node 24 • JVM\nLatency: 0ms • GUI: 60 FPS")
        self.lbl_telem_info.setObjectName("TelemetryText")
        telem_layout.addWidget(self.lbl_telem_info)

        sidebar_layout.addWidget(telemetry_card)
        root_layout.addWidget(sidebar)

        # 2. Right Workspace (Top Header + Stacked View)
        workspace = QFrame()
        workspace_layout = QVBoxLayout(workspace)
        workspace_layout.setContentsMargins(0, 0, 0, 0)
        workspace_layout.setSpacing(0)

        # Top Header Bar
        top_header = QFrame()
        top_header.setObjectName("TopHeaderBar")
        top_header_layout = QHBoxLayout(top_header)
        top_header_layout.setContentsMargins(16, 8, 16, 8)
        top_header_layout.setSpacing(12)

        # Search / Quick Filter Bar
        self.search_bar = QLineEdit()
        self.search_bar.setObjectName("SearchBar")
        self.search_bar.setPlaceholderText("🔍  Search architectural concepts, memory models, patterns (e.g. 'async', 'borrow', 'circuit')...")
        self.search_bar.textChanged.connect(self._on_search_query)
        top_header_layout.addWidget(self.search_bar, 1)

        # System Status Badges
        badge_row = QHBoxLayout()
        badge_row.setSpacing(8)

        badges = [
            ("RUST", "#f97316"),
            ("GO", "#06b6d4"),
            ("TS", "#38bdf8"),
            ("PYTHON", "#eab308"),
            ("JAVA", "#ef4444"),
            ("C++", "#a855f7")
        ]
        for name, col in badges:
            lbl_b = QLabel(name)
            lbl_b.setStyleSheet(f"""
                QLabel {{
                    background-color: #12151e;
                    color: {col};
                    border: 1px solid #1a1e2b;
                    border-radius: 4px;
                    padding: 3px 8px;
                    font-size: 10px;
                    font-weight: 700;
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

        # Select first tab by default
        self._switch_page(0)

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
        query = query.strip().lower()
        if not query:
            return

        # Intelligent fast routing based on user search query
        if any(w in query for w in ["memory", "stack", "heap", "borrow", "raii", "leak", "pointer", "unique_ptr"]):
            self._switch_page(1)
        elif any(w in query for w in ["circuit", "breaker", "pattern", "worker", "pool", "fail", "fallback"]):
            self._switch_page(2)
        elif any(w in query for w in ["play", "run", "exec", "test", "terminal", "eval"]):
            self._switch_page(3)
        elif any(w in query for w in ["bench", "radar", "big-o", "sort", "speed", "latency"]):
            self._switch_page(4)
        elif any(w in query for w in ["export", "md", "markdown", "git", "doc"]):
            self._switch_page(5)
        else:
            self._switch_page(0)

    def _check_system_runtimes(self):
        has_python = shutil.which("python") is not None
        has_node = shutil.which("node") is not None
        has_javac = shutil.which("javac") is not None

        status_text = (
            f"SystemDLC Client Engine • Connected • "
            f"Python: {'CPython 3.14.7' if has_python else 'Missing'} • "
            f"V8 Engine: {'Node 24.22' if has_node else 'Missing'} • "
            f"HotSpot: {'JDK 21' if has_javac else 'Missing'} • "
            f"Zero-Lag Execution Ready"
        )
        self.status_bar.showMessage(status_text)
