from config.colors import Colors

def get_modern_stylesheet() -> str:
    return f"""
    QMainWindow {{ background-color: {Colors.BG_DARK}; }}
    QWidget {{ background-color: {Colors.BG_DARK}; color: {Colors.TEXT_PRIMARY}; font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif; font-size: 13px; }}
    QPushButton {{ background-color: {Colors.BG_LIGHT}; color: {Colors.TEXT_PRIMARY}; border: 1px solid {Colors.BORDER_LIGHT}; border-radius: 10px; padding: 8px 16px; font-weight: 600; min-height: 36px; font-size: 13px; }}
    QPushButton:hover {{ background-color: {Colors.BG_LIGHT}; border-color: {Colors.PRIMARY}; color: {Colors.PRIMARY}; }}
    QPushButton:pressed {{ background-color: {Colors.PRIMARY_DARK}; }}
    QPushButton:disabled {{ background-color: {Colors.BG_LIGHT}; color: {Colors.TEXT_MUTED}; }}
    QLineEdit {{ border:none; background:transparent; }}
    QLineEdit:focus {{ border-color: {Colors.PRIMARY}; background-color: {Colors.BG_LIGHT}; }}
    QComboBox {{ background-color: {Colors.BG_MEDIUM}; color: {Colors.TEXT_PRIMARY}; border: 1px solid {Colors.BORDER_LIGHT}; border-radius: 8px; padding: 8px 12px; min-height: 36px; }}
    QComboBox:hover, QComboBox:focus {{ border-color: {Colors.PRIMARY}; }}
    QComboBox::drop-down {{ border: none; width: 30px; }}
    QComboBox QAbstractItemView {{ background-color: {Colors.BG_MEDIUM}; color: {Colors.TEXT_PRIMARY}; border: 1px solid {Colors.BORDER_LIGHT}; border-radius: 8px; selection-background-color: {Colors.PRIMARY}; padding: 5px; }}
    QListWidget {{ background-color: transparent; color: {Colors.TEXT_PRIMARY}; border: none; border-radius: 8px; padding: 5px; outline: none; }}
    QListWidget::item {{ padding: 8px 12px; border-radius: 8px; margin: 2px 4px; border: 1px solid transparent; }}
    QListWidget::item:hover {{ background: rgba(0,212,255,0.08); }}
    QListWidget::item:selected {{ background: rgba(0,212,255,0.18); border-radius: 8px; color: white; }}
    QFrame#cardFrame {{ background-color: {Colors.BG_CARD}; border: 1px solid {Colors.BORDER_LIGHT}; border-radius: 12px; }}
    QFrame#sidebarFrame {{ background-color: {Colors.BG_SIDEBAR}; border: 1px solid {Colors.BORDER_LIGHT}; border-radius: 12px; }}
    QFrame#separator {{ background-color: {Colors.BORDER_LIGHT}; max-height: 1px; }}
    QLabel#statusLabel {{ color: {Colors.ACCENT_GREEN}; background-color: {Colors.BG_MEDIUM}; padding: 8px 15px; border-radius: 8px; font-family: 'Consolas', monospace; font-size: 12px; }}
    QLabel#loadingLabel {{ color: {Colors.PRIMARY}; background-color: rgba(10, 14, 26, 0.95); font-size: 28px; font-weight: 700; border: 2px solid {Colors.PRIMARY}; border-radius: 15px; padding: 30px 50px; }}
    QSplitter::handle {{ background-color: {Colors.BORDER_LIGHT}; border-radius: 4px; width: 6px; margin: 5px 0; }}
    QSplitter::handle:hover {{ background-color: {Colors.PRIMARY}; }}
    QScrollBar:vertical {{ background: {Colors.BG_DARK}; width: 8px; border-radius: 4px; }}
    QScrollBar::handle:vertical {{ background: {Colors.BORDER_LIGHT}; border-radius: 4px; min-height: 30px; }}
    QScrollBar::handle:vertical:hover {{ background: {Colors.PRIMARY}; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
    """