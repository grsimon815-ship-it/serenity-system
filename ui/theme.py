"""
Modern Dark Glassmorphic & Cyber Styling for PolyglotForge
"""

DARK_THEME_QSS = """
QMainWindow, QWidget#CentralWidget {
    background-color: #080c14;
    color: #e2e8f0;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
}

/* ScrollBars */
QScrollBar:vertical {
    background: #0f172a;
    width: 10px;
    margin: 0px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background: #334155;
    min-height: 20px;
    border-radius: 5px;
}
QScrollBar::handle:vertical:hover {
    background: #6366f1;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar:horizontal {
    background: #0f172a;
    height: 10px;
    margin: 0px;
    border-radius: 5px;
}
QScrollBar::handle:horizontal {
    background: #334155;
    min-width: 20px;
    border-radius: 5px;
}
QScrollBar::handle:horizontal:hover {
    background: #6366f1;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Tabs */
QTabWidget::pane {
    border: 1px solid #1e293b;
    background-color: #0b1120;
    border-radius: 8px;
    top: -1px;
}
QTabBar::tab {
    background-color: #0f172a;
    color: #94a3b8;
    padding: 10px 18px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: 600;
    font-size: 13px;
    border: 1px solid #1e293b;
    border-bottom: none;
}
QTabBar::tab:selected {
    background-color: #0b1120;
    color: #38bdf8;
    border-top: 2px solid #38bdf8;
    border-left: 1px solid #1e293b;
    border-right: 1px solid #1e293b;
}
QTabBar::tab:hover:!selected {
    background-color: #1e293b;
    color: #f1f5f9;
}

/* Cards & Frames */
QFrame.CardFrame {
    background-color: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 10px;
}
QFrame.CardFrame:hover {
    border: 1px solid #334155;
}

/* Buttons */
QPushButton {
    background-color: #1e293b;
    color: #f8fafc;
    border: 1px solid #334155;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: 600;
    font-size: 12px;
}
QPushButton:hover {
    background-color: #334155;
    border-color: #6366f1;
    color: #ffffff;
}
QPushButton:pressed {
    background-color: #4338ca;
}
QPushButton.PrimaryBtn {
    background-color: #4f46e5;
    border: 1px solid #6366f1;
    color: #ffffff;
}
QPushButton.PrimaryBtn:hover {
    background-color: #6366f1;
    border-color: #818cf8;
}
QPushButton.SuccessBtn {
    background-color: #059669;
    border: 1px solid #10b981;
    color: #ffffff;
}
QPushButton.SuccessBtn:hover {
    background-color: #10b981;
}
QPushButton.DangerBtn {
    background-color: #dc2626;
    border: 1px solid #ef4444;
    color: #ffffff;
}
QPushButton.DangerBtn:hover {
    background-color: #ef4444;
}

/* ComboBox */
QComboBox {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 6px 12px;
    color: #f8fafc;
    font-size: 12px;
    font-weight: 500;
}
QComboBox:hover {
    border-color: #6366f1;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 25px;
    border-left: 1px solid #334155;
}
QComboBox QAbstractItemView {
    background-color: #0f172a;
    border: 1px solid #334155;
    selection-background-color: #4f46e5;
    selection-color: #ffffff;
    color: #e2e8f0;
    padding: 4px;
}

/* Labels */
QLabel {
    color: #cbd5e1;
}
QLabel.TitleLabel {
    font-size: 18px;
    font-weight: 700;
    color: #f8fafc;
}
QLabel.SubtitleLabel {
    font-size: 12px;
    color: #94a3b8;
}
QLabel.BadgeLabel {
    background-color: #1e293b;
    color: #38bdf8;
    border: 1px solid #0284c7;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: 600;
}

/* Status Bar */
QStatusBar {
    background-color: #05080f;
    color: #64748b;
    border-top: 1px solid #1e293b;
    font-size: 11px;
}
"""
