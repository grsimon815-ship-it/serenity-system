"""
Serenity System Theme
Clean, high-legibility dark theme:
- Deep background: #0c0d11
- Surface / Cards: #13151b
- Borders: #222530
- Primary accent: #7c3aed
- Crisp UI typography: 'Segoe UI Variable Text', 'Segoe UI', sans-serif (13px)
- Crisp Code typography: 'Cascadia Code', 'Consolas', monospace (12px)
"""

SERENITY_THEME = """
QMainWindow, QWidget#CentralWidget {
    background-color: #0c0d11;
    color: #e2e8f0;
    font-family: 'Segoe UI Variable Text', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 13px;
}

/* Sidebar */
QFrame#SidebarFrame {
    background-color: #0f1016;
    border-right: 1px solid #1e2029;
}

QLabel#LogoTitle {
    font-size: 15px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 0.5px;
    padding: 6px 4px;
}

/* Sidebar Navigation Buttons */
QPushButton.SidebarNavBtn {
    background-color: transparent;
    color: #94a3b8;
    border: none;
    border-radius: 6px;
    text-align: left;
    padding: 9px 12px;
    font-size: 13px;
    font-weight: 500;
}
QPushButton.SidebarNavBtn:hover {
    background-color: #1a1c24;
    color: #ffffff;
}
QPushButton.SidebarNavBtn:checked, QPushButton.SidebarNavBtn.Active {
    background-color: #1e202b;
    color: #ffffff;
    border-left: 3px solid #7c3aed;
    font-weight: 600;
}

/* Header Bar */
QFrame#TopHeaderBar {
    background-color: #0f1016;
    border-bottom: 1px solid #1e2029;
}
QLineEdit#SearchBar {
    background-color: #14161f;
    color: #f8fafc;
    border: 1px solid #242735;
    border-radius: 6px;
    padding: 7px 12px;
    font-size: 13px;
}
QLineEdit#SearchBar:focus {
    border: 1px solid #7c3aed;
    background-color: #181a25;
}

/* Cards & Containers */
QFrame.DlcCard {
    background-color: #13151b;
    border: 1px solid #20232e;
    border-radius: 6px;
}

/* Buttons */
QPushButton {
    background-color: #181a24;
    color: #e2e8f0;
    border: 1px solid #262938;
    padding: 6px 14px;
    border-radius: 5px;
    font-size: 12px;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #222533;
    border-color: #3b4055;
    color: #ffffff;
}
QPushButton:pressed {
    background-color: #151720;
}
QPushButton.PrimaryBtn {
    background-color: #7c3aed;
    border: 1px solid #8b5cf6;
    color: #ffffff;
    font-weight: 600;
}
QPushButton.PrimaryBtn:hover {
    background-color: #8b5cf6;
}

/* ComboBox */
QComboBox {
    background-color: #14161f;
    border: 1px solid #242735;
    border-radius: 5px;
    padding: 5px 10px;
    color: #f1f5f9;
    font-size: 12px;
}
QComboBox:hover {
    border-color: #7c3aed;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 22px;
    border-left: 1px solid #242735;
}
QComboBox QAbstractItemView {
    background-color: #14161f;
    border: 1px solid #242735;
    selection-background-color: #7c3aed;
    selection-color: #ffffff;
    color: #f1f5f9;
    padding: 4px;
}

/* ScrollBars */
QScrollBar:vertical {
    background: #0c0d11;
    width: 8px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #252837;
    min-height: 20px;
    border-radius: 4px;
}
QScrollBar::handle:vertical:hover {
    background: #7c3aed;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar:horizontal {
    background: #0c0d11;
    height: 8px;
    margin: 0px;
}
QScrollBar::handle:horizontal {
    background: #252837;
    min-width: 20px;
    border-radius: 4px;
}
QScrollBar::handle:horizontal:hover {
    background: #7c3aed;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Status Bar */
QStatusBar {
    background-color: #0c0d11;
    color: #94a3b8;
    border-top: 1px solid #1e2029;
    font-size: 12px;
    padding: 3px 10px;
}
"""
