from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QPushButton, QFrame, QTextEdit, QFileDialog, QApplication, QMessageBox
)
from PyQt6.QtCore import Qt

from core.languages import LANGUAGES
from core.paradigms_data import PARADIGM_TOPICS

class ExporterTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self.generate_markdown()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 14, 16, 14)
        main_layout.setSpacing(10)

        # Control Bar
        top_bar = QFrame()
        top_bar.setProperty("class", "DlcCard")
        top_bar.setStyleSheet("background-color: #0e0f14; border: 1px solid #1c1d27; border-radius: 6px; padding: 4px;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(8, 4, 8, 4)
        top_layout.setSpacing(8)

        lbl_topic = QLabel("Topic:")
        lbl_topic.setStyleSheet("font-weight: 600; color: #9ca3af; font-size: 11px;")
        top_layout.addWidget(lbl_topic)

        self.cb_topic = QComboBox()
        for t in PARADIGM_TOPICS:
            self.cb_topic.addItem(t.title, t.id)
        self.cb_topic.currentIndexChanged.connect(self.generate_markdown)
        top_layout.addWidget(self.cb_topic, 2)

        top_layout.addSpacing(12)

        self.btn_copy = QPushButton("Copy to Clipboard")
        self.btn_copy.clicked.connect(self.copy_to_clipboard)
        top_layout.addWidget(self.btn_copy)

        self.btn_save = QPushButton("Save to File (.md)")
        self.btn_save.setProperty("class", "PrimaryBtn")
        self.btn_save.clicked.connect(self.save_to_file)
        top_layout.addWidget(self.btn_save)

        main_layout.addWidget(top_bar)

        # Markdown Buffer
        preview_panel = QFrame()
        preview_panel.setStyleSheet("background-color: #0e0f14; border: 1px solid #1c1d27; border-radius: 6px;")
        preview_layout = QVBoxLayout(preview_panel)
        preview_layout.setContentsMargins(8, 6, 8, 6)
        preview_layout.setSpacing(4)

        lbl_header = QLabel("Generated Markdown Buffer")
        lbl_header.setStyleSheet("font-weight: 600; color: #6b7280; font-size: 11px; font-family: 'Consolas', monospace;")
        preview_layout.addWidget(lbl_header)

        self.txt_markdown = QTextEdit()
        self.txt_markdown.setStyleSheet("""
            QTextEdit {
                background-color: #0a0b0e;
                color: #d1d5db;
                font-family: 'Consolas', monospace;
                font-size: 11px;
                border: 1px solid #1c1d27;
                border-radius: 4px;
                padding: 6px;
            }
        """)
        preview_layout.addWidget(self.txt_markdown, 1)

        main_layout.addWidget(preview_panel, 1)

    def generate_markdown(self):
        topic_idx = self.cb_topic.currentIndex()
        if topic_idx < 0 or topic_idx >= len(PARADIGM_TOPICS):
            return
        topic = PARADIGM_TOPICS[topic_idx]

        md = []
        md.append(f"# {topic.title}\n")
        md.append(f"> {topic.subtitle}\n\n")

        md.append("## Specification & Theoretical Model\n")
        md.append(f"{topic.deep_theory}\n\n")

        md.append("### Architectural Tradeoffs\n")
        md.append("- **Advantages:**\n")
        for pro in topic.tradeoffs_pros:
            md.append(f"  - {pro}\n")
        md.append("- **Overhead & Constraints:**\n")
        for con in topic.tradeoffs_cons:
            md.append(f"  - {con}\n")
        md.append(f"\n**Target Application:** `{topic.best_use_case}`\n\n")

        md.append("## Concurrency & Control Flow (Mermaid)\n")
        md.append("```mermaid\ngraph LR\n")
        md.append("    A[Dispatch Request] --> B{Execution Runtime}\n")
        md.append("    B -->|Go CSP| C[Goroutine + Channel Sync]\n")
        md.append("    B -->|Rust Async| D[Zero-Cost Future Poll State Machine]\n")
        md.append("    B -->|Node.js V8| E[Event Loop Microtask Resolution]\n")
        md.append("    B -->|Java Loom| F[Virtual Thread Fiber Continuation]\n")
        md.append("```\n\n")

        md.append("## Multi-Language Implementations\n\n")
        for lang_id, snip in topic.snippets.items():
            lang_name = LANGUAGES[lang_id].name
            md.append(f"### {lang_name}\n")
            md.append(f"- **Runtime Cost:** `{snip.complexity}`\n")
            md.append(f"- **Mechanics:** {snip.explanation}\n\n")
            md.append(f"```{lang_id}\n{snip.code}\n```\n\n")

        md.append("---\n*PolyglotForge Workbench Output*\n")
        self.txt_markdown.setPlainText("".join(md))

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.txt_markdown.toPlainText())

    def save_to_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Markdown Report", "SPEC_REPORT.md", "Markdown Files (*.md)")
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.txt_markdown.toPlainText())
            QMessageBox.information(self, "Export", f"Report written to:\n{filename}")
