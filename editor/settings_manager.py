from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QSpinBox, QFontComboBox, QPushButton, QFormLayout,
)
from PyQt6.QtGui import QFont

DEFAULTS = {
    "font_family": "Menlo",
    "font_size": 13,
    "line_spacing": 0,
    "tab_width": 4,
    "word_wrap": False,
    "show_whitespace": False,
    "theme": "light",
}

ENCODING_LIST = [
    "UTF-8", "GBK", "GB2312", "GB18030", "BIG5",
    "Shift-JIS", "EUC-JP", "EUC-KR",
    "ISO-8859-1", "Windows-1252", "ASCII",
]


class SettingsManager:
    """Persists user preferences via QSettings."""

    _qs = QSettings("TextEditMac", "TextEditMac")

    @classmethod
    def get(cls, key: str):
        default = DEFAULTS.get(key)
        val = cls._qs.value(key, default)
        if isinstance(default, bool):
            if isinstance(val, str):
                return val.lower() == "true"
            return bool(val)
        if isinstance(default, int):
            return int(val)
        return val

    @classmethod
    def set(cls, key: str, value):
        cls._qs.setValue(key, value)

    @classmethod
    def all_settings(cls) -> dict:
        return {k: cls.get(k) for k in DEFAULTS}


class SettingsDialog(QDialog):
    """Preferences dialog for font, spacing, tab width."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("首选项")
        self.setMinimumWidth(420)
        self._build_ui()
        self._load_current()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        font_group = QGroupBox("字体")
        font_form = QFormLayout(font_group)

        self.font_combo = QFontComboBox()
        self.font_combo.setFontFilters(QFontComboBox.FontFilter.MonospacedFonts)
        font_form.addRow("字体：", self.font_combo)

        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 72)
        font_form.addRow("字号：", self.font_size_spin)

        self.line_spacing_spin = QSpinBox()
        self.line_spacing_spin.setRange(0, 20)
        self.line_spacing_spin.setSuffix(" px")
        font_form.addRow("行间距：", self.line_spacing_spin)

        layout.addWidget(font_group)

        editor_group = QGroupBox("编辑器")
        editor_form = QFormLayout(editor_group)

        self.tab_width_spin = QSpinBox()
        self.tab_width_spin.setRange(1, 8)
        editor_form.addRow("Tab 宽度：", self.tab_width_spin)

        layout.addWidget(editor_group)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.apply_btn = QPushButton("应用")
        self.ok_btn = QPushButton("确定")
        self.cancel_btn = QPushButton("取消")
        btn_row.addWidget(self.apply_btn)
        btn_row.addWidget(self.ok_btn)
        btn_row.addWidget(self.cancel_btn)
        layout.addLayout(btn_row)

        self.apply_btn.clicked.connect(self._apply)
        self.ok_btn.clicked.connect(self._ok)
        self.cancel_btn.clicked.connect(self.reject)

    def _load_current(self):
        self.font_combo.setCurrentFont(QFont(SettingsManager.get("font_family")))
        self.font_size_spin.setValue(SettingsManager.get("font_size"))
        self.line_spacing_spin.setValue(SettingsManager.get("line_spacing"))
        self.tab_width_spin.setValue(SettingsManager.get("tab_width"))

    def _save(self):
        SettingsManager.set("font_family", self.font_combo.currentFont().family())
        SettingsManager.set("font_size", self.font_size_spin.value())
        SettingsManager.set("line_spacing", self.line_spacing_spin.value())
        SettingsManager.set("tab_width", self.tab_width_spin.value())

    def _apply(self):
        self._save()
        p = self.parent()
        if p and hasattr(p, "apply_settings"):
            p.apply_settings()

    def _ok(self):
        self._apply()
        self.accept()
