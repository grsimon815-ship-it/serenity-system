from dataclasses import dataclass
from typing import Dict, List

@dataclass
class ParadigmSnippet:
    code: str
    explanation: str
    complexity: str
    key_points: List[str]

@dataclass
class ParadigmTopic:
    id: str
    title: str
    subtitle: str
    deep_theory: str
    tradeoffs_pros: List[str]
    tradeoffs_cons: List[str]
    best_use_case: str
    snippets: Dict[str, ParadigmSnippet]

PARADIGM_TOPICS: List[ParadigmTopic] = [
    ParadigmTopic(
        id="concurrency_models",
        title="Concurrency & Asynchronous Execution",
        subtitle="CSP vs Zero-Cost Futures vs Event Loop vs Virtual Threads",
        deep_theory=(
            "Modern high-level concurrency resolves how compute resources manage IO-bound waiting "
            "and CPU-bound parallelism without unbounded OS thread exhaustion.\n\n"
            "• CSP (Go): Goroutines (starting at ~2KB resizable stack) multiplexed onto OS threads, "
            "communicating over synchronized, typed channels.\n"
            "• Zero-Cost Futures (Rust): Async blocks compiled into state machine structs with zero heap overhead, "
            "driven cooperatively by an executor like Tokio.\n"
            "• Event Loop (TypeScript/Node): Single execution thread driven by non-blocking IO demultiplexing "
            "and a prioritized microtask/macrotask queue.\n"
            "• Virtual Threads (Java Loom): Continuation-stealing userland fibers mounted/unmounted "
            "from carrier thread pools upon blocking operations."
        ),
        tradeoffs_pros=[
            "Supports 100k+ concurrent connections with minimal memory footprint",
            "Eliminates deadlocks via message-passing channels and actor isolation",
            "High CPU core saturation during heavy network or file IO"
        ],
        tradeoffs_cons=[
            "Risk of event loop or carrier thread starvation from blocking CPU loops",
            "Function coloring problem (async/await propagation across interfaces)",
            "Stack traces across asynchronous continuations require specialized tooling"
        ],
        best_use_case="Microservice gateways, high-throughput WebSockets, distributed RPC pipelines.",
        snippets={
            "rust": ParadigmSnippet(
                code="""use tokio::sync::mpsc;
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    let (tx, mut rx) = mpsc::channel(32);

    for id in 1..=3 {
        let producer = tx.clone();
        tokio::spawn(async move {
            sleep(Duration::from_millis(id * 40)).await;
            producer.send(format!("Rust task #{} done", id)).await.ok();
        });
    }
    drop(tx); // drop main sender so rx terminates

    while let Some(msg) = rx.recv().await {
        println!("[Rust Async] {}", msg);
    }
}""",
                explanation="Rust futures are passive state machines compiled without heap allocations. Polled via Send/Sync safe executors.",
                complexity="O(1) allocation per task, M:N work-stealing scheduler",
                key_points=["Zero-cost state machine", "Send/Sync safety", "MPSC channel", "Work stealing"]
            ),
            "go": ParadigmSnippet(
                code="""package main

import (
    "fmt"
    "sync"
    "time"
)

func main() {
    ch := make(chan string, 3)
    var wg sync.WaitGroup

    for i := 1; i <= 3; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            time.Sleep(time.Duration(id*40) * time.Millisecond)
            ch <- fmt.Sprintf("Go goroutine #%d done", id)
        }(i)
    }

    go func() {
        wg.Wait()
        close(ch)
    }()

    for msg := range ch {
        fmt.Println("[Go CSP]", msg)
    }
}""",
                explanation="Goroutines are scheduled cooperatively and preemptively by the Go runtime (M:P:G model) with 2KB initial stacks.",
                complexity="O(1) scheduling overhead, channels serve as synchronization primitives",
                key_points=["CSP paradigm", "Segmented/growable stack", "Typed channels", "WaitGroup sync"]
            ),
            "typescript": ParadigmSnippet(
                code="""// Node.js / TypeScript Event Loop Concurrency
async function runTasks() {
    const ids = [1, 2, 3];
    const promises = ids.map(async (id) => {
        await new Promise((resolve) => setTimeout(resolve, id * 40));
        return `TypeScript worker #${id} done`;
    });

    const results = await Promise.all(promises);
    results.forEach((msg) => console.log(`[TS EventLoop] ${msg}`));
}

runTasks();""",
                explanation="Node.js executes JavaScript on a single thread using libuv's reactor pattern. Promises resolve in microtask checkpoints.",
                complexity="O(1) thread overhead, non-blocking I/O event multiplexer",
                key_points=["Single thread reactor", "Promise.all batching", "Microtask queue priority"]
            ),
            "python": ParadigmSnippet(
                code="""import asyncio

async def worker(task_id: int) -> str:
    await asyncio.sleep(task_id * 0.04)
    return f"Python async task #{task_id} done"

async def main():
    tasks = [worker(i) for i in range(1, 4)]
    results = await asyncio.gather(*tasks)
    for res in results:
        print(f"[Python Asyncio] {res}")

if __name__ == "__main__":
    asyncio.run(main())""",
                explanation="Python's asyncio runs a cooperative single-threaded loop, switching execution at await boundaries.",
                complexity="O(N) task structs on heap, single OS thread",
                key_points=["Cooperative multitasking", "asyncio.gather", "Non-blocking event loop"]
            ),
            "java": ParadigmSnippet(
                code="""import java.util.concurrent.Executors;
import java.util.stream.IntStream;

public class VirtualThreadDemo {
    public static void main(String[] args) throws Exception {
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            var futures = IntStream.rangeClosed(1, 3).mapToObj(id ->
                executor.submit(() -> {
                    Thread.sleep(id * 40);
                    return "Java Loom fiber #" + id + " done";
                })
            ).toList();

            for (var f : futures) {
                System.out.println("[Java Loom] " + f.get());
            }
        }
    }
}""",
                explanation="Java 21 Project Loom mounts userland virtual threads onto ForkJoin carrier threads, decoupling concurrency from OS limits.",
                complexity="Sub-kilobyte heap allocation per virtual thread",
                key_points=["Project Loom", "Carrier thread unmounting", "Structured concurrency"]
            ),
            "cpp": ParadigmSnippet(
                code="""#include <iostream>
#include <vector>
#include <future>
#include <chrono>

int main() {
    std::vector<std::future<std::string>> tasks;

    for (int i = 1; i <= 3; ++i) {
        tasks.push_back(std::async(std::launch::async, [i]() {
            std::this_thread::sleep_for(std::chrono::milliseconds(i * 40));
            return "C++ async task #" + std::to_string(i) + " done";
        }));
    }

    for (auto& t : tasks) {
        std::cout << "[C++ Future] " << t.get() << std::endl;
    }
    return 0;
}""",
                explanation="C++ standard library std::async provides future-based asynchronous task execution without managed runtime baggage.",
                complexity="Direct OS thread per std::launch::async task",
                key_points=["std::future/promise", "Zero runtime overhead", "Deterministic thread joining"]
            )
        }
    ),
    ParadigmTopic(
        id="memory_safety_ownership",
        title="Memory Safety & Lifetime Governance",
        subtitle="Affine Borrow Checker vs Tracing GC vs RAII Smart Pointers",
        deep_theory=(
            "Memory safety determines how memory allocations are created, tracked, and released.\n\n"
            "• Rust enforces affine types where a value has exactly one owner at any time. "
            "Borrowing guarantees aliasing XOR mutability at compile time, eliminating both GC overhead and data races.\n"
            "• C++ uses RAII (Resource Acquisition Is Initialization) with std::unique_ptr for exclusive ownership "
            "and std::shared_ptr for atomic reference counting.\n"
            "• Go & Java use concurrent tracing garbage collectors that detect live objects from root sets and reclaim unreachable memory.\n"
            "• Python uses reference counting backed by a tri-generational cycle detector."
        ),
        tradeoffs_pros=[
            "Zero use-after-free, double-free, and dangling pointer vulnerabilities",
            "Deterministic deallocation delivers consistent sub-millisecond latencies",
            "Cache locality optimization via contiguous stack and inline value layout"
        ],
        tradeoffs_cons=[
            "Strict borrow checker rules increase initial developer cognitive load",
            "Tracing GCs may induce periodic latency jitter or memory amplification",
            "Shared ownership and circular references require explicit weak pointer design"
        ],
        best_use_case="Operating system kernels, browser engines, financial trading, high-reliability backend services.",
        snippets={
            "rust": ParadigmSnippet(
                code="""struct FrameBuffer {
    bytes: Vec<u8>,
}

fn analyze_immutable(fb: &FrameBuffer) {
    println!("Shared read buffer size: {} bytes", fb.bytes.len());
}

fn mutate_exclusive(fb: &mut FrameBuffer) {
    fb.bytes.push(0xAB);
}

fn main() {
    let mut buffer = FrameBuffer { bytes: vec![1, 2, 3] };
    analyze_immutable(&buffer);  // shared borrow &T
    mutate_exclusive(&mut buffer); // exclusive borrow &mut T

    let moved_buffer = buffer;   // move ownership
    // buffer is now invalidated at compile time!
    println!("Final owner byte count: {}", moved_buffer.bytes.len());
}""",
                explanation="Rust verifies the Single Owner rule and Borrow Checker constraints entirely at compile time.",
                complexity="Zero runtime CPU overhead, zero allocation overhead",
                key_points=["Compile-time affine types", "Borrow checker (& / &mut)", "Deterministic drop glue"]
            ),
            "cpp": ParadigmSnippet(
                code="""#include <iostream>
#include <memory>
#include <vector>

struct Buffer {
    std::vector<uint8_t> data;
    Buffer(size_t sz) : data(sz, 0) {
        std::cout << "Buffer allocated\\n";
    }
    ~Buffer() {
        std::cout << "Buffer destroyed (RAII deterministic)\\n";
    }
};

int main() {
    auto p1 = std::make_unique<Buffer>(1024);
    
    // Explicit ownership transfer via move semantics
    std::unique_ptr<Buffer> p2 = std::move(p1);
    
    if (!p1) {
        std::cout << "p1 was nulled; p2 holds ownership\\n";
    }
    // When p2 leaves scope, destructor frees buffer memory instantly!
    return 0;
}""",
                explanation="C++ RAII pairs object initialization with stack destruction. std::unique_ptr provides exclusive ownership without overhead.",
                complexity="O(1) deallocation, zero pointer indirection overhead",
                key_points=["RAII idiom", "std::unique_ptr", "std::move semantics", "Deterministic cleanup"]
            ),
            "go": ParadigmSnippet(
                code="""package main

import "fmt"

type DataBlock struct {
    Payload []byte
}

func allocateBlock() *DataBlock {
    // Escape analysis determines if block escapes to heap
    b := DataBlock{Payload: make([]byte, 512)}
    return &b // Escapes stack because pointer is returned
}

func main() {
    block := allocateBlock()
    fmt.Printf("[Go GC] Allocated block with %d bytes\\n", len(block.Payload))
    // Reclaimed concurrently by Tri-color Mark-Sweep GC
}""",
                explanation="Go's escape analysis puts local variables on the stack unless their lifetime escapes the function frame.",
                complexity="Concurrent GC with sub-millisecond stop-the-world pauses",
                key_points=["Escape analysis", "Tri-color GC", "Write barrier", "Automatic heap recovery"]
            ),
            "typescript": ParadigmSnippet(
                code="""class SessionContext {
    constructor(public id: string, public createdAt: number) {}
}

function processSession() {
    // Allocated in V8 Nursery (New Space)
    const session = new SessionContext("sess_42", Date.now());
    return session.id;
    // session becomes unreachable and is collected in Minor GC (Scavenge)
}

const activeIds = processSession();
console.log(`[V8 Engine] Handled session: ${activeIds}`);""",
                explanation="V8 organizes memory into Generational spaces: Young Generation (fast semi-space scavenge) and Old Generation (mark-sweep-compact).",
                complexity="Minor GC runs in single-digit milliseconds",
                key_points=["Generational hypothesis", "Scavenger copy", "Mark-compact old space"]
            ),
            "python": ParadigmSnippet(
                code="""import sys
import gc

class Entity:
    def __init__(self, name: str):
        self.name = name
        self.link = None

a = Entity("Alpha")
b = Entity("Beta")
a.link = b
b.link = a  # Circular reference cycle

del a
del b
# Refcount cannot deallocate cyclic loop; cyclic GC collects it
swept = gc.collect()
print(f"[Python GC] Cyclic garbage sweep collected {swept} objects")""",
                explanation="CPython combines immediate Reference Counting with a generational cyclic garbage collector for unreferenced cycles.",
                complexity="O(1) immediate cleanup for acyclic; periodic cycle detection",
                key_points=["Reference count PyObject", "Generational cyclic collector", "Weak references"]
            ),
            "java": ParadigmSnippet(
                code="""import java.lang.ref.WeakReference;

public class MemoryCollectorDemo {
    static class CacheEntry {
        byte[] buffer = new byte[64 * 1024];
    }

    public static void main(String[] args) {
        CacheEntry entry = new CacheEntry();
        WeakReference<CacheEntry> weakRef = new WeakReference<>(entry);

        System.out.println("Object accessible: " + (weakRef.get() != null));
        entry = null; // Clear strong reference

        System.gc(); // Suggest collection
        System.out.println("After GC, weak ref cleared: " + (weakRef.get() == null));
    }
}""",
                explanation="The HotSpot JVM supports advanced collectors (G1GC, ZGC) that leverage colored pointers and load barriers for concurrent compaction.",
                complexity="ZGC maintains max pause times below 1ms regardless of heap size",
                key_points=["ZGC / G1GC", "Colored pointers", "Load barriers", "WeakReference semantics"]
            )
        }
    ),
    ParadigmTopic(
        id="algebraic_types_error_handling",
        title="Algebraic Data Types & Error Modeling",
        subtitle="Monadic Result/Option vs Discriminated Unions vs Multiple Return Values",
        deep_theory=(
            "Type-directed error handling models software states without unchecked runtime crashes.\n\n"
            "• Sum Types / Enums with Payloads (Rust): Result<T, E> and Option<T> encode success and failure "
            "directly into the return signature. Non-exhaustive matches trigger compile-time errors.\n"
            "• Discriminated Unions (TypeScript): Tagged unions combined with control-flow narrowing allow "
            "exhaustive type matching without class inheritance.\n"
            "• Multiple Return Values (Go): Explicit (value, error) pairs with error wrapping and unwrapping.\n"
            "• Sealed Classes / Record Matching (Java): Sealed hierarchies ensure closed sets of subtype variants."
        ),
        tradeoffs_pros=[
            "Eliminates null-pointer dereferences and untyped runtime panics",
            "Self-documenting functional API contracts in method signatures",
            "Predictable execution paths without the overhead of exception unwinding"
        ],
        tradeoffs_cons=[
            "Requires explicit error propagation syntax across call stacks",
            "Pattern matching boilerplate for deeply nested data structures",
            "Translating legacy untyped exceptions into typed sum-type errors"
        ],
        best_use_case="Domain-driven architectures, financial logic, compilers, protocol parsers.",
        snippets={
            "rust": ParadigmSnippet(
                code="""#[derive(Debug)]
enum TransactionError {
    InsufficientFunds { needed: f64, available: f64 },
    AccountSuspended,
    InvalidCurrency,
}

type TxResult<T> = Result<T, TransactionError>;

fn transfer(amount: f64, balance: f64) -> TxResult<f64> {
    if amount <= 0.0 {
        return Err(TransactionError::InvalidCurrency);
    }
    if amount > balance {
        return Err(TransactionError::InsufficientFunds {
            needed: amount,
            available: balance,
        });
    }
    Ok(balance - amount)
}

fn main() {
    match transfer(250.0, 100.0) {
        Ok(new_bal) => println!("Success, remaining: ${:.2}", new_bal),
        Err(TransactionError::InsufficientFunds { needed, available }) => {
            println!("Declined: needed ${:.2}, available ${:.2}", needed, available);
        }
        Err(e) => println!("Transaction failed: {:?}", e),
    }
}""",
                explanation="Rust enums are tagged unions that can carry varied typed payloads with zero heap allocation overhead.",
                complexity="Tagged union stored in registers or single stack frame",
                key_points=["Result<T, E> enum", "Exhaustive pattern matching", "Zero-cost tagged union", "? error operator"]
            ),
            "typescript": ParadigmSnippet(
                code="""// Discriminated / Tagged Union Pattern
type TransactionOutcome =
  | { status: 'success'; newBalance: number; txHash: string }
  | { status: 'insufficient_funds'; deficit: number }
  | { status: 'forbidden'; reason: string };

function processTransfer(amount: number, balance: number): TransactionOutcome {
    if (amount > balance) {
        return { status: 'insufficient_funds', deficit: amount - balance };
    }
    return { status: 'success', newBalance: balance - amount, txHash: '0x9fa1c' };
}

const outcome = processTransfer(500, 200);

switch (outcome.status) {
    case 'success':
        console.log(`Success! New balance: $${outcome.newBalance}`);
        break;
    case 'insufficient_funds':
        console.warn(`Failed: missing $${outcome.deficit}`);
        break;
    case 'forbidden':
        console.error(`Blocked: ${outcome.reason}`);
        break;
}""",
                explanation="TypeScript uses string literal tags to refine types in switch statements through control flow analysis.",
                complexity="Zero runtime code generated; erased upon compilation",
                key_points=["Discriminated unions", "Type narrowing", "Never exhaustive check", "Literal types"]
            ),
            "go": ParadigmSnippet(
                code="""package main

import (
    "errors"
    "fmt"
)

var ErrInsufficientFunds = errors.New("insufficient balance")

func ExecuteTransfer(amount, balance float64) (float64, error) {
    if amount > balance {
        return 0, fmt.Errorf("transfer declined: %w", ErrInsufficientFunds)
    }
    return balance - amount, nil
}

func main() {
    newBal, err := ExecuteTransfer(300, 100)
    if err != nil {
        if errors.Is(err, ErrInsufficientFunds) {
            fmt.Println("[Go] Handled specific error:", err)
            return
        }
        fmt.Println("[Go] Unexpected error:", err)
        return
    }
    fmt.Printf("[Go] New Balance: $%.2f\\n", newBal)
}""",
                explanation="Go returns errors as regular values. Error wrapping (%w) preserves call context for errors.Is inspection.",
                complexity="Multiple register returns, zero stack unwind overhead",
                key_points=["Explicit return tuples", "Error wrapping with %w", "errors.Is Sentinel matching"]
            ),
            "python": ParadigmSnippet(
                code="""from dataclasses import dataclass
from typing import Union

@dataclass
class TxApproved:
    balance: float
    receipt: str

@dataclass
class TxDeclined:
    code: int
    reason: str

TxState = Union[TxApproved, TxDeclined]

def evaluate(amount: float, balance: float) -> TxState:
    if amount > balance:
        return TxDeclined(402, "Insufficient capital")
    return TxApproved(balance - amount, "REC-8841")

state = evaluate(150, 50)
match state:
    case TxApproved(bal, r):
        print(f"[Python 3.14] Approved with receipt {r}, balance: ${bal}")
    case TxDeclined(code, reason):
        print(f"[Python 3.14] Declined ({code}): {reason}")""",
                explanation="Python 3.10+ structural pattern matching (PEP 634) unpacks dataclass properties cleanly in match statements.",
                complexity="Dynamic type verification, optimized via bytecode opcodes",
                key_points=["Dataclasses as variants", "match/case PEP 634", "Union type hints"]
            ),
            "java": ParadigmSnippet(
                code="""public class SealedResultDemo {
    sealed interface TxOutcome permits Approved, Declined {}

    record Approved(double balance, String txId) implements TxOutcome {}
    record Declined(String message, int errorCode) implements TxOutcome {}

    static void handle(TxOutcome outcome) {
        String info = switch (outcome) {
            case Approved(var bal, var id) -> "Tx " + id + " approved! Balance: $" + bal;
            case Declined(var msg, var code) -> "Declined [" + code + "]: " + msg;
        };
        System.out.println("[Java 21+] " + info);
    }

    public static void main(String[] args) {
        handle(new Declined("Card limit exceeded", 403));
    }
}""",
                explanation="Java 21 sealed interfaces restrict implementers. Switch pattern matching checks completeness at compile time.",
                complexity="Constant-time switch jump, JVM record deconstruction",
                key_points=["Sealed interfaces", "Record patterns", "Exhaustive switch", "Compile-time enforcement"]
            ),
            "cpp": ParadigmSnippet(
                code="""#include <iostream>
#include <variant>
#include <string>

struct Approved { double newBalance; };
struct Declined { std::string reason; };

using Result = std::variant<Approved, Declined>;

template<class... Ts> struct overloaded : Ts... { using Ts::operator()...; };

int main() {
    Result res = Declined{"Exceeded daily threshold"};

    std::visit(overloaded{
        [](const Approved& ok) { std::cout << "Approved: $" << ok.newBalance << std::endl; },
        [](const Declined& fail) { std::cout << "Declined: " << fail.reason << std::endl; }
    }, res);

    return 0;
}""",
                explanation="C++17 std::variant provides type-safe sum types without heap allocations, visited with template lambdas.",
                complexity="Size equal to largest variant + discriminator byte",
                key_points=["std::variant", "std::visit", "Overloaded visitor", "Zero heap usage"]
            )
        }
    )
]
