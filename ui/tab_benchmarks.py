import numpy as np
import matplotlib
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
    QTableWidget, QTableWidgetItem, QHeaderView, QSplitter
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from core.benchmarks_data import BENCHMARKS, ALGORITHMS

class BenchmarkRadarTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Header Title
        lbl_title = QLabel("Architectural Tradeoff Radar & Algorithmic Complexity Matrix")
        lbl_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #f8fafc;")
        main_layout.addWidget(lbl_title)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(6)

        # Left Column: Matplotlib Radar Chart
        radar_panel = QFrame()
        radar_panel.setStyleSheet("background-color: #0b1120; border: 1px solid #1e293b; border-radius: 8px;")
        radar_layout = QVBoxLayout(radar_panel)
        radar_layout.setContentsMargins(8, 8, 8, 8)

        lbl_chart_header = QLabel("Multi-Paradigm Performance Vector (Relative Scale 1-10)")
        lbl_chart_header.setStyleSheet("font-weight: 600; color: #38bdf8; font-size: 12px;")
        radar_layout.addWidget(lbl_chart_header)

        self.figure, self.ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
        self.figure.patch.set_facecolor("#0b1120")
        self.ax.set_facecolor("#080c14")

        self.canvas = FigureCanvas(self.figure)
        radar_layout.addWidget(self.canvas)
        splitter.addWidget(radar_panel)

        # Right Column: Big-O Complexity Table
        table_panel = QFrame()
        table_panel.setStyleSheet("background-color: #0b1120; border: 1px solid #1e293b; border-radius: 8px;")
        table_layout = QVBoxLayout(table_panel)
        table_layout.setContentsMargins(10, 8, 10, 10)

        lbl_table_header = QLabel("High-Level Data Structures & Cache Locality")
        lbl_table_header.setStyleSheet("font-weight: 600; color: #f59e0b; font-size: 12px;")
        table_layout.addWidget(lbl_table_header)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Algorithm / Structure", "Avg Time", "Worst Time", "Space", "Cache Locality"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #080c14;
                color: #e2e8f0;
                border: 1px solid #1e293b;
                border-radius: 6px;
                gridline-color: #1e293b;
                font-size: 11px;
            }
            QHeaderView::section {
                background-color: #0f172a;
                color: #94a3b8;
                font-weight: 700;
                padding: 6px;
                border: 1px solid #1e293b;
            }
        """)
        self.populate_table()
        table_layout.addWidget(self.table)
        splitter.addWidget(table_panel)

        splitter.setStretchFactor(0, 5)
        splitter.setStretchFactor(1, 5)

        main_layout.addWidget(splitter, 1)

        self.plot_radar()

    def plot_radar(self):
        categories = ['Low Memory', 'Fast Startup', 'Throughput', 'Low Latency', 'Type Safety']
        N = len(categories)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]

        self.ax.clear()
        self.ax.set_theta_offset(np.pi / 2)
        self.ax.set_theta_direction(-1)
        self.ax.set_rlabel_position(0)
        self.ax.tick_params(colors='#94a3b8', labelsize=9)
        self.ax.spines['polar'].set_color('#1e293b')
        self.ax.grid(color='#1e293b', linestyle='--')

        plt.xticks(angles[:-1], categories, color="#cbd5e1", size=9)

        # Plot Rust
        rust_vals = [9.5, 9.8, 10.0, 9.8, 10.0]
        rust_vals += rust_vals[:1]
        self.ax.plot(angles, rust_vals, linewidth=2, linestyle='solid', color='#f97316', label='Rust')
        self.ax.fill(angles, rust_vals, '#f97316', alpha=0.15)

        # Plot Go
        go_vals = [8.0, 8.5, 9.0, 8.8, 8.0]
        go_vals += go_vals[:1]
        self.ax.plot(angles, go_vals, linewidth=2, linestyle='solid', color='#06b6d4', label='Go')
        self.ax.fill(angles, go_vals, '#06b6d4', alpha=0.15)

        # Plot TypeScript
        ts_vals = [6.5, 6.0, 6.5, 5.5, 8.0]
        ts_vals += ts_vals[:1]
        self.ax.plot(angles, ts_vals, linewidth=1.5, linestyle='solid', color='#3b82f6', label='TypeScript')
        self.ax.fill(angles, ts_vals, '#3b82f6', alpha=0.10)

        # Plot Python
        py_vals = [6.0, 6.5, 4.0, 4.0, 7.0]
        py_vals += py_vals[:1]
        self.ax.plot(angles, py_vals, linewidth=1.5, linestyle='solid', color='#eab308', label='Python')
        self.ax.fill(angles, py_vals, '#eab308', alpha=0.10)

        legend = self.ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), facecolor='#0f172a', edgecolor='#1e293b')
        for text in legend.get_texts():
            text.set_color('#f8fafc')

        self.canvas.draw()

    def populate_table(self):
        self.table.setRowCount(len(ALGORITHMS))
        for row, algo in enumerate(ALGORITHMS):
            item_name = QTableWidgetItem(algo.name)
            item_avg = QTableWidgetItem(algo.avg_time)
            item_worst = QTableWidgetItem(algo.worst_time)
            item_space = QTableWidgetItem(algo.space_complexity)
            item_cache = QTableWidgetItem(algo.cache_locality)

            item_name.setForeground(QColor("#38bdf8"))
            item_avg.setForeground(QColor("#10b981"))
            item_worst.setForeground(QColor("#f59e0b"))
            item_space.setForeground(QColor("#e2e8f0"))
            item_cache.setForeground(QColor("#c084fc"))

            self.table.setItem(row, 0, item_name)
            self.table.setItem(row, 1, item_avg)
            self.table.setItem(row, 2, item_worst)
            self.table.setItem(row, 3, item_space)
            self.table.setItem(row, 4, item_cache)
