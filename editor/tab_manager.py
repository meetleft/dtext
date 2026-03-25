import os
from PyQt6.QtWidgets import QTabWidget, QFileDialog, QMessageBox, QMenu
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QAction

from editor.code_editor import CodeEditor
from editor.syntax_manager import SyntaxManager


class TabManager(QTabWidget):
    """Multi-tab manager that holds CodeEditor instances."""

    editor_status_changed = pyqtSignal(object)

    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.syntax_manager = SyntaxManager()

        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)

        self.tabCloseRequested.connect(self.close_tab)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._tab_context_menu)

        self._populate_language_menu()

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
