import time
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QPushButton, QFrame, QSplitter, QTextEdit, QGraphicsView, QGraphicsScene
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen, QBrush, QFont

from core.patterns_data import PATTERNS, ArchitecturePattern
from ui.code_editor import PolyglotCodeEditor

class PatternGraphView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setBackgroundBrush(QBrush(QColor("#0d0e14")))
        self.setStyleSheet("border: 1px solid #1e2029; border-radius: 6px;")

    def render_pattern(self, pattern: ArchitecturePattern, state_overrides=None):
        self.scene.clear()
        if not pattern:
            return

        font_label = QFont("Cascadia Code", 10, QFont.Weight.Bold)
        font_sub = QFont("Cascadia Code", 9)

        status_colors = {
            "idle": ("#13151b", "#272a38", "#64748b"),
            "active": ("#151b27", "#38bdf8", "#38bdf8"),
            "success": ("#062c21", "#059669", "#34d399"),
            "warning": ("#2e1f06", "#d97706", "#fbbf24"),
            "error": ("#2e0b11", "#e11d48", "#fb7185"),
        }

        node_positions = {}

        for node in pattern.nodes:
            status = state_overrides.get(node.id, node.status) if state_overrides else node.status
            bg, border, text_col = status_colors.get(status, status_colors["idle"])

            w, h = 135, 54
            x, y = node.x, node.y
            node_positions[node.id] = (x + w / 2, y + h / 2)

            self.scene.addRect(x, y, w, h, QPen(QColor(border), 1.2), QBrush(QColor(bg)))

            t1 = self.scene.addText(node.label, font_label)
            t1.setDefaultTextColor(QColor(text_col))
            t1.setPos(x + 6, y + 4)

            t2 = self.scene.addText(f"[{node.role}]", font_sub)
            t2.setDefaultTextColor(QColor("#475569"))
            t2.setPos(x + 6, y + 26)

        pen_edge = QPen(QColor("#33384a"), 1.2)
        for edge in pattern.edges:
            p1 = node_positions.get(edge.source_id)
            p2 = node_positions.get(edge.target_id)
            if p1 and p2:
                self.scene.addLine(p1[0], p1[1], p2[0], p2[1], pen_edge)
                mid_x = (p1[0] + p2[0]) / 2
                mid_y = (p1[1] + p2[1]) / 2 - 8
                t_edge = self.scene.addText(edge.label, font_sub)
                t_edge.setDefaultTextColor(QColor("#64748b"))
                t_edge.setPos(mid_x - 30, mid_y)


class PatternLabTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_pattern_idx = 0
        self.cb_state = "CLOSED"
        self.cb_failures = 0
        self.cb_threshold = 3
        
        self._init_ui()
        self.load_pattern(0)

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 12, 14, 12)
        main_layout.setSpacing(8)

        # Top Bar
        top_bar = QFrame()
        top_bar.setProperty("class", "DlcCard")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(10, 6, 10, 6)
        top_layout.setSpacing(10)

        top_layout.addWidget(QLabel("Pattern:"))
        self.cb_pattern = QComboBox()
        for p in PATTERNS:
            self.cb_pattern.addItem(f"{p.name} ({p.category})", p.id)
        self.cb_pattern.currentIndexChanged.connect(self.on_pattern_changed)
        top_layout.addWidget(self.cb_pattern, 2)

        top_layout.addSpacing(10)

        self.btn_action_success = QPushButton("Trigger Request (200)")
        self.btn_action_success.clicked.connect(self.simulate_success)
        top_layout.addWidget(self.btn_action_success)

        self.btn_action_fail = QPushButton("Inject Fault (500)")
        self.btn_action_fail.clicked.connect(self.simulate_failure)
        top_layout.addWidget(self.btn_action_fail)

        self.btn_action_reset = QPushButton("Reset Circuit")
        self.btn_action_reset.clicked.connect(self.simulate_reset)
        top_layout.addWidget(self.btn_action_reset)

        main_layout.addWidget(top_bar)

        # Body Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(6)

        # Left Column: Graph View + Console Log
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: #0d0e14; border: 1px solid #1e2029; border-radius: 6px;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(8, 8, 8, 8)
        left_layout.setSpacing(6)

        self.graph_view = PatternGraphView()
        left_layout.addWidget(self.graph_view, 2)

        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        self.txt_log.setStyleSheet("""
            QTextEdit {
                background-color: #090a0f;
                color: #e2e8f0;
                font-family: 'Cascadia Code', monospace;
                font-size: 11px;
                border: 1px solid #1e2029;
                border-radius: 4px;
                padding: 6px;
            }
        """)
        self.txt_log.setMaximumHeight(110)
        left_layout.addWidget(self.txt_log, 1)

        splitter.addWidget(left_panel)

        # Right Column: Implementation Code
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #0d0e14; border: 1px solid #1e2029; border-radius: 6px;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(8, 6, 8, 8)
        right_layout.setSpacing(6)

        code_header = QHBoxLayout()
        code_header.addWidget(QLabel("Language:"))
        self.cb_code_lang = QComboBox()
        self.cb_code_lang.addItem("Rust", "rust")
        self.cb_code_lang.addItem("TypeScript", "typescript")
        self.cb_code_lang.addItem("Go", "go")
        self.cb_code_lang.currentIndexChanged.connect(self.update_code_view)
        code_header.addWidget(self.cb_code_lang)
        code_header.addStretch()

        right_layout.addLayout(code_header)

        self.code_editor = PolyglotCodeEditor(read_only=True)
        right_layout.addWidget(self.code_editor, 1)

        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 5)
        splitter.setStretchFactor(1, 5)

        main_layout.addWidget(splitter, 1)

    def on_pattern_changed(self, idx):
        self.load_pattern(idx)

    def load_pattern(self, idx):
        if idx < 0 or idx >= len(PATTERNS):
            return
        self.current_pattern_idx = idx
        pattern = PATTERNS[idx]

        self.update_code_view()
        self.update_graph()
        self.log(f"Initialized {pattern.name}")

    def update_code_view(self):
        pattern = PATTERNS[self.current_pattern_idx]
        lang_id = self.cb_code_lang.currentData()
        code = pattern.code_implementations.get(lang_id, "// Implementation not found")
        self.code_editor.set_language(lang_id)
        self.code_editor.setPlainText(code)

    def update_graph(self):
        pattern = PATTERNS[self.current_pattern_idx]
        overrides = {}
        if pattern.id == "circuit_breaker":
            if self.cb_state == "CLOSED":
                overrides = {"client": "active", "breaker": "success", "downstream": "active", "fallback": "idle"}
            elif self.cb_state == "OPEN":
                overrides = {"client": "active", "breaker": "error", "downstream": "idle", "fallback": "warning"}
            elif self.cb_state == "HALF_OPEN":
                overrides = {"client": "active", "breaker": "warning", "downstream": "active", "fallback": "idle"}
        self.graph_view.render_pattern(pattern, overrides)

    def simulate_success(self):
        pattern = PATTERNS[self.current_pattern_idx]
        if pattern.id == "circuit_breaker":
            if self.cb_state == "OPEN":
                self.log("[FAST_FAIL] Circuit OPEN; call rejected.")
            else:
                self.cb_state = "CLOSED"
                self.cb_failures = 0
                self.log(f"[HTTP 200] Downstream OK. Circuit State={self.cb_state}")
                self.update_graph()
        else:
            self.log("[WORKER_POOL] Job completed.")

    def simulate_failure(self):
        pattern = PATTERNS[self.current_pattern_idx]
        if pattern.id == "circuit_breaker":
            if self.cb_state == "OPEN":
                self.log("[FAST_FAIL] Circuit already OPEN; falling back.")
                return

            self.cb_failures += 1
            self.log(f"[HTTP 500] Error detected ({self.cb_failures}/{self.cb_threshold})")
            
            if self.cb_failures >= self.cb_threshold:
                self.cb_state = "OPEN"
                self.log(">> Threshold reached: Circuit TRIPPED to OPEN.")
            self.update_graph()
        else:
            self.log("[WORKER_POOL] Worker fault isolated.")

    def simulate_reset(self):
        self.cb_state = "CLOSED"
        self.cb_failures = 0
        self.log("Circuit state reset to CLOSED.")
        self.update_graph()

    def log(self, text):
        timestamp = time.strftime("%H:%M:%S")
        self.txt_log.append(f"[{timestamp}] {text}")
