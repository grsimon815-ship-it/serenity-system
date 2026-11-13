from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QPushButton, QFrame, QSplitter, QGraphicsView, QGraphicsScene,
    QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem, QGraphicsPolygonItem
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
        self.setBackgroundBrush(QBrush(QColor("#0a0b0e")))
        self.setRenderHint(self.renderHints())
        self.setStyleSheet("border: 1px solid #1c1d27; border-radius: 6px;")

    def render_step(self, step):
        self.scene.clear()
        if not step:
            return

        font_header = QFont("Consolas", 10, QFont.Weight.Bold)
        font_box = QFont("Consolas", 9)
        font_sub = QFont("Consolas", 8)

        # 1. Stack Column
        lbl_stack = self.scene.addText("STACK (Call Frames)", font_header)
        lbl_stack.setDefaultTextColor(QColor("#38bdf8"))
        lbl_stack.setPos(20, 10)

        # 2. Heap Column
        lbl_heap = self.scene.addText("HEAP (Dynamic Allocations)", font_header)
        lbl_heap.setDefaultTextColor(QColor("#a855f7"))
        lbl_heap.setPos(380, 10)

        # Divider line
        pen_divider = QPen(QColor("#1c1d27"), 1, Qt.PenStyle.DashLine)
        self.scene.addLine(340, 10, 340, 500, pen_divider)

        stack_addr_map = {}
        heap_addr_map = {}

        # Render Stack Frames
        y_cursor = 40
        for frame in step.stack:
            frame_title = self.scene.addText(f">> {frame.func_name}", font_sub)
            frame_title.setDefaultTextColor(QColor("#6b7280"))
            frame_title.setPos(25, y_cursor)
            y_cursor += 22

            for var in frame.variables:
                border_col = QColor(var.color_hex if not var.is_freed else "#ef4444")
                self.scene.addRect(25, y_cursor, 280, 44, 
                                  QPen(border_col, 1.2), 
                                  QBrush(QColor("#111218")))
                stack_addr_map[var.address] = (25 + 280, y_cursor + 22)

                t_var = self.scene.addText(f"{var.label} [{var.address}]", font_box)
                t_var.setDefaultTextColor(QColor("#e5e7eb"))
                t_var.setPos(30, y_cursor + 2)

                t_val = self.scene.addText(f"Value: {var.value} ({var.size_bytes}B)", font_sub)
                t_val.setDefaultTextColor(QColor("#9ca3af" if not var.is_freed else "#ef4444"))
                t_val.setPos(30, y_cursor + 20)

                y_cursor += 50

        # Render Heap Blocks
        y_heap = 40
        for block in step.heap:
            border_color = QColor(block.color_hex if not block.is_freed else "#ef4444")
            bg_color = QColor("#111218" if not block.is_freed else "#170f11")
            
            self.scene.addRect(380, y_heap, 320, 48, 
                              QPen(border_color, 1.2), 
                              QBrush(bg_color))
            heap_addr_map[block.address] = (380, y_heap + 24)

            t_hb = self.scene.addText(f"{block.label} @ {block.address}", font_box)
            t_hb.setDefaultTextColor(QColor("#e5e7eb" if not block.is_freed else "#ef4444"))
            t_hb.setPos(386, y_heap + 2)

            t_val = self.scene.addText(f"Payload: {block.value} | Size: {block.size_bytes}B", font_sub)
            t_val.setDefaultTextColor(QColor("#9ca3af" if not block.is_freed else "#6b7280"))
            t_val.setPos(386, y_heap + 22)

            y_heap += 56

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
        main_layout.setContentsMargins(16, 14, 16, 14)
        main_layout.setSpacing(10)

        # Control Bar
        top_bar = QFrame()
        top_bar.setProperty("class", "DlcCard")
        top_bar.setStyleSheet("background-color: #0e0f14; border: 1px solid #1c1d27; border-radius: 6px; padding: 4px;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(8, 4, 8, 4)
        top_layout.setSpacing(8)

        lbl_scenario = QLabel("Scenario:")
        lbl_scenario.setStyleSheet("font-weight: 600; color: #9ca3af; font-size: 11px;")
        top_layout.addWidget(lbl_scenario)

        self.cb_scenario = QComboBox()
        for sc in MEMORY_SCENARIOS:
            self.cb_scenario.addItem(sc.title, sc.id)
        self.cb_scenario.currentIndexChanged.connect(self.on_scenario_changed)
        top_layout.addWidget(self.cb_scenario, 2)

        top_layout.addSpacing(12)

        self.btn_prev = QPushButton("Prev Step")
        self.btn_prev.clicked.connect(self.prev_step)
        top_layout.addWidget(self.btn_prev)

        self.lbl_step_counter = QLabel("Step 1 / 4")
        self.lbl_step_counter.setStyleSheet("font-family: 'Consolas', monospace; color: #a855f7; font-size: 11px;")
        top_layout.addWidget(self.lbl_step_counter)

        self.btn_next = QPushButton("Next Step")
        self.btn_next.setProperty("class", "PrimaryBtn")
        self.btn_next.clicked.connect(self.next_step)
        top_layout.addWidget(self.btn_next)

        self.btn_reset = QPushButton("Reset")
        self.btn_reset.clicked.connect(self.reset_steps)
        top_layout.addWidget(self.btn_reset)

        main_layout.addWidget(top_bar)

        # Splitter: Left (Code & Step Explanation) vs Right (Visual Diagram)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(4)

        # Left Column: Code & Step Note
        left_panel = QFrame()
        left_panel.setStyleSheet("background-color: #0e0f14; border: 1px solid #1c1d27; border-radius: 6px;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(8, 6, 8, 6)
        left_layout.setSpacing(4)

        lbl_code_title = QLabel("Source Execution Flow")
        lbl_code_title.setStyleSheet("font-weight: 600; color: #6b7280; font-size: 11px; font-family: 'Consolas', monospace;")
        left_layout.addWidget(lbl_code_title)

        self.code_editor = PolyglotCodeEditor(read_only=True)
        left_layout.addWidget(self.code_editor, 1)

        # Step Detail Box
        self.step_box = QFrame()
        self.step_box.setStyleSheet("background-color: #0a0b0e; border: 1px solid #1c1d27; border-radius: 4px; padding: 6px;")
        step_layout = QVBoxLayout(self.step_box)
        step_layout.setSpacing(2)

        self.lbl_action = QLabel()
        self.lbl_action.setStyleSheet("font-weight: 700; color: #e5e7eb; font-size: 11px; font-family: 'Consolas', monospace;")
        step_layout.addWidget(self.lbl_action)

        self.lbl_explanation = QLabel()
        self.lbl_explanation.setWordWrap(True)
        self.lbl_explanation.setStyleSheet("color: #9ca3af; font-size: 11px;")
        step_layout.addWidget(self.lbl_explanation)

        self.lbl_notes = QLabel()
        self.lbl_notes.setWordWrap(True)
        self.lbl_notes.setStyleSheet("color: #6b7280; font-size: 10px; font-family: 'Consolas', monospace;")
        step_layout.addWidget(self.lbl_notes)

        left_layout.addWidget(self.step_box)
        splitter.addWidget(left_panel)

        # Right Column: Memory Diagram
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
        self.lbl_action.setText(f">> {step.action_title} (Line {step.line_number})")
        self.lbl_explanation.setText(step.explanation)
        self.lbl_notes.setText(f"Underlying layout: {step.notes}")

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
