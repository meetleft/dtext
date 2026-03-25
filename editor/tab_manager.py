import os
import json
from pathlib import Path
from PyQt6.QtWidgets import (
    QTabWidget, QFileDialog, QMessageBox, QMenu,
    QToolButton, QTabBar,
)
from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QAction

from editor.code_editor import CodeEditor
from editor.syntax_manager import SyntaxManager

SESSION_DIR = Path.home() / ".TextEditMac"
SESSION_FILE = SESSION_DIR / "session.json"


class _CloseButton(QToolButton):
    """Small visible close button for tab bar."""

    def __init__(self, tab_bar: QTabBar, parent=None):
        super().__init__(parent)
        self._tab_bar = tab_bar
        self.setText("✕")
        self.setObjectName("tabCloseBtn")
        self.setFixedSize(QSize(20, 20))
        self.setAutoRaise(True)
        self.clicked.connect(self._on_click)

    def _on_click(self):
        for i in range(self._tab_bar.count()):
            left = self._tab_bar.tabButton(i, QTabBar.ButtonPosition.LeftSide)
            right = self._tab_bar.tabButton(i, QTabBar.ButtonPosition.RightSide)
            if left is self or right is self:
                tw = self._tab_bar.parent()
                if isinstance(tw, TabManager):
                    tw.close_tab(i)
                return


class TabManager(QTabWidget):
    """Multi-tab manager that holds CodeEditor instances."""

    editor_status_changed = pyqtSignal(object)

    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.syntax_manager = SyntaxManager()

        self.setTabsClosable(False)
        self.setMovable(True)
        self.setDocumentMode(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._tab_context_menu)

        self._populate_language_menu()

    # ---- Close button ----

    def _install_close_button(self, index: int):
        bar = self.tabBar()
        btn = _CloseButton(bar)
        bar.setTabButton(index, QTabBar.ButtonPosition.RightSide, btn)

    def tabInserted(self, index: int):
        super().tabInserted(index)
        self._install_close_button(index)

    # ---- Tab operations ----

    def add_new_tab(self, title: str = "未命名") -> CodeEditor:
        editor = self._create_editor()
        index = self.addTab(editor, title)
        self.setCurrentIndex(index)
        return editor

    def open_file(self, path: str) -> CodeEditor | None:
        for i in range(self.count()):
            ed = self.widget(i)
            if isinstance(ed, CodeEditor) and ed.file_path == path:
                self.setCurrentIndex(i)
                return ed

        editor = self._create_editor()
        if not editor.load_file(path):
            QMessageBox.warning(self, "错误", f"无法打开文件：\n{path}")
            editor.deleteLater()
            return None

        self.syntax_manager.apply_lexer(editor, path)
        name = os.path.basename(path)
        index = self.addTab(editor, name)
        self.setCurrentIndex(index)
        return editor

    def save_current(self) -> bool:
        editor = self.current_editor()
        if not editor:
            return False
        if editor.file_path:
            ok = editor.save_file()
            if ok:
                self._update_tab_title(self.currentIndex())
            return ok
        return self.save_current_as()

    def save_current_as(self) -> bool:
        editor = self.current_editor()
        if not editor:
            return False
        path, _ = QFileDialog.getSaveFileName(self, "另存为")
        if not path:
            return False
        ok = editor.save_file(path)
        if ok:
            self.syntax_manager.apply_lexer(editor, path)
            self.setTabText(self.currentIndex(), os.path.basename(path))
            self.editor_status_changed.emit(editor)
        return ok

    def close_tab(self, index: int) -> bool:
        editor = self.widget(index)
        if not isinstance(editor, CodeEditor):
            return True
        if editor.is_modified:
            name = self.tabText(index).rstrip("*").strip()
            ans = QMessageBox.question(
                self, "未保存的更改",
                f"'{name}' 有未保存的更改。\n是否在关闭前保存？",
                QMessageBox.StandardButton.Save |
                QMessageBox.StandardButton.Discard |
                QMessageBox.StandardButton.Cancel,
            )
            if ans == QMessageBox.StandardButton.Save:
                if not self.save_current():
                    return False
            elif ans == QMessageBox.StandardButton.Cancel:
                return False
        self.removeTab(index)
        editor.deleteLater()
        return True

    def close_all_tabs(self) -> bool:
        while self.count() > 0:
            if not self.close_tab(0):
                return False
        return True

    def current_editor(self) -> CodeEditor | None:
        w = self.currentWidget()
        return w if isinstance(w, CodeEditor) else None

    def set_word_wrap(self, enabled: bool):
        for i in range(self.count()):
            w = self.widget(i)
            if isinstance(w, CodeEditor):
                w.set_word_wrap(enabled)

    def set_show_whitespace(self, enabled: bool):
        for i in range(self.count()):
            w = self.widget(i)
            if isinstance(w, CodeEditor):
                w.set_show_whitespace(enabled)

    def apply_settings_to_all(self):
        for i in range(self.count()):
            w = self.widget(i)
            if isinstance(w, CodeEditor):
                w.apply_settings()
                lexer = w.lexer()
                if lexer is not None:
                    self.syntax_manager.apply_lexer_by_name(w, w.language_name)

    def get_all_tab_info(self) -> list[dict]:
        result = []
        for i in range(self.count()):
            w = self.widget(i)
            if isinstance(w, CodeEditor):
                result.append({
                    "index": i,
                    "title": self.tabText(i).rstrip("*").strip(),
                    "path": w.file_path,
                    "editor": w,
                })
        return result

    # ---- Internal ----

    def _create_editor(self) -> CodeEditor:
        editor = CodeEditor(self)
        editor.textChanged.connect(lambda: self._on_editor_modified(editor))
        editor.cursor_changed.connect(lambda: self.editor_status_changed.emit(editor))
        return editor

    def _on_editor_modified(self, editor: CodeEditor):
        idx = self.indexOf(editor)
        if idx < 0:
            return
        title = self.tabText(idx)
        if editor.is_modified and not title.endswith(" *"):
            self.setTabText(idx, title + " *")

    def _update_tab_title(self, index: int):
        editor = self.widget(index)
        if isinstance(editor, CodeEditor) and editor.file_path:
            self.setTabText(index, os.path.basename(editor.file_path))

    def _tab_context_menu(self, pos):
        index = self.tabBar().tabAt(pos)
        if index < 0:
            return
        menu = QMenu(self)

        close_action = QAction("关闭", self)
        close_action.triggered.connect(lambda: self.close_tab(index))
        menu.addAction(close_action)

        close_others = QAction("关闭其他", self)
        close_others.triggered.connect(lambda: self._close_others(index))
        menu.addAction(close_others)

        close_all = QAction("关闭全部", self)
        close_all.triggered.connect(self.close_all_tabs)
        menu.addAction(close_all)

        menu.exec(self.mapToGlobal(pos))

    def _close_others(self, keep_index: int):
        i = self.count() - 1
        while i >= 0:
            if i != keep_index:
                if not self.close_tab(i):
                    break
                if i < keep_index:
                    keep_index -= 1
            i -= 1

    def _populate_language_menu(self):
        langs = self.syntax_manager.available_languages()
        self.main_window.populate_language_menu(langs, self._change_language)

    def _change_language(self, language: str):
        editor = self.current_editor()
        if editor:
            self.syntax_manager.apply_lexer_by_name(editor, language)
            self.editor_status_changed.emit(editor)

    # ---- Session persistence ----

    def save_session(self):
        tabs = []
        for i in range(self.count()):
            w = self.widget(i)
            if not isinstance(w, CodeEditor):
                continue
            line, col = w.getCursorPosition()
            tabs.append({
                "file_path": w.file_path,
                "title": self.tabText(i).rstrip("*").strip(),
                "content": w.text(),
                "language": w.language_name or "Plain Text",
                "encoding": w.file_encoding or "UTF-8",
                "cursor_line": line,
                "cursor_col": col,
            })
        data = {"active_index": self.currentIndex(), "tabs": tabs}
        try:
            SESSION_DIR.mkdir(parents=True, exist_ok=True)
            SESSION_FILE.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        except OSError:
            pass

    def restore_session(self) -> bool:
        if not SESSION_FILE.exists():
            return False
        try:
            data = json.loads(SESSION_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return False

        tabs = data.get("tabs", [])
        if not tabs:
            return False

        for info in tabs:
            editor = self._create_editor()
            fp = info.get("file_path")
            content = info.get("content", "")
            title = info.get("title", "未命名")
            lang = info.get("language", "Plain Text")
            enc = info.get("encoding", "UTF-8")
            cur_line = info.get("cursor_line", 0)
            cur_col = info.get("cursor_col", 0)

            if fp and os.path.isfile(fp):
                editor.load_file(fp)
                self.syntax_manager.apply_lexer(editor, fp)
                title = os.path.basename(fp)
            else:
                editor.setText(content)
                editor.file_path = fp
                editor.file_encoding = enc
                editor.setModified(False)
                editor._modified_since_save = False
                if lang != "Plain Text":
                    self.syntax_manager.apply_lexer_by_name(editor, lang)

            editor.language_name = lang
            editor.file_encoding = enc
            self.addTab(editor, title)
            editor.setCursorPosition(cur_line, cur_col)

        active = data.get("active_index", 0)
        if 0 <= active < self.count():
            self.setCurrentIndex(active)

        return True
