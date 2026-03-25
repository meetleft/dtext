from PyQt6.QtWidgets import (
    QMainWindow, QStatusBar, QLabel, QFileDialog,
    QMessageBox, QPushButton, QMenu,
)
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import Qt

from editor.tab_manager import TabManager
from editor.find_replace import FindReplaceDialog
from editor.json_formatter import JsonFormatter
from editor.diff_viewer import DiffDialog
from editor.settings_manager import SettingsManager, SettingsDialog, ENCODING_LIST


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TextEditMac")
        self.resize(1200, 800)

        self.find_replace_dialog = None
        self.language_menu = None

        self._create_actions()
        self._create_menus()
        self._create_statusbar()

        self.tab_manager = TabManager(self)
        self.setCentralWidget(self.tab_manager)

        self.tab_manager.currentChanged.connect(self._on_tab_changed)
        self.tab_manager.editor_status_changed.connect(self._update_status)

        self.setAcceptDrops(True)

        self.tab_manager.add_new_tab()

        saved_theme = SettingsManager.get("theme") or "light"
        self._set_theme(saved_theme)

    # ---- Actions ----

    def _create_actions(self):
        self.new_action = QAction("新建", self)
        self.new_action.setShortcut(QKeySequence.StandardKey.New)
        self.new_action.triggered.connect(self._new_tab)

        self.open_action = QAction("打开...", self)
        self.open_action.setShortcut(QKeySequence.StandardKey.Open)
        self.open_action.triggered.connect(self._open_file)

        self.save_action = QAction("保存", self)
        self.save_action.setShortcut(QKeySequence.StandardKey.Save)
        self.save_action.triggered.connect(self._save_file)

        self.save_as_action = QAction("另存为...", self)
        self.save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        self.save_as_action.triggered.connect(self._save_file_as)

        self.close_tab_action = QAction("关闭标签", self)
        self.close_tab_action.setShortcut(QKeySequence("Ctrl+W"))
        self.close_tab_action.triggered.connect(
            lambda: self.tab_manager.close_tab(self.tab_manager.currentIndex())
        )

        self.undo_action = QAction("撤销", self)
        self.undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        self.undo_action.triggered.connect(self._undo)

        self.redo_action = QAction("重做", self)
        self.redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        self.redo_action.triggered.connect(self._redo)

        self.cut_action = QAction("剪切", self)
        self.cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        self.cut_action.triggered.connect(self._cut)

        self.copy_action = QAction("复制", self)
        self.copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        self.copy_action.triggered.connect(self._copy)

        self.paste_action = QAction("粘贴", self)
        self.paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        self.paste_action.triggered.connect(self._paste)

        self.select_all_action = QAction("全选", self)
        self.select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)
        self.select_all_action.triggered.connect(self._select_all)

        self.find_action = QAction("查找 / 替换...", self)
        self.find_action.setShortcut(QKeySequence.StandardKey.Find)
        self.find_action.triggered.connect(self._show_find_replace)

        self.word_wrap_action = QAction("自动换行", self)
        self.word_wrap_action.setCheckable(True)
        self.word_wrap_action.setChecked(SettingsManager.get("word_wrap"))
        self.word_wrap_action.triggered.connect(self._toggle_word_wrap)

        self.show_whitespace_action = QAction("显示特殊字符", self)
        self.show_whitespace_action.setCheckable(True)
        self.show_whitespace_action.setChecked(SettingsManager.get("show_whitespace"))
        self.show_whitespace_action.triggered.connect(self._toggle_whitespace)

        self.json_format_action = QAction("JSON 格式化", self)
        self.json_format_action.setShortcut(QKeySequence("Ctrl+Shift+J"))
        self.json_format_action.triggered.connect(self._format_json)

        self.json_compress_action = QAction("JSON 压缩", self)
        self.json_compress_action.triggered.connect(self._compress_json)

        self.json_validate_action = QAction("JSON 校验", self)
        self.json_validate_action.triggered.connect(self._validate_json)

        self.diff_action = QAction("文本对比...", self)
        self.diff_action.setShortcut(QKeySequence("Ctrl+D"))
        self.diff_action.triggered.connect(self._show_diff)

        self.theme_light_action = QAction("亮色主题", self)
        self.theme_light_action.triggered.connect(lambda: self._set_theme("light"))

        self.theme_dark_action = QAction("暗色主题", self)
        self.theme_dark_action.triggered.connect(lambda: self._set_theme("dark"))

        self.theme_system_action = QAction("跟随系统", self)
        self.theme_system_action.triggered.connect(lambda: self._set_theme("system"))

        self.settings_action = QAction("首选项...", self)
        self.settings_action.setShortcut(QKeySequence("Ctrl+,"))
        self.settings_action.triggered.connect(self._show_settings)

    # ---- Menus ----

    def _create_menus(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("文件")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addSeparator()
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.close_tab_action)

        edit_menu = menubar.addMenu("编辑")
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.select_all_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.find_action)

        view_menu = menubar.addMenu("视图")
        view_menu.addAction(self.word_wrap_action)
        view_menu.addAction(self.show_whitespace_action)
        view_menu.addSeparator()
        self.language_menu = view_menu.addMenu("语言")
        theme_menu = view_menu.addMenu("主题")
        theme_menu.addAction(self.theme_light_action)
        theme_menu.addAction(self.theme_dark_action)
        theme_menu.addAction(self.theme_system_action)

        tools_menu = menubar.addMenu("工具")
        json_menu = tools_menu.addMenu("JSON")
        json_menu.addAction(self.json_format_action)
        json_menu.addAction(self.json_compress_action)
        json_menu.addAction(self.json_validate_action)
        tools_menu.addSeparator()
        tools_menu.addAction(self.diff_action)

        settings_menu = menubar.addMenu("设置")
        settings_menu.addAction(self.settings_action)

    # ---- Status bar ----

    def _create_statusbar(self):
        self.statusbar = QStatusBar()
        self.statusbar.setObjectName("mainStatusBar")
        self.setStatusBar(self.statusbar)

        self.filepath_label = QLabel("未命名")
        self.filepath_label.setObjectName("filepathLabel")
        self.statusbar.addPermanentWidget(self.filepath_label, 1)

        self.language_btn = QPushButton("Plain Text")
        self.language_btn.setObjectName("statusBtn")
        self.language_btn.setFlat(True)
        self.language_btn.clicked.connect(self._show_language_popup)
        self.statusbar.addPermanentWidget(self.language_btn)

        self.encoding_btn = QPushButton("UTF-8")
        self.encoding_btn.setObjectName("statusBtn")
        self.encoding_btn.setFlat(True)
        self.encoding_btn.clicked.connect(self._show_encoding_popup)
        self.statusbar.addPermanentWidget(self.encoding_btn)

        self.line_col_label = QLabel("行 1, 列 1")
        self.statusbar.addPermanentWidget(self.line_col_label)

    # ---- Language / encoding helpers ----

    def populate_language_menu(self, languages: list[str], callback):
        self.language_menu.clear()
        for lang in sorted(languages):
            action = QAction(lang, self)
            action.triggered.connect(lambda checked, l=lang: callback(l))
            self.language_menu.addAction(action)

    def _show_language_popup(self):
        menu = QMenu(self)
        for lang in self.tab_manager.syntax_manager.available_languages():
            action = menu.addAction(lang)
            action.triggered.connect(lambda checked, l=lang: self._set_language(l))
        menu.exec(self.language_btn.mapToGlobal(self.language_btn.rect().topLeft()))

    def _show_encoding_popup(self):
        menu = QMenu(self)
        for enc in ENCODING_LIST:
            action = menu.addAction(enc)
            action.triggered.connect(lambda checked, e=enc: self._set_encoding(e))
        menu.exec(self.encoding_btn.mapToGlobal(self.encoding_btn.rect().topLeft()))

    def _set_language(self, language: str):
        editor = self.tab_manager.current_editor()
        if editor:
            self.tab_manager.syntax_manager.apply_lexer_by_name(editor, language)
            self.tab_manager.editor_status_changed.emit(editor)

    def _set_encoding(self, encoding: str):
        editor = self.tab_manager.current_editor()
        if editor:
            editor.set_encoding(encoding)
            self._update_status(editor)

    # ---- Slots ----

    def _on_tab_changed(self, index: int):
        editor = self.tab_manager.current_editor()
        if editor:
            self._update_status(editor)

    def _update_status(self, editor=None):
        if editor is None:
            editor = self.tab_manager.current_editor()
        if editor is None:
            return

        line, col = editor.getCursorPosition()
        self.line_col_label.setText(f"行 {line + 1}, 列 {col + 1}")
        self.encoding_btn.setText(editor.file_encoding or "UTF-8")
        self.language_btn.setText(editor.language_name or "Plain Text")
        self.filepath_label.setText(editor.file_path or "未命名")

    def _open_file(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "打开文件", "",
            "所有文件 (*);;文本文件 (*.txt);;Python (*.py);;JSON (*.json)"
        )
        for path in paths:
            self.tab_manager.open_file(path)

    def _save_file(self):
        self.tab_manager.save_current()

    def _save_file_as(self):
        self.tab_manager.save_current_as()

    def _undo(self):
        e = self.tab_manager.current_editor()
        if e:
            e.undo()

    def _redo(self):
        e = self.tab_manager.current_editor()
        if e:
            e.redo()

    def _cut(self):
        e = self.tab_manager.current_editor()
        if e:
            e.cut()

    def _copy(self):
        e = self.tab_manager.current_editor()
        if e:
            e.copy()

    def _paste(self):
        e = self.tab_manager.current_editor()
        if e:
            e.paste()

    def _select_all(self):
        e = self.tab_manager.current_editor()
        if e:
            e.selectAll()

    def _show_find_replace(self):
        editor = self.tab_manager.current_editor()
        if not editor:
            return
        if self.find_replace_dialog is None:
            self.find_replace_dialog = FindReplaceDialog(self)
        self.find_replace_dialog.set_editor(editor)
        self.find_replace_dialog.show()
        self.find_replace_dialog.raise_()
        self.find_replace_dialog.activateWindow()

    def _toggle_word_wrap(self, checked: bool):
        self.tab_manager.set_word_wrap(checked)
        SettingsManager.set("word_wrap", checked)

    def _toggle_whitespace(self, checked: bool):
        self.tab_manager.set_show_whitespace(checked)
        SettingsManager.set("show_whitespace", checked)

    def _ensure_json_lexer(self, language: str):
        editor = self.tab_manager.current_editor()
        if editor:
            self.tab_manager.syntax_manager.apply_lexer_by_name(editor, language)
            self.tab_manager.editor_status_changed.emit(editor)

    def _format_json(self):
        editor = self.tab_manager.current_editor()
        if editor:
            JsonFormatter.format_json(
                editor, parent=self, on_language_set=self._ensure_json_lexer
            )

    def _compress_json(self):
        editor = self.tab_manager.current_editor()
        if editor:
            JsonFormatter.compress_json(
                editor, parent=self, on_language_set=self._ensure_json_lexer
            )

    def _validate_json(self):
        editor = self.tab_manager.current_editor()
        if editor:
            JsonFormatter.validate_json(editor, parent=self)

    def _show_diff(self):
        tabs_info = self.tab_manager.get_all_tab_info()
        dlg = DiffDialog(tabs_info, parent=self)
        dlg.exec()

    def _set_theme(self, theme_name: str):
        from editor.theme_manager import ThemeManager
        ThemeManager.apply_theme(self, theme_name)
        SettingsManager.set("theme", ThemeManager.current_theme_name())

    def _show_settings(self):
        dlg = SettingsDialog(self)
        dlg.exec()

    def apply_settings(self):
        self.tab_manager.apply_settings_to_all()

    def _new_tab(self):
        self.tab_manager.add_new_tab()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path:
                self.tab_manager.open_file(path)

    def closeEvent(self, event):
        if self.tab_manager.close_all_tabs():
            event.accept()
        else:
            event.ignore()
