# Serenity System

A desktop workbench for comparative analysis, interactive memory simulation, and execution across programming languages (Rust, Go, TypeScript, Python, Java, C++).

## Features

- **Paradigms Matrix**: Side-by-side comparative views with live syntax highlighting, disassembly, and AST inspection.
- **Memory Engine**: Step-by-step visualizer for stack frame allocations, heap blocks, move semantics, and lifetimes.
- **Design Patterns**: Interactive circuit breaker and worker pool state machines with live fault injection and request triggers.
- **Playground**: Integrated multi-language runner with real-time stdout/stderr, execution timing, and bytecode disassembler.
- **Metrics**: Matplotlib polar radar chart and Big-O data structure complexity table.
- **Export**: Markdown report exporter with Mermaid flowcharts.

## Quick Start

### Installation

```bash
git clone https://github.com/your-username/serenity-system.git
cd serenity-system
pip install -r requirements.txt
```

### Run

- Windows:
  ```cmd
  run.bat
  ```
- Linux / macOS:
  ```bash
  chmod +x run.sh
  ./run.sh
  ```

## Testing

```bash
python -m unittest discover tests
```

## Shortcuts

- `Ctrl + 1` .. `Ctrl + 6`: Switch workspaces
- `Ctrl + F`: Focus search
- `Ctrl + Enter`: Execute code in Playground

## License

MIT
