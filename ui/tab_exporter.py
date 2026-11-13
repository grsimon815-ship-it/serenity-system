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
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Control Bar
        top_bar = QFrame()
        top_bar.setStyleSheet("background-color: #0e1119; border: 1px solid #181b26; border-radius: 9px; padding: 6px;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(8, 6, 8, 6)

        lbl_topic = QLabel("Export Paradigm:")
        lbl_topic.setStyleSheet("font-weight: 700; color: #f8fafc;")
        top_layout.addWidget(lbl_topic)

        self.cb_topic = QComboBox()
        for t in PARADIGM_TOPICS:
            self.cb_topic.addItem(t.title, t.id)
        self.cb_topic.currentIndexChanged.connect(self.generate_markdown)
        top_layout.addWidget(self.cb_topic, 2)

        top_layout.addSpacing(16)

        self.btn_copy = QPushButton("Copy Markdown")
        self.btn_copy.clicked.connect(self.copy_to_clipboard)
        top_layout.addWidget(self.btn_copy)

        self.btn_save = QPushButton("Save to File (.md)")
        self.btn_save.setProperty("class", "PrimaryBtn")
        self.btn_save.clicked.connect(self.save_to_file)
        top_layout.addWidget(self.btn_save)

        main_layout.addWidget(top_bar)

        # Markdown Preview Area
        preview_panel = QFrame()
        preview_panel.setStyleSheet("background-color: #0b1120; border: 1px solid #1e293b; border-radius: 8px;")
        preview_layout = QVBoxLayout(preview_panel)
        preview_layout.setContentsMargins(10, 8, 10, 10)

        lbl_header = QLabel("Generated GitHub-Ready Markdown (with Mermaid & Badges)")
        lbl_header.setStyleSheet("font-weight: 600; color: #38bdf8; font-size: 12px;")
        preview_layout.addWidget(lbl_header)

        self.txt_markdown = QTextEdit()
        self.txt_markdown.setStyleSheet("""
            QTextEdit {
                background-color: #080c14;
                color: #e2e8f0;
                font-family: Consolas, monospace;
                font-size: 11px;
                border: 1px solid #1e293b;
                border-radius: 6px;
                padding: 8px;
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
        md.append(f"> **{topic.subtitle}**\n")
        md.append("![Rust](https://img.shields.io/badge/Rust-DEA584?style=for-the-badge&logo=rust&logoColor=black) ")
        md.append("![Go](https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white) ")
        md.append("![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white) ")
        md.append("![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)\n\n")

        md.append("## 📐 Architectural Theory\n")
        md.append(f"{topic.deep_theory}\n\n")

        md.append("### ⚖️ Architectural Tradeoffs\n")
        md.append("**Advantages:**\n")
        for pro in topic.tradeoffs_pros:
            md.append(f"- ✅ {pro}\n")
        md.append("\n**Considerations & Overhead:**\n")
        for con in topic.tradeoffs_cons:
            md.append(f"- ⚠️ {con}\n")
        md.append(f"\n**Optimal Scope:** `{topic.best_use_case}`\n\n")

        md.append("## 🔄 Paradigm State Machine Flow (Mermaid)\n")
        md.append("```mermaid\ngraph LR\n")
        md.append("    A[Client Request] --> B{Concurrency Demuxer}\n")
        md.append("    B -->|Go CSP| C[Goroutine + Channel]\n")
        md.append("    B -->|Rust Async| D[Zero-Cost Future State Machine]\n")
        md.append("    B -->|Node.js| E[Event Loop Microtask Queue]\n")
        md.append("    B -->|Java Loom| F[Virtual Thread Fiber Pool]\n")
        md.append("```\n\n")

        md.append("## 💻 Multi-Language Implementation Matrix\n\n")
        for lang_id, snip in topic.snippets.items():
            lang_name = LANGUAGES[lang_id].name
            md.append(f"### {lang_name}\n")
            md.append(f"- **Runtime Cost:** `{snip.complexity}`\n")
            md.append(f"- **Core Mechanics:** {snip.explanation}\n\n")
            md.append(f"```{lang_id}\n{snip.code}\n```\n\n")

        md.append("---\n*Generated automatically with [PolyglotForge Studio](https://github.com/polyglotforge)*\n")

        self.txt_markdown.setPlainText("".join(md))

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.txt_markdown.toPlainText())
        QMessageBox.information(self, "Success", "Markdown copied to clipboard!")

    def save_to_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Markdown Report", "ARCHITECTURE_COMPARISON.md", "Markdown Files (*.md)")
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.txt_markdown.toPlainText())
            QMessageBox.information(self, "Saved", f"Exported successfully to:\n{filename}")
