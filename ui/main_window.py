import shutil
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QTabWidget, QStatusBar, QFrame, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont

from ui.theme import DARK_THEME_QSS
from ui.tab_matrix import ParadigmMatrixTab
from ui.tab_memory import MemorySimulatorTab
from ui.tab_patterns import PatternLabTab
from ui.tab_playground import CodePlaygroundTab
from ui.tab_benchmarks import BenchmarkRadarTab
from ui.tab_exporter import ExporterTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PolyglotForge — Universal High-Level Architecture & Multi-Language Studio")
        self.resize(1280, 820)
        self.setMinimumSize(1024, 680)

        self._init_ui()
        self._check_system_runtimes()

    def _init_ui(self):
        self.setStyleSheet(DARK_THEME_QSS)

        central_widget = QWidget()
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)

        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(12, 10, 12, 8)
        root_layout.setSpacing(8)

        # Header Bar
        header_bar = QFrame()
        header_bar.setStyleSheet("""
            QFrame {
                background-color: #0b1120;
                border: 1px solid #1e293b;
                border-radius: 8px;
                padding: 6px 12px;
            }
        """)
        header_layout = QHBoxLayout(header_bar)
        header_layout.setContentsMargins(8, 4, 8, 4)

        # App Logo & Title
        title_box = QVBoxLayout()
        title_box.setSpacing(1)

        lbl_logo = QLabel("POLYGLOT FORGE")
        lbl_logo.setStyleSheet("font-size: 16px; font-weight: 800; color: #38bdf8; letter-spacing: 1px;")
        title_box.addWidget(lbl_logo)

        lbl_subtitle = QLabel("Universal High-Level Architecture, Memory Models & Multi-Language Paradigm Studio")
        lbl_subtitle.setStyleSheet("font-size: 11px; color: #94a3b8;")
        title_box.addWidget(lbl_subtitle)
        header_layout.addLayout(title_box)

        header_layout.addStretch()

        # Language Badges in Header
        badges_layout = QHBoxLayout()
        badges_layout.setSpacing(6)
        badges = [
            ("Rust", "#f97316"),
            ("Go", "#06b6d4"),
            ("TypeScript", "#3b82f6"),
            ("Python", "#eab308"),
            ("Java", "#ef4444"),
            ("C++", "#a855f7")
        ]
        for name, color in badges:
            lbl_b = QLabel(name)
            lbl_b.setStyleSheet(f"""
                QLabel {{
                    background-color: #0f172a;
                    color: {color};
                    border: 1px solid {color}44;
                    border-radius: 4px;
                    padding: 2px 8px;
                    font-size: 11px;
                    font-weight: 600;
                }}
            """)
            badges_layout.addWidget(lbl_b)
        header_layout.addLayout(badges_layout)

        root_layout.addWidget(header_bar)

        # Main Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self.tab_matrix = ParadigmMatrixTab()
        self.tab_memory = MemorySimulatorTab()
        self.tab_patterns = PatternLabTab()
        self.tab_playground = CodePlaygroundTab()
        self.tab_benchmarks = BenchmarkRadarTab()
        self.tab_exporter = ExporterTab()

        self.tabs.addTab(self.tab_matrix, "🌟 Paradigm Matrix")
        self.tabs.addTab(self.tab_memory, "🧠 Memory & Lifetimes")
        self.tabs.addTab(self.tab_patterns, "🏛️ Architecture Patterns")
        self.tabs.addTab(self.tab_playground, "⚡ Code Playground")
        self.tabs.addTab(self.tab_benchmarks, "📊 Benchmarks & Big-O")
        self.tabs.addTab(self.tab_exporter, "📑 GitHub Exporter")

        root_layout.addWidget(self.tabs, 1)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def _check_system_runtimes(self):
        has_python = shutil.which("python") is not None
        has_node = shutil.which("node") is not None
        has_javac = shutil.which("javac") is not None
        has_rustc = shutil.which("rustc") is not None
        has_go = shutil.which("go") is not None

        status_text = (
            f"Runtimes: Python ({'✓ 3.14' if has_python else '✕'}) | "
            f"Node.js ({'✓ V24' if has_node else '✕'}) | "
            f"Java ({'✓ JDK' if has_javac else '✕'}) | "
            f"Rust ({'✓' if has_rustc else 'Simulated'}) | "
            f"Go ({'✓' if has_go else 'Simulated'}) | "
            f"Engine: PyQt6 High-DPI GUI Ready"
        )
        self.status_bar.showMessage(status_text)
