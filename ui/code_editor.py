import sys
from PyQt6.QtWidgets import QWidget, QPlainTextEdit, QTextEdit, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QApplication
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QColor, QPainter, QTextFormat, QFont, QSyntaxHighlighter, QTextCharFormat

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatter import Formatter

class QSyntaxHighlighterPygments(QSyntaxHighlighter):
    def __init__(self, parent, lexer_name="python"):
        super().__init__(parent)
        self.set_lexer(lexer_name)
        self._init_formats()

    def set_lexer(self, lexer_name):
        try:
            self.lexer = get_lexer_by_name(lexer_name)
        except Exception:
            self.lexer = get_lexer_by_name("text")
        self.rehighlight()

    def _init_formats(self):
        self.formats = {}
        # Cyber / One Dark style color mapping
        theme_map = {
            "Keyword": "#c678dd",
            "Keyword.Type": "#e5c07b",
            "Name.Function": "#61afef",
            "Name.Class": "#e5c07b",
            "Name.Builtin": "#56b6c2",
            "String": "#98c379",
            "Number": "#d19a66",
            "Comment": "#5c6370",
            "Operator": "#56b6c2",
            "Punctuation": "#abb2bf",
            "Generic": "#e06c75"
        }
        for token_key, color_code in theme_map.items():
            fmt = QTextCharFormat()
            fmt.setForeground(QColor(color_code))
            if "Keyword" in token_key:
                fmt.setFontWeight(QFont.Weight.Bold)
            if "Comment" in token_key:
                fmt.setFontItalic(True)
            self.formats[token_key] = fmt

    def highlightBlock(self, text):
        if not text:
            return
        from pygments import lex
        from pygments.token import Token
        
        try:
            tokens = list(lex(text, self.lexer))
            index = 0
            for ttype, val in tokens:
                length = len(val)
                # match token type hierarchy
                matched_fmt = None
                curr_type = ttype
                while curr_type.parent:
                    str_type = str(curr_type).replace("Token.", "")
                    if str_type in self.formats:
                        matched_fmt = self.formats[str_type]
                        break
                    curr_type = curr_type.parent

                if matched_fmt:
                    self.setFormat(index, length, matched_fmt)
                else:
                    default_fmt = QTextCharFormat()
                    default_fmt.setForeground(QColor("#abb2bf"))
                    self.setFormat(index, length, default_fmt)
                index += length
        except Exception:
            pass


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)


class PolyglotCodeEditor(QPlainTextEdit):
    def __init__(self, parent=None, language="python", read_only=False):
        super().__init__(parent)
        self.language = language
        self.setReadOnly(read_only)
        
        # Configure Font
        font = QFont("Consolas", 11)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)
        
        # Styling
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #0b1120;
                color: #e2e8f0;
                border: 1px solid #1e293b;
                border-radius: 6px;
                padding: 4px;
                selection-background-color: #3b82f6;
                selection-color: #ffffff;
            }
        """)

        # Line Number Area
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.update_line_number_area_width(0)

        # Pygments Highlighter
        self.highlighter = QSyntaxHighlighterPygments(self.document(), language)
        self.highlight_current_line()

    def set_language(self, language: str):
        self.language = language
        self.highlighter.set_lexer(language)

    def line_number_area_width(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num //= 10
            digits += 1
        space = 20 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor("#1e293b")
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#080c14"))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor("#475569"))
                painter.drawText(0, top, self.line_number_area.width() - 8, self.fontMetrics().height(),
                                 Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1
