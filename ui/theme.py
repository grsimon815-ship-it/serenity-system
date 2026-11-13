"""
SystemDLC Professional Dark Theme
Pure utilitarian dark palette:
- Background: #0a0b0e (Obsidian / Pitch Black)
- Surface: #111217 (Charcoal Card)
- Elevated / Focus: #171821
- Border: #1f212c (Hairline 1px)
- Border Focus: #7c3aed (System DLC Amethyst)
- Text Primary: #e1e4ea
- Text Muted: #6b7280
- Accent: #7c3aed
"""

SYSTEM_DLC_THEME = """
QMainWindow, QWidget#CentralWidget {
    background-color: #0a0b0e;
    color: #d1d5db;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 12px;
}

/* Left Sidebar */
QFrame#SidebarFrame {
    background-color: #0e0f14;
    border-right: 1px solid #1c1d26;
}

QLabel#LogoTitle {
    font-size: 14px;
    font-weight: 700;
    color: #f3f4f6;
    letter-spacing: 1px;
}
QLabel#LogoSubtitle {
    font-size: 10px;
    font-weight: 600;
    color: #7c3aed;
    letter-spacing: 1px;
}
QLabel#SidebarCategoryHeader {
    font-size: 10px;
    font-weight: 700;
    color: #4b5263;
    letter-spacing: 0.8px;
    padding-top: 10px;
    padding-bottom: 2px;
    padding-left: 6px;
}

/* Sidebar Navigation Buttons */
QPushButton.SidebarNavBtn {
    background-color: transparent;
    color: #8b92a4;
    border: none;
    border-radius: 4px;
    text-align: left;
    padding: 7px 10px;
    font-size: 12px;
    font-weight: 500;
}
QPushButton.SidebarNavBtn:hover {
    background-color: #15161f;
    color: #e5e7eb;
}
QPushButton.SidebarNavBtn:checked, QPushButton.SidebarNavBtn.Active {
    background-color: #181924;
    color: #f3f4f6;
    border-left: 2px solid #7c3aed;
    font-weight: 600;
}

/* Telemetry Card in Sidebar Footer */
QFrame#TelemetryFrame {
    background-color: #12131a;
    border: 1px solid #1f202b;
    border-radius: 6px;
    padding: 6px;
}
QLabel#TelemetryText {
    font-size: 10px;
    color: #6b7280;
    font-family: 'Consolas', monospace;
    line-height: 1.3;
}

/* Header Bar */
QFrame#TopHeaderBar {
    background-color: #0e0f14;
    border-bottom: 1px solid #1c1d26;
}
QLineEdit#SearchBar {
    background-color: #12131a;
    color: #e5e7eb;
    border: 1px solid #1f212c;
    border-radius: 5px;
    padding: 5px 10px;
    font-size: 12px;
}
QLineEdit#SearchBar:focus {
    border: 1px solid #7c3aed;
    background-color: #161722;
}

/* General Panels & Cards */
QFrame.DlcCard {
    background-color: #111218;
    border: 1px solid #1c1d27;
    border-radius: 6px;
}

/* Buttons */
QPushButton {
    background-color: #15161e;
    color: #d1d5db;
    border: 1px solid #232532;
    padding: 5px 12px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #1c1e2a;
    border-color: #353849;
    color: #ffffff;
}
QPushButton:pressed {
    background-color: #13141c;
}
QPushButton.PrimaryBtn {
    background-color: #6d28d9;
    border: 1px solid #7c3aed;
    color: #ffffff;
}
QPushButton.PrimaryBtn:hover {
    background-color: #7c3aed;
}
QPushButton.SuccessBtn {
    background-color: #065f46;
    border: 1px solid #059669;
    color: #ffffff;
}
QPushButton.SuccessBtn:hover {
    background-color: #059669;
}
QPushButton.DangerBtn {
    background-color: #881337;
    border: 1px solid #be123c;
    color: #ffffff;
}
QPushButton.DangerBtn:hover {
    background-color: #be123c;
}

/* ComboBox */
QComboBox {
    background-color: #12131a;
    border: 1px solid #1f212c;
    border-radius: 4px;
    padding: 4px 8px;
    color: #e5e7eb;
    font-size: 11px;
}
QComboBox:hover {
    border-color: #7c3aed;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid #1f212c;
}
QComboBox QAbstractItemView {
    background-color: #12131a;
    border: 1px solid #232532;
    selection-background-color: #5b21b6;
    selection-color: #ffffff;
    color: #e5e7eb;
    padding: 2px;
}

/* ScrollBars */
QScrollBar:vertical {
    background: #0a0b0e;
    width: 6px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #232533;
    min-height: 16px;
    border-radius: 3px;
}
QScrollBar::handle:vertical:hover {
    background: #7c3aed;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar:horizontal {
    background: #0a0b0e;
    height: 6px;
    margin: 0px;
}
QScrollBar::handle:horizontal {
    background: #232533;
    min-width: 16px;
    border-radius: 3px;
}
QScrollBar::handle:horizontal:hover {
    background: #7c3aed;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Status Bar */
QStatusBar {
    background-color: #0b0c10;
    color: #6b7280;
    border-top: 1px solid #181922;
    font-size: 11px;
    padding: 2px 8px;
    font-family: 'Consolas', monospace;
}
"""
