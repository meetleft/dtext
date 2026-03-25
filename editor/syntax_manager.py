import os
from PyQt6.QtGui import QFont
from PyQt6.Qsci import (
    QsciLexerPython, QsciLexerJavaScript, QsciLexerHTML, QsciLexerCSS,
    QsciLexerJava, QsciLexerCPP, QsciLexerSQL, QsciLexerJSON,
    QsciLexerXML, QsciLexerMarkdown, QsciLexerBash, QsciLexerYAML,
    QsciLexerRuby, QsciLexerPerl, QsciLexerLua,
)

from editor.settings_manager import SettingsManager


EXTENSION_MAP: dict[str, str] = {
    ".py": "Python", ".pyw": "Python",
    ".js": "JavaScript", ".mjs": "JavaScript",
    ".ts": "JavaScript", ".tsx": "JavaScript", ".jsx": "JavaScript",
    ".html": "HTML", ".htm": "HTML",
    ".css": "CSS", ".scss": "CSS", ".less": "CSS",
    ".java": "Java",
    ".c": "C/C++", ".cpp": "C/C++", ".cc": "C/C++",
    ".cxx": "C/C++", ".h": "C/C++", ".hpp": "C/C++",
    ".sql": "SQL",
    ".json": "JSON",
    ".xml": "XML", ".xsl": "XML", ".xslt": "XML", ".svg": "XML",
    ".md": "Markdown", ".markdown": "Markdown",
    ".sh": "Bash", ".bash": "Bash", ".zsh": "Bash",
    ".yml": "YAML", ".yaml": "YAML",
    ".rb": "Ruby",
    ".pl": "Perl", ".pm": "Perl",
    ".lua": "Lua",
}

LEXER_CLASSES: dict[str, type] = {
    "Python": QsciLexerPython,
    "JavaScript": QsciLexerJavaScript,
    "HTML": QsciLexerHTML,
    "CSS": QsciLexerCSS,
    "Java": QsciLexerJava,
    "C/C++": QsciLexerCPP,
    "SQL": QsciLexerSQL,
    "JSON": QsciLexerJSON,
    "XML": QsciLexerXML,
    "Markdown": QsciLexerMarkdown,
    "Bash": QsciLexerBash,
    "YAML": QsciLexerYAML,
    "Ruby": QsciLexerRuby,
    "Perl": QsciLexerPerl,
    "Lua": QsciLexerLua,
}


def _editor_font() -> QFont:
    family = SettingsManager.get("font_family")
    size = SettingsManager.get("font_size")
    font = QFont(family, size)
    font.setFixedPitch(True)
    return font


class SyntaxManager:
    """Maps file extensions to QScintilla lexers and applies them."""

    def available_languages(self) -> list[str]:
        return ["Plain Text"] + sorted(LEXER_CLASSES.keys())

    def detect_language(self, filepath: str) -> str:
        ext = os.path.splitext(filepath)[1].lower()
        return EXTENSION_MAP.get(ext, "Plain Text")

    def apply_lexer(self, editor, filepath: str):
        lang = self.detect_language(filepath)
        self.apply_lexer_by_name(editor, lang)

    def apply_lexer_by_name(self, editor, language: str):
        editor.language_name = language
        cls = LEXER_CLASSES.get(language)
        if cls is None:
            editor.setLexer(None)
            return

        lexer = cls(editor)
        font = _editor_font()
        lexer.setDefaultFont(font)
        lexer.setFont(font)
        editor.setLexer(lexer)
