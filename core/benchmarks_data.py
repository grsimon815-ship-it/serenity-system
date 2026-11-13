from dataclasses import dataclass
from typing import Dict, List

@dataclass
class LanguageBenchmark:
    language_id: str
    startup_ms: float
    memory_mb: float
    throughput_k_rps: float
    latency_p99_ms: float
    type_safety_score: int  # 1-10
    concurrency_score: int  # 1-10

BENCHMARKS: Dict[str, LanguageBenchmark] = {
    "rust": LanguageBenchmark(
        language_id="rust",
        startup_ms=1.8,
        memory_mb=18.5,
        throughput_k_rps=420.0,
        latency_p99_ms=0.6,
        type_safety_score=10,
        concurrency_score=10
    ),
    "cpp": LanguageBenchmark(
        language_id="cpp",
        startup_ms=2.1,
        memory_mb=21.0,
        throughput_k_rps=410.0,
        latency_p99_ms=0.5,
        type_safety_score=8,
        concurrency_score=9
    ),
    "go": LanguageBenchmark(
        language_id="go",
        startup_ms=5.4,
        memory_mb=34.0,
        throughput_k_rps=360.0,
        latency_p99_ms=1.4,
        type_safety_score=8,
        concurrency_score=10
    ),
    "java": LanguageBenchmark(
        language_id="java",
        startup_ms=120.0,
        memory_mb=145.0,
        throughput_k_rps=310.0,
        latency_p99_ms=2.2,
        type_safety_score=9,
        concurrency_score=9
    ),
    "typescript": LanguageBenchmark(
        language_id="typescript",
        startup_ms=45.0,
        memory_mb=68.0,
        throughput_k_rps=140.0,
        latency_p99_ms=6.8,
        type_safety_score=8,
        concurrency_score=8
    ),
    "python": LanguageBenchmark(
        language_id="python",
        startup_ms=38.0,
        memory_mb=52.0,
        throughput_k_rps=45.0,
        latency_p99_ms=14.2,
        type_safety_score=7,
        concurrency_score=7
    )
}

@dataclass
class AlgorithmComplexity:
    name: str
    category: str
    best_time: str
    avg_time: str
    worst_time: str
    space_complexity: str
    cache_locality: str
    notes: str

ALGORITHMS: List[AlgorithmComplexity] = [
    AlgorithmComplexity(
        name="QuickSort (Introsort)",
        category="Divide & Conquer",
        best_time="O(N log N)",
        avg_time="O(N log N)",
        worst_time="O(N log N)",
        space_complexity="O(log N)",
        cache_locality="High (contiguous array sweeps)",
        notes="Standard library choice in Rust (pdqsort), C++ (std::sort), and Go."
    ),
    AlgorithmComplexity(
        name="LSM-Tree Compaction",
        category="Storage Engine",
        best_time="O(1) write",
        avg_time="O(log N) read",
        worst_time="O(N) during major compaction",
        space_complexity="O(N) with amplification factor ~1.3",
        cache_locality="High for sequential write logs, Medium for block cache",
        notes="Used in RocksDB, Cassandra, and high-throughput write pipelines."
    ),
    AlgorithmComplexity(
        name="Red-Black Tree Insertion",
        category="Self-Balancing BST",
        best_time="O(log N)",
        avg_time="O(log N)",
        worst_time="O(log N)",
        space_complexity="O(N) node pointers",
        cache_locality="Low (pointer indirection across heap nodes)",
        notes="Underlies std::map (C++), TreeMap (Java), but superseded by B-Trees in modern cache-conscious systems."
    ),
    AlgorithmComplexity(
        name="B-Tree Page Search & Split",
        category="Cache-Conscious Index",
        best_time="O(log_B N)",
        avg_time="O(log_B N)",
        worst_time="O(log_B N)",
        space_complexity="O(N)",
        cache_locality="Very High (nodes fit exactly into CPU L1/L2 cache lines)",
        notes="Industry standard for databases (PostgreSQL, SQLite, BTreeMap in Rust)."
    )
]
