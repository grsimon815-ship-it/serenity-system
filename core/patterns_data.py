from dataclasses import dataclass
from typing import Dict, List

@dataclass
class PatternGraphNode:
    id: str
    label: str
    role: str
    status: str  # idle, active, success, warning, error
    x: float
    y: float

@dataclass
class PatternGraphEdge:
    source_id: str
    target_id: str
    label: str

@dataclass
class ArchitecturePattern:
    id: str
    name: str
    category: str
    summary: str
    problem: str
    solution: str
    nodes: List[PatternGraphNode]
    edges: List[PatternGraphEdge]
    code_implementations: Dict[str, str]

PATTERNS: List[ArchitecturePattern] = [
    ArchitecturePattern(
        id="circuit_breaker",
        name="Circuit Breaker Pattern",
        category="Resilience & Fault Tolerance",
        summary="Prevents cascading failures by tripping open when failure thresholds are exceeded.",
        problem="Downstream service degradation causes thread pool exhaustion and cascading system outages.",
        solution="Wrap calls in a state machine (CLOSED -> OPEN -> HALF-OPEN). Fast-fail requests when OPEN without calling downstream services.",
        nodes=[
            PatternGraphNode("client", "API Client", "Caller", "active", 50, 150),
            PatternGraphNode("breaker", "Circuit Breaker", "State Machine", "idle", 220, 150),
            PatternGraphNode("downstream", "Payment Gateway", "External Microservice", "idle", 400, 150),
            PatternGraphNode("fallback", "Fallback Cache", "Degraded Response", "idle", 220, 270),
        ],
        edges=[
            PatternGraphEdge("client", "breaker", "Request"),
            PatternGraphEdge("breaker", "downstream", "Proxy Call (CLOSED)"),
            PatternGraphEdge("breaker", "fallback", "Fast-Fail (OPEN)"),
        ],
        code_implementations={
            "rust": """pub enum CircuitState {
    Closed,
    Open { opened_at: std::time::Instant },
    HalfOpen,
}

pub struct CircuitBreaker {
    pub failure_threshold: u32,
    pub failure_count: u32,
    pub state: CircuitState,
    pub timeout: std::time::Duration,
}

impl CircuitBreaker {
    pub fn call<F, T, E>(&mut self, action: F) -> Result<T, &'static str>
    where
        F: FnOnce() -> Result<T, E>,
    {
        match self.state {
            CircuitState::Open { opened_at } => {
                if opened_at.elapsed() > self.timeout {
                    self.state = CircuitState::HalfOpen;
                } else {
                    return Err("Circuit breaker is OPEN (fast-fail)");
                }
            }
            _ => {}
        }

        match action() {
            Ok(val) => {
                self.failure_count = 0;
                self.state = CircuitState::Closed;
                Ok(val)
            }
            Err(_) => {
                self.failure_count += 1;
                if self.failure_count >= self.failure_threshold {
                    self.state = CircuitState::Open {
                        opened_at: std::time::Instant::now(),
                    };
                }
                Err("Downstream invocation failed")
            }
        }
    }
}""",
            "typescript": """type CircuitState = 'CLOSED' | 'OPEN' | 'HALF_OPEN';

export class CircuitBreaker {
    private state: CircuitState = 'CLOSED';
    private failureCount = 0;
    private nextAttempt = 0;

    constructor(
        private threshold = 3,
        private resetTimeoutMs = 5000
    ) {}

    async execute<T>(action: () => Promise<T>, fallback: () => T): Promise<T> {
        if (this.state === 'OPEN') {
            if (Date.now() > this.nextAttempt) {
                this.state = 'HALF_OPEN';
            } else {
                return fallback(); // Fast-fail fallback
            }
        }

        try {
            const result = await action();
            this.state = 'CLOSED';
            this.failureCount = 0;
            return result;
        } catch (err) {
            this.failureCount++;
            if (this.failureCount >= this.threshold || this.state === 'HALF_OPEN') {
                this.state = 'OPEN';
                this.nextAttempt = Date.now() + this.resetTimeoutMs;
            }
            return fallback();
        }
    }
}""",
            "go": """package main

import (
    "errors"
    "sync"
    "time"
)

type State int

const (
    StateClosed State = iota
    StateOpen
    StateHalfOpen
)

type CircuitBreaker struct {
    mu           sync.Mutex
    state        State
    failures     int
    threshold    int
    timeout      time.Duration
    lastTripTime time.Time
}

func (cb *CircuitBreaker) Execute(op func() error) error {
    cb.mu.Lock()
    if cb.state == StateOpen {
        if time.Since(cb.lastTripTime) > cb.timeout {
            cb.state = StateHalfOpen
        } else {
            cb.mu.Unlock()
            return errors.New("circuit breaker is OPEN")
        }
    }
    cb.mu.Unlock()

    err := op()

    cb.mu.Lock()
    defer cb.mu.Unlock()
    if err != nil {
        cb.failures++
        if cb.failures >= cb.threshold {
            cb.state = StateOpen
            cb.lastTripTime = time.Now()
        }
        return err
    }

    cb.failures = 0
    cb.state = StateClosed
    return nil
}"""
        }
    ),
    ArchitecturePattern(
        id="worker_pool",
        name="Worker Pool / Fan-Out Fan-In",
        category="Concurrency & Scaling",
        summary="Distributes incoming concurrent workloads across a bounded set of reusable workers.",
        problem="Uncontrolled concurrency spawns millions of threads, leading to OOM crashes and resource exhaustion.",
        solution="Buffer tasks in a thread-safe work queue; worker pool dequeues and processes tasks with backpressure.",
        nodes=[
            PatternGraphNode("dispatcher", "Task Dispatcher", "Producer", "active", 50, 150),
            PatternGraphNode("queue", "Job Channel / Queue", "Buffer", "idle", 180, 150),
            PatternGraphNode("w1", "Worker #1", "Consumer", "idle", 320, 80),
            PatternGraphNode("w2", "Worker #2", "Consumer", "idle", 320, 150),
            PatternGraphNode("w3", "Worker #3", "Consumer", "idle", 320, 220),
            PatternGraphNode("sink", "Result Collector", "Fan-In", "idle", 460, 150),
        ],
        edges=[
            PatternGraphEdge("dispatcher", "queue", "Enqueue Task"),
            PatternGraphEdge("queue", "w1", "Dispatch"),
            PatternGraphEdge("queue", "w2", "Dispatch"),
            PatternGraphEdge("queue", "w3", "Dispatch"),
            PatternGraphEdge("w1", "sink", "Emit Result"),
            PatternGraphEdge("w2", "sink", "Emit Result"),
            PatternGraphEdge("w3", "sink", "Emit Result"),
        ],
        code_implementations={
            "go": """package main

import (
    "fmt"
    "sync"
)

func worker(id int, jobs <-chan int, results chan<- int, wg *sync.WaitGroup) {
    defer wg.Done()
    for j := range jobs {
        results <- j * 2 // Process job
    }
}

func main() {
    const numJobs = 10
    const numWorkers = 3

    jobs := make(chan int, numJobs)
    results := make(chan int, numJobs)
    var wg sync.WaitGroup

    // Spawn bounded worker pool
    for w := 1; w <= numWorkers; w++ {
        wg.Add(1)
        go worker(w, jobs, results, &wg)
    }

    // Fan-out: send jobs
    for j := 1; j <= numJobs; j++ {
        jobs <- j
    }
    close(jobs)

    wg.Wait()
    close(results)

    // Fan-in: collect results
    for r := range results {
        fmt.Println("[WorkerPool Result]", r)
    }
}""",
            "rust": """use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (task_tx, mut task_rx) = mpsc::channel::<u32>(100);
    let (res_tx, mut res_rx) = mpsc::channel::<u32>(100);

    // Spawn 3 workers
    for id in 1..=3 {
        let mut rx = task_tx.clone(); // Note: use Arc<Mutex> or multi-consumer channel
        let tx = res_tx.clone();
        tokio::spawn(async move {
            // Process jobs
        });
    }
}"""
        }
    )
]
