import { LanguageMeta, SupportedLanguage } from '../types';

export const LANGUAGES: Record<SupportedLanguage, LanguageMeta> = {
  rust: {
    id: 'rust',
    name: 'Rust',
    category: 'Systems / Poly-paradigm',
    typing: 'Static, Strong, Affine / Linear',
    memory: 'Compile-time Ownership & Lifetimes (Zero-cost RAII)',
    concurrencyModel: 'Fearless Concurrency, Send/Sync Traits, Tokio / Async-Await',
    color: '#f97316',
    badgeBg: 'bg-orange-500/10 text-orange-400 border-orange-500/30',
    extension: '.rs',
    version: '1.82+'
  },
  go: {
    id: 'go',
    name: 'Go',
    category: 'Concurrent / Systems',
    typing: 'Static, Structural / Duck-like interfaces',
    memory: 'Concurrent Tracing Tri-color Mark-Sweep GC',
    concurrencyModel: 'Communicating Sequential Processes (Goroutines + Channels)',
    color: '#06b6d4',
    badgeBg: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30',
    extension: '.go',
    version: '1.23+'
  },
  typescript: {
    id: 'typescript',
    name: 'TypeScript',
    category: 'High-Level Application / Web',
    typing: 'Static, Gradual, Structural Type System',
    memory: 'Automatic V8 Generational Mark-Compact GC',
    concurrencyModel: 'Single-threaded Non-blocking Event Loop + Worker Threads',
    color: '#3b82f6',
    badgeBg: 'bg-blue-500/10 text-blue-400 border-blue-500/30',
    extension: '.ts',
    version: '5.6+'
  },
  python: {
    id: 'python',
    name: 'Python',
    category: 'High-Level / Data / Scripting',
    typing: 'Dynamic, Strong, Duck Typing (Optional Type Hints)',
    memory: 'Reference Counting + Generational Cycle Detector',
    concurrencyModel: 'Asyncio Event Loop, Multiprocessing (GIL / Free-threaded 3.13+)',
    color: '#eab308',
    badgeBg: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/30',
    extension: '.py',
    version: '3.14'
  },
  java: {
    id: 'java',
    name: 'Java',
    category: 'Enterprise / JVM OOP',
    typing: 'Static, Strong, Nominal Typing with Generics',
    memory: 'Generational Tracing GC (G1, ZGC, Shenandoah)',
    concurrencyModel: 'Project Loom Virtual Threads + Structured Concurrency',
    color: '#ef4444',
    badgeBg: 'bg-red-500/10 text-red-400 border-red-500/30',
    extension: '.java',
    version: '21 LTS / 23'
  },
  cpp: {
    id: 'cpp',
    name: 'C++',
    category: 'High-Performance Multi-paradigm',
    typing: 'Static, Strong, Nominal with Concepts & Template Metaprogramming',
    memory: 'Manual Allocation + RAII (Smart Pointers: unique_ptr, shared_ptr)',
    concurrencyModel: 'std::jthread, Coroutines (C++20), Atomics, Execution Policies',
    color: '#8b5cf6',
    badgeBg: 'bg-purple-500/10 text-purple-400 border-purple-500/30',
    extension: '.cpp',
    version: 'C++23'
  },
  elixir: {
    id: 'elixir',
    name: 'Elixir',
    category: 'Functional / Distributed Systems',
    typing: 'Dynamic, Strong, Structural Pattern Matching',
    memory: 'Per-Process Isolated BEAM Garbage Collection',
    concurrencyModel: 'Actor Model (Erlang OTP GenServer, Millions of isolated processes)',
    color: '#c084fc',
    badgeBg: 'bg-fuchsia-500/10 text-fuchsia-400 border-fuchsia-500/30',
    extension: '.ex',
    version: '1.17'
  }
};
