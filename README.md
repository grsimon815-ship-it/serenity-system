# Serenity System

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-7c3aed.svg?style=flat-square)](LICENSE)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-0c0d11.svg?style=flat-square&logo=python)](https://python.org)
[![GUI: PyQt6](https://img.shields.io/badge/GUI-PyQt6-10b981.svg?style=flat-square)](https://riverbankcomputing.com/software/pyqt/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-38bdf8.svg?style=flat-square)](https://github.com)

**High-level programming paradigm workbench, interactive memory model engine, and multi-language execution runtime.**

</div>

---

## Overview

Serenity System is an open-source desktop engineering workbench designed for comparative language analysis, low-level execution inspection, and architecture modeling across **Rust, Go, TypeScript, Python, Java, and C++**.

It focuses on verifiable runtime mechanics rather than abstract syntax, providing live bytecode disassembly, AST parsing, step-by-step memory model simulations (stack frames, heap blocks, borrow checker mechanics), and resilient architecture patterns.

---

## Core Modules

### 1. Paradigms Matrix
- **Synchronized Comparative Views**: Side-by-side inspection between any two languages.
- **Three Inspection Modes**:
  - `Source`: Syntax-highlighted idiomatic implementations.
  - `Bytecode`: Real-time CPython bytecode disassembly via standard `dis` (`LOAD_FAST`, `CALL`, `RETURN_VALUE`).
  - `AST`: Concrete abstract syntax tree dumping via `ast.dump`.
- **Covered Paradigms**:
  - Concurrency: CSP channels vs Tokio futures vs Event Loop vs Project Loom virtual threads.
  - Memory: Compile-time affine ownership vs Generational Tracing GC vs RAII smart pointers.
  - Types: Monadic `Result<T, E>` / `Option<T>` vs Discriminated Unions vs Sentinel errors.

### 2. Memory Engine
- **Visual Call Stack & Heap Store**: Renders stack frames, variable addresses, byte sizes, and dynamic heap allocations.
- **Pointer & Reference Tracking**: Visualizes pointers, shared borrows (`&T`), exclusive borrows (`&mut T`), moves, and drop glue deallocations.
- **Supported Scenarios**:
  - Rust move semantics and borrowing rules.
  - C++ RAII with `std::unique_ptr` and `std::move`.
  - Go escape analysis and tri-color garbage collection boundaries.

### 3. Architecture Patterns
- **Interactive State Machine**: Circuit Breaker with live transitions (`CLOSED` ➔ `OPEN` ➔ `HALF-OPEN`).
- **Interactive Fault Injection**: Trigger successful requests (HTTP 200), inject faults (HTTP 500) to trip thresholds, and test fast-fail fallback routing.
- **Worker Pool / Fan-Out Fan-In**: Job queues, worker pools, and result aggregators.

### 4. Code Playground
- **Native Local Execution**: Direct subprocess execution for Python 3.14, Node.js V8 (TypeScript), and Java HotSpot.
- **Real-Time Telemetry**: Stdout/stderr capture, process return codes, and execution duration in milliseconds.
- **On-Demand Inspection**: Disassemble bytecode or dump AST directly from the playground buffer.

### 5. Metrics & Algorithmic Complexity
- **Polar Radar Matrix**: Relative comparison across 5 vectors (Memory Efficiency, Cold Start, Throughput, Tail Latency P99, Type Safety).
- **Cache Locality Matrix**: Big-O time and space complexity with L1/L2 cache impact analysis for Introsort, LSM-Trees, Red-Black Trees, and B-Trees.

### 6. Document Exporter
- **Automated Report Generation**: Exports complete comparison matrices to clean GitHub Markdown format with Mermaid flowcharts and syntax blocks.

---

## Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| `Ctrl + 1` | Switch to **Paradigms** |
| `Ctrl + 2` | Switch to **Memory** |
| `Ctrl + 3` | Switch to **Patterns** |
| `Ctrl + 4` | Switch to **Playground** |
| `Ctrl + 5` | Switch to **Metrics** |
| `Ctrl + 6` | Switch to **Export** |
| `Ctrl + F` | Focus search / filter bar |
| `Ctrl + Enter` | Execute current buffer in Playground |

---

## Directory Structure

```
serenity-system/
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions automated test pipeline
├── core/
│   ├── benchmarks_data.py  # Benchmark metrics and Big-O models
│   ├── code_runner.py      # Subprocess runner, bytecode disassembler & AST dumper
│   ├── languages.py        # Language definitions, lexers, and metadata
│   ├── memory_scenarios.py # Memory models (Stack/Heap/Pointers/Lifetimes)
│   ├── paradigms_data.py   # High-level paradigm code and theory
│   └── patterns_data.py    # Architecture pattern definitions (Circuit Breaker)
├── ui/
│   ├── code_editor.py      # High-legibility Pygments syntax editor with line numbers
│   ├── main_window.py      # Workbench navigation, shortcuts, and stacked views
│   ├── tab_benchmarks.py   # Polar radar chart and complexity matrix
│   ├── tab_exporter.py     # GitHub Markdown document generator
│   ├── tab_matrix.py       # Comparative paradigm matrix (Source/Bytecode/AST)
│   ├── tab_memory.py       # Stack/Heap memory visualizer
│   ├── tab_patterns.py     # Interactive design pattern lab
│   ├── tab_playground.py   # Multi-language runner and terminal console
│   └── theme.py            # Serenity dark theme and high-contrast typography
├── tests/
│   └── test_core.py        # Unit test suite
├── main.py                 # Application entry point
├── requirements.txt        # Python package dependencies
├── run.bat                 # Windows one-click launcher
├── run.sh                  # Linux/macOS launcher
├── CONTRIBUTING.md         # Guidelines for contributors
└── LICENSE                 # MIT License
```

---

## Installation & Launch

### Prerequisites
- Python 3.10 or newer (tested on Python 3.14)
- Pip

### 1. Clone the repository
```bash
git clone https://github.com/your-username/serenity-system.git
cd serenity-system
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
- **Windows**:
  ```cmd
  run.bat
  ```
  *or*
  ```cmd
  python main.py
  ```

- **Linux / macOS**:
  ```bash
  chmod +x run.sh
  ./run.sh
  ```

---

## Running Automated Tests

```bash
python -m unittest discover tests
```

---

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on code style, testing, and pull request process.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
