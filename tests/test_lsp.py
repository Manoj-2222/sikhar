import unittest
import sys
import io
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sikhar.lsp.server import LanguageServer


class TestLSP(unittest.TestCase):
    def setUp(self):
        self.in_buf = io.BytesIO()
        self.out_buf = io.BytesIO()
        self.server = LanguageServer(self.in_buf, self.out_buf)

    def send_msg(self, msg: dict) -> dict:
        self.out_buf.seek(0)
        self.out_buf.truncate(0)
        self.server.handle_request(msg)
        raw = self.out_buf.getvalue()
        if not raw:
            return None
        parts = raw.split(b"\r\n\r\n", 1)
        if len(parts) == 2:
            return json.loads(parts[1].decode("utf-8"))
        return None

    def test_initialize_and_capabilities(self):
        req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"capabilities": {}}
        }
        res = self.send_msg(req)
        self.assertIsNotNone(res)
        self.assertIn("capabilities", res["result"])
        caps = res["result"]["capabilities"]
        self.assertTrue(caps["hoverProvider"])
        self.assertTrue(caps["documentSymbolProvider"])

    def test_document_sync_and_diagnostics(self):
        broken_code = "kaam ( broken"
        notif = {
            "jsonrpc": "2.0",
            "method": "textDocument/didOpen",
            "params": {
                "textDocument": {
                    "uri": "file:///test.sk",
                    "languageId": "sikhar",
                    "version": 1,
                    "text": broken_code
                }
            }
        }
        diag_res = self.send_msg(notif)
        self.assertIsNotNone(diag_res)
        self.assertEqual(diag_res["method"], "textDocument/publishDiagnostics")
        self.assertGreater(len(diag_res["params"]["diagnostics"]), 0)

    def test_hover_and_completion(self):
        valid_code = "rakha x = 10\nkaam add(a, b) { farka a + b }\n"
        self.send_msg({
            "jsonrpc": "2.0",
            "method": "textDocument/didOpen",
            "params": {
                "textDocument": {
                    "uri": "file:///valid.sk",
                    "languageId": "sikhar",
                    "version": 1,
                    "text": valid_code
                }
            }
        })

        # Hover over 'rakha'
        hover_req = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "textDocument/hover",
            "params": {
                "textDocument": {"uri": "file:///valid.sk"},
                "position": {"line": 0, "character": 2}
            }
        }
        hover_res = self.send_msg(hover_req)
        self.assertIsNotNone(hover_res)
        self.assertIn("contents", hover_res["result"])
        self.assertIn("mutable variable", hover_res["result"]["contents"]["value"])

        # Completion request
        comp_req = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "textDocument/completion",
            "params": {
                "textDocument": {"uri": "file:///valid.sk"},
                "position": {"line": 1, "character": 0}
            }
        }
        comp_res = self.send_msg(comp_req)
        items = comp_res["result"]["items"]
        labels = [item["label"] for item in items]
        self.assertIn("rakha", labels)
        self.assertIn("kaam", labels)
        self.assertIn("std.crypto", labels)

    def test_document_symbol(self):
        code = "kaam compute() { farka 42 }\nkaam greet() { dekha \"hi\" }"
        self.send_msg({
            "jsonrpc": "2.0",
            "method": "textDocument/didOpen",
            "params": {
                "textDocument": {
                    "uri": "file:///sym.sk",
                    "languageId": "sikhar",
                    "version": 1,
                    "text": code
                }
            }
        })
        sym_req = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "textDocument/documentSymbol",
            "params": {
                "textDocument": {"uri": "file:///sym.sk"}
            }
        }
        sym_res = self.send_msg(sym_req)
        symbols = sym_res["result"]
        names = [s["name"] for s in symbols]
        self.assertIn("compute", names)
        self.assertIn("greet", names)


if __name__ == "__main__":
    unittest.main()
