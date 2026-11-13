from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QPushButton, QFrame, QSplitter, QTextEdit, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from core.languages import LANGUAGES
from core.code_runner import CodeRunner, RunOutput
from ui.code_editor import PolyglotCodeEditor

PLAYGROUND_TEMPLATES = {
    "python": """# Python 3.14 Playground
import asyncio

async def compute_primes():
    print("[Python 3.14] Starting high-level async compute...")
    await asyncio.sleep(0.05)
    numbers = [x for x in range(2, 30) if all(x % d != 0 for d in range(2, int(x**0.5) + 1))]
    print(f"[Result] Primes up to 30: {numbers}")

asyncio.run(compute_primes())
""",
    "typescript": """// TypeScript / Node.js V8 Playground
console.log("[TypeScript] Initializing pipeline...");

interface TaskPayload {
    id: number;
    title: string;
    completed: boolean;
}

const tasks: TaskPayload[] = [
    { id: 1, title: "Compile AST", completed: true },
    { id: 2, title: "Verify Lifetimes", completed: true },
    { id: 3, title: "Demultiplex IO", completed: false }
];

const completed = tasks.filter(t => t.completed).map(t => t.title);
console.log(`[Result] Completed tasks: ${completed.join(', ')}`);
""",
    "java": """public class VirtualThreadDemo {
    public static void main(String[] args) {
        System.out.println("[Java 21+] Executing on JVM...");
        int sum = 0;
        for (int i = 1; i <= 10; i++) {
            sum += i * i;
        }
        System.out.println("[Result] Sum of squares (1..10): " + sum);
    }
}
""",
    "rust": """// Rust Zero-Cost Concurrency Template
fn main() {
    println!("[Rust] Fearless concurrency and compile-time ownership verification.");
    let numbers = vec![10, 20, 30, 40];
    let sum: i32 = numbers.iter().sum();
    println!("[Result] Vector sum: {}", sum);
}
""",
    "go": """package main

import "fmt"

func main() {
    fmt.Println("[Go CSP] Communicating Sequential Processes runtime.")
    ch := make(chan string, 1)
    ch <- "Go channel message received"
    fmt.Println("[Result]", <-ch)
}
""",
    "cpp": """#include <iostream>
#include <vector>
#include <numeric>

int main() {
    std::cout << "[C++ RAII] Zero abstraction penalty." << std::endl;
    std::vector<int> v = {1, 2, 3, 4, 5};
    int total = std::accumulate(v.begin(), v.end(), 0);
    std::cout << "[Result] Accumulate sum: " << total << std::endl;
    return 0;
}
"""
}

class CodePlaygroundTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self.on_language_changed(0)

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Control Bar
        top_bar = QFrame()
        top_bar.setStyleSheet("background-color: #0e1119; border: 1px solid #181b26; border-radius: 9px; padding: 6px;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(8, 6, 8, 6)

        lbl_lang = QLabel("Language Target:")
        lbl_lang.setStyleSheet("font-weight: 700; color: #f8fafc;")
        top_layout.addWidget(lbl_lang)

        self.cb_lang = QComboBox()
        for lang_id, lang in LANGUAGES.items():
            self.cb_lang.addItem(f"{lang.name} ({lang.extension})", lang_id)
        self.cb_lang.currentIndexChanged.connect(self.on_language_changed)
        top_layout.addWidget(self.cb_lang, 1)

        top_layout.addSpacing(16)

        self.btn_reset_template = QPushButton("Load Template")
        self.btn_reset_template.clicked.connect(self.load_template)
        top_layout.addWidget(self.btn_reset_template)

        self.btn_run = QPushButton("▶ Run Code (F5)")
        self.btn_run.setProperty("class", "SuccessBtn")
        self.btn_run.setStyleSheet("""
            QPushButton {
                background-color: #059669;
                border: 1px solid #10b981;
                color: #ffffff;
                font-weight: 700;
                padding: 6px 18px;
            }
            QPushButton:hover {
                background-color: #10b981;
            }
        """)
        self.btn_run.clicked.connect(self.execute_code)
        top_layout.addWidget(self.btn_run)

        self.lbl_status_badge = QLabel("Ready")
        self.lbl_status_badge.setStyleSheet("color: #94a3b8; font-size: 11px; padding-left: 10px;")
        top_layout.addWidget(self.lbl_status_badge, 2)

        main_layout.addWidget(top_bar)

        # Splitter: Code Editor (Top) & Terminal Console (Bottom)
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.setHandleWidth(6)

        # Editor Panel
        editor_panel = QFrame()
        editor_panel.setStyleSheet("background-color: #0b1120; border: 1px solid #1e293b; border-radius: 8px;")
        editor_layout = QVBoxLayout(editor_panel)
        editor_layout.setContentsMargins(10, 8, 10, 10)

        lbl_editor_header = QLabel("Interactive Source Buffer")
        lbl_editor_header.setStyleSheet("font-weight: 600; color: #94a3b8; font-size: 12px;")
        editor_layout.addWidget(lbl_editor_header)

        self.editor = PolyglotCodeEditor(read_only=False)
        editor_layout.addWidget(self.editor, 1)
        splitter.addWidget(editor_panel)

        # Console Output Panel
        console_panel = QFrame()
        console_panel.setStyleSheet("background-color: #080c14; border: 1px solid #1e293b; border-radius: 8px;")
        console_layout = QVBoxLayout(console_panel)
        console_layout.setContentsMargins(10, 8, 10, 10)

        lbl_console_header = QLabel("Execution Output (Stdout / Stderr)")
        lbl_console_header.setStyleSheet("font-weight: 600; color: #94a3b8; font-size: 12px;")
        console_layout.addWidget(lbl_console_header)

        self.txt_output = QTextEdit()
        self.txt_output.setReadOnly(True)
        self.txt_output.setStyleSheet("""
            QTextEdit {
                background-color: #05080f;
                color: #e2e8f0;
                font-family: Consolas, monospace;
                font-size: 11px;
                border: 1px solid #1e293b;
                border-radius: 6px;
            }
        """)
        console_layout.addWidget(self.txt_output, 1)
        splitter.addWidget(console_panel)

        splitter.setStretchFactor(0, 6)
        splitter.setStretchFactor(1, 4)

        main_layout.addWidget(splitter, 1)

    def on_language_changed(self, idx):
        lang_id = self.cb_lang.currentData()
        lexer = LANGUAGES[lang_id].pygments_lexer
        self.editor.set_language(lexer)
        self.load_template()

    def load_template(self):
        lang_id = self.cb_lang.currentData()
        code = PLAYGROUND_TEMPLATES.get(lang_id, f"// Write {lang_id} code here\n")
        self.editor.setPlainText(code)
        self.txt_output.clear()
        self.lbl_status_badge.setText(f"Template loaded for {LANGUAGES[lang_id].name}")

    def execute_code(self):
        lang_id = self.cb_lang.currentData()
        code = self.editor.toPlainText()
        self.lbl_status_badge.setText("Executing...")
        QApplication.processEvents()

        output: RunOutput = CodeRunner.run(lang_id, code)

        self.txt_output.clear()
        if output.stdout:
            self.txt_output.append(output.stdout)
        if output.stderr:
            self.txt_output.append(f"<span style='color: #ef4444;'>[STDERR]\n{output.stderr}</span>")

        status_color = "#10b981" if output.exit_code == 0 else "#ef4444"
        self.lbl_status_badge.setText(f"<span style='color: {status_color}; font-weight: bold;'>{output.status_label}</span> (Exit: {output.exit_code})")
