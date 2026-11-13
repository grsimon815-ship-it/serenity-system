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
        self.setBackgroundBrush(QBrush(QColor("#08090d")))
        self.setStyleSheet("border: 1px solid #181b26; border-radius: 9px;")

    def render_pattern(self, pattern: ArchitecturePattern, state_overrides=None):
        self.scene.clear()
        if not pattern:
            return

        font_label = QFont("Segoe UI", 10, QFont.Weight.Bold)
        font_sub = QFont("Segoe UI", 8)

        status_colors = {
            "idle": ("#0f172a", "#334155", "#94a3b8"),
            "active": ("#1e293b", "#38bdf8", "#38bdf8"),
            "success": ("#064e3b", "#10b981", "#6ee7b7"),
            "warning": ("#78350f", "#f59e0b", "#fde68a"),
            "error": ("#7f1d1d", "#ef4444", "#fca5a5"),
        }

        node_positions = {}

        # Draw Nodes
        for node in pattern.nodes:
            status = state_overrides.get(node.id, node.status) if state_overrides else node.status
            bg, border, text_col = status_colors.get(status, status_colors["idle"])

            w, h = 130, 60
            x, y = node.x, node.y
            node_positions[node.id] = (x + w / 2, y + h / 2)

            self.scene.addRect(x, y, w, h, QPen(QColor(border), 1.8), QBrush(QColor(bg)))

            t1 = self.scene.addText(node.label, font_label)
            t1.setDefaultTextColor(QColor(text_col))
            t1.setPos(x + 8, y + 6)

            t2 = self.scene.addText(f"[{node.role}]", font_sub)
            t2.setDefaultTextColor(QColor("#64748b"))
            t2.setPos(x + 8, y + 30)

        # Draw Edges
        pen_edge = QPen(QColor("#475569"), 1.5)
        for edge in pattern.edges:
            p1 = node_positions.get(edge.source_id)
            p2 = node_positions.get(edge.target_id)
            if p1 and p2:
                self.scene.addLine(p1[0], p1[1], p2[0], p2[1], pen_edge)
                mid_x = (p1[0] + p2[0]) / 2
                mid_y = (p1[1] + p2[1]) / 2 - 10
                t_edge = self.scene.addText(edge.label, font_sub)
                t_edge.setDefaultTextColor(QColor("#94a3b8"))
                t_edge.setPos(mid_x - 30, mid_y)


class PatternLabTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_pattern_idx = 0
        
        # Interactive state machine for circuit breaker
        self.cb_state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.cb_failures = 0
        self.cb_threshold = 3
        
        self._init_ui()
        self.load_pattern(0)

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Top Bar: Pattern Selection & Interactive Action Triggers
        top_bar = QFrame()
        top_bar.setStyleSheet("background-color: #0e1119; border: 1px solid #181b26; border-radius: 9px; padding: 6px;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(8, 6, 8, 6)

        lbl_pattern = QLabel("Pattern:")
        lbl_pattern.setStyleSheet("font-weight: 700; color: #f8fafc;")
        top_layout.addWidget(lbl_pattern)

        self.cb_pattern = QComboBox()
        for p in PATTERNS:
            self.cb_pattern.addItem(f"{p.name} ({p.category})", p.id)
        self.cb_pattern.currentIndexChanged.connect(self.on_pattern_changed)
        top_layout.addWidget(self.cb_pattern, 2)

        top_layout.addSpacing(16)

        # Action Buttons
        self.btn_action_success = QPushButton("✓ Send Request (200 OK)")
        self.btn_action_success.clicked.connect(self.simulate_success)
        top_layout.addWidget(self.btn_action_success)

        self.btn_action_fail = QPushButton("✕ Trigger Failure (500 Error)")
        self.btn_action_fail.clicked.connect(self.simulate_failure)
        top_layout.addWidget(self.btn_action_fail)

        self.btn_action_reset = QPushButton("⟲ Reset State")
        self.btn_action_reset.clicked.connect(self.simulate_reset)
        top_layout.addWidget(self.btn_action_reset)

        main_layout.addWidget(top_bar)

        # Body: Left (Interactive Diagram + Event Log) & Right (Implementation Code)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(6)

        # Left Column: Graph View + Console Log
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: #0b1120; border: 1px solid #1e293b; border-radius: 8px;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)

        # Problem / Solution Banner
        self.lbl_desc = QLabel()
        self.lbl_desc.setWordWrap(True)
        self.lbl_desc.setStyleSheet("color: #cbd5e1; font-size: 11px; padding: 4px; background: #080c14; border-radius: 4px;")
        left_layout.addWidget(self.lbl_desc)

        # Graph View
        self.graph_view = PatternGraphView()
        left_layout.addWidget(self.graph_view, 2)

        # Event Console
        lbl_console = QLabel("Interactive Event Log")
        lbl_console.setStyleSheet("font-weight: 600; color: #94a3b8; font-size: 11px;")
        left_layout.addWidget(lbl_console)

        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        self.txt_log.setStyleSheet("""
            QTextEdit {
                background-color: #080c14;
                color: #10b981;
                font-family: Consolas, monospace;
                font-size: 11px;
                border: 1px solid #1e293b;
                border-radius: 4px;
            }
        """)
        self.txt_log.setMaximumHeight(110)
        left_layout.addWidget(self.txt_log, 1)

        splitter.addWidget(left_panel)

        # Right Column: Multi-Language Code
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #0b1120; border: 1px solid #1e293b; border-radius: 8px;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)

        code_header = QHBoxLayout()
        lbl_code = QLabel("Idiomatic Implementation")
        lbl_code.setStyleSheet("font-weight: 700; color: #f8fafc;")
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

        self.lbl_desc.setText(f"Problem: {pattern.problem}\nSolution Architecture: {pattern.solution}")
        self.update_code_view()
        self.update_graph()
        self.log(f"Loaded architecture pattern: {pattern.name}")

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
                self.log("[FAST-FAIL] Circuit is OPEN! Request blocked without calling downstream service.")
            else:
                self.cb_state = "CLOSED"
                self.cb_failures = 0
                self.log(f"[200 OK] Request dispatched successfully to Downstream. Breaker state: {self.cb_state}")
                self.update_graph()
        else:
            self.log("[WORKER POOL] Task enqueued -> Worker dequeued and finished task.")

    def simulate_failure(self):
        pattern = PATTERNS[self.current_pattern_idx]
        if pattern.id == "circuit_breaker":
            if self.cb_state == "OPEN":
                self.log("[FAST-FAIL] Circuit is already OPEN! Routing to Fallback cache.")
                return

            self.cb_failures += 1
            self.log(f"[500 ERROR] Downstream service failed! (Failures: {self.cb_failures}/{self.cb_threshold})")
            
            if self.cb_failures >= self.cb_threshold:
                self.cb_state = "OPEN"
                self.log("⚠️ THRESHOLD EXCEEDED! Circuit Breaker TRIPPED to [OPEN]! Fast-failing enabled.")
            self.update_graph()
        else:
            self.log("[WORKER POOL] Worker error caught and isolated by supervisor.")

    def simulate_reset(self):
        self.cb_state = "CLOSED"
        self.cb_failures = 0
        self.log("Circuit Breaker reset to [CLOSED]. Downstream restored.")
        self.update_graph()

    def log(self, text):
        timestamp = time.strftime("%H:%M:%S")
        self.txt_log.append(f"[{timestamp}] {text}")
