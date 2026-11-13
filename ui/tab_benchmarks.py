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
        main_layout.setContentsMargins(16, 14, 16, 14)
        main_layout.setSpacing(10)

        # Header Title
        lbl_title = QLabel("[METRICS] Algorithmic Complexity & Architecture Vectors")
        lbl_title.setStyleSheet("font-size: 13px; font-weight: 700; color: #e5e7eb; font-family: 'Consolas', monospace;")
        main_layout.addWidget(lbl_title)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(4)

        # Left Column: Matplotlib Radar Chart
        radar_panel = QFrame()
        radar_panel.setStyleSheet("background-color: #0e0f14; border: 1px solid #1c1d27; border-radius: 6px;")
        radar_layout = QVBoxLayout(radar_panel)
        radar_layout.setContentsMargins(8, 6, 8, 6)
        radar_layout.setSpacing(4)

        lbl_chart_header = QLabel("Runtime Characteristic Vectors (Scale 1-10)")
        lbl_chart_header.setStyleSheet("font-weight: 600; color: #6b7280; font-size: 11px; font-family: 'Consolas', monospace;")
        radar_layout.addWidget(lbl_chart_header)

        self.figure, self.ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
        self.figure.patch.set_facecolor("#0e0f14")
        self.ax.set_facecolor("#0a0b0e")

        self.canvas = FigureCanvas(self.figure)
        radar_layout.addWidget(self.canvas)
        splitter.addWidget(radar_panel)

        # Right Column: Big-O Complexity Table
        table_panel = QFrame()
        table_panel.setStyleSheet("background-color: #0e0f14; border: 1px solid #1c1d27; border-radius: 6px;")
        table_layout = QVBoxLayout(table_panel)
        table_layout.setContentsMargins(8, 6, 8, 6)
        table_layout.setSpacing(4)

        lbl_table_header = QLabel("Data Structure Performance & Memory Hierarchy")
        lbl_table_header.setStyleSheet("font-weight: 600; color: #6b7280; font-size: 11px; font-family: 'Consolas', monospace;")
        table_layout.addWidget(lbl_table_header)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Algorithm / Structure", "Average", "Worst Case", "Space", "Cache Locality"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #0a0b0e;
                color: #d1d5db;
                border: 1px solid #1c1d27;
                border-radius: 4px;
                gridline-color: #171822;
                font-family: 'Consolas', monospace;
                font-size: 11px;
            }
            QHeaderView::section {
                background-color: #12131a;
                color: #9ca3af;
                font-weight: 600;
                padding: 4px;
                border: 1px solid #1c1d27;
                font-family: 'Consolas', monospace;
                font-size: 10px;
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
        categories = ['Low Memory', 'Cold Start', 'Throughput', 'Low Latency', 'Type Safety']
        N = len(categories)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]

        self.ax.clear()
        self.ax.set_theta_offset(np.pi / 2)
        self.ax.set_theta_direction(-1)
        self.ax.set_rlabel_position(0)
        self.ax.tick_params(colors='#6b7280', labelsize=8)
        self.ax.spines['polar'].set_color('#1c1d27')
        self.ax.grid(color='#1c1d27', linestyle='--')

        plt.xticks(angles[:-1], categories, color="#9ca3af", size=8, fontfamily="sans-serif")

        # Plot Rust
        rust_vals = [9.5, 9.8, 10.0, 9.8, 10.0]
        rust_vals += rust_vals[:1]
        self.ax.plot(angles, rust_vals, linewidth=1.8, color='#f97316', label='Rust')
        self.ax.fill(angles, rust_vals, '#f97316', alpha=0.10)

        # Plot Go
        go_vals = [8.0, 8.5, 9.0, 8.8, 8.0]
        go_vals += go_vals[:1]
        self.ax.plot(angles, go_vals, linewidth=1.8, color='#06b6d4', label='Go')
        self.ax.fill(angles, go_vals, '#06b6d4', alpha=0.10)

        # Plot TypeScript
        ts_vals = [6.5, 6.0, 6.5, 5.5, 8.0]
        ts_vals += ts_vals[:1]
        self.ax.plot(angles, ts_vals, linewidth=1.2, color='#38bdf8', label='TypeScript')
        self.ax.fill(angles, ts_vals, '#38bdf8', alpha=0.08)

        # Plot Python
        py_vals = [6.0, 6.5, 4.0, 4.0, 7.0]
        py_vals += py_vals[:1]
        self.ax.plot(angles, py_vals, linewidth=1.2, color='#eab308', label='Python')
        self.ax.fill(angles, py_vals, '#eab308', alpha=0.08)

        legend = self.ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), facecolor='#12131a', edgecolor='#1c1d27')
        for text in legend.get_texts():
            text.set_color('#d1d5db')
            text.set_fontsize(8)

        self.canvas.draw()

    def populate_table(self):
        self.table.setRowCount(len(ALGORITHMS))
        for row, algo in enumerate(ALGORITHMS):
            item_name = QTableWidgetItem(algo.name)
            item_avg = QTableWidgetItem(algo.avg_time)
            item_worst = QTableWidgetItem(algo.worst_time)
            item_space = QTableWidgetItem(algo.space_complexity)
            item_cache = QTableWidgetItem(algo.cache_locality)

            item_name.setForeground(QColor("#e5e7eb"))
            item_avg.setForeground(QColor("#10b981"))
            item_worst.setForeground(QColor("#f59e0b"))
            item_space.setForeground(QColor("#9ca3af"))
            item_cache.setForeground(QColor("#a855f7"))

            self.table.setItem(row, 0, item_name)
            self.table.setItem(row, 1, item_avg)
            self.table.setItem(row, 2, item_worst)
            self.table.setItem(row, 3, item_space)
            self.table.setItem(row, 4, item_cache)
