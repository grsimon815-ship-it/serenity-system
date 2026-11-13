from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QPushButton, QFrame, QSplitter, QGraphicsView, QGraphicsScene
)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QColor, QPen, QBrush, QFont, QPolygonF

from core.memory_scenarios import MEMORY_SCENARIOS, MemoryScenario
from ui.code_editor import PolyglotCodeEditor

class MemoryVisualizerWidget(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setBackgroundBrush(QBrush(QColor("#0d0e14")))
        self.setRenderHint(self.renderHints())
        self.setStyleSheet("border: 1px solid #1e2029; border-radius: 6px;")

    def render_step(self, step):
        self.scene.clear()
        if not step:
            return

        font_header = QFont("Cascadia Code", 11, QFont.Weight.Bold)
        font_box = QFont("Cascadia Code", 10)
        font_sub = QFont("Cascadia Code", 9)

        # 1. Stack Column
        lbl_stack = self.scene.addText("STACK (Frames)", font_header)
        lbl_stack.setDefaultTextColor(QColor("#38bdf8"))
        lbl_stack.setPos(20, 10)

        # 2. Heap Column
        lbl_heap = self.scene.addText("HEAP (Allocations)", font_header)
        lbl_heap.setDefaultTextColor(QColor("#a855f7"))
        lbl_heap.setPos(380, 10)

        # Divider line
        pen_divider = QPen(QColor("#1e2029"), 1, Qt.PenStyle.DashLine)
        self.scene.addLine(340, 10, 340, 500, pen_divider)

        stack_addr_map = {}
        heap_addr_map = {}

        # Render Stack Frames
        y_cursor = 45
        for frame in step.stack:
            frame_title = self.scene.addText(f">> {frame.func_name}", font_sub)
            frame_title.setDefaultTextColor(QColor("#64748b"))
            frame_title.setPos(25, y_cursor)
            y_cursor += 24

            for var in frame.variables:
                border_col = QColor(var.color_hex if not var.is_freed else "#ef4444")
                self.scene.addRect(25, y_cursor, 280, 46, 
                                  QPen(border_col, 1.2), 
                                  QBrush(QColor("#13151b")))
                stack_addr_map[var.address] = (25 + 280, y_cursor + 23)

                t_var = self.scene.addText(f"{var.label} [{var.address}]", font_box)
                t_var.setDefaultTextColor(QColor("#e2e8f0"))
                t_var.setPos(30, y_cursor + 2)

                t_val = self.scene.addText(f"{var.value} ({var.size_bytes}B)", font_sub)
                t_val.setDefaultTextColor(QColor("#94a3b8" if not var.is_freed else "#ef4444"))
                t_val.setPos(30, y_cursor + 22)

                y_cursor += 54

        # Render Heap Blocks
        y_heap = 45
        for block in step.heap:
            border_color = QColor(block.color_hex if not block.is_freed else "#ef4444")
            bg_color = QColor("#13151b" if not block.is_freed else "#1c1114")
            
            self.scene.addRect(380, y_heap, 320, 50, 
                              QPen(border_color, 1.2), 
                              QBrush(bg_color))
            heap_addr_map[block.address] = (380, y_heap + 25)

            t_hb = self.scene.addText(f"{block.label} @ {block.address}", font_box)
            t_hb.setDefaultTextColor(QColor("#e2e8f0" if not block.is_freed else "#ef4444"))
            t_hb.setPos(386, y_heap + 2)

            t_val = self.scene.addText(f"{block.value} | {block.size_bytes}B", font_sub)
            t_val.setDefaultTextColor(QColor("#94a3b8" if not block.is_freed else "#64748b"))
            t_val.setPos(386, y_heap + 24)

            y_heap += 60

        # Draw Pointer Arrows (Stack -> Heap)
        pen_arrow = QPen(QColor("#7c3aed"), 1.5)
        for frame in step.stack:
            for var in frame.variables:
                if var.target_address and var.target_address in heap_addr_map:
                    p1 = stack_addr_map.get(var.address)
                    p2 = heap_addr_map.get(var.target_address)
                    if p1 and p2:
                        self.scene.addLine(p1[0], p1[1], p2[0], p2[1], pen_arrow)
                        self._draw_arrow_head(p1, p2, pen_arrow)

    def _draw_arrow_head(self, p1, p2, pen):
        x, y = p2
        poly = QPolygonF([
            QPointF(x, y),
            QPointF(x - 6, y - 4),
            QPointF(x - 6, y + 4)
        ])
        self.scene.addPolygon(poly, pen, QBrush(QColor("#7c3aed")))


class MemorySimulatorTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_scenario_idx = 0
        self.current_step_idx = 0
        self._init_ui()
        self.load_scenario(0)

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 12, 14, 12)
        main_layout.setSpacing(8)

        # Control Bar
        top_bar = QFrame()
        top_bar.setProperty("class", "DlcCard")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(10, 6, 10, 6)
        top_layout.setSpacing(10)

        top_layout.addWidget(QLabel("Scenario:"))
        self.cb_scenario = QComboBox()
        for sc in MEMORY_SCENARIOS:
            self.cb_scenario.addItem(sc.title, sc.id)
        self.cb_scenario.currentIndexChanged.connect(self.on_scenario_changed)
        top_layout.addWidget(self.cb_scenario, 2)

        top_layout.addSpacing(10)

        self.btn_prev = QPushButton("Previous")
        self.btn_prev.clicked.connect(self.prev_step)
        top_layout.addWidget(self.btn_prev)

        self.lbl_step_counter = QLabel("Step 1 / 4")
        self.lbl_step_counter.setStyleSheet("font-weight: 600; color: #a855f7; padding: 0 4px;")
        top_layout.addWidget(self.lbl_step_counter)

        self.btn_next = QPushButton("Next")
        self.btn_next.setProperty("class", "PrimaryBtn")
        self.btn_next.clicked.connect(self.next_step)
        top_layout.addWidget(self.btn_next)

        self.btn_reset = QPushButton("Reset")
        self.btn_reset.clicked.connect(self.reset_steps)
        top_layout.addWidget(self.btn_reset)

        main_layout.addWidget(top_bar)

        # Body Splitter: Left (Code) vs Right (Diagram)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(6)

        self.code_editor = PolyglotCodeEditor(read_only=True)
        splitter.addWidget(self.code_editor)

        self.visualizer = MemoryVisualizerWidget()
        splitter.addWidget(self.visualizer)

        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 6)

        main_layout.addWidget(splitter, 1)

    def on_scenario_changed(self, idx):
        self.load_scenario(idx)

    def load_scenario(self, idx):
        if idx < 0 or idx >= len(MEMORY_SCENARIOS):
            return
        self.current_scenario_idx = idx
        self.current_step_idx = 0
        scenario = MEMORY_SCENARIOS[idx]

        self.code_editor.set_language(scenario.language)
        self.code_editor.setPlainText("\n".join(scenario.code_lines))
        self.update_step_view()

    def update_step_view(self):
        scenario = MEMORY_SCENARIOS[self.current_scenario_idx]
        total_steps = len(scenario.steps)
        if self.current_step_idx < 0:
            self.current_step_idx = 0
        if self.current_step_idx >= total_steps:
            self.current_step_idx = total_steps - 1

        step = scenario.steps[self.current_step_idx]
        self.lbl_step_counter.setText(f"Step {self.current_step_idx + 1} / {total_steps}")
        self.visualizer.render_step(step)

    def next_step(self):
        scenario = MEMORY_SCENARIOS[self.current_scenario_idx]
        if self.current_step_idx < len(scenario.steps) - 1:
            self.current_step_idx += 1
            self.update_step_view()

    def prev_step(self):
        if self.current_step_idx > 0:
            self.current_step_idx -= 1
            self.update_step_view()

    def reset_steps(self):
        self.current_step_idx = 0
        self.update_step_view()
