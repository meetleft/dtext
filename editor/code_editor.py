from PyQt6.Qsci import QsciScintilla
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import pyqtSignal

from editor.settings_manager import SettingsManager


class CodeEditor(QsciScintilla):
    """Single editor pane wrapping QScintilla with common IDE features."""

    cursor_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.file_path: str | None = None
        self.file_encoding: str | None = "UTF-8"
        self.language_name: str = "Plain Text"
        self._modified_since_save = False

        self._setup_font()
        self._setup_margins()
        self._setup_folding()
        self._setup_caret()
        self._setup_editing()
        self._apply_line_spacing()

        self.textChanged.connect(self._on_text_changed)
        self.cursorPositionChanged.connect(lambda l, c: self.cursor_changed.emit())

    def _current_font(self) -> QFont:
        family = SettingsManager.get("font_family")
        size = SettingsManager.get("font_size")
        font = QFont(family, size)
        font.setFixedPitch(True)
        return font

    def _setup_font(self):
        font = self._current_font()
        self.setFont(font)
        self.setMarginsFont(font)

    def _setup_margins(self):
        self.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.setMarginWidth(0, "00000")
        self.setMarginLineNumbers(0, True)

        self.setMarginType(1, QsciScintilla.MarginType.SymbolMargin)
        self.setMarginWidth(1, 16)
        self.setMarginSensitivity(1, True)
        self.marginClicked.connect(self._on_margin_clicked)

    def _setup_folding(self):
        self.setFolding(QsciScintilla.FoldStyle.BoxedTreeFoldStyle, 1)

    def _setup_caret(self):
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#E8E8FF"))
        self.setCaretForegroundColor(QColor("#000000"))

    def _setup_editing(self):
        self.setAutoIndent(True)
        self.setIndentationsUseTabs(False)
        self.setTabWidth(SettingsManager.get("tab_width"))
        self.setIndentationGuides(True)
        self.setBraceMatching(QsciScintilla.BraceMatch.SloppyBraceMatch)
        self.setUtf8(True)
        self.setEolMode(QsciScintilla.EolMode.EolUnix)
        self.setWrapMode(QsciScintilla.WrapMode.WrapNone)

    def _apply_line_spacing(self):
        px = SettingsManager.get("line_spacing")
        half = px // 2
        self.setExtraAscent(half)
        self.setExtraDescent(px - half)

    # ---- Public API ----

    def apply_settings(self):
        font = self._current_font()
        self.setFont(font)
        self.setMarginsFont(font)
        self.setTabWidth(SettingsManager.get("tab_width"))
        self._apply_line_spacing()

        lexer = self.lexer()
        if lexer is not None:
            lexer.setDefaultFont(font)
            lexer.setFont(font)

    def load_file(self, path: str) -> bool:
        import chardet
        try:
            raw = open(path, "rb").read()
        except OSError:
            return False

        detected = chardet.detect(raw)
        encoding = detected.get("encoding") or "utf-8"
        try:
            text = raw.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            text = raw.decode("utf-8", errors="replace")
            encoding = "UTF-8"

        self.setText(text)
        self.file_path = path
        self.file_encoding = encoding.upper()
        self._modified_since_save = False
        self.setModified(False)
        return True

    def save_file(self, path: str | None = None) -> bool:
        target = path or self.file_path
        if not target:
            return False
        enc = self.file_encoding or "UTF-8"
        try:
            with open(target, "w", encoding=enc, errors="replace") as f:
                f.write(self.text())
        except OSError:
            return False
        self.file_path = target
        self._modified_since_save = False
        self.setModified(False)
        return True

    @property
    def is_modified(self) -> bool:
        return self.isModified() or self._modified_since_save

    def set_word_wrap(self, enabled: bool):
        mode = QsciScintilla.WrapMode.WrapWord if enabled else QsciScintilla.WrapMode.WrapNone
        self.setWrapMode(mode)

    def set_show_whitespace(self, enabled: bool):
        vis = (QsciScintilla.WhitespaceVisibility.WsVisible if enabled
               else QsciScintilla.WhitespaceVisibility.WsInvisible)
        self.setWhitespaceVisibility(vis)

    def set_encoding(self, encoding: str):
        self.file_encoding = encoding

    # ---- Private slots ----

    def _on_text_changed(self):
        self._modified_since_save = True

    def _on_margin_clicked(self, margin: int, line: int, modifiers):
        if margin == 1:
            self.foldLine(line)
