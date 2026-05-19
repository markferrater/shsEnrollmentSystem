COLORS = {
    'primary':    '#1B3A6B',   # Deep navy
    'secondary':  '#2E6DA4',   # Blue
    'accent':     '#4AA8D8',   # Sky blue
    'success':    '#27AE60',
    'warning':    '#F39C12',
    'danger':     '#E74C3C',
    'light_bg':   '#F0F4F8',
    'white':      '#FFFFFF',
    'text_dark':  '#1A2530',
    'text_muted': '#7F8C8D',
    'border':     '#D5DCE4',
    'sidebar_bg': '#1B3A6B',
    'card_bg':    '#FFFFFF',
    'header_bg':  '#1B3A6B',
}

APP_STYLE = f"""
QWidget {{
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 13px;
    color: {COLORS['text_dark']};
}}
QMainWindow {{
    background: {COLORS['light_bg']};
}}
QPushButton {{
    background: {COLORS['secondary']};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 18px;
    font-weight: 600;
    font-size: 13px;
    min-height: 34px;
}}
QPushButton:hover {{
    background: {COLORS['primary']};
}}
QPushButton:pressed {{
    background: #102850;
}}
QPushButton:disabled {{
    background: #B0BEC5;
    color: #78909C;
}}
QPushButton#danger_btn {{
    background: {COLORS['danger']};
}}
QPushButton#danger_btn:hover {{
    background: #C0392B;
}}
QPushButton#success_btn {{
    background: {COLORS['success']};
}}
QPushButton#success_btn:hover {{
    background: #1E8449;
}}
QPushButton#outline_btn {{
    background: transparent;
    color: {COLORS['secondary']};
    border: 2px solid {COLORS['secondary']};
}}
QPushButton#outline_btn:hover {{
    background: {COLORS['secondary']};
    color: white;
}}
QLineEdit, QTextEdit, QComboBox, QDateEdit {{
    border: 1.5px solid {COLORS['border']};
    border-radius: 5px;
    padding: 7px 10px;
    background: white;
    color: {COLORS['text_dark']};
    font-size: 13px;
}}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
    border-color: {COLORS['accent']};
}}
QComboBox::drop-down {{
    border: none;
    padding-right: 8px;
}}
QLabel {{
    color: {COLORS['text_dark']};
}}
QLabel#section_title {{
    font-size: 18px;
    font-weight: 700;
    color: {COLORS['primary']};
}}
QLabel#card_title {{
    font-size: 14px;
    font-weight: 600;
    color: {COLORS['primary']};
}}
QGroupBox {{
    border: 1.5px solid {COLORS['border']};
    border-radius: 8px;
    margin-top: 12px;
    padding: 10px;
    background: white;
    font-weight: 600;
    color: {COLORS['primary']};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: {COLORS['primary']};
    font-size: 13px;
    font-weight: 700;
}}
QTableWidget {{
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    background: white;
    gridline-color: {COLORS['border']};
    selection-background-color: {COLORS['accent']};
    selection-color: white;
}}
QTableWidget::item {{
    padding: 6px 10px;
}}
QHeaderView::section {{
    background: {COLORS['primary']};
    color: white;
    padding: 8px 10px;
    border: none;
    font-weight: 700;
    font-size: 12px;
}}
QScrollBar:vertical {{
    border: none;
    background: #EEF2F7;
    width: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: {COLORS['border']};
    border-radius: 4px;
}}
QTabWidget::pane {{
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    background: white;
}}
QTabBar::tab {{
    background: {COLORS['light_bg']};
    color: {COLORS['text_muted']};
    padding: 8px 20px;
    border: 1px solid {COLORS['border']};
    border-bottom: none;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    font-weight: 600;
}}
QTabBar::tab:selected {{
    background: {COLORS['primary']};
    color: white;
}}
QMessageBox {{
    background: white;
}}
"""

SIDEBAR_STYLE = f"""
QWidget#sidebar {{
    background: {COLORS['sidebar_bg']};
}}
QPushButton#nav_btn {{
    background: transparent;
    color: rgba(255,255,255,0.75);
    border: none;
    border-radius: 6px;
    padding: 10px 16px;
    text-align: left;
    font-size: 13px;
    font-weight: 500;
    min-height: 40px;
}}
QPushButton#nav_btn:hover {{
    background: rgba(255,255,255,0.12);
    color: white;
}}
QPushButton#nav_btn_active {{
    background: rgba(255,255,255,0.2);
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 16px;
    text-align: left;
    font-size: 13px;
    font-weight: 700;
    min-height: 40px;
    border-left: 3px solid #4AA8D8;
}}
QPushButton#logout_btn {{
    background: rgba(231,76,60,0.15);
    color: #FF8A80;
    border: 1px solid rgba(231,76,60,0.3);
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
    min-height: 36px;
}}
QPushButton#logout_btn:hover {{
    background: {COLORS['danger']};
    color: white;
}}
"""
