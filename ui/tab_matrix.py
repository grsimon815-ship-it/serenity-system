from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QFrame, QSplitter, QTextBrowser, QPushButton, QApplication
)
from PyQt6.QtCore import Qt

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
        main_layout.setContentsMargins(18, 16, 18, 16)
        main_layout.setSpacing(12)

        # Top Bar: Topic Selection & Language Targets
        top_bar = QFrame()
        top_bar.setProperty("class", "DlcCard")
        top_bar.setStyleSheet("""
            QFrame.DlcCard {
                background-color: #0e1119;
                border: 1px solid #181b26;
                border-radius: 9px;
                padding: 6px;
            }
        """)
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(10, 6, 10, 6)
        top_layout.setSpacing(10)

        lbl_topic = QLabel("Paradigm:")
        lbl_topic.setStyleSheet("font-weight: 700; color: #a855f7; font-size: 12px;")
        top_layout.addWidget(lbl_topic)

        self.cb_topic = QComboBox()
        for topic in PARADIGM_TOPICS:
            self.cb_topic.addItem(topic.title, topic.id)
        self.cb_topic.currentIndexChanged.connect(self.on_topic_changed)
        top_layout.addWidget(self.cb_topic, 2)

        top_layout.addSpacing(16)

        # Target A
        lbl_lang_a = QLabel("Left:")
        lbl_lang_a.setStyleSheet("font-weight: 600; color: #38bdf8; font-size: 11px;")
        top_layout.addWidget(lbl_lang_a)

        self.cb_lang_a = QComboBox()
        for lang_id, lang in LANGUAGES.items():
            self.cb_lang_a.addItem(f"{lang.name}", lang_id)
        self.cb_lang_a.setCurrentIndex(0) # Rust
        self.cb_lang_a.currentIndexChanged.connect(self.update_snippets)
        top_layout.addWidget(self.cb_lang_a, 1)

        # Target B
        lbl_lang_b = QLabel("Right:")
        lbl_lang_b.setStyleSheet("font-weight: 600; color: #c084fc; font-size: 11px;")
        top_layout.addWidget(lbl_lang_b)

        self.cb_lang_b = QComboBox()
        for lang_id, lang in LANGUAGES.items():
            self.cb_lang_b.addItem(f"{lang.name}", lang_id)
        self.cb_lang_b.setCurrentIndex(1) # Go
        self.cb_lang_b.currentIndexChanged.connect(self.update_snippets)
        top_layout.addWidget(self.cb_lang_b, 1)

        main_layout.addWidget(top_bar)

        # Splitter: Theory Card & Comparative Code
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.setHandleWidth(5)

        # Theory Card
        self.theory_card = QFrame()
        self.theory_card.setProperty("class", "DlcCard")
        self.theory_card.setStyleSheet("""
            QFrame.DlcCard {
                background-color: #0c0e15;
                border: 1px solid #181b26;
                border-radius: 9px;
            }
        """)
        theory_layout = QVBoxLayout(self.theory_card)
        theory_layout.setContentsMargins(14, 10, 14, 10)
        theory_layout.setSpacing(4)

        self.lbl_theory_title = QLabel()
        self.lbl_theory_title.setStyleSheet("font-size: 14px; font-weight: 800; color: #a855f7;")
        theory_layout.addWidget(self.lbl_theory_title)

        self.txt_theory = QTextBrowser()
        self.txt_theory.setStyleSheet("""
            QTextBrowser {
                background-color: transparent;
                border: none;
                color: #cbd5e1;
                font-size: 12px;
            }
        """)
        self.txt_theory.setMaximumHeight(115)
        theory_layout.addWidget(self.txt_theory)

        splitter.addWidget(self.theory_card)

        # Comparative Code Splitter (Horizontal)
        code_splitter = QSplitter(Qt.Orientation.Horizontal)
        code_splitter.setHandleWidth(6)

        # Panel A
        panel_a = QFrame()
        panel_a.setStyleSheet("background-color: #0c0e15; border: 1px solid #181b26; border-radius: 9px;")
        layout_a = QVBoxLayout(panel_a)
        layout_a.setContentsMargins(10, 8, 10, 8)
        layout_a.setSpacing(6)

        header_a = QHBoxLayout()
        self.lbl_title_a = QLabel("Target A")
        self.lbl_title_a.setStyleSheet("font-weight: 700; font-size: 12px; color: #38bdf8;")
        header_a.addWidget(self.lbl_title_a)
        header_a.addStretch()

        self.btn_copy_a = QPushButton("Copy")
        self.btn_copy_a.clicked.connect(lambda: self.copy_code(self.editor_a))
        header_a.addWidget(self.btn_copy_a)
        layout_a.addLayout(header_a)

        self.editor_a = PolyglotCodeEditor(read_only=True)
        layout_a.addWidget(self.editor_a, 1)

        self.lbl_info_a = QLabel()
        self.lbl_info_a.setWordWrap(True)
        self.lbl_info_a.setStyleSheet("color: #94a3b8; font-size: 11px; padding: 4px; background: #08090d; border-radius: 5px;")
        layout_a.addWidget(self.lbl_info_a)

        code_splitter.addWidget(panel_a)

        # Panel B
        panel_b = QFrame()
        panel_b.setStyleSheet("background-color: #0c0e15; border: 1px solid #181b26; border-radius: 9px;")
        layout_b = QVBoxLayout(panel_b)
        layout_b.setContentsMargins(10, 8, 10, 8)
        layout_b.setSpacing(6)

        header_b = QHBoxLayout()
        self.lbl_title_b = QLabel("Target B")
        self.lbl_title_b.setStyleSheet("font-weight: 700; font-size: 12px; color: #c084fc;")
        header_b.addWidget(self.lbl_title_b)
        header_b.addStretch()

        self.btn_copy_b = QPushButton("Copy")
        self.btn_copy_b.clicked.connect(lambda: self.copy_code(self.editor_b))
        header_b.addWidget(self.btn_copy_b)
        layout_b.addLayout(header_b)

        self.editor_b = PolyglotCodeEditor(read_only=True)
        layout_b.addWidget(self.editor_b, 1)

        self.lbl_info_b = QLabel()
        self.lbl_info_b.setWordWrap(True)
        self.lbl_info_b.setStyleSheet("color: #94a3b8; font-size: 11px; padding: 4px; background: #08090d; border-radius: 5px;")
        layout_b.addWidget(self.lbl_info_b)

        code_splitter.addWidget(panel_b)

        splitter.addWidget(code_splitter)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 4)

        main_layout.addWidget(splitter, 1)

    def on_topic_changed(self, index):
        self.load_topic(index)

    def load_topic(self, index):
        if index < 0 or index >= len(PARADIGM_TOPICS):
            return
        topic = PARADIGM_TOPICS[index]
        self.lbl_theory_title.setText(f"◆ {topic.title}  —  {topic.subtitle}")
        
        theory_html = f"""
        <div style='color: #cbd5e1; font-family: Segoe UI, sans-serif;'>
            <p style='margin: 0 0 6px 0; line-height: 1.4;'>{topic.deep_theory.replace(chr(10), '<br>')}</p>
            <div style='margin-top: 4px; font-size: 11px;'>
                <span style='color: #10b981; font-weight: 700;'>PROS:</span> {'; '.join(topic.tradeoffs_pros[:2])}<br>
                <span style='color: #f43f5e; font-weight: 700;'>CONS:</span> {'; '.join(topic.tradeoffs_cons[:2])}<br>
                <span style='color: #a855f7; font-weight: 700;'>BEST FIT:</span> {topic.best_use_case}
            </div>
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

        snip_a = topic.snippets.get(lang_a_id)
        if snip_a:
            self.lbl_title_a.setText(f"{LANGUAGES[lang_a_id].name} (Runtime: {snip_a.complexity})")
            self.editor_a.set_language(LANGUAGES[lang_a_id].pygments_lexer)
            self.editor_a.setPlainText(snip_a.code)
            self.lbl_info_a.setText(f"• Mechanics: {snip_a.explanation}")
        else:
            self.editor_a.setPlainText("// Implementation not loaded")
            self.lbl_info_a.setText("")

        snip_b = topic.snippets.get(lang_b_id)
        if snip_b:
            self.lbl_title_b.setText(f"{LANGUAGES[lang_b_id].name} (Runtime: {snip_b.complexity})")
            self.editor_b.set_language(LANGUAGES[lang_b_id].pygments_lexer)
            self.editor_b.setPlainText(snip_b.code)
            self.lbl_info_b.setText(f"• Mechanics: {snip_b.explanation}")
        else:
            self.editor_b.setPlainText("// Implementation not loaded")
            self.lbl_info_b.setText("")

    def copy_code(self, editor):
        clipboard = QApplication.clipboard()
        clipboard.setText(editor.toPlainText())
