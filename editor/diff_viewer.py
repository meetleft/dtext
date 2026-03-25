import difflib
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QSplitter,
    QComboBox, QPushButton, QLabel, QFileDialog,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.Qsci import QsciScintilla

from editor.settings_manager import SettingsManager

ADDED_COLOR = QColor("#CCFFCC")
REMOVED_COLOR = QColor("#FFCCCC")
CHANGED_COLOR = QColor("#FFFFAA")

MARKER_ADDED = 8
MARKER_REMOVED = 9
MARKER_CHANGED = 10


class DiffEditor(QsciScintilla):
    """Read-only Scintilla pane used inside the diff viewer."""

    def __init__(self, parent=None):
        super().__init__(parent)
        family = SettingsManager.get("font_family")
        size = SettingsManager.get("font_size")
        font = QFont(family, size)
        font.setFixedPitch(True)
        self.setFont(font)
        self.setMarginsFont(font)
        self.setReadOnly(True)
        self.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.setMarginWidth(0, "00000")
        self.setMarginLineNumbers(0, True)
        self.setWrapMode(QsciScintilla.WrapMode.WrapNone)

        self.markerDefine(QsciScintilla.MarkerSymbol.Background, MARKER_ADDED)
        self.setMarkerBackgroundColor(ADDED_COLOR, MARKER_ADDED)
        self.markerDefine(QsciScintilla.MarkerSymbol.Background, MARKER_REMOVED)
        self.setMarkerBackgroundColor(REMOVED_COLOR, MARKER_REMOVED)
        self.markerDefine(QsciScintilla.MarkerSymbol.Background, MARKER_CHANGED)
        self.setMarkerBackgroundColor(CHANGED_COLOR, MARKER_CHANGED)


class DiffDialog(QDialog):
    """Side-by-side file comparison dialog."""

    def __init__(self, tabs_info: list[dict], parent=None):
        super().__init__(parent)
        self.setWindowTitle("文本对比")
        self.resize(1100, 700)
        self.tabs_info = tabs_info
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        selector = QHBoxLayout()

        selector.addWidget(QLabel("左侧："))
        self.left_combo = QComboBox()
        self.left_combo.setMinimumWidth(200)
        selector.addWidget(self.left_combo, 1)

        self.left_browse = QPushButton("浏览...")
        self.left_browse.clicked.connect(lambda: self._browse("left"))
        selector.addWidget(self.left_browse)

        selector.addWidget(QLabel("右侧："))
        self.right_combo = QComboBox()
        self.right_combo.setMinimumWidth(200)
        selector.addWidget(self.right_combo, 1)

        self.right_browse = QPushButton("浏览...")
        self.right_browse.clicked.connect(lambda: self._browse("right"))
        selector.addWidget(self.right_browse)

        self.compare_btn = QPushButton("开始对比")
        self.compare_btn.clicked.connect(self._run_diff)
        selector.addWidget(self.compare_btn)

        layout.addLayout(selector)

        self._populate_combos()

        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.left_editor = DiffEditor()
        self.right_editor = DiffEditor()
        splitter.addWidget(self.left_editor)
        splitter.addWidget(self.right_editor)
        splitter.setSizes([550, 550])
        layout.addWidget(splitter, 1)

        self.left_editor.verticalScrollBar().valueChanged.connect(
            self.right_editor.verticalScrollBar().setValue
        )
        self.right_editor.verticalScrollBar().valueChanged.connect(
            self.left_editor.verticalScrollBar().setValue
        )

    def _populate_combos(self):
        self.left_combo.clear()
        self.right_combo.clear()

        self.left_combo.addItem("（请选择文件）", None)
        self.right_combo.addItem("（请选择文件）", None)

        for info in self.tabs_info:
            label = info["path"] or info["title"]
            self.left_combo.addItem(label, info)
            self.right_combo.addItem(label, info)

        if self.left_combo.count() > 1:
            self.left_combo.setCurrentIndex(1)
        if self.right_combo.count() > 2:
            self.right_combo.setCurrentIndex(2)

    def _browse(self, side: str):
        path, _ = QFileDialog.getOpenFileName(self, "选择文件")
        if not path:
            return
        combo = self.left_combo if side == "left" else self.right_combo
        combo.addItem(path, {"path": path, "editor": None, "title": path})
        combo.setCurrentIndex(combo.count() - 1)

    def _get_text(self, combo: QComboBox) -> str | None:
        data = combo.currentData()
        if data is None:
            return None
        if data.get("editor") is not None:
            return data["editor"].text()
        path = data.get("path")
        if path:
            try:
                with open(path, "r", errors="replace") as f:
                    return f.read()
            except OSError:
                return None
        return None

    def _run_diff(self):
        left_text = self._get_text(self.left_combo)
        right_text = self._get_text(self.right_combo)

        if left_text is None or right_text is None:
            return

        left_lines = left_text.splitlines(keepends=True)
        right_lines = right_text.splitlines(keepends=True)

        self.left_editor.setReadOnly(False)
        self.right_editor.setReadOnly(False)
        self.left_editor.setText(left_text)
        self.right_editor.setText(right_text)
        self.left_editor.setReadOnly(True)
        self.right_editor.setReadOnly(True)

        self.left_editor.markerDeleteAll(-1)
        self.right_editor.markerDeleteAll(-1)

        matcher = difflib.SequenceMatcher(None, left_lines, right_lines)
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                continue
            elif tag == "replace":
                for line_no in range(i1, i2):
                    self.left_editor.markerAdd(line_no, MARKER_CHANGED)
                for line_no in range(j1, j2):
                    self.right_editor.markerAdd(line_no, MARKER_CHANGED)
            elif tag == "delete":
                for line_no in range(i1, i2):
                    self.left_editor.markerAdd(line_no, MARKER_REMOVED)
            elif tag == "insert":
                for line_no in range(j1, j2):
                    self.right_editor.markerAdd(line_no, MARKER_ADDED)
