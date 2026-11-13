import { ParadigmTopic } from '../types';

export const PARADIGMS: ParadigmTopic[] = [
  {
    id: 'concurrency-asynchrony',
    title: 'Concurrency & Asynchronous Runtimes',
    category: 'concurrency',
    tagline: 'Goroutines vs Tokio Futures vs Event Loop vs Virtual Threads vs Actors',
    theoreticalCore: `How execution threads are scheduled and synchronized fundamentally dictates memory consumption, latency, and throughput under heavy I/O and CPU loads.

1. CSP (Communicating Sequential Processes): Light green-threads communicating via first-class typed channels without shared memory (Go).
2. Zero-cost Cooperative Futures: Poll-based state-machine generation compiled without heap allocations unless boxed (Rust Tokio).
3. Reactor / Event Loop: Single-threaded cooperative multiplexing via epoll/kqueue/IOCP and non-blocking microtask queues (Node.js / JS).
4. M:N Virtual Threads: Continuation-stealing fiber runtimes hosted atop kernel carrier threads (Java 21+ Project Loom).
5. Share-Nothing Actor Model: Preemptively scheduled lightweight processes with isolated heaps and asynchronous mailboxes (Elixir/Erlang BEAM).`,
    architecturalTradeoffs: {
      pros: [
        'Massive concurrent connections (100k+ sockets) without kernel stack overhead',
        'Elimination of raw mutex deadlock scenarios through channels or actor mailboxes',
        'Predictable tail latency when non-blocking I/O is strictly enforced'
      ],
      cons: [
        'Hidden CPU starvation if long-running synchronous work blocks worker threads',
        'Coloring of functions (async/await viral boundary in TS, Python, Rust)',
        'Complex stack traces across asynchronous continuation boundaries'
      ],
      bestFor: 'High-throughput microservices, real-time message routers, and distributed RPC gateways.'
    },
    implementations: {
      rust: {
        language: 'rust',
        code: `use tokio::sync::mpsc;
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    // Rust: Zero-cost futures compiled to state machines.
    // Fearless concurrency guaranteed by Send + Sync trait boundaries!
    let (tx, mut rx) = mpsc::channel::<String>(32);

    for worker_id in 0..3 {
        let worker_tx = tx.clone();
        tokio::spawn(async move {
            sleep(Duration::from_millis(50 * (worker_id + 1))).await;
            let msg = format!("Worker #{} completed task", worker_id);
            worker_tx.send(msg).await.unwrap();
        });
    }
    drop(tx); // Close original transmitter to allow iterator termination

    while let Some(result) = rx.recv().await {
        println!("[Rust Tokio] Received: {}", result);
    }
}`,
        explanation: 'Rust transforms async blocks into zero-cost stack-allocated state machines at compile time. Memory safety is checked via Send and Sync traits.',
        complexity: 'O(1) allocation per task, M:N work-stealing scheduler',
        runtimeMechanics: 'Tokio runtime manages worker OS threads; futures are driven by poll() calls triggered by Waker notifications.',
        keyConcepts: ['Future state-machines', 'Send/Sync bounds', 'MPSC channels', 'Work-stealing pool']
      },
      go: {
        language: 'go',
        code: `package main

import (
	"fmt"
	"sync"
	"time"
)

// Go: CSP (Communicating Sequential Processes)
// "Do not communicate by sharing memory; instead, share memory by communicating."
func main() {
	ch := make(chan string, 3)
	var wg sync.WaitGroup

	for i := 1; i <= 3; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			time.Sleep(time.Duration(id*50) * time.Millisecond)
			ch <- fmt.Sprintf("Goroutine #%d done", id)
		}(i)
	}

	go func() {
		wg.Wait()
		close(ch)
	}()

	for msg := range ch {
		fmt.Printf("[Go CSP] Received: %s\\n", msg)
	}
}`,
        explanation: 'Go uses segmented/resizable stacks starting at only 2KB per goroutine, orchestrated by the M:P:G cooperative/preemptive scheduler.',
        complexity: 'O(1) goroutine creation overhead, 2KB initial stack',
        runtimeMechanics: 'Go runtime schedules G (goroutines) across M (OS threads) mediated by P (logical processors).',
        keyConcepts: ['CSP paradigm', 'Goroutines', 'Buffered channels', 'WaitGroup synchronization']
      },
      typescript: {
        language: 'typescript',
        code: `// TypeScript / JavaScript: Single-Threaded Event Loop with Microtasks
async function runConcurrentPipeline() {
  const tasks = [1, 2, 3].map(async (id) => {
    await new Promise((resolve) => setTimeout(resolve, id * 50));
    return \`Promise Worker #\${id} resolved\`;
  });

  // Concurrently settle all promises via Promise.all
  const results = await Promise.all(tasks);
  
  for (const res of results) {
    console.log(\`[TS EventLoop] \${res}\`);
  }
}

runConcurrentPipeline();`,
        explanation: 'V8 uses a single execution thread with an epoll-backed event loop (libuv). Asynchronous operations register callbacks in macrotask and microtask queues.',
        complexity: 'O(1) call stack allocation, non-blocking I/O event demultiplexing',
        runtimeMechanics: 'Microtask queue (Promises, queueMicrotask) empties completely after each macrotask tick (timers, I/O).',
        keyConcepts: ['Event Loop', 'Microtask queue', 'Promise.all concurrency', 'libuv reactor']
      },
      python: {
        language: 'python',
        code: `import asyncio

async def worker(worker_id: int) -> str:
    # Cooperative multitasking via asyncio event loop
    await asyncio.sleep(worker_id * 0.05)
    return f"Asyncio Task #{worker_id} completed"

async def main():
    # Gather creates concurrent tasks scheduled on current loop
    tasks = [worker(i) for i in range(1, 4)]
    results = await asyncio.gather(*tasks)
    
    for item in results:
        print(f"[Python Asyncio] {item}")

if __name__ == "__main__":
    asyncio.run(main())`,
        explanation: 'Python asyncio provides a single-threaded cooperative event loop using generator-based coroutines and async/await syntax.',
        complexity: 'Cooperative single thread, I/O bound concurrency',
        runtimeMechanics: 'Event loop runs tasks sequentially until an "await" suspends the frame and yields control back to the selector.',
        keyConcepts: ['Coroutines', 'asyncio event loop', 'Task gathering', 'Yielding execution']
      },
      java: {
        language: 'java',
        code: `import java.util.concurrent.Executors;
import java.util.List;
import java.util.stream.IntStream;

public class ConcurrencyDemo {
    public static void main(String[] args) throws Exception {
        // Java 21+ Project Loom: Lightweight Virtual Threads (Fibers)
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            var futures = IntStream.rangeClosed(1, 3).mapToObj(id -> 
                executor.submit(() -> {
                    Thread.sleep(id * 50);
                    return "VirtualThread #" + id + " completed";
                })
            ).toList();

            for (var f : futures) {
                System.out.println("[Java Loom] " + f.get());
            }
        }
    }
}`,
        explanation: 'Project Loom decouples Java threads from OS kernel threads. Virtual threads park when performing blocking I/O, freeing the underlying carrier thread.',
        complexity: 'Millions of threads, few hundred bytes heap overhead each',
        runtimeMechanics: 'Continuation stacks are stored in JVM heap and mounted/unmounted onto ForkJoinPool carrier OS threads.',
        keyConcepts: ['Virtual Threads', 'Structured Concurrency', 'Carrier Threads', 'Project Loom']
      },
      cpp: {
        language: 'cpp',
        code: `#include <iostream>
#include <vector>
#include <future>
#include <chrono>

int main() {
    // C++ std::async with futures
    std::vector<std::future<std::string>> futures;

    for (int i = 1; i <= 3; ++i) {
        futures.push_back(std::async(std::launch::async, [i]() {
            std::this_thread::sleep_for(std::chrono::milliseconds(i * 50));
            return "C++ std::async #" + std::to_string(i) + " finished";
        }));
    }

    for (auto& fut : futures) {
        std::cout << "[C++ Future] " << fut.get() << std::endl;
    }
    return 0;
}`,
        explanation: 'C++ std::async launches tasks either on OS threads or deferred pools, returning std::future with zero abstraction penalty.',
        complexity: 'OS Kernel Thread per std::launch::async by default',
        runtimeMechanics: 'Futures block on .get() or can be composed using modern C++20 coroutines (co_await, co_return).',
        keyConcepts: ['std::future & promise', 'std::jthread', 'Zero abstraction cost', 'C++20 Coroutines']
      },
      elixir: {
        language: 'elixir',
        code: `defmodule ConcurrencyDemo do
  # Elixir / Erlang OTP: Actor Model
  # Every process has its own isolated heap, GC, and mailbox
  def worker(id, parent) do
    :timer.sleep(id * 50)
    send(parent, {:done, "BEAM Process #\#{id} finished"})
  end

  def run do
    parent = self()
    for id <- 1..3 do
      spawn(fn -> worker(id, parent) end)
    end

    for _ <- 1..3 do
      receive do
        {:done, msg} -> IO.puts("[Elixir Actor] \#{msg}")
      end
    end
  end
end

ConcurrencyDemo.run()`,
        explanation: 'BEAM virtual machine runs millions of isolated actor processes with no shared mutable memory. Failures are isolated and supervised.',
        complexity: '300 words initial heap, per-process garbage collection',
        runtimeMechanics: 'Preemptive reduction-based scheduler switches processes after 2000 reductions/operations, preventing CPU monopolization.',
        keyConcepts: ['Actor model', 'Share-nothing architecture', 'BEAM reductions', 'Mailbox pattern matching']
      }
    }
  },
  {
    id: 'memory-ownership-lifetimes',
    title: 'Memory Management & Lifetimes',
    category: 'memory',
    tagline: 'Affine Borrow Checker vs Generational GC vs RAII Smart Pointers vs Cycle Collectors',
    theoreticalCore: `How languages guarantee spatial and temporal memory safety without sacrificing performance or ergonomics:

1. Compile-Time Affine Type System (Rust): Enforces strict single-ownership with aliasing XOR mutability guarantees at compile time. No runtime GC pause.
2. Tracing Generational Garbage Collection (Go, Java): Runtime periodically traverses live object graphs (Root set -> Heap) to sweep or compact unreferenced memory.
3. Reference Counting with Cycle Detectors (Python, Swift): Immediate deallocation on reference count hitting zero, supplemented by a heuristic cycle detector.
4. RAII & Deterministic Destructors (C++): Resource Acquisition Is Initialization binds heap allocations to stack-frame lifecycles (unique_ptr, shared_ptr).`,
    architecturalTradeoffs: {
      pros: [
        'Deterministic deallocation guarantees predictable latency profiles',
        'Zero use-after-free, double-free, and dangling pointer vulnerabilities',
        'Cache-friendly memory layouts when value types are stack-allocated'
      ],
      cons: [
        'Steep learning curve with borrow checker / lifetime annotations',
        'GC stop-the-world pauses in high-throughput low-latency pipelines',
        'Reference cycle leaks in naive refcount implementations'
      ],
      bestFor: 'Critical infrastructure, high-frequency trading, and memory-constrained embedded / cloud environments.'
    },
    implementations: {
      rust: {
        language: 'rust',
        code: `struct Packet {
    payload: Vec<u8>,
}

fn process_immutable(pkt: &Packet) {
    // Borrowed immutably: &Packet (Shared reference)
    // Multiple readers allowed simultaneously!
    println!("Inspecting packet size: {} bytes", pkt.payload.len());
}

fn process_mutable(pkt: &mut Packet) {
    // Borrowed mutably: &mut Packet (Exclusive reference)
    // Guaranteed by compiler: NO other references exist!
    pkt.payload.push(0xFF);
}

fn main() {
    let mut data = Packet { payload: vec![1, 2, 3] };
    
    process_immutable(&data);
    process_mutable(&mut data);
    
    // Move semantics: ownership is transferred, 'data' is invalidated
    let moved_data = data;
    // println!("{:?}", data); // COMPILE ERROR: value used here after move!
    
    println!("Final ownership in moved_data: {} bytes", moved_data.payload.len());
}`,
        explanation: 'Rust enforces the Aliasing XOR Mutability rule at compile time: you can have either many shared references (&T) OR exactly one mutable reference (&mut T), never both.',
        complexity: 'O(0) runtime cost, 100% compile-time verification',
        runtimeMechanics: 'Compiler inserts Drop::drop glue at the exact scope boundary where an owner variable falls out of scope.',
        keyConcepts: ['Affine types', 'Ownership transfer', 'Borrowing (& / &mut)', 'Drop glue']
      },
      cpp: {
        language: 'cpp',
        code: `#include <iostream>
#include <memory>
#include <vector>

struct Resource {
    std::string name;
    Resource(std::string n) : name(std::move(n)) {
        std::cout << "Allocated: " << name << std::endl;
    }
    ~Resource() {
        std::cout << "Destroyed (RAII): " << name << std::endl;
    }
};

int main() {
    // RAII with std::unique_ptr (Exclusive ownership)
    auto res1 = std::make_unique<Resource>("Primary Buffer");
    
    // Ownership transfer via std::move
    std::unique_ptr<Resource> res2 = std::move(res1);
    
    // res1 is now nullptr; res2 holds ownership
    if (!res1) {
        std::cout << "res1 gave up ownership successfully" << std::endl;
    }
    
    // At end of scope, res2 destructor automatically frees memory!
    return 0;
}`,
        explanation: 'C++ utilizes RAII (Resource Acquisition Is Initialization). std::unique_ptr has zero runtime overhead compared to raw pointers and prevents memory leaks.',
        complexity: 'O(1) destruction, zero runtime indirection penalty',
        runtimeMechanics: 'Destructors run in reverse order of declaration when stack frames unwind (normal exit or exception).',
        keyConcepts: ['RAII', 'std::unique_ptr', 'std::move semantics', 'Zero-cost destructors']
      },
      go: {
        language: 'go',
        code: `package main

import "fmt"

type Buffer struct {
	Data []byte
}

// Escape Analysis determines whether buffer escapes to Heap
func createBuffer() *Buffer {
	// Stack allocated if it doesn't escape;
	// Escapes to heap because pointer is returned!
	buf := Buffer{Data: make([]byte, 1024)}
	return &buf
}

func main() {
	buf := createBuffer()
	fmt.Printf("[Go GC] Buffer allocated with %d bytes\\n", len(buf.Data))
	// Go runtime's concurrent Tri-color Mark-Sweep GC will sweep
	// buf automatically when it is no longer reachable from root sets.
}`,
        explanation: 'Go uses compile-time escape analysis: if a variable reference outlives its frame, it is allocated on the heap; otherwise, it remains on the ultra-fast stack.',
        complexity: 'Sub-millisecond stop-the-world pauses (P99 < 1ms)',
        runtimeMechanics: 'Concurrent tri-color mark and sweep algorithm runs in parallel with application mutator threads.',
        keyConcepts: ['Escape analysis', 'Tri-color Mark-Sweep', 'Write barrier', 'Root sets']
      },
      typescript: {
        language: 'typescript',
        code: `// TypeScript / V8 Memory Model: Generational GC
class Session {
  constructor(public id: string, public token: string) {}
}

function allocateShortLived() {
  // Allocated in V8 New Space (Nursery)
  const temp = new Session("temp-1", "jwt.token.abc");
  return temp.id;
} // temp becomes unreachable -> collected during Scavenge (Minor GC)

const longLivedCache = new Map<string, Session>();
// Survives multiple minor GCs -> Promoted to Old Space (Major GC / Mark-Compact)
longLivedCache.set("root", new Session("root", "jwt.token.root"));

console.log("[V8 GC] Active cache size:", longLivedCache.size);`,
        explanation: 'V8 partitions the heap into New Space (Nursery + Intermediate) and Old Space. Scavenge GC copies survivors quickly, while Old Space uses Mark-Sweep-Compact.',
        complexity: 'Minor GC: few ms, Major GC: incremental marking',
        runtimeMechanics: 'Weak references (WeakMap / WeakRef) allow objects to be collected when no strong references remain.',
        keyConcepts: ['Generational hypothesis', 'Scavenger GC', 'Old/New Space', 'WeakMap']
      },
      python: {
        language: 'python',
        code: `import sys
import gc

class Node:
    def __init__(self, name):
        self.name = name
        self.next = None

def demo_reference_counting():
    a = Node("Node A")
    # Reference count increments
    print(f"[Python] Refcount of a: {sys.getrefcount(a) - 1}")
    
    b = Node("Node B")
    # Create circular reference
    a.next = b
    b.next = a
    
    # Delete local names
    del a
    del b
    # Immediate refcount fails to collect cyclic graph!
    # Generational cycle detector sweeps unreachable cycles:
    collected = gc.collect()
    print(f"[Python GC] Cyclic garbage collected: {collected} objects")

demo_reference_counting()`,
        explanation: 'CPython relies primarily on immediate Reference Counting (Py_INCREF/Py_DECREF) combined with a tri-generational cyclic garbage collector.',
        complexity: 'Immediate deallocation for acyclic, O(N) periodic cycle sweep',
        runtimeMechanics: 'gc module tracks container objects (lists, dicts, custom classes) in 3 generations based on allocation survival count.',
        keyConcepts: ['Reference counting', 'Cyclic GC', 'PyObject header', 'Generation 0/1/2']
      },
      java: {
        language: 'java',
        code: `import java.lang.ref.WeakReference;

public class MemoryDemo {
    static class HeavyPayload {
        byte[] buffer = new byte[1024 * 1024]; // 1MB
    }

    public static void main(String[] args) {
        HeavyPayload strongRef = new HeavyPayload();
        WeakReference<HeavyPayload> weakRef = new WeakReference<>(strongRef);

        System.out.println("WeakRef points to object: " + (weakRef.get() != null));

        // Dereference strong pointer
        strongRef = null;

        // Hint JVM Garbage Collector (G1 / ZGC)
        System.gc();

        // Object collected since only weak reference remains
        System.out.println("After GC, WeakRef is cleared: " + (weakRef.get() == null));
    }
}`,
        explanation: 'Modern JVMs offer state-of-the-art garbage collectors like ZGC and Shenandoah with sub-millisecond pauses, using colored pointers and load barriers.',
        complexity: 'ZGC max pause < 1ms regardless of heap size (up to 16TB)',
        runtimeMechanics: 'Concurrent marking and compacting runs concurrently with Java application threads using load barriers.',
        keyConcepts: ['ZGC / G1GC', 'Colored pointers', 'Load barriers', 'Weak/Soft references']
      },
      elixir: {
        language: 'elixir',
        code: `defmodule MemoryDemo do
  # In Erlang / Elixir BEAM:
  # Every process has its own private heap.
  # When a process terminates, its ENTIRE heap is reclaimed instantly!
  def run do
    pid = spawn(fn ->
      # Large binary > 64 bytes is allocated in shared Refc Binary Heap
      large_bin = :crypto.strong_rand_bytes(100_000)
      IO.puts("[Elixir] Process allocated isolated binary: \#{byte_size(large_bin)} bytes")
      # Process exits -> zero stop-the-world pause for the rest of the node!
    end)

    Process.monitor(pid)
    receive do
      {:DOWN, _ref, :process, _pid, :normal} ->
        IO.puts("[Elixir] Process died: whole heap instantly recycled without global GC.")
    end
  end
end

MemoryDemo.run()`,
        explanation: 'BEAM isolates memory per process. Garbage collection never stops the entire virtual machine; only individual small process heaps are collected.',
        complexity: 'Zero global STW pauses; O(1) process heap cleanup on exit',
        runtimeMechanics: 'Binaries over 64 bytes use reference-counted global off-heap storage; process local data uses private generational copying GC.',
        keyConcepts: ['Isolated process heaps', 'Refc binaries', 'Zero global GC pause', 'Share-nothing architecture']
      }
    }
  },
  {
    id: 'algebraic-data-types-errors',
    title: 'Algebraic Data Types & Error Handling',
    category: 'types',
    tagline: 'Result/Option Monads vs Exceptions vs Discriminated Unions vs Multiple Return Values',
    theoreticalCore: `Error handling and data modeling reflect the fundamental type system philosophy of a language:

1. Sum Types / Monadic Results (Rust, Elixir): Errors are explicit values encoded into the return type (Result<T, E>). Missing case handling is caught at compile time.
2. Discriminated Unions (TypeScript): Structural type refinement through literal tag properties, enabling exhaustive switch/matching.
3. Multiple Return Values with Sentinels (Go): Explicit comma-ok pattern ((val, err)) with no unwinding or try-catch.
4. Exceptional Control Flow (Java, C++, Python): Stack unwinding with structured exception handling, separating happy path from failure branches.`,
    architecturalTradeoffs: {
      pros: [
        'Monadic Result prevents unhandled runtime null-pointer and panic crashes',
        'Discriminated unions provide self-documenting domain-driven data models',
        'Predictable control flow without hidden cost of stack-frame unwinding'
      ],
      cons: [
        'Boilerplate propagation (`?` operator in Rust, `if err != nil` in Go)',
        'Exceptions can be silently unhandled if not documented or enforced',
        'Difficulty mapping external dynamic JSON payloads to strict sum types'
      ],
      bestFor: 'Domain-Driven Design (DDD), mission-critical banking/crypto, and robust protocol parsers.'
    },
    implementations: {
      rust: {
        language: 'rust',
        code: `#[derive(Debug)]
enum NetworkError {
    Timeout(u32),
    Unauthorized,
    NotFound(String),
}

// Result<T, E> enforces exhaustive compile-time handling!
fn fetch_user_balance(id: u64) -> Result<f64, NetworkError> {
    if id == 0 {
        return Err(NetworkError::NotFound(format!("User #{}", id)));
    }
    if id == 401 {
        return Err(NetworkError::Unauthorized);
    }
    Ok(1337.50)
}

fn main() {
    let user_id = 0;
    // Pattern matching with exhaustive check
    match fetch_user_balance(user_id) {
        Ok(balance) => println!("Balance: \${:.2}", balance),
        Err(NetworkError::NotFound(msg)) => println!("Error: {}", msg),
        Err(NetworkError::Timeout(ms)) => println!("Timed out after {}ms", ms),
        Err(NetworkError::Unauthorized) => println!("Auth failed!"),
    }
}`,
        explanation: 'Rust treats errors as first-class values using the Result<T, E> sum type enum. The compiler rejects code if pattern matching is non-exhaustive.',
        complexity: 'Zero cost: Result is represented as tagged union in registers/stack',
        runtimeMechanics: 'The ? operator expands to early-return Err(From::from(err)), propagating errors up the call stack without unwinding.',
        keyConcepts: ['Sum types (Enums)', 'Result<T, E>', 'Exhaustiveness checking', '? operator']
      },
      typescript: {
        language: 'typescript',
        code: `// Discriminated Union (Tagged Union) Pattern
type ApiResponse<T> =
  | { status: 'success'; data: T; timestamp: number }
  | { status: 'error'; code: number; message: string }
  | { status: 'loading' };

function handleResponse(response: ApiResponse<string[]>) {
  switch (response.status) {
    case 'success':
      // TypeScript automatically narrows type to success variant!
      console.log(\`Items: \${response.data.join(', ')}\`);
      break;
    case 'error':
      // Compiler knows 'code' and 'message' exist here
      console.error(\`[\${response.code}] \${response.message}\`);
      break;
    case 'loading':
      console.log('Fetching data...');
      break;
  }
}

handleResponse({ status: 'success', data: ['Rust', 'Go', 'TypeScript'], timestamp: Date.now() });`,
        explanation: 'TypeScript uses discriminated unions with literal string tags. The type checker narrows types within conditional/switch branches.',
        complexity: 'Zero runtime overhead: pure compile-time type erasure',
        runtimeMechanics: 'Structural subtyping checks that all possible discriminant values are handled using the "never" exhaustive check idiom.',
        keyConcepts: ['Discriminated Unions', 'Control Flow Analysis', 'Type Narrowing', 'Exhaustive matching']
      },
      go: {
        language: 'go',
        code: `package main

import (
	"errors"
	"fmt"
)

var ErrNotFound = errors.New("record not found")

// Idiomatic Go: Explicit multiple return values (value, error)
func QueryUser(id int) (string, error) {
	if id <= 0 {
		return "", fmt.Errorf("user query failed: %w", ErrNotFound)
	}
	return "Alice", nil
}

func main() {
	name, err := QueryUser(-1)
	if err != nil {
		// Modern Go error unwrapping with errors.Is
		if errors.Is(err, ErrNotFound) {
			fmt.Println("[Go] Specific error detected:", err)
			return
		}
		fmt.Println("[Go] Unknown error:", err)
		return
	}
	fmt.Println("[Go] Found:", name)
}`,
        explanation: 'Go avoids exceptions for control flow. Functions return error as the last return value. Errors can be wrapped with %w and inspected via errors.Is/errors.As.',
        complexity: 'Two register/stack returns, no stack unwinding penalty',
        runtimeMechanics: 'Errors are simple interfaces with an Error() string method. No runtime unwinding overhead occurs.',
        keyConcepts: ['Explicit error returns', 'Error wrapping %w', 'errors.Is / errors.As', 'Sentinel errors']
      },
      python: {
        language: 'python',
        code: `from typing import Union
from dataclasses import dataclass

@dataclass
class Success:
    data: dict

@dataclass
class Failure:
    reason: str

# Modern Python 3.10+ Pattern Matching (PEP 634)
Result = Union[Success, Failure]

def process_transaction(amount: float) -> Result:
    if amount <= 0:
        return Failure("Invalid transfer amount")
    return Success({"amount": amount, "status": "APPROVED"})

res = process_transaction(-50)
match res:
    case Success(data):
        print(f"[Python 3.14] Approved: {data}")
    case Failure(reason):
        print(f"[Python 3.14] Rejected: {reason}")`,
        explanation: 'Python 3.10+ introduced structural pattern matching (match/case), enabling idiomatic sum-type matching similar to functional languages.',
        complexity: 'Dynamic class pattern matching, runtime type validation',
        runtimeMechanics: 'CPython bytecode uses MATCH_CLASS and MATCH_MAPPING instructions for optimized pattern inspection.',
        keyConcepts: ['Structural Pattern Matching', 'Dataclasses', 'PEP 634 match/case', 'Union types']
      },
      java: {
        language: 'java',
        code: `// Java 21+: Sealed Interfaces + Record Pattern Matching
public class SealedPatternDemo {
    sealed interface PaymentResult permits Success, Failed {}
    
    record Success(String transactionId, double amount) implements PaymentResult {}
    record Failed(String reason, int errorCode) implements PaymentResult {}

    static void evaluate(PaymentResult result) {
        // Compiler guarantees all permits are handled without 'default' branch!
        String status = switch (result) {
            case Success(var txId, var amt) -> "Payment approved: " + txId + " ($" + amt + ")";
            case Failed(var reason, var code) -> "Payment declined [" + code + "]: " + reason;
        };
        System.out.println(status);
    }

    public static void main(String[] args) {
        evaluate(new Failed("Insufficient funds", 402));
    }
}`,
        explanation: 'Java 21 introduced pattern matching for switch combined with sealed hierarchies, bringing algebraic sum-types and compile-time exhaustiveness to the JVM.',
        complexity: 'Constant-time tableswitch / dynamic type test',
        runtimeMechanics: 'Javac verifies exhaustive branch coverage. JIT compiles pattern switches into efficient jump tables.',
        keyConcepts: ['Sealed interfaces', 'Record patterns', 'Pattern matching switch', 'Exhaustiveness']
      },
      cpp: {
        language: 'cpp',
        code: `#include <iostream>
#include <variant>
#include <string>

// C++17 std::variant (Type-safe Union)
using Result = std::variant<std::string, int>;

// Overloaded visitor helper
template<class... Ts> struct overloaded : Ts... { using Ts::operator()...; };

int main() {
    Result res = "Data loaded successfully";

    std::visit(overloaded {
        [](const std::string& str) { std::cout << "[C++ Variant] String: " << str << std::endl; },
        [](int errCode) { std::cout << "[C++ Variant] Error Code: " << errCode << std::endl; }
    }, res);

    return 0;
}`,
        explanation: 'C++17 std::variant provides type-safe sum types. std::visit applies template-overloaded lambdas with zero heap allocation.',
        complexity: 'Tagged union: size of largest member + alignment padding',
        runtimeMechanics: 'std::visit uses a compiler-generated function pointer jump table based on index() of the variant.',
        keyConcepts: ['std::variant', 'std::visit', 'Visitor pattern', 'Type-safe unions']
      },
      elixir: {
        language: 'elixir',
        code: `defmodule ErrorDemo do
  # Elixir tagged tuples with pattern matching & 'with' macro
  def parse_id(str) do
    case Integer.parse(str) do
      {num, ""} -> {:ok, num}
      _ -> {:error, :invalid_format}
    end
  end

  def authenticate(user_id) do
    if user_id > 100, do: {:ok, "Authorized User"}, else: {:error, :forbidden}
  end

  def run(input) do
    # 'with' pipeline chains monadic {:ok, val} / {:error, reason}
    result = with {:ok, id} <- parse_id(input),
                  {:ok, user} <- authenticate(id) do
      {:success, "Welcome \#{user} (ID: \#{id})"}
    else
      {:error, :invalid_format} -> {:failure, "Bad ID format"}
      {:error, :forbidden} -> {:failure, "Access denied"}
    end

    IO.inspect(result, label: "[Elixir Monadic with]")
  end
end

ErrorDemo.run("150")`,
        explanation: 'Elixir uses tagged tuples `{:ok, val}` and `{:error, reason}`. The `with` special form chains sequential operations, aborting on the first mismatch.',
        complexity: 'O(1) tuple pattern matching in BEAM',
        runtimeMechanics: 'Pattern matching is implemented as optimized VM comparison opcodes directly in BEAM.',
        keyConcepts: ['Tagged tuples', 'with macro', 'Railway Oriented Programming', 'Pattern matching']
      }
    }
  }
];
