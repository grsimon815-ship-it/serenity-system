"""
SystemDLC Design System & Dark Theme for PolyglotForge
Inspired by System Client (systemdlc.com):
- Deep Obsidian / Void Black palette (#090a0f, #0f1118, #151822)
- Electric Amethyst & Violet accents (#7c3aed, #8b5cf6, #a855f7)
- Cyan & Emerald telemetry glows (#06b6d4, #10b981)
- Tight, responsive, pro-client layout (Zero AI-slop, clean minimalism)
"""

SYSTEM_DLC_THEME = """
/* Global Window & Background */
QMainWindow, QWidget#CentralWidget {
    background-color: #08090d;
    color: #e2e8f0;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', Roboto, sans-serif;
    font-size: 13px;
}

/* Left Sidebar */
QFrame#SidebarFrame {
    background-color: #0b0d13;
    border-right: 1px solid #161922;
}

/* Sidebar Logo & Branding */
QLabel#LogoTitle {
    font-size: 17px;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: 1.5px;
}
QLabel#LogoSubtitle {
    font-size: 10px;
    font-weight: 700;
    color: #8b5cf6;
    letter-spacing: 2px;
}
QLabel#SidebarCategoryHeader {
    font-size: 10px;
    font-weight: 800;
    color: #475069;
    letter-spacing: 1.2px;
    padding-top: 12px;
    padding-bottom: 4px;
    padding-left: 8px;
}

/* Sidebar Navigation Buttons */
QPushButton.SidebarNavBtn {
    background-color: transparent;
    color: #8f9bb3;
    border: none;
    border-radius: 8px;
    text-align: left;
    padding: 10px 14px;
    font-size: 13px;
    font-weight: 600;
}
QPushButton.SidebarNavBtn:hover {
    background-color: #131620;
    color: #f1f5f9;
}
QPushButton.SidebarNavBtn:checked, QPushButton.SidebarNavBtn.Active {
    background-color: #181b26;
    color: #a855f7;
    border-left: 3px solid #8b5cf6;
    border-radius: 6px;
    font-weight: 700;
}

/* Telemetry Card in Sidebar Footer */
QFrame#TelemetryFrame {
    background-color: #0e111a;
    border: 1px solid #1a1e2b;
    border-radius: 8px;
    padding: 8px;
}
QLabel#TelemetryText {
    font-size: 10px;
    color: #64748b;
    font-family: 'Consolas', monospace;
}

/* Header Top Bar */
QFrame#TopHeaderBar {
    background-color: #0b0d13;
    border-bottom: 1px solid #161922;
    padding: 8px 16px;
}
QLineEdit#SearchBar {
    background-color: #12151e;
    color: #f8fafc;
    border: 1px solid #1e2330;
    border-radius: 7px;
    padding: 7px 14px;
    font-size: 12px;
}
QLineEdit#SearchBar:focus {
    border: 1px solid #7c3aed;
    background-color: #151824;
}

/* Cards & Surface Containers */
QFrame.DlcCard {
    background-color: #0e1119;
    border: 1px solid #181b26;
    border-radius: 9px;
}
QFrame.DlcCard:hover {
    border: 1px solid #232838;
}

/* Buttons */
QPushButton {
    background-color: #141722;
    color: #e2e8f0;
    border: 1px solid #202534;
    padding: 7px 14px;
    border-radius: 6px;
    font-weight: 600;
    font-size: 12px;
}
QPushButton:hover {
    background-color: #1a1e2c;
    border-color: #3b435b;
    color: #ffffff;
}
QPushButton:pressed {
    background-color: #11131c;
}
QPushButton.PrimaryBtn, QPushButton.DlcAccentBtn {
    background-color: #6d28d9;
    border: 1px solid #7c3aed;
    color: #ffffff;
}
QPushButton.PrimaryBtn:hover, QPushButton.DlcAccentBtn:hover {
    background-color: #7c3aed;
    border-color: #8b5cf6;
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
    background-color: #991b1b;
    border: 1px solid #b91c1c;
    color: #ffffff;
}
QPushButton.DangerBtn:hover {
    background-color: #b91c1c;
}

/* ComboBox */
QComboBox {
    background-color: #12151e;
    border: 1px solid #1f2331;
    border-radius: 6px;
    padding: 6px 12px;
    color: #f1f5f9;
    font-size: 12px;
    font-weight: 500;
}
QComboBox:hover {
    border-color: #7c3aed;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
    border-left: 1px solid #1f2331;
}
QComboBox QAbstractItemView {
    background-color: #0e111a;
    border: 1px solid #1f2331;
    selection-background-color: #5b21b6;
    selection-color: #ffffff;
    color: #e2e8f0;
    padding: 4px;
}

/* ScrollBars */
QScrollBar:vertical {
    background: #090a0f;
    width: 8px;
    margin: 0px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #1f2433;
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
    background: #090a0f;
    height: 8px;
    margin: 0px;
    border-radius: 4px;
}
QScrollBar::handle:horizontal {
    background: #1f2433;
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
    background-color: #06070a;
    color: #64748b;
    border-top: 1px solid #141620;
    font-size: 11px;
    padding: 2px 8px;
}
"""
