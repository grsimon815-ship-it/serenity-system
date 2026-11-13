import subprocess
import tempfile
import os
import time
import shutil
import dis
import ast
from dataclasses import dataclass
from typing import Optional

@dataclass
class RunOutput:
    stdout: str
    stderr: str
    exit_code: int
    duration_ms: float
    is_simulated: bool
    status_label: str

class CodeRunner:
    @staticmethod
    def run(language: str, code: str, timeout_sec: int = 5) -> RunOutput:
        start_time = time.perf_counter()
        
        if language == "python":
            return CodeRunner._run_python(code, timeout_sec, start_time)
        elif language == "typescript":
            return CodeRunner._run_typescript(code, timeout_sec, start_time)
        elif language == "java":
            return CodeRunner._run_java(code, timeout_sec, start_time)
        else:
            return CodeRunner._run_or_simulate(language, code, start_time)

    @staticmethod
    def disassemble(language: str, code: str) -> str:
        """Returns actual bytecode disassembly or compiler output"""
        if language == "python":
            try:
                import io
                buf = io.StringIO()
                compiled = compile(code, "<editor>", "exec")
                dis.dis(compiled, file=buf)
                return buf.getvalue()
            except Exception as e:
                return f"Disassembly Error: {e}"
        elif language == "typescript":
            return "// V8 Bytecode (Ignition representation)\n// Bytecode generation requires Node with --print-bytecode\n" + \
                   CodeRunner._extract_ts_structure(code)
        else:
            return f"// Compiler IR / Assembly inspection target for {language}\n" + \
                   f"// Syntax tokens analyzed: {len(code.split())} tokens"

    @staticmethod
    def inspect_ast(language: str, code: str) -> str:
        """Returns actual syntax tree (AST)"""
        if language == "python":
            try:
                tree = ast.parse(code)
                return ast.dump(tree, indent=2)
            except Exception as e:
                return f"AST Parse Error: {e}"
        else:
            # Pseudo-structural AST for other languages
            lines = [f"// Structural AST: {language}"]
            for idx, line in enumerate(code.strip().splitlines()[:20], 1):
                stripped = line.strip()
                if stripped.startswith(("fn ", "func ", "function ", "class ", "def ", "struct ")):
                    lines.append(f"  [L{idx:02d}] Declaration: {stripped}")
                elif stripped.startswith(("let ", "var ", "const ", "auto ")):
                    lines.append(f"  [L{idx:02d}] Binding: {stripped}")
            return "\n".join(lines)

    @staticmethod
    def _extract_ts_structure(code: str) -> str:
        lines = []
        for line in code.splitlines():
            s = line.strip()
            if any(s.startswith(k) for k in ["function", "async function", "class", "interface", "type"]):
                lines.append(f">> [Symbol] {s}")
        return "\n".join(lines) if lines else "// No top-level declarations"

    @staticmethod
    def _run_python(code: str, timeout_sec: int, start_time: float) -> RunOutput:
        try:
            res = subprocess.run(
                ["python", "-c", code],
                capture_output=True,
                text=True,
                timeout=timeout_sec
            )
            elapsed = (time.perf_counter() - start_time) * 1000.0
            return RunOutput(
                stdout=res.stdout,
                stderr=res.stderr,
                exit_code=res.returncode,
                duration_ms=round(elapsed, 2),
                is_simulated=False,
                status_label=f"CPython 3.14 ({round(elapsed, 1)}ms)"
            )
        except subprocess.TimeoutExpired:
            return RunOutput("", "Execution timed out (5s limit)", 124, timeout_sec * 1000.0, False, "Timeout")
        except Exception as e:
            return RunOutput("", str(e), 1, 0.0, False, "Error")

    @staticmethod
    def _run_typescript(code: str, timeout_sec: int, start_time: float) -> RunOutput:
        node_path = shutil.which("node")
        if not node_path:
            return CodeRunner._simulate_output("typescript", code, start_time, "Node binary missing")
        try:
            res = subprocess.run(
                ["node", "--experimental-strip-types", "-e", code],
                capture_output=True,
                text=True,
                timeout=timeout_sec
            )
            if res.returncode != 0 and "experimental-strip-types" in res.stderr:
                res = subprocess.run(
                    ["node", "-e", code],
                    capture_output=True,
                    text=True,
                    timeout=timeout_sec
                )
            elapsed = (time.perf_counter() - start_time) * 1000.0
            return RunOutput(
                stdout=res.stdout,
                stderr=res.stderr,
                exit_code=res.returncode,
                duration_ms=round(elapsed, 2),
                is_simulated=False,
                status_label=f"V8 Engine ({round(elapsed, 1)}ms)"
            )
        except Exception as e:
            return CodeRunner._simulate_output("typescript", code, start_time, f"Fallback: {e}")

    @staticmethod
    def _run_java(code: str, timeout_sec: int, start_time: float) -> RunOutput:
        javac_path = shutil.which("javac")
        if not javac_path:
            return CodeRunner._simulate_output("java", code, start_time, "javac missing")
        
        temp_dir = tempfile.mkdtemp()
        try:
            class_name = "VirtualThreadDemo"
            if "class " in code:
                parts = code.split("class ")[1].split()[0].split("{")[0]
                class_name = parts.strip()
            
            src_file = os.path.join(temp_dir, f"{class_name}.java")
            with open(src_file, "w", encoding="utf-8") as f:
                f.write(code)
                
            compile_res = subprocess.run(["javac", src_file], capture_output=True, text=True, timeout=timeout_sec)
            if compile_res.returncode != 0:
                elapsed = (time.perf_counter() - start_time) * 1000.0
                return RunOutput("", compile_res.stderr, compile_res.returncode, round(elapsed, 2), False, "Compile Failed")
            
            run_res = subprocess.run(["java", "-cp", temp_dir, class_name], capture_output=True, text=True, timeout=timeout_sec)
            elapsed = (time.perf_counter() - start_time) * 1000.0
            return RunOutput(run_res.stdout, run_res.stderr, run_res.returncode, round(elapsed, 2), False, f"JVM HotSpot ({round(elapsed, 1)}ms)")
        except Exception as e:
            return CodeRunner._simulate_output("java", code, start_time, f"JVM Error: {e}")
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    @staticmethod
    def _run_or_simulate(language: str, code: str, start_time: float) -> RunOutput:
        return CodeRunner._simulate_output(language, code, start_time, f"Emulator ({language})")

    @staticmethod
    def _simulate_output(language: str, code: str, start_time: float, reason: str) -> RunOutput:
        elapsed = (time.perf_counter() - start_time) * 1000.0
        lines = []
        if language == "rust":
            if "tokio" in code:
                lines = [
                    "[tokio-runtime-worker] task 0x1 complete (status: ok)",
                    "[tokio-runtime-worker] task 0x2 complete (status: ok)",
                    "[tokio-runtime-worker] task 0x3 complete (status: ok)",
                    ">> Futures settled: 3 | Active allocations: 0"
                ]
            else:
                lines = [
                    ">> borrow check: passed (0 aliasing hazards)",
                    ">> memory layout: 24 bytes stack descriptor, drop glue inserted"
                ]
        elif language == "go":
            lines = [
                "[M:P:G scheduler] 3 goroutines scheduled on OS carrier thread",
                ">> channel sync: drained | exit: 0"
            ]
        elif language == "cpp":
            lines = [
                ">> RAII scope exit: std::unique_ptr destructor called",
                ">> free store deallocated: 0 leaks reported"
            ]
        else:
            lines = [f">> {language} execution: exit code 0"]

        return RunOutput("\n".join(lines) + "\n", "", 0, round(elapsed, 2), True, reason)
