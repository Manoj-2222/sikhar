"""
Sikhar Language Server Protocol (LSP) Implementation
Full JSON-RPC 2.0 stdio server providing live diagnostics, hover documentation,
document symbols, and autocompletion for Sikhar (.sk).
"""

import json
import sys
from typing import Any, Dict, List, Optional, Tuple

from ..lexer.lexer import Lexer
from ..lexer.token_type import KEYWORDS
from ..parser.parser import Parser
from ..parser.ast_nodes import FunctionDeclaration, VariableDeclaration, ConstantDeclaration
from ..errors.error_types import SikharError

KEYWORD_DOCS = {
    "rakha": "**rakha** (let/var): Declares a mutable variable.\n```sk\nrakha count = 0\n```",
    "sthayi": "**sthayi** (const): Declares an immutable constant.\n```sk\nsthayi PI = 3.14159\n```",
    "badla": "**badla** (set): Mutates an existing variable, list element, or map key.\n```sk\nbadla count = count + 1\n```",
    "yadi": "**yadi** (if): Conditional branching statement.\n```sk\nyadi x > 10 { ... }\n```",
    "athawa": "**athawa** (else if): Alternative conditional branch.\n```sk\nathawa x == 5 { ... }\n```",
    "natra": "**natra** (else): Fallback branch when prior conditions fail.\n```sk\nnatra { ... }\n```",
    "jaba": "**jaba** (while): Loop executing as long as the condition evaluates to true.\n```sk\njaba i < 10 { ... }\n```",
    "ko_lagi": "**ko_lagi** (for): Traversal loop over lists, strings, or maps.\n```sk\nko_lagi item ma items { ... }\n```",
    "ma": "**ma** (in): Connects iteration variable to the target collection in `ko_lagi`.",
    "rok": "**rok** (break): Immediately terminates the enclosing loop.",
    "jaari": "**jaari** (continue): Skips to the next iteration of the loop.",
    "kaam": "**kaam** (function): Defines a named function or anonymous closure.\n```sk\nkaam add(a, b) { farka a + b }\n```",
    "farka": "**farka** (return): Returns a value from a function call.",
    "koshish": "**koshish** (try): Initiates an exception-handling block.\n```sk\nkoshish { ... } samata e { ... }\n```",
    "samata": "**samata** (catch): Intercepts exceptions raised inside a `koshish` block.",
    "fal": "**fal** (throw): Raises an exception with an error message or object.",
    "aayaat": "**aayaat** (import): Imports a local file module or standard library namespace.\n```sk\naayaat std.math\n```",
    "pathaau": "**pathaau** (export): Exports a variable, constant, or function from a module.",
    "jaach": "**jaach** (assert): In-language test assertion asserting a boolean condition.\n```sk\njaach x == 10, \"Expected 10\"\n```",
    "dekha": "**dekha** (print): Outputs an expression to standard output.",
    "sacho": "**sacho** (true): Boolean true literal.",
    "jutho": "**jutho** (false): Boolean false literal.",
    "khali": "**khali** (null): Null literal representing the absence of a value.",
    "ra": "**ra** (and): Logical AND operation.",
    "wa": "**wa** (or): Logical OR operation.",
    "hoina": "**hoina** (not): Logical NOT operation.",
}


class SikharLanguageServer:
    """JSON-RPC 2.0 Language Server implementation for Sikhar."""

    def __init__(self, in_stream=None, out_stream=None):
        self.in_stream = in_stream or sys.stdin.buffer
        self.out_stream = out_stream or sys.stdout.buffer
        self.documents: Dict[str, str] = {}
        self.running: bool = True

    def send_response(self, id_val: Any, result: Any = None, error: Any = None) -> None:
        payload = {"jsonrpc": "2.0", "id": id_val}
        if error is not None:
            payload["error"] = error
        else:
            payload["result"] = result
        self._write_msg(payload)

    def send_notification(self, method: str, params: Any) -> None:
        payload = {"jsonrpc": "2.0", "method": method, "params": params}
        self._write_msg(payload)

    def _write_msg(self, payload: Dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        header = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
        self.out_stream.write(header + body)
        self.out_stream.flush()

    def read_message(self) -> Optional[Dict[str, Any]]:
        # Read headers until empty line
        content_length = 0
        while True:
            line = self.in_stream.readline()
            if not line:
                return None
            line_str = line.decode("latin1").strip()
            if not line_str:
                break
            if line_str.lower().startswith("content-length:"):
                content_length = int(line_str.split(":", 1)[1].strip())

        if content_length <= 0:
            return None

        body = self.in_stream.read(content_length)
        if not body:
            return None
        return json.loads(body.decode("utf-8"))

    def compute_diagnostics(self, uri: str, text: str) -> List[Dict[str, Any]]:
        diagnostics = []
        try:
            tokens = Lexer(text, uri).tokenize()
            Parser(tokens, text, uri).parse()
        except SikharError as err:
            line = max(0, err.line - 1)
            col = max(0, err.column - 1)
            diag = {
                "range": {
                    "start": {"line": line, "character": col},
                    "end": {"line": line, "character": col + 1},
                },
                "severity": 1,  # Error
                "source": "sikhar",
                "message": err.message,
            }
            diagnostics.append(diag)
        except Exception as e:
            diagnostics.append({
                "range": {
                    "start": {"line": 0, "character": 0},
                    "end": {"line": 0, "character": 1},
                },
                "severity": 1,
                "source": "sikhar",
                "message": str(e),
            })
        return diagnostics

    def handle_request(self, req: Dict[str, Any]) -> None:
        method = req.get("method")
        msg_id = req.get("id")
        params = req.get("params", {})

        if method == "initialize":
            capabilities = {
                "capabilities": {
                    "textDocumentSync": 1,  # Full sync
                    "hoverProvider": True,
                    "completionProvider": {
                        "resolveProvider": False,
                        "triggerCharacters": [".", " "],
                    },
                    "documentSymbolProvider": True,
                },
                "serverInfo": {
                    "name": "sikhar-lsp",
                    "version": "1.0.0",
                },
            }
            self.send_response(msg_id, capabilities)

        elif method == "shutdown":
            self.send_response(msg_id, None)

        elif method == "exit":
            self.running = False

        elif method == "textDocument/didOpen":
            doc = params.get("textDocument", {})
            uri = doc.get("uri", "")
            text = doc.get("text", "")
            self.documents[uri] = text
            diags = self.compute_diagnostics(uri, text)
            self.send_notification("textDocument/publishDiagnostics", {"uri": uri, "diagnostics": diags})

        elif method == "textDocument/didChange":
            doc = params.get("textDocument", {})
            uri = doc.get("uri", "")
            changes = params.get("contentChanges", [])
            if changes:
                text = changes[-1].get("text", "")
                self.documents[uri] = text
                diags = self.compute_diagnostics(uri, text)
                self.send_notification("textDocument/publishDiagnostics", {"uri": uri, "diagnostics": diags})

        elif method == "textDocument/didClose":
            doc = params.get("textDocument", {})
            uri = doc.get("uri", "")
            if uri in self.documents:
                del self.documents[uri]

        elif method == "textDocument/hover":
            doc = params.get("textDocument", {})
            uri = doc.get("uri", "")
            pos = params.get("position", {})
            line_no = pos.get("line", 0)
            char_no = pos.get("character", 0)

            hover_content = None
            if uri in self.documents:
                text = self.documents[uri]
                lines = text.splitlines()
                if 0 <= line_no < len(lines):
                    line_text = lines[line_no]
                    # Find word at char_no
                    start = char_no
                    while start > 0 and (line_text[start - 1].isalnum() or line_text[start - 1] == "_"):
                        start -= 1
                    end = char_no
                    while end < len(line_text) and (line_text[end].isalnum() or line_text[end] == "_"):
                        end += 1
                    word = line_text[start:end]
                    if word in KEYWORD_DOCS:
                        hover_content = {"kind": "markdown", "value": KEYWORD_DOCS[word]}

            if hover_content:
                self.send_response(msg_id, {"contents": hover_content})
            else:
                self.send_response(msg_id, None)

        elif method == "textDocument/completion":
            items = []
            # Keywords
            for kw in KEYWORDS:
                items.append({
                    "label": kw,
                    "kind": 14,  # Keyword
                    "detail": f"Sikhar keyword '{kw}'",
                })
            # Builtins
            builtins = ["dekha", "sodh", "lamba", "jod_suchi", "hatau_suchi", "prakar", "khola", "banda", "padh", "lekh"]
            for b in builtins:
                items.append({
                    "label": b,
                    "kind": 3,  # Function
                    "detail": f"Builtin function '{b}'",
                })
            # Stdlib namespaces
            std_modules = ["std.math", "std.text", "std.list", "std.map", "std.file", "std.time", "std.json", "std.http", "std.web", "std.db", "std.crypto", "std.csv", "std.regex", "std.process", "std.task"]
            for m in std_modules:
                items.append({
                    "label": m,
                    "kind": 9,  # Module
                    "detail": f"Standard library module '{m}'",
                })
            self.send_response(msg_id, {"isIncomplete": False, "items": items})

        elif method == "textDocument/documentSymbol":
            doc = params.get("textDocument", {})
            uri = doc.get("uri", "")
            symbols = []
            if uri in self.documents:
                text = self.documents[uri]
                try:
                    tokens = Lexer(text, uri).tokenize()
                    ast = Parser(tokens, text, uri).parse()
                    for stmt in ast.statements:
                        if isinstance(stmt, FunctionDeclaration):
                            symbols.append({
                                "name": stmt.name,
                                "kind": 12,  # Function
                                "range": {
                                    "start": {"line": stmt.line - 1, "character": stmt.column - 1},
                                    "end": {"line": stmt.line - 1, "character": stmt.column + len(stmt.name)},
                                },
                                "selectionRange": {
                                    "start": {"line": stmt.line - 1, "character": stmt.column - 1},
                                    "end": {"line": stmt.line - 1, "character": stmt.column + len(stmt.name)},
                                },
                            })
                        elif isinstance(stmt, (VariableDeclaration, ConstantDeclaration)):
                            symbols.append({
                                "name": stmt.name,
                                "kind": 13 if isinstance(stmt, VariableDeclaration) else 14,
                                "range": {
                                    "start": {"line": stmt.line - 1, "character": stmt.column - 1},
                                    "end": {"line": stmt.line - 1, "character": stmt.column + len(stmt.name)},
                                },
                                "selectionRange": {
                                    "start": {"line": stmt.line - 1, "character": stmt.column - 1},
                                    "end": {"line": stmt.line - 1, "character": stmt.column + len(stmt.name)},
                                },
                            })
                except Exception:
                    pass
            self.send_response(msg_id, symbols)

        elif msg_id is not None:
            # Unsupported request
            self.send_response(msg_id, None)

    def run(self) -> None:
        while self.running:
            try:
                msg = self.read_message()
                if msg is None:
                    break
                self.handle_request(msg)
            except Exception:
                break


def start_lsp_server() -> int:
    """Launch the Sikhar LSP server listening on stdio."""
    server = SikharLanguageServer()
    server.run()
    return 0


LanguageServer = SikharLanguageServer

