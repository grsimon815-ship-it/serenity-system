from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QPushButton, QFrame, QSplitter, QTextEdit, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut

from core.languages import LANGUAGES
from core.code_runner import CodeRunner, RunOutput
from ui.code_editor import PolyglotCodeEditor

PLAYGROUND_TEMPLATES = {
    "python": """# CPython 3.14 Execution & Disassembly Target
import asyncio

async def compute_primes(limit: int = 30):
    primes = [x for x in range(2, limit) if all(x % d != 0 for d in range(2, int(x**0.5) + 1))]
    return primes

async def main():
    res = await compute_primes()
    print(f">> Computed primes ({len(res)} items): {res}")

asyncio.run(main())
""",
    "typescript": """// Node.js V8 Runtime Target
const data = [10, 25, 40, 55, 70];
const evens = data.filter(n => n % 2 === 0);
const sum = evens.reduce((acc, curr) => acc + curr, 0);

console.log(`>> Input count: ${data.length} items`);
console.log(`>> Even sum: ${sum}`);
""",
    "java": """public class VirtualThreadDemo {
    public static void main(String[] args) {
        long sum = 0;
        for (int i = 1; i <= 100; i++) {
            sum += (long) i * i;
        }
        System.out.println(">> JVM HotSpot output. Sum: " + sum);
    }
}
""",
    "rust": """// Rust Zero-Cost Verification
fn main() {
    let mut numbers = vec![1, 2, 3, 4, 5];
    numbers.push(6);
    let total: i32 = numbers.iter().sum();
    println!(">> Rust vector aggregate: {}", total);
}
""",
    "go": """package main

import "fmt"

func main() {
    ch := make(chan string, 1)
    ch <- "Go channel synchronization event"
    close(ch)
    fmt.Printf(">> Received: %s\\n", <-ch)
}
""",
    "cpp": """#include <iostream>
#include <vector>
#include <numeric>

int main() {
    std::vector<int> v = {10, 20, 30, 40, 50};
    int sum = std::accumulate(v.begin(), v.end(), 0);
    std::cout << ">> C++ RAII aggregate sum: " << sum << std::endl;
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
        main_layout.setContentsMargins(16, 14, 16, 14)
        main_layout.setSpacing(10)

        # Control Bar
        top_bar = QFrame()
        top_bar.setProperty("class", "DlcCard")
        top_bar.setStyleSheet("background-color: #0e0f14; border: 1px solid #1c1d27; border-radius: 6px; padding: 4px;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(8, 4, 8, 4)
        top_layout.setSpacing(8)

        lbl_lang = QLabel("Language:")
        lbl_lang.setStyleSheet("font-weight: 600; color: #9ca3af; font-size: 11px;")
        top_layout.addWidget(lbl_lang)

        self.cb_lang = QComboBox()
        for lang_id, lang in LANGUAGES.items():
            self.cb_lang.addItem(f"{lang.name} ({lang.extension})", lang_id)
        self.cb_lang.currentIndexChanged.connect(self.on_language_changed)
        top_layout.addWidget(self.cb_lang, 1)

        top_layout.addSpacing(10)

        self.btn_template = QPushButton("Reset Template")
        self.btn_template.clicked.connect(self.load_template)
        top_layout.addWidget(self.btn_template)

        self.btn_run = QPushButton("Run (Ctrl+Enter)")
        self.btn_run.setProperty("class", "PrimaryBtn")
        self.btn_run.setStyleSheet("""
            QPushButton {
                background-color: #6d28d9;
                border: 1px solid #7c3aed;
                color: #ffffff;
                font-weight: 600;
                padding: 5px 14px;
            }
            QPushButton:hover {
                background-color: #7c3aed;
            }
        """)
        self.btn_run.clicked.connect(self.execute_code)
        top_layout.addWidget(self.btn_run)

        # Disassemble button
        self.btn_disasm = QPushButton("Bytecode")
        self.btn_disasm.clicked.connect(self.show_bytecode)
        top_layout.addWidget(self.btn_disasm)

        # AST button
        self.btn_ast = QPushButton("AST")
        self.btn_ast.clicked.connect(self.show_ast)
        top_layout.addWidget(self.btn_ast)

        self.btn_clear = QPushButton("Clear")
        self.btn_clear.clicked.connect(self.clear_output)
        top_layout.addWidget(self.btn_clear)

        self.lbl_status = QLabel("Idle")
        self.lbl_status.setStyleSheet("color: #6b7280; font-family: 'Consolas', monospace; font-size: 11px; padding-left: 8px;")
        top_layout.addWidget(self.lbl_status, 2)

        main_layout.addWidget(top_bar)

        # Splitter: Source Buffer vs Output Console
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.setHandleWidth(4)

        # Editor Panel
        editor_panel = QFrame()
        editor_panel.setStyleSheet("background-color: #0e0f14; border: 1px solid #1c1d27; border-radius: 6px;")
        editor_layout = QVBoxLayout(editor_panel)
        editor_layout.setContentsMargins(8, 6, 8, 6)
        editor_layout.setSpacing(4)

        lbl_editor_header = QLabel("Source Buffer")
        lbl_editor_header.setStyleSheet("font-weight: 600; color: #6b7280; font-size: 11px; font-family: 'Consolas', monospace;")
        editor_layout.addWidget(lbl_editor_header)

        self.editor = PolyglotCodeEditor(read_only=False)
        editor_layout.addWidget(self.editor, 1)
        splitter.addWidget(editor_panel)

        # Output Panel
        output_panel = QFrame()
        output_panel.setStyleSheet("background-color: #0e0f14; border: 1px solid #1c1d27; border-radius: 6px;")
        output_layout = QVBoxLayout(output_panel)
        output_layout.setContentsMargins(8, 6, 8, 6)
        output_layout.setSpacing(4)

        lbl_output_header = QLabel("Output / Terminal Console")
        lbl_output_header.setStyleSheet("font-weight: 600; color: #6b7280; font-size: 11px; font-family: 'Consolas', monospace;")
        output_layout.addWidget(lbl_output_header)

        self.txt_output = QTextEdit()
        self.txt_output.setReadOnly(True)
        self.txt_output.setStyleSheet("""
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
        output_layout.addWidget(self.txt_output, 1)
        splitter.addWidget(output_panel)

        splitter.setStretchFactor(0, 6)
        splitter.setStretchFactor(1, 4)

        main_layout.addWidget(splitter, 1)

        # Keyboard Shortcut: Ctrl+Enter to execute
        self.shortcut_run = QShortcut(QKeySequence("Ctrl+Return"), self)
        self.shortcut_run.activated.connect(self.execute_code)

    def on_language_changed(self, idx):
        lang_id = self.cb_lang.currentData()
        lexer = LANGUAGES[lang_id].pygments_lexer
        self.editor.set_language(lexer)
        self.load_template()

    def load_template(self):
        lang_id = self.cb_lang.currentData()
        code = PLAYGROUND_TEMPLATES.get(lang_id, f"// Write {lang_id} source code here\n")
        self.editor.setPlainText(code)
        self.txt_output.clear()
        self.lbl_status.setText(f"Loaded template: {LANGUAGES[lang_id].name}")

    def execute_code(self):
        lang_id = self.cb_lang.currentData()
        code = self.editor.toPlainText()
        self.lbl_status.setText("Executing...")
        QApplication.processEvents()

        output: RunOutput = CodeRunner.run(lang_id, code)

        self.txt_output.clear()
        if output.stdout:
            self.txt_output.append(output.stdout)
        if output.stderr:
            self.txt_output.append(f"<span style='color: #ef4444;'>[STDERR]\n{output.stderr}</span>")

        status_color = "#10b981" if output.exit_code == 0 else "#ef4444"
        self.lbl_status.setText(f"<span style='color: {status_color};'>{output.status_label}</span> (Exit Code: {output.exit_code})")

    def show_bytecode(self):
        lang_id = self.cb_lang.currentData()
        code = self.editor.toPlainText()
        disasm = CodeRunner.disassemble(lang_id, code)
        self.txt_output.clear()
        self.txt_output.append(f"<span style='color: #a855f7;'>--- BYTECODE DISASSEMBLY ({lang_id}) ---\n</span>")
        self.txt_output.append(disasm)
        self.lbl_status.setText("Disassembly generated")

    def show_ast(self):
        lang_id = self.cb_lang.currentData()
        code = self.editor.toPlainText()
        ast_tree = CodeRunner.inspect_ast(lang_id, code)
        self.txt_output.clear()
        self.txt_output.append(f"<span style='color: #38bdf8;'>--- ABSTRACT SYNTAX TREE (AST) ---\n</span>")
        self.txt_output.append(ast_tree)
        self.lbl_status.setText("AST parsed")

    def clear_output(self):
        self.txt_output.clear()
        self.lbl_status.setText("Console cleared")
