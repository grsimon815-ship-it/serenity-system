from dataclasses import dataclass
from typing import List, Optional

@dataclass
class MemoryBlock:
    label: str
    address: str
    size_bytes: int
    value: str
    color_hex: str
    target_address: Optional[str] = None
    is_borrowed: bool = False
    is_freed: bool = False
    ref_count: int = 1

@dataclass
class StackFrame:
    func_name: str
    variables: List[MemoryBlock]

@dataclass
class SimStep:
    step_num: int
    line_number: int
    action_title: str
    explanation: str
    stack: List[StackFrame]
    heap: List[MemoryBlock]
    notes: str

@dataclass
class MemoryScenario:
    id: str
    title: str
    language: str
    description: str
    code_lines: List[str]
    steps: List[SimStep]

MEMORY_SCENARIOS: List[MemoryScenario] = [
    MemoryScenario(
        id="rust_move_borrow",
        title="Rust: Stack Allocation, Move Semantics & Borrowing",
        language="rust",
        description="Visualize stack frame layout, heap buffer allocation, affine ownership transfer (Move), and borrowing (&T vs &mut T).",
        code_lines=[
            "fn main() {",
            "    let s1 = String::from(\"POLYGLOT\"); // Line 2: Heap allocation & stack descriptor",
            "    let len = inspect_ref(&s1);       // Line 3: Shared borrow &String",
            "    let s2 = s1;                      // Line 4: Ownership moved to s2; s1 invalidated",
            "    // s1 cannot be used here",
            "}                                     // Line 6: s2 dropped, heap buffer freed"
        ],
        steps=[
            SimStep(
                step_num=1,
                line_number=2,
                action_title="Allocate String on Heap",
                explanation="s1 is allocated on the stack (pointer, capacity=8, length=8). It points to 'POLYGLOT' on the heap.",
                stack=[
                    StackFrame(
                        func_name="main()",
                        variables=[
                            MemoryBlock(
                                label="s1 (ptr, cap, len)",
                                address="0x7FFF0010",
                                size_bytes=24,
                                value="ptr -> 0x00A010",
                                color_hex="#f97316",
                                target_address="0x00A010"
                            )
                        ]
                    )
                ],
                heap=[
                    MemoryBlock(
                        label="String Buffer (\"POLYGLOT\")",
                        address="0x00A010",
                        size_bytes=8,
                        value="['P','O','L','Y','G','L','O','T']",
                        color_hex="#06b6d4",
                        ref_count=1
                    )
                ],
                notes="Rust stack strings consist of 3 usize fields: ptr, cap, len (24 bytes total on 64-bit systems)."
            ),
            SimStep(
                step_num=2,
                line_number=3,
                action_title="Shared Borrow (&s1)",
                explanation="A shared reference &s1 is passed to inspect_ref. Stack frame pushes inspect_ref with an immutable borrow pointer.",
                stack=[
                    StackFrame(
                        func_name="main()",
                        variables=[
                            MemoryBlock(
                                label="s1",
                                address="0x7FFF0010",
                                size_bytes=24,
                                value="ptr -> 0x00A010",
                                color_hex="#f97316",
                                target_address="0x00A010",
                                is_borrowed=True
                            )
                        ]
                    ),
                    StackFrame(
                        func_name="inspect_ref(s: &String)",
                        variables=[
                            MemoryBlock(
                                label="s (&s1)",
                                address="0x7FFF0040",
                                size_bytes=8,
                                value="ptr -> 0x7FFF0010",
                                color_hex="#10b981",
                                target_address="0x7FFF0010"
                            )
                        ]
                    )
                ],
                heap=[
                    MemoryBlock(
                        label="String Buffer (\"POLYGLOT\")",
                        address="0x00A010",
                        size_bytes=8,
                        value="['P','O','L','Y','G','L','O','T']",
                        color_hex="#06b6d4",
                        is_borrowed=True
                    )
                ],
                notes="Shared borrow &T allows multiple concurrent readers. Mutation is prevented while borrowed."
            ),
            SimStep(
                step_num=3,
                line_number=4,
                action_title="Affine Move: s1 -> s2",
                explanation="s1 is moved into s2. Bitwise copy of the 24-byte descriptor occurs, but s1 is marked uninitialized by the compiler.",
                stack=[
                    StackFrame(
                        func_name="main()",
                        variables=[
                            MemoryBlock(
                                label="s1 [INVALID / MOVED]",
                                address="0x7FFF0010",
                                size_bytes=24,
                                value="<uninitialized>",
                                color_hex="#64748b",
                                is_freed=True
                            ),
                            MemoryBlock(
                                label="s2 (New Owner)",
                                address="0x7FFF0028",
                                size_bytes=24,
                                value="ptr -> 0x00A010",
                                color_hex="#f97316",
                                target_address="0x00A010"
                            )
                        ]
                    )
                ],
                heap=[
                    MemoryBlock(
                        label="String Buffer (\"POLYGLOT\")",
                        address="0x00A010",
                        size_bytes=8,
                        value="['P','O','L','Y','G','L','O','T']",
                        color_hex="#06b6d4",
                        ref_count=1
                    )
                ],
                notes="Zero-cost move: only 24 bytes are copied on the stack; the heap buffer is not reallocated."
            ),
            SimStep(
                step_num=4,
                line_number=6,
                action_title="Scope Exit & Drop Glue",
                explanation="main() ends. s2 is dropped, executing Drop::drop glue to deallocate heap memory at 0x00A010.",
                stack=[
                    StackFrame(
                        func_name="main() [unwinding]",
                        variables=[]
                    )
                ],
                heap=[
                    MemoryBlock(
                        label="String Buffer (Deallocated)",
                        address="0x00A010",
                        size_bytes=0,
                        value="<FREED MEMORY>",
                        color_hex="#ef4444",
                        is_freed=True
                    )
                ],
                notes="Drop glue runs deterministically at compile-time determined scope boundaries. No GC pause occurs."
            )
        ]
    ),
    MemoryScenario(
        id="cpp_raii_unique_ptr",
        title="C++: RAII, std::unique_ptr & Heap Ownership",
        language="cpp",
        description="Track how std::unique_ptr encapsulates heap pointers on the stack and safely transfers ownership with std::move.",
        code_lines=[
            "int main() {",
            "    auto p1 = std::make_unique<Resource>(); // Line 2: Stack pointer holding Heap Resource",
            "    auto p2 = std::move(p1);                // Line 3: Ownership transfer; p1 becomes nullptr",
            "    // p1 == nullptr",
            "}                                           // Line 5: p2 destructor called automatically"
        ],
        steps=[
            SimStep(
                step_num=1,
                line_number=2,
                action_title="std::make_unique Allocation",
                explanation="p1 is created on the stack (8 bytes). It points to Resource on the free store (heap).",
                stack=[
                    StackFrame(
                        func_name="main()",
                        variables=[
                            MemoryBlock(
                                label="p1 (std::unique_ptr)",
                                address="0x7FFF0010",
                                size_bytes=8,
                                value="0x00B020",
                                color_hex="#a855f7",
                                target_address="0x00B020"
                            )
                        ]
                    )
                ],
                heap=[
                    MemoryBlock(
                        label="Resource Object",
                        address="0x00B020",
                        size_bytes=64,
                        value="{ id: 101, state: ACTIVE }",
                        color_hex="#06b6d4"
                    )
                ],
                notes="std::unique_ptr has the exact same size as a raw pointer (8 bytes on 64-bit systems)."
            ),
            SimStep(
                step_num=2,
                line_number=3,
                action_title="std::move Ownership Transfer",
                explanation="Move constructor transfers the heap pointer to p2 and resets p1 to nullptr.",
                stack=[
                    StackFrame(
                        func_name="main()",
                        variables=[
                            MemoryBlock(
                                label="p1 (nullptr)",
                                address="0x7FFF0010",
                                size_bytes=8,
                                value="nullptr (0x0)",
                                color_hex="#64748b"
                            ),
                            MemoryBlock(
                                label="p2 (std::unique_ptr)",
                                address="0x7FFF0018",
                                size_bytes=8,
                                value="0x00B020",
                                color_hex="#a855f7",
                                target_address="0x00B020"
                            )
                        ]
                    )
                ],
                heap=[
                    MemoryBlock(
                        label="Resource Object",
                        address="0x00B020",
                        size_bytes=64,
                        value="{ id: 101, state: ACTIVE }",
                        color_hex="#06b6d4"
                    )
                ],
                notes="Move semantics prevents double-free by guaranteeing single ownership."
            ),
            SimStep(
                step_num=3,
                line_number=5,
                action_title="RAII Scope Destructor",
                explanation="End of main(). p2 goes out of scope and its destructor calls delete on 0x00B020.",
                stack=[
                    StackFrame(
                        func_name="main() [exit]",
                        variables=[]
                    )
                ],
                heap=[
                    MemoryBlock(
                        label="Resource Object (Deleted)",
                        address="0x00B020",
                        size_bytes=0,
                        value="<DELETED>",
                        color_hex="#ef4444",
                        is_freed=True
                    )
                ],
                notes="Deterministic destruction avoids both memory leaks and GC overhead."
            )
        ]
    )
]
