from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QFrame, QSplitter, QPushButton, QApplication, QButtonGroup
)
from PyQt6.QtCore import Qt

from core.languages import LANGUAGES
from core.paradigms_data import PARADIGM_TOPICS
from core.code_runner import CodeRunner
from ui.code_editor import PolyglotCodeEditor

class ParadigmMatrixTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.view_mode = "code"
        self._init_ui()
        self.load_topic(0)

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 12, 14, 12)
        main_layout.setSpacing(8)

        # Interactive Toolbar
        top_bar = QFrame()
        top_bar.setProperty("class", "DlcCard")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(10, 6, 10, 6)
        top_layout.setSpacing(10)

        top_layout.addWidget(QLabel("Topic:"))
        self.cb_topic = QComboBox()
        for topic in PARADIGM_TOPICS:
            self.cb_topic.addItem(topic.title, topic.id)
        self.cb_topic.currentIndexChanged.connect(self.on_topic_changed)
        top_layout.addWidget(self.cb_topic, 2)

        top_layout.addWidget(QLabel("Left:"))
        self.cb_lang_a = QComboBox()
        for lang_id, lang in LANGUAGES.items():
            self.cb_lang_a.addItem(lang.name, lang_id)
        self.cb_lang_a.setCurrentIndex(0)
        self.cb_lang_a.currentIndexChanged.connect(self.update_snippets)
        top_layout.addWidget(self.cb_lang_a, 1)

        top_layout.addWidget(QLabel("Right:"))
        self.cb_lang_b = QComboBox()
        for lang_id, lang in LANGUAGES.items():
            self.cb_lang_b.addItem(lang.name, lang_id)
        self.cb_lang_b.setCurrentIndex(1)
        self.cb_lang_b.currentIndexChanged.connect(self.update_snippets)
        top_layout.addWidget(self.cb_lang_b, 1)

        # View Mode Toggle: Source / Bytecode / AST
        top_layout.addWidget(QLabel("Mode:"))
        self.btn_mode_code = QPushButton("Source")
        self.btn_mode_code.setCheckable(True)
        self.btn_mode_code.setChecked(True)
        self.btn_mode_code.clicked.connect(lambda: self.set_view_mode("code"))
        top_layout.addWidget(self.btn_mode_code)

        self.btn_mode_disasm = QPushButton("Bytecode")
        self.btn_mode_disasm.setCheckable(True)
        self.btn_mode_disasm.clicked.connect(lambda: self.set_view_mode("disasm"))
        top_layout.addWidget(self.btn_mode_disasm)

        self.btn_mode_ast = QPushButton("AST")
        self.btn_mode_ast.setCheckable(True)
        self.btn_mode_ast.clicked.connect(lambda: self.set_view_mode("ast"))
        top_layout.addWidget(self.btn_mode_ast)

        self.mode_group = QButtonGroup(self)
        self.mode_group.addButton(self.btn_mode_code)
        self.mode_group.addButton(self.btn_mode_disasm)
        self.mode_group.addButton(self.btn_mode_ast)

        main_layout.addWidget(top_bar)

        # Side-by-side Comparative Code Splitter
        code_splitter = QSplitter(Qt.Orientation.Horizontal)
        code_splitter.setHandleWidth(6)

        # Panel A
        panel_a = QFrame()
        panel_a.setStyleSheet("background-color: #0d0e14; border: 1px solid #1e2029; border-radius: 6px;")
        layout_a = QVBoxLayout(panel_a)
        layout_a.setContentsMargins(8, 6, 8, 8)
        layout_a.setSpacing(6)

        header_a = QHBoxLayout()
        self.lbl_title_a = QLabel("Target A")
        self.lbl_title_a.setStyleSheet("font-weight: 600; font-size: 12px; color: #38bdf8;")
        header_a.addWidget(self.lbl_title_a)
        header_a.addStretch()

        self.btn_copy_a = QPushButton("Copy")
        self.btn_copy_a.clicked.connect(lambda: self.copy_code(self.editor_a))
        header_a.addWidget(self.btn_copy_a)
        layout_a.addLayout(header_a)

        self.editor_a = PolyglotCodeEditor(read_only=True)
        layout_a.addWidget(self.editor_a, 1)

        code_splitter.addWidget(panel_a)

        # Panel B
        panel_b = QFrame()
        panel_b.setStyleSheet("background-color: #0d0e14; border: 1px solid #1e2029; border-radius: 6px;")
        layout_b = QVBoxLayout(panel_b)
        layout_b.setContentsMargins(8, 6, 8, 8)
        layout_b.setSpacing(6)

        header_b = QHBoxLayout()
        self.lbl_title_b = QLabel("Target B")
        self.lbl_title_b.setStyleSheet("font-weight: 600; font-size: 12px; color: #a855f7;")
        header_b.addWidget(self.lbl_title_b)
        header_b.addStretch()

        self.btn_copy_b = QPushButton("Copy")
        self.btn_copy_b.clicked.connect(lambda: self.copy_code(self.editor_b))
        header_b.addWidget(self.btn_copy_b)
        layout_b.addLayout(header_b)

        self.editor_b = PolyglotCodeEditor(read_only=True)
        layout_b.addWidget(self.editor_b, 1)

        code_splitter.addWidget(panel_b)

        main_layout.addWidget(code_splitter, 1)

    def set_view_mode(self, mode: str):
        self.view_mode = mode
        self.update_snippets()

    def on_topic_changed(self, index):
        self.load_topic(index)

    def load_topic(self, index):
        self.update_snippets()

    def update_snippets(self):
        topic_idx = self.cb_topic.currentIndex()
        if topic_idx < 0 or topic_idx >= len(PARADIGM_TOPICS):
            return
        topic = PARADIGM_TOPICS[topic_idx]

        lang_a_id = self.cb_lang_a.currentData()
        lang_b_id = self.cb_lang_b.currentData()

        # Update Target A
        snip_a = topic.snippets.get(lang_a_id)
        if snip_a:
            self.lbl_title_a.setText(f"{LANGUAGES[lang_a_id].name} ({snip_a.complexity})")
            content_a = self._format_content(lang_a_id, snip_a.code)
            self.editor_a.set_language("python" if self.view_mode != "code" else LANGUAGES[lang_a_id].pygments_lexer)
            self.editor_a.setPlainText(content_a)
        else:
            self.editor_a.setPlainText("// Not available")

        # Update Target B
        snip_b = topic.snippets.get(lang_b_id)
        if snip_b:
            self.lbl_title_b.setText(f"{LANGUAGES[lang_b_id].name} ({snip_b.complexity})")
            content_b = self._format_content(lang_b_id, snip_b.code)
            self.editor_b.set_language("python" if self.view_mode != "code" else LANGUAGES[lang_b_id].pygments_lexer)
            self.editor_b.setPlainText(content_b)
        else:
            self.editor_b.setPlainText("// Not available")

    def _format_content(self, lang_id: str, raw_code: str) -> str:
        if self.view_mode == "disasm":
            return CodeRunner.disassemble(lang_id, raw_code)
        elif self.view_mode == "ast":
            return CodeRunner.inspect_ast(lang_id, raw_code)
        return raw_code

    def copy_code(self, editor):
        clipboard = QApplication.clipboard()
        clipboard.setText(editor.toPlainText())
