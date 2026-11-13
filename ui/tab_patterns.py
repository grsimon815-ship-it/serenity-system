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
        self.setBackgroundBrush(QBrush(QColor("#0a0b0e")))
        self.setStyleSheet("border: 1px solid #1c1d27; border-radius: 6px;")

    def render_pattern(self, pattern: ArchitecturePattern, state_overrides=None):
        self.scene.clear()
        if not pattern:
            return

        font_label = QFont("Consolas", 9, QFont.Weight.Bold)
        font_sub = QFont("Consolas", 8)

        status_colors = {
            "idle": ("#111218", "#232532", "#6b7280"),
            "active": ("#161926", "#38bdf8", "#38bdf8"),
            "success": ("#062c21", "#059669", "#34d399"),
            "warning": ("#2e1f06", "#d97706", "#fbbf24"),
            "error": ("#2e0b11", "#e11d48", "#fb7185"),
        }

        node_positions = {}

        for node in pattern.nodes:
            status = state_overrides.get(node.id, node.status) if state_overrides else node.status
            bg, border, text_col = status_colors.get(status, status_colors["idle"])

            w, h = 130, 52
            x, y = node.x, node.y
            node_positions[node.id] = (x + w / 2, y + h / 2)

            self.scene.addRect(x, y, w, h, QPen(QColor(border), 1.2), QBrush(QColor(bg)))

            t1 = self.scene.addText(node.label, font_label)
            t1.setDefaultTextColor(QColor(text_col))
            t1.setPos(x + 6, y + 4)

            t2 = self.scene.addText(f"[{node.role}]", font_sub)
            t2.setDefaultTextColor(QColor("#4b5263"))
            t2.setPos(x + 6, y + 26)

        pen_edge = QPen(QColor("#2d3142"), 1.2)
        for edge in pattern.edges:
            p1 = node_positions.get(edge.source_id)
            p2 = node_positions.get(edge.target_id)
            if p1 and p2:
                self.scene.addLine(p1[0], p1[1], p2[0], p2[1], pen_edge)
                mid_x = (p1[0] + p2[0]) / 2
                mid_y = (p1[1] + p2[1]) / 2 - 8
                t_edge = self.scene.addText(edge.label, font_sub)
                t_edge.setDefaultTextColor(QColor("#6b7280"))
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
        main_layout.setContentsMargins(16, 14, 16, 14)
        main_layout.setSpacing(10)

        # Top Bar
        top_bar = QFrame()
        top_bar.setProperty("class", "DlcCard")
        top_bar.setStyleSheet("background-color: #0e0f14; border: 1px solid #1c1d27; border-radius: 6px; padding: 4px;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(8, 4, 8, 4)
        top_layout.setSpacing(8)

        lbl_pattern = QLabel("Pattern:")
        lbl_pattern.setStyleSheet("font-weight: 600; color: #9ca3af; font-size: 11px;")
        top_layout.addWidget(lbl_pattern)

        self.cb_pattern = QComboBox()
        for p in PATTERNS:
            self.cb_pattern.addItem(f"{p.name} ({p.category})", p.id)
        self.cb_pattern.currentIndexChanged.connect(self.on_pattern_changed)
        top_layout.addWidget(self.cb_pattern, 2)

        top_layout.addSpacing(12)

        self.btn_action_success = QPushButton("Invoke Request (200 OK)")
        self.btn_action_success.clicked.connect(self.simulate_success)
        top_layout.addWidget(self.btn_action_success)

        self.btn_action_fail = QPushButton("Inject Fault (500 Error)")
        self.btn_action_fail.clicked.connect(self.simulate_failure)
        top_layout.addWidget(self.btn_action_fail)

        self.btn_action_reset = QPushButton("Reset State")
        self.btn_action_reset.clicked.connect(self.simulate_reset)
        top_layout.addWidget(self.btn_action_reset)

        main_layout.addWidget(top_bar)

        # Body Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(4)

        # Left Column: Graph View + Console Log
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: #0e0f14; border: 1px solid #1c1d27; border-radius: 6px;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(8, 6, 8, 6)
        left_layout.setSpacing(4)

        self.lbl_desc = QLabel()
        self.lbl_desc.setWordWrap(True)
        self.lbl_desc.setStyleSheet("color: #9ca3af; font-size: 11px; padding: 4px; background: #0a0b0e; border-radius: 4px; font-family: 'Consolas', monospace;")
        left_layout.addWidget(self.lbl_desc)

        self.graph_view = PatternGraphView()
        left_layout.addWidget(self.graph_view, 2)

        lbl_console = QLabel("Telemetry Event Stream")
        lbl_console.setStyleSheet("font-weight: 600; color: #6b7280; font-size: 10px; font-family: 'Consolas', monospace;")
        left_layout.addWidget(lbl_console)

        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        self.txt_log.setStyleSheet("""
            QTextEdit {
                background-color: #0a0b0e;
                color: #d1d5db;
                font-family: 'Consolas', monospace;
                font-size: 10px;
                border: 1px solid #1c1d27;
                border-radius: 4px;
                padding: 4px;
            }
        """)
        self.txt_log.setMaximumHeight(95)
        left_layout.addWidget(self.txt_log, 1)

        splitter.addWidget(left_panel)

        # Right Column: Implementation Code
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #0e0f14; border: 1px solid #1c1d27; border-radius: 6px;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(8, 6, 8, 6)
        right_layout.setSpacing(4)

        code_header = QHBoxLayout()
        lbl_code = QLabel("Implementation")
        lbl_code.setStyleSheet("font-weight: 600; color: #6b7280; font-size: 11px; font-family: 'Consolas', monospace;")
        code_header.addWidget(lbl_code)
        code_header.addStretch()

        self.cb_code_lang = QComboBox()
        self.cb_code_lang.addItem("Rust", "rust")
        self.cb_code_lang.addItem("TypeScript", "typescript")
        self.cb_code_lang.addItem("Go", "go")
        self.cb_code_lang.currentIndexChanged.connect(self.update_code_view)
        code_header.addWidget(self.cb_code_lang)

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

        self.lbl_desc.setText(f"[PROBLEM] {pattern.problem}\n[ARCHITECTURE] {pattern.solution}")
        self.update_code_view()
        self.update_graph()
        self.log(f"Initialized pattern: {pattern.name}")

    def update_code_view(self):
        pattern = PATTERNS[self.current_pattern_idx]
        lang_id = self.cb_code_lang.currentData()
        code = pattern.code_implementations.get(lang_id, "// Implementation in progress...")
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
                self.log("[FAST_FAIL] Circuit OPEN; call rejected before network dispatch.")
            else:
                self.cb_state = "CLOSED"
                self.cb_failures = 0
                self.log(f"[HTTP 200] Target invocation succeeded. State={self.cb_state}")
                self.update_graph()
        else:
            self.log("[WORKER_POOL] Job enqueued; worker dequeued and settled task.")

    def simulate_failure(self):
        pattern = PATTERNS[self.current_pattern_idx]
        if pattern.id == "circuit_breaker":
            if self.cb_state == "OPEN":
                self.log("[FAST_FAIL] Circuit is already OPEN; short-circuiting to fallback.")
                return

            self.cb_failures += 1
            self.log(f"[HTTP 500] Fault detected ({self.cb_failures}/{self.cb_threshold})")
            
            if self.cb_failures >= self.cb_threshold:
                self.cb_state = "OPEN"
                self.log(">> THRESHOLD REACHED: Circuit tripped to OPEN state.")
            self.update_graph()
        else:
            self.log("[SUPERVISOR] Worker failure isolated.")

    def simulate_reset(self):
        self.cb_state = "CLOSED"
        self.cb_failures = 0
        self.log("State machine reset to CLOSED.")
        self.update_graph()

    def log(self, text):
        timestamp = time.strftime("%H:%M:%S")
        self.txt_log.append(f"[{timestamp}] {text}")
