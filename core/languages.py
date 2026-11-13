from dataclasses import dataclass
from typing import Dict, List

@dataclass
class LanguageDefinition:
    id: str
    name: str
    category: str
    type_system: str
    memory_model: str
    concurrency: str
    color_hex: str
    extension: str
    pygments_lexer: str
    runtime_cmd: str

LANGUAGES: Dict[str, LanguageDefinition] = {
    "rust": LanguageDefinition(
        id="rust",
        name="Rust",
        category="Systems / Poly-paradigm",
        type_system="Affine / Linear, Static Strong",
        memory_model="Compile-time Ownership & Lifetimes (Zero-cost RAII)",
        concurrency="Fearless Concurrency, Send/Sync, Tokio Async",
        color_hex="#f97316",
        extension=".rs",
        pygments_lexer="rust",
        runtime_cmd="rustc"
    ),
    "go": LanguageDefinition(
        id="go",
        name="Go",
        category="Concurrent Systems",
        type_system="Structural Interfaces, Static Strong",
        memory_model="Tri-color Concurrent Mark-Sweep GC",
        concurrency="CSP (Goroutines & Channels)",
        color_hex="#06b6d4",
        extension=".go",
        pygments_lexer="go",
        runtime_cmd="go"
    ),
    "typescript": LanguageDefinition(
        id="typescript",
        name="TypeScript",
        category="High-Level Application",
        type_system="Gradual Structural Type System",
        memory_model="Generational Scavenge + Mark-Compact (V8)",
        concurrency="Single-Threaded Event Loop with Microtasks",
        color_hex="#3b82f6",
        extension=".ts",
        pygments_lexer="typescript",
        runtime_cmd="node"
    ),
    "python": LanguageDefinition(
        id="python",
        name="Python",
        category="High-Level Scripting & Data",
        type_system="Dynamic Duck Typing, Strong",
        memory_model="Reference Counting + Cyclic Generational GC",
        concurrency="Asyncio Cooperative Loop & Free-Threading",
        color_hex="#eab308",
        extension=".py",
        pygments_lexer="python",
        runtime_cmd="python"
    ),
    "java": LanguageDefinition(
        id="java",
        name="Java",
        category="Enterprise Object-Oriented",
        type_system="Nominal with Generics, Static Strong",
        memory_model="Generational Tracing (G1, ZGC)",
        concurrency="Project Loom Virtual Threads & Concurrency Utilities",
        color_hex="#ef4444",
        extension=".java",
        pygments_lexer="java",
        runtime_cmd="javac"
    ),
    "cpp": LanguageDefinition(
        id="cpp",
        name="C++",
        category="High-Performance Multi-paradigm",
        type_system="Static Strong with Concepts",
        memory_model="Manual + RAII (Smart Pointers unique/shared)",
        concurrency="std::jthread, Coroutines, Atomics",
        color_hex="#a855f7",
        extension=".cpp",
        pygments_lexer="cpp",
        runtime_cmd="g++"
    )
}
