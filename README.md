# ⚡ PolyglotForge Studio

<div align="center">

![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue?style=for-the-badge&logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green?style=for-the-badge&logo=qt)
![CI](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge&logo=githubactions)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-purple?style=for-the-badge)

**The Universal Interactive Studio for Mastering High-Level Paradigms, Memory Models, and Architectural Patterns across Rust, Go, TypeScript, Python, Java, and C++.**

</div>

---

## 🌟 Why PolyglotForge?

In high-level systems design, writing code in a single language is no longer enough. Senior engineers and system architects need an intuitive mental model of how **concurrency, memory lifetimes, sum types, and resilient architecture patterns** translate across different runtimes:

- How does **Rust's zero-cost compile-time affine type system** compare to **Go's Tri-color Mark-Sweep GC** and **Java's ZGC**?
- How does **Go's CSP (Goroutines + Channels)** compare to **Rust Tokio's asynchronous future state machines** and the **JavaScript Event Loop**?
- What actually happens on the **Stack and Heap** during move semantics, smart pointer transfers, and escape analysis?

**PolyglotForge** provides a visual, interactive desktop workbench to explore, simulate, benchmark, and execute these concepts side-by-side with zero guesswork.

---

## 🚀 Key Modules

### 1. 🌟 Paradigm Matrix (The Polyglot Rosetta Stone)
- Synchronized side-by-side comparative inspection between any two languages.
- Deep theoretical breakdown of architectural principles, pros, cons, and runtime mechanics.
- Pygments-powered syntax highlighting with line numbering and instant clipboard copying.

### 2. 🧠 Memory & Lifetime Visual Simulator
- Step-by-step visual inspection of **Stack Frames** and **Heap Allocations**.
- Visual representation of pointers, references, affine ownership moves, shared borrows, and scope deallocations.
- Supported scenarios: **Rust Move Semantics & Borrowing**, **C++ RAII std::unique_ptr**, and **Go Escape Analysis**.

### 3. 🏛️ Architecture & Design Pattern Lab
- Interactive visual graph sandboxes for resilience and distributed patterns:
  - **Circuit Breaker Pattern**: Live state transitions (`CLOSED` ➔ `OPEN` ➔ `HALF-OPEN`) with interactive failure spikes and fast-fail fallbacks.
  - **Worker Pool / Fan-Out Fan-In**: Work queues, dynamic task dispatching, and worker status tracking.
- Idiomatic, production-grade implementations in Rust, Go, and TypeScript.

### 4. ⚡ Universal Code Playground & Runner
- Real-time execution engine for multi-language snippets.
- Executes Python, Node.js/TypeScript, and Java natively on your machine, with high-fidelity simulated execution for Rust, Go, and C++.
- Real-time stdout/stderr capture, exit code inspection, and execution duration metrics.

### 5. 📊 Algorithmic Complexity & Benchmark Radar
- Interactive Matplotlib polar radar chart comparing Memory Efficiency, Cold Startup Speed, Concurrency Throughput, Latency, and Type Safety across runtimes.
- Big-O algorithmic complexity matrix with cache-locality impact analysis for Introsort, LSM-Trees, Red-Black Trees, and B-Trees.

### 6. 📑 GitHub Markdown Exporter
- Generates GitHub-ready Markdown reports with badges, Mermaid architecture diagrams, and syntax-highlighted code comparison blocks.

---

## 🖥️ Quick Start

### Prerequisites
- Python 3.10+ (Tested up to Python 3.14)
- Pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/polyglot-forge.git
   cd polyglot-forge
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the studio:
   - On Windows:
     ```bash
     run.bat
     # or
     python main.py
     ```
   - On Linux / macOS:
     ```bash
     chmod +x run.sh
     ./run.sh
     # or
     python3 main.py
     ```

---

## 🧪 Running Tests

To verify that all components, runtimes, and scenarios are functioning correctly:

```bash
python -m unittest discover tests
```

---

## 📁 Project Architecture

```
polyglot-forge/
├── .github/workflows/ci.yml # GitHub Actions automated CI
├── core/
│   ├── languages.py         # Language definitions and metadata
│   ├── paradigms_data.py    # Paradigm matrix data and comparative code
│   ├── memory_scenarios.py  # Memory simulation steps (Stack/Heap/Pointers)
│   ├── patterns_data.py     # Architecture patterns (Circuit Breaker, Worker Pool)
│   ├── benchmarks_data.py   # Benchmark metrics and Big-O models
│   └── code_runner.py       # Multi-language execution runner
├── ui/
│   ├── theme.py             # Modern dark glassmorphic styling
│   ├── code_editor.py       # Pygments syntax highlighter & line number area
│   ├── tab_matrix.py        # Paradigm Matrix view
│   ├── tab_memory.py        # Memory & Lifetime visual simulator
│   ├── tab_patterns.py      # Architecture Patterns lab
│   ├── tab_playground.py    # Code playground & runner
│   ├── tab_benchmarks.py    # Matplotlib radar chart & Big-O matrix
│   ├── tab_exporter.py      # GitHub Markdown report generator
│   └── main_window.py       # Main window and status bar
├── tests/
│   └── test_core.py         # Automated test suite
├── main.py                  # Application entry point
├── requirements.txt         # Dependencies
├── run.bat                  # Windows one-click launcher
└── README.md
```

---

## 📄 License

This project is licensed under the MIT License.
