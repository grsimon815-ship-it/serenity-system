from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QFrame, QSplitter, QTextBrowser, QPushButton, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from core.languages import LANGUAGES
from core.paradigms_data import PARADIGM_TOPICS
from ui.code_editor import PolyglotCodeEditor

class ParadigmMatrixTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self.load_topic(0)

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Top Bar: Topic Selection & Language Selectors
        top_bar = QFrame()
        top_bar.setObjectName("TopBar")
        top_bar.setStyleSheet("""
            QFrame#TopBar {
                background-color: #0f172a;
                border: 1px solid #1e293b;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(8, 8, 8, 8)

        lbl_topic = QLabel("Architectural Paradigm:")
        lbl_topic.setStyleSheet("font-weight: 700; color: #f8fafc;")
        top_layout.addWidget(lbl_topic)

        self.cb_topic = QComboBox()
        for topic in PARADIGM_TOPICS:
            self.cb_topic.addItem(topic.title, topic.id)
        self.cb_topic.currentIndexChanged.connect(self.on_topic_changed)
        top_layout.addWidget(self.cb_topic, 2)

        top_layout.addSpacing(20)

        # Compare Lang A & Lang B
        lbl_lang_a = QLabel("Left Target:")
        lbl_lang_a.setStyleSheet("font-weight: 600; color: #38bdf8;")
        top_layout.addWidget(lbl_lang_a)

        self.cb_lang_a = QComboBox()
        for lang_id, lang in LANGUAGES.items():
            self.cb_lang_a.addItem(f"{lang.name} ({lang.category})", lang_id)
        self.cb_lang_a.setCurrentIndex(0) # Rust
        self.cb_lang_a.currentIndexChanged.connect(self.update_snippets)
        top_layout.addWidget(self.cb_lang_a, 1)

        lbl_lang_b = QLabel("Right Target:")
        lbl_lang_b.setStyleSheet("font-weight: 600; color: #f59e0b;")
        top_layout.addWidget(lbl_lang_b)

        self.cb_lang_b = QComboBox()
        for lang_id, lang in LANGUAGES.items():
            self.cb_lang_b.addItem(f"{lang.name} ({lang.category})", lang_id)
        self.cb_lang_b.setCurrentIndex(1) # Go
        self.cb_lang_b.currentIndexChanged.connect(self.update_snippets)
        top_layout.addWidget(self.cb_lang_b, 1)

        main_layout.addWidget(top_bar)

        # Splitter: Theory Info Panel (Top) & Comparative Code (Bottom)
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.setHandleWidth(6)

        # Theory Card
        self.theory_card = QFrame()
        self.theory_card.setStyleSheet("""
            QFrame {
                background-color: #0d1322;
                border: 1px solid #1e293b;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        theory_layout = QVBoxLayout(self.theory_card)
        theory_layout.setContentsMargins(12, 10, 12, 10)

        self.lbl_theory_title = QLabel()
        self.lbl_theory_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #38bdf8;")
        theory_layout.addWidget(self.lbl_theory_title)

        self.txt_theory = QTextBrowser()
        self.txt_theory.setStyleSheet("""
            QTextBrowser {
                background-color: transparent;
                border: none;
                color: #cbd5e1;
                font-size: 12px;
                line-height: 1.5;
            }
        """)
        self.txt_theory.setMaximumHeight(140)
        theory_layout.addWidget(self.txt_theory)

        splitter.addWidget(self.theory_card)

        # Comparative Code Splitter (Horizontal)
        code_splitter = QSplitter(Qt.Orientation.Horizontal)
        code_splitter.setHandleWidth(6)

        # Panel A
        panel_a = QFrame()
        panel_a.setStyleSheet("background-color: #0b1120; border: 1px solid #1e293b; border-radius: 8px;")
        layout_a = QVBoxLayout(panel_a)
        layout_a.setContentsMargins(10, 8, 10, 10)

        header_a = QHBoxLayout()
        self.lbl_title_a = QLabel("Target A")
        self.lbl_title_a.setStyleSheet("font-weight: 700; font-size: 13px; color: #38bdf8;")
        header_a.addWidget(self.lbl_title_a)
        header_a.addStretch()

        self.btn_copy_a = QPushButton("Copy Snippet")
        self.btn_copy_a.clicked.connect(lambda: self.copy_code(self.editor_a))
        header_a.addWidget(self.btn_copy_a)
        layout_a.addLayout(header_a)

        self.editor_a = PolyglotCodeEditor(read_only=True)
        layout_a.addWidget(self.editor_a, 1)

        self.lbl_info_a = QLabel()
        self.lbl_info_a.setWordWrap(True)
        self.lbl_info_a.setStyleSheet("color: #94a3b8; font-size: 11px; padding: 4px; background: #080c14; border-radius: 4px;")
        layout_a.addWidget(self.lbl_info_a)

        code_splitter.addWidget(panel_a)

        # Panel B
        panel_b = QFrame()
        panel_b.setStyleSheet("background-color: #0b1120; border: 1px solid #1e293b; border-radius: 8px;")
        layout_b = QVBoxLayout(panel_b)
        layout_b.setContentsMargins(10, 8, 10, 10)

        header_b = QHBoxLayout()
        self.lbl_title_b = QLabel("Target B")
        self.lbl_title_b.setStyleSheet("font-weight: 700; font-size: 13px; color: #f59e0b;")
        header_b.addWidget(self.lbl_title_b)
        header_b.addStretch()

        self.btn_copy_b = QPushButton("Copy Snippet")
        self.btn_copy_b.clicked.connect(lambda: self.copy_code(self.editor_b))
        header_b.addWidget(self.btn_copy_b)
        layout_b.addLayout(header_b)

        self.editor_b = PolyglotCodeEditor(read_only=True)
        layout_b.addWidget(self.editor_b, 1)

        self.lbl_info_b = QLabel()
        self.lbl_info_b.setWordWrap(True)
        self.lbl_info_b.setStyleSheet("color: #94a3b8; font-size: 11px; padding: 4px; background: #080c14; border-radius: 4px;")
        layout_b.addWidget(self.lbl_info_b)

        code_splitter.addWidget(panel_b)

        splitter.addWidget(code_splitter)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

        main_layout.addWidget(splitter, 1)

    def on_topic_changed(self, index):
        self.load_topic(index)

    def load_topic(self, index):
        if index < 0 or index >= len(PARADIGM_TOPICS):
            return
        topic = PARADIGM_TOPICS[index]
        self.lbl_theory_title.setText(f"{topic.title} — {topic.subtitle}")
        
        theory_html = f"""
        <p style='color: #e2e8f0; margin-bottom: 6px;'>{topic.deep_theory.replace(chr(10), '<br>')}</p>
        <div style='margin-top: 6px;'>
            <span style='color: #10b981; font-weight: bold;'>Pros:</span> {'; '.join(topic.tradeoffs_pros)}<br>
            <span style='color: #ef4444; font-weight: bold;'>Tradeoffs:</span> {'; '.join(topic.tradeoffs_cons)}<br>
            <span style='color: #6366f1; font-weight: bold;'>Optimal Scope:</span> {topic.best_use_case}
        </div>
        """
        self.txt_theory.setHtml(theory_html)
        self.update_snippets()

    def update_snippets(self):
        topic_idx = self.cb_topic.currentIndex()
        if topic_idx < 0 or topic_idx >= len(PARADIGM_TOPICS):
            return
        topic = PARADIGM_TOPICS[topic_idx]

        lang_a_id = self.cb_lang_a.currentData()
        lang_b_id = self.cb_lang_b.currentData()

        # Update Lang A
        snip_a = topic.snippets.get(lang_a_id)
        if snip_a:
            self.lbl_title_a.setText(f"{LANGUAGES[lang_a_id].name} Implementation")
            self.editor_a.set_language(LANGUAGES[lang_a_id].pygments_lexer)
            self.editor_a.setPlainText(snip_a.code)
            self.lbl_info_a.setText(f"Mechanics: {snip_a.explanation} | Cost: {snip_a.complexity}")
        else:
            self.editor_a.setPlainText("// No snippet available for this language")
            self.lbl_info_a.setText("")

        # Update Lang B
        snip_b = topic.snippets.get(lang_b_id)
        if snip_b:
            self.lbl_title_b.setText(f"{LANGUAGES[lang_b_id].name} Implementation")
            self.editor_b.set_language(LANGUAGES[lang_b_id].pygments_lexer)
            self.editor_b.setPlainText(snip_b.code)
            self.lbl_info_b.setText(f"Mechanics: {snip_b.explanation} | Cost: {snip_b.complexity}")
        else:
            self.editor_b.setPlainText("// No snippet available for this language")
            self.lbl_info_b.setText("")

    def copy_code(self, editor):
        clipboard = QApplication.clipboard()
        clipboard.setText(editor.toPlainText())
