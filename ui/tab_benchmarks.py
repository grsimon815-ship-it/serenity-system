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
        main_layout.setContentsMargins(14, 12, 14, 12)
        main_layout.setSpacing(8)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(6)

        # Left Column: Radar Chart
        radar_panel = QFrame()
        radar_panel.setStyleSheet("background-color: #0d0e14; border: 1px solid #1e2029; border-radius: 6px;")
        radar_layout = QVBoxLayout(radar_panel)
        radar_layout.setContentsMargins(8, 8, 8, 8)
        radar_layout.setSpacing(4)

        self.figure, self.ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
        self.figure.patch.set_facecolor("#0d0e14")
        self.ax.set_facecolor("#090a0f")

        self.canvas = FigureCanvas(self.figure)
        radar_layout.addWidget(self.canvas)
        splitter.addWidget(radar_panel)

        # Right Column: Complexity Table
        table_panel = QFrame()
        table_panel.setStyleSheet("background-color: #0d0e14; border: 1px solid #1e2029; border-radius: 6px;")
        table_layout = QVBoxLayout(table_panel)
        table_layout.setContentsMargins(8, 8, 8, 8)
        table_layout.setSpacing(4)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Algorithm", "Average", "Worst", "Space", "Cache Locality"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #090a0f;
                color: #e2e8f0;
                border: 1px solid #1e2029;
                border-radius: 4px;
                gridline-color: #1a1c25;
                font-family: 'Cascadia Code', monospace;
                font-size: 11px;
            }
            QHeaderView::section {
                background-color: #14161f;
                color: #94a3b8;
                font-weight: 600;
                padding: 6px;
                border: 1px solid #1e2029;
                font-family: 'Segoe UI', sans-serif;
                font-size: 11px;
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
        self.ax.tick_params(colors='#64748b', labelsize=9)
        self.ax.spines['polar'].set_color('#1e2029')
        self.ax.grid(color='#1e2029', linestyle='--')

        plt.xticks(angles[:-1], categories, color="#cbd5e1", size=9, fontfamily="sans-serif")

        rust_vals = [9.5, 9.8, 10.0, 9.8, 10.0]
        rust_vals += rust_vals[:1]
        self.ax.plot(angles, rust_vals, linewidth=2, color='#f97316', label='Rust')
        self.ax.fill(angles, rust_vals, '#f97316', alpha=0.10)

        go_vals = [8.0, 8.5, 9.0, 8.8, 8.0]
        go_vals += go_vals[:1]
        self.ax.plot(angles, go_vals, linewidth=2, color='#06b6d4', label='Go')
        self.ax.fill(angles, go_vals, '#06b6d4', alpha=0.10)

        ts_vals = [6.5, 6.0, 6.5, 5.5, 8.0]
        ts_vals += ts_vals[:1]
        self.ax.plot(angles, ts_vals, linewidth=1.5, color='#38bdf8', label='TypeScript')
        self.ax.fill(angles, ts_vals, '#38bdf8', alpha=0.08)

        py_vals = [6.0, 6.5, 4.0, 4.0, 7.0]
        py_vals += py_vals[:1]
        self.ax.plot(angles, py_vals, linewidth=1.5, color='#eab308', label='Python')
        self.ax.fill(angles, py_vals, '#eab308', alpha=0.08)

        legend = self.ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), facecolor='#14161f', edgecolor='#1e2029')
        for text in legend.get_texts():
            text.set_color('#e2e8f0')
            text.set_fontsize(9)

        self.canvas.draw()

    def populate_table(self):
        self.table.setRowCount(len(ALGORITHMS))
        for row, algo in enumerate(ALGORITHMS):
            item_name = QTableWidgetItem(algo.name)
            item_avg = QTableWidgetItem(algo.avg_time)
            item_worst = QTableWidgetItem(algo.worst_time)
            item_space = QTableWidgetItem(algo.space_complexity)
            item_cache = QTableWidgetItem(algo.cache_locality)

            item_name.setForeground(QColor("#f8fafc"))
            item_avg.setForeground(QColor("#10b981"))
            item_worst.setForeground(QColor("#f59e0b"))
            item_space.setForeground(QColor("#94a3b8"))
            item_cache.setForeground(QColor("#a855f7"))

            self.table.setItem(row, 0, item_name)
            self.table.setItem(row, 1, item_avg)
            self.table.setItem(row, 2, item_worst)
            self.table.setItem(row, 3, item_space)
            self.table.setItem(row, 4, item_cache)
