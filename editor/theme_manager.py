from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication
from PyQt6.Qsci import QsciScintilla


LIGHT_THEME = {
    "name": "light",
    "paper": "#FFFFFF",
    "text": "#1E1E1E",
    "caret_line": "#F0F4FF",
    "caret_fg": "#1E1E1E",
    "margin_bg": "#F0F0F0",
    "margin_fg": "#8C8C8C",
    "fold_margin_bg": "#F5F5F5",
    "selection_bg": "#CADEFC",
    "selection_fg": "#1E1E1E",
    "matched_brace_bg": "#CADEFC",
    "matched_brace_fg": "#C82829",
}

DARK_THEME = {
    "name": "dark",
    "paper": "#1E1E1E",
    "text": "#D4D4D4",
    "caret_line": "#2A2D3A",
    "caret_fg": "#AEAFAD",
    "margin_bg": "#252526",
    "margin_fg": "#858585",
    "fold_margin_bg": "#252526",
    "selection_bg": "#264F78",
    "selection_fg": "#FFFFFF",
    "matched_brace_bg": "#264F78",
    "matched_brace_fg": "#FFD700",
}


_LIGHT_STYLESHEET = """
/* ===== Global ===== */
QMainWindow, QDialog {
    background-color: #FAFAFA;
    color: #333333;
    font-family: -apple-system, "Helvetica Neue", sans-serif;
}

/* ===== Menu bar ===== */
QMenuBar {
    background-color: #F5F5F5;
    color: #333333;
    border-bottom: 1px solid #E0E0E0;
    padding: 1px 0;
}
QMenuBar::item {
    padding: 4px 10px;
    border-radius: 4px;
}
QMenuBar::item:selected {
    background-color: #E3EEFA;
    color: #1A73E8;
}
QMenu {
    background-color: #FFFFFF;
    color: #333333;
    border: 1px solid #E0E0E0;
    border-radius: 6px;
    padding: 4px 0;
}
QMenu::item {
    padding: 5px 28px 5px 20px;
}
QMenu::item:selected {
    background-color: #E3EEFA;
    color: #1A73E8;
}
QMenu::separator {
    height: 1px;
    background: #ECECEC;
    margin: 4px 10px;
}

/* ===== Toolbar ===== */
QToolBar#mainToolBar {
    background-color: #F5F5F5;
    border-bottom: 1px solid #E0E0E0;
    spacing: 2px;
    padding: 3px 6px;
}
QToolBar#mainToolBar QToolButton {
    background-color: transparent;
    color: #555555;
    border: none;
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 12px;
}
QToolBar#mainToolBar QToolButton:hover {
    background-color: #E3EEFA;
    color: #1A73E8;
}
QToolBar#mainToolBar QToolButton:pressed {
    background-color: #CADEFC;
}
QToolBar#mainToolBar QToolButton:checked {
    background-color: #D6E8FC;
    color: #1A73E8;
    border: 1px solid #B0CFF5;
}
QToolBar#mainToolBar::separator {
    width: 1px;
    background: #E0E0E0;
    margin: 4px 4px;
}

/* ===== Tab bar ===== */
QTabWidget::pane {
    border: none;
}
QTabBar {
    background-color: #EAECED;
    qproperty-drawBase: 0;
}
QTabBar::tab {
    background-color: #DCDFE2;
    color: #6B7280;
    padding: 7px 20px 7px 14px;
    margin: 3px 1px 0 1px;
    border: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    min-width: 80px;
    font-size: 12px;
}
QTabBar::tab:hover {
    background-color: #E8EAEE;
    color: #374151;
}
QTabBar::tab:selected {
    background-color: #FFFFFF;
    color: #1F2937;
    border-bottom: none;
}
QTabBar::tab:!selected {
    margin-top: 4px;
}
QToolButton#tabCloseBtn {
    background: transparent;
    color: #999999;
    border: none;
    border-radius: 4px;
    font-size: 12px;
    padding: 0;
    margin: 0 2px;
}
QToolButton#tabCloseBtn:hover {
    background-color: rgba(0, 0, 0, 0.1);
    color: #333333;
}

/* ===== Status bar ===== */
QStatusBar#mainStatusBar {
    background-color: #E8ECF0;
    color: #555555;
    border-top: 1px solid #D8DCE0;
    font-size: 12px;
    padding: 0;
    min-height: 24px;
}
QStatusBar#mainStatusBar QLabel {
    color: #555555;
    padding: 0 6px;
    font-size: 12px;
}
QStatusBar#mainStatusBar QPushButton#statusBtn {
    background-color: transparent;
    color: #555555;
    border: none;
    border-radius: 3px;
    padding: 2px 8px;
    font-size: 12px;
}
QStatusBar#mainStatusBar QPushButton#statusBtn:hover {
    background-color: #D6E0EA;
    color: #1A73E8;
}

/* ===== Inputs ===== */
QLineEdit, QSpinBox {
    background-color: #FFFFFF;
    color: #333333;
    border: 1px solid #D0D0D0;
    border-radius: 4px;
    padding: 4px 6px;
}
QLineEdit:focus, QSpinBox:focus {
    border: 1px solid #1A73E8;
}
QComboBox {
    background-color: #FFFFFF;
    color: #333333;
    border: 1px solid #D0D0D0;
    border-radius: 4px;
    padding: 4px 8px 4px 6px;
}
QComboBox:focus {
    border: 1px solid #1A73E8;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    color: #333333;
    border: 1px solid #D0D0D0;
    selection-background-color: #E3EEFA;
    selection-color: #1A73E8;
}

/* ===== Buttons ===== */
QPushButton {
    background-color: #1A73E8;
    color: #FFFFFF;
    border: none;
    border-radius: 5px;
    padding: 5px 16px;
    font-size: 13px;
}
QPushButton:hover {
    background-color: #1567D3;
}
QPushButton:pressed {
    background-color: #0F52A5;
}
QPushButton:flat {
    background-color: transparent;
    color: #555555;
}
QPushButton:flat:hover {
    background-color: #E3EEFA;
    color: #1A73E8;
}

/* ===== Checkbox / GroupBox ===== */
QCheckBox {
    color: #333333;
    spacing: 6px;
}
QGroupBox {
    color: #333333;
    border: 1px solid #D8DCE0;
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 14px;
    font-weight: 600;
}
QGroupBox::title {
    subcontrol-origin: margin;
    padding: 0 8px;
    color: #555555;
}

/* ===== Font combo ===== */
QFontComboBox {
    background-color: #FFFFFF;
    color: #333333;
    border: 1px solid #D0D0D0;
    border-radius: 4px;
}

/* ===== Splitter ===== */
QSplitter::handle {
    background-color: #E0E0E0;
}

/* ===== Scrollbar ===== */
QScrollBar:vertical {
    background: #F5F5F5;
    width: 10px;
    border: none;
}
QScrollBar::handle:vertical {
    background: #C8C8C8;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #A8A8A8;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
QScrollBar:horizontal {
    background: #F5F5F5;
    height: 10px;
    border: none;
}
QScrollBar::handle:horizontal {
    background: #C8C8C8;
    border-radius: 4px;
    min-width: 30px;
}
QScrollBar::handle:horizontal:hover {
    background: #A8A8A8;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
}
"""

_DARK_STYLESHEET = """
/* ===== Global ===== */
QMainWindow, QDialog {
    background-color: #1E1E1E;
    color: #D4D4D4;
    font-family: -apple-system, "Helvetica Neue", sans-serif;
}

/* ===== Menu bar ===== */
QMenuBar {
    background-color: #252526;
    color: #CCCCCC;
    border-bottom: 1px solid #3C3C3C;
    padding: 1px 0;
}
QMenuBar::item {
    padding: 4px 10px;
    border-radius: 4px;
}
QMenuBar::item:selected {
    background-color: #094771;
    color: #FFFFFF;
}
QMenu {
    background-color: #252526;
    color: #CCCCCC;
    border: 1px solid #454545;
    border-radius: 6px;
    padding: 4px 0;
}
QMenu::item {
    padding: 5px 28px 5px 20px;
}
QMenu::item:selected {
    background-color: #094771;
    color: #FFFFFF;
}
QMenu::separator {
    height: 1px;
    background: #3C3C3C;
    margin: 4px 10px;
}

/* ===== Toolbar ===== */
QToolBar#mainToolBar {
    background-color: #2D2D2D;
    border-bottom: 1px solid #3C3C3C;
    spacing: 2px;
    padding: 3px 6px;
}
QToolBar#mainToolBar QToolButton {
    background-color: transparent;
    color: #CCCCCC;
    border: none;
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 12px;
}
QToolBar#mainToolBar QToolButton:hover {
    background-color: #3C3C3C;
    color: #FFFFFF;
}
QToolBar#mainToolBar QToolButton:pressed {
    background-color: #094771;
}
QToolBar#mainToolBar QToolButton:checked {
    background-color: #094771;
    color: #FFFFFF;
    border: 1px solid #007ACC;
}
QToolBar#mainToolBar::separator {
    width: 1px;
    background: #3C3C3C;
    margin: 4px 4px;
}

/* ===== Tab bar ===== */
QTabWidget::pane {
    border: none;
}
QTabBar {
    background-color: #1E1E1E;
    qproperty-drawBase: 0;
}
QTabBar::tab {
    background-color: #2D2D2D;
    color: #8C8C8C;
    padding: 7px 20px 7px 14px;
    margin: 3px 1px 0 1px;
    border: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    min-width: 80px;
    font-size: 12px;
}
QTabBar::tab:hover {
    background-color: #353535;
    color: #CCCCCC;
}
QTabBar::tab:selected {
    background-color: #1E1E1E;
    color: #FFFFFF;
    border-bottom: none;
}
QTabBar::tab:!selected {
    margin-top: 4px;
}
QToolButton#tabCloseBtn {
    background: transparent;
    color: #666666;
    border: none;
    border-radius: 4px;
    font-size: 12px;
    padding: 0;
    margin: 0 2px;
}
QToolButton#tabCloseBtn:hover {
    background-color: rgba(255, 255, 255, 0.15);
    color: #FFFFFF;
}

/* ===== Status bar ===== */
QStatusBar#mainStatusBar {
    background-color: #007ACC;
    color: #FFFFFF;
    border-top: none;
    font-size: 12px;
    padding: 0;
    min-height: 24px;
}
QStatusBar#mainStatusBar QLabel {
    color: #FFFFFF;
    padding: 0 6px;
    font-size: 12px;
}
QStatusBar#mainStatusBar QPushButton#statusBtn {
    background-color: transparent;
    color: #FFFFFF;
    border: none;
    border-radius: 3px;
    padding: 2px 8px;
    font-size: 12px;
}
QStatusBar#mainStatusBar QPushButton#statusBtn:hover {
    background-color: rgba(255, 255, 255, 0.18);
}

/* ===== Inputs ===== */
QLineEdit, QSpinBox {
    background-color: #3C3C3C;
    color: #D4D4D4;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 4px 6px;
}
QLineEdit:focus, QSpinBox:focus {
    border: 1px solid #007ACC;
}
QComboBox {
    background-color: #3C3C3C;
    color: #D4D4D4;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 4px 8px 4px 6px;
}
QComboBox:focus {
    border: 1px solid #007ACC;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #AAAAAA;
    margin-right: 6px;
}
QComboBox QAbstractItemView {
    background-color: #3C3C3C;
    color: #D4D4D4;
    border: 1px solid #555555;
    selection-background-color: #094771;
    selection-color: #FFFFFF;
}

/* ===== Buttons ===== */
QPushButton {
    background-color: #0E639C;
    color: #FFFFFF;
    border: none;
    border-radius: 5px;
    padding: 5px 16px;
    font-size: 13px;
}
QPushButton:hover {
    background-color: #1177BB;
}
QPushButton:pressed {
    background-color: #094771;
}
QPushButton:flat {
    background-color: transparent;
    color: #CCCCCC;
}
QPushButton:flat:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

/* ===== Checkbox / GroupBox ===== */
QCheckBox {
    color: #D4D4D4;
    spacing: 6px;
}
QGroupBox {
    color: #D4D4D4;
    border: 1px solid #555555;
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 14px;
    font-weight: 600;
}
QGroupBox::title {
    subcontrol-origin: margin;
    padding: 0 8px;
    color: #BBBBBB;
}

/* ===== Font combo ===== */
QFontComboBox {
    background-color: #3C3C3C;
    color: #D4D4D4;
    border: 1px solid #555555;
    border-radius: 4px;
}

/* ===== Splitter ===== */
QSplitter::handle {
    background-color: #3C3C3C;
}

/* ===== Scrollbar ===== */
QScrollBar:vertical {
    background: #1E1E1E;
    width: 10px;
    border: none;
}
QScrollBar::handle:vertical {
    background: #424242;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #555555;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
QScrollBar:horizontal {
    background: #1E1E1E;
    height: 10px;
    border: none;
}
QScrollBar::handle:horizontal {
    background: #424242;
    border-radius: 4px;
    min-width: 30px;
}
QScrollBar::handle:horizontal:hover {
    background: #555555;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
}

/* ===== Label ===== */
QLabel {
    color: #D4D4D4;
}
"""


class ThemeManager:
    _current = "light"

    @classmethod
    def apply_theme(cls, main_window, theme_name: str):
        if theme_name == "system":
            palette = QApplication.instance().palette()
            lightness = palette.color(QPalette.ColorRole.Window).lightness()
            theme_name = "dark" if lightness < 128 else "light"

        cls._current = theme_name
        theme = DARK_THEME if theme_name == "dark" else LIGHT_THEME

        if theme_name == "dark":
            main_window.setStyleSheet(_DARK_STYLESHEET)
        else:
            main_window.setStyleSheet(_LIGHT_STYLESHEET)

        tab_manager = main_window.tab_manager
        for i in range(tab_manager.count()):
            editor = tab_manager.widget(i)
            if isinstance(editor, QsciScintilla):
                cls._apply_to_editor(editor, theme)

    @classmethod
    def current_theme_name(cls) -> str:
        return cls._current

    @classmethod
    def current_theme(cls) -> dict:
        return DARK_THEME if cls._current == "dark" else LIGHT_THEME

    @classmethod
    def _apply_to_editor(cls, editor: QsciScintilla, theme: dict):
        editor.setCaretLineBackgroundColor(QColor(theme["caret_line"]))
        editor.setCaretForegroundColor(QColor(theme["caret_fg"]))

        editor.setMarginsBackgroundColor(QColor(theme["margin_bg"]))
        editor.setMarginsForegroundColor(QColor(theme["margin_fg"]))
        editor.setFoldMarginColors(
            QColor(theme["fold_margin_bg"]),
            QColor(theme["fold_margin_bg"]),
        )

        editor.setSelectionBackgroundColor(QColor(theme["selection_bg"]))
        editor.setSelectionForegroundColor(QColor(theme["selection_fg"]))

        editor.setMatchedBraceBackgroundColor(QColor(theme["matched_brace_bg"]))
        editor.setMatchedBraceForegroundColor(QColor(theme["matched_brace_fg"]))

        editor.setPaper(QColor(theme["paper"]))
        editor.setColor(QColor(theme["text"]))

        lexer = editor.lexer()
        if lexer is not None:
            lexer.setDefaultPaper(QColor(theme["paper"]))
            lexer.setDefaultColor(QColor(theme["text"]))
