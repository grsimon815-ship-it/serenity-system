import shutil
import os
import platform
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QStackedWidget, QStatusBar, QFrame, QPushButton, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut

from ui.theme import SERENITY_THEME
from ui.tab_matrix import ParadigmMatrixTab
from ui.tab_memory import MemorySimulatorTab
from ui.tab_patterns import PatternLabTab
from ui.tab_playground import CodePlaygroundTab
from ui.tab_benchmarks import BenchmarkRadarTab
from ui.tab_exporter import ExporterTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Serenity System")
        self.resize(1300, 820)
        self.setMinimumSize(1020, 660)

        self._nav_buttons = []
        self._init_ui()
        self._init_shortcuts()

    def _init_ui(self):
        self.setStyleSheet(SERENITY_THEME)

        central_widget = QWidget()
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Left Navigation Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("SidebarFrame")
        sidebar.setFixedWidth(180)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 14, 10, 14)
        sidebar_layout.setSpacing(4)

        # Brand Title
        lbl_brand = QLabel("SERENITY SYSTEM")
        lbl_brand.setObjectName("LogoTitle")
        sidebar_layout.addWidget(lbl_brand)
        sidebar_layout.addSpacing(10)

        # Direct, functional navigation buttons
        self._add_nav_item(sidebar_layout, "Paradigms", 0)
        self._add_nav_item(sidebar_layout, "Memory", 1)
        self._add_nav_item(sidebar_layout, "Patterns", 2)
        self._add_nav_item(sidebar_layout, "Playground", 3)
        self._add_nav_item(sidebar_layout, "Metrics", 4)
        self._add_nav_item(sidebar_layout, "Export", 5)

        sidebar_layout.addStretch()
        root_layout.addWidget(sidebar)

        # Right Workspace
        workspace = QFrame()
        workspace_layout = QVBoxLayout(workspace)
        workspace_layout.setContentsMargins(0, 0, 0, 0)
        workspace_layout.setSpacing(0)

        # Top Header Bar (Search input)
        top_header = QFrame()
        top_header.setObjectName("TopHeaderBar")
        top_header_layout = QHBoxLayout(top_header)
        top_header_layout.setContentsMargins(14, 8, 14, 8)
        top_header_layout.setSpacing(10)

        self.search_bar = QLineEdit()
        self.search_bar.setObjectName("SearchBar")
        self.search_bar.setPlaceholderText("Search paradigms, memory models, patterns (Ctrl+F)...")
        self.search_bar.textChanged.connect(self._on_search_query)
        top_header_layout.addWidget(self.search_bar, 1)

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
        self.status_bar.showMessage("Ready")

        self._switch_page(0)

    def _init_shortcuts(self):
        for i in range(6):
            shortcut = QShortcut(QKeySequence(f"Ctrl+{i+1}"), self)
            shortcut.activated.connect(lambda idx=i: self._switch_page(idx))
        
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
