import json
from PyQt6.QtWidgets import QMessageBox


class JsonFormatter:
    """JSON formatting, compressing, and validation."""

    @staticmethod
    def format_json(editor, indent: int = 4, sort_keys: bool = False,
                    parent=None, on_language_set=None):
        text = editor.text()
        try:
            obj = json.loads(text)
        except json.JSONDecodeError as e:
            QMessageBox.warning(
                parent, "JSON 错误",
                f"无效的 JSON，无法格式化。\n\n{e}",
            )
            return
        formatted = json.dumps(obj, indent=indent, sort_keys=sort_keys, ensure_ascii=False)
        editor.selectAll()
        editor.replaceSelectedText(formatted)
        if on_language_set and editor.language_name != "JSON":
            on_language_set("JSON")

    @staticmethod
    def compress_json(editor, parent=None, on_language_set=None):
        text = editor.text()
        try:
            obj = json.loads(text)
        except json.JSONDecodeError as e:
            QMessageBox.warning(
                parent, "JSON 错误",
                f"无效的 JSON，无法压缩。\n\n{e}",
            )
            return
        compressed = json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
        editor.selectAll()
        editor.replaceSelectedText(compressed)
        if on_language_set and editor.language_name != "JSON":
            on_language_set("JSON")

    @staticmethod
    def validate_json(editor, parent=None):
        text = editor.text()
        try:
            json.loads(text)
        except json.JSONDecodeError as e:
            line = e.lineno or 0
            col = e.colno or 0
            QMessageBox.warning(
                parent, "JSON 校验",
                f"无效的 JSON，第 {line} 行，第 {col} 列：\n\n{e.msg}",
            )
            if line > 0:
                editor.setCursorPosition(line - 1, max(col - 1, 0))
            return
        QMessageBox.information(parent, "JSON 校验", "JSON 格式正确。")
