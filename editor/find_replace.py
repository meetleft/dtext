from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QCheckBox, QLabel, QMessageBox,
)
from PyQt6.QtCore import Qt
from PyQt6.Qsci import QsciScintilla


class FindReplaceDialog(QDialog):
    """Non-modal find/replace dialog."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("查找 / 替换")
        self.setMinimumWidth(440)
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowType.Tool
        )
        self._editor: QsciScintilla | None = None
        self._build_ui()

    def set_editor(self, editor: QsciScintilla):
        self._editor = editor
        selected = editor.selectedText()
        if selected and "\n" not in selected:
            self.find_input.setText(selected)

    def _build_ui(self):
        layout = QVBoxLayout(self)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("查找："))
        self.find_input = QLineEdit()
        row1.addWidget(self.find_input)
        layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("替换："))
        self.replace_input = QLineEdit()
        row2.addWidget(self.replace_input)
        layout.addLayout(row2)

        opts = QHBoxLayout()
        self.case_cb = QCheckBox("区分大小写")
        self.word_cb = QCheckBox("整词匹配")
        self.regex_cb = QCheckBox("正则表达式")
        opts.addWidget(self.case_cb)
        opts.addWidget(self.word_cb)
        opts.addWidget(self.regex_cb)
        layout.addLayout(opts)

        btns = QHBoxLayout()
        self.find_next_btn = QPushButton("查找下一个")
        self.find_prev_btn = QPushButton("查找上一个")
        self.replace_btn = QPushButton("替换")
        self.replace_all_btn = QPushButton("全部替换")

        btns.addWidget(self.find_next_btn)
        btns.addWidget(self.find_prev_btn)
        btns.addWidget(self.replace_btn)
        btns.addWidget(self.replace_all_btn)
        layout.addLayout(btns)

        self.find_next_btn.clicked.connect(self._find_next)
        self.find_prev_btn.clicked.connect(self._find_previous)
        self.replace_btn.clicked.connect(self._replace)
        self.replace_all_btn.clicked.connect(self._replace_all)

        self.find_input.returnPressed.connect(self._find_next)

    def _find_next(self):
        self._find(forward=True)

    def _find_previous(self):
        self._find(forward=False)

    def _find(self, forward: bool):
        if not self._editor:
            return
        text = self.find_input.text()
        if not text:
            return

        found = self._editor.findFirst(
            text,
            self.regex_cb.isChecked(),
            self.case_cb.isChecked(),
            self.word_cb.isChecked(),
            True,
            forward,
        )
        if not found:
            QMessageBox.information(self, "查找", "未找到匹配内容。")

    def _replace(self):
        if not self._editor:
            return
        if self._editor.hasSelectedText():
            self._editor.replace(self.replace_input.text())
        self._find_next()

    def _replace_all(self):
        if not self._editor:
            return
        text = self.find_input.text()
        replacement = self.replace_input.text()
        if not text:
            return

        self._editor.setCursorPosition(0, 0)
        count = 0
        while self._editor.findFirst(
            text,
            self.regex_cb.isChecked(),
            self.case_cb.isChecked(),
            self.word_cb.isChecked(),
            False,
            True,
        ):
            self._editor.replace(replacement)
            count += 1

        QMessageBox.information(self, "全部替换", f"已替换 {count} 处。")
