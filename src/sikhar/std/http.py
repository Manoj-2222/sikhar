"""
Sikhar Standard Library: std.http
HTTP client requests and HTTP server implementation.
"""

import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Dict, List, Optional
import urllib.request
import urllib.error
from urllib.parse import urlparse, parse_qs

from ..interpreter.values import BuiltinFunction, SikharModule, SikharCallable
from ..errors.error_types import SikharTypeError, SikharRuntimeError


def _prepare_headers(headers_val: Any) -> Dict[str, str]:
    if not isinstance(headers_val, dict):
        return {}
    return {str(k): str(v) for k, v in headers_val.items()}


def _perform_request(
    method: str,
    url: str,
    body: Optional[Any] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: float = 30.0,
) -> Dict[str, Any]:
    req_headers = dict(headers or {})
    data_bytes: Optional[bytes] = None

    if body is not None:
        if isinstance(body, (dict, list)):
            if "Content-Type" not in req_headers and "content-type" not in req_headers:
                req_headers["Content-Type"] = "application/json; charset=utf-8"
            data_bytes = json.dumps(body).encode("utf-8")
        elif isinstance(body, str):
            data_bytes = body.encode("utf-8")
        elif isinstance(body, (bytes, bytearray)):
            data_bytes = bytes(body)
        else:
            data_bytes = str(body).encode("utf-8")

    req = urllib.request.Request(url, data=data_bytes, headers=req_headers, method=method.upper())

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            resp_body = resp.read().decode("utf-8", errors="replace")
            status = resp.status
            resp_headers = {k.lower(): v for k, v in resp.headers.items()}
            return {
                "status": status,
                "body": resp_body,
                "headers": resp_headers,
                "ok": 200 <= status < 400,
            }
    except urllib.error.HTTPError as err:
        resp_body = err.read().decode("utf-8", errors="replace")
        resp_headers = {k.lower(): v for k, v in err.headers.items()}
        return {
            "status": err.code,
            "body": resp_body,
            "headers": resp_headers,
            "ok": False,
        }
    except Exception as e:
        raise SikharRuntimeError(f"HTTP request to '{url}' failed: {e}")


class SikharHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, interp: Any, handler_fn: Any, *args, **kwargs):
        self.interp = interp
        self.handler_fn = handler_fn
        super().__init__(*args, **kwargs)

    def log_message(self, format: str, *args: Any) -> None:
        # Suppress noisy standard HTTP access logs in production/tests
        pass

    def _handle_request(self) -> None:
        content_length = int(self.headers.get("Content-Length", 0))
        body_str = ""
        if content_length > 0:
            body_bytes = self.rfile.read(content_length)
            body_str = body_bytes.decode("utf-8", errors="replace")

        header_dict = {k.lower(): v for k, v in self.headers.items()}
        parsed_url = urlparse(self.path)
        path_only = parsed_url.path or "/"
        query_dict = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(parsed_url.query).items()}
        req_obj = {
            "method": self.command,
            "path": path_only,
            "url": self.path,
            "query": query_dict,
            "headers": header_dict,
            "body": body_str,
        }

        try:
            if hasattr(self.handler_fn, "call"):
                res = self.handler_fn.call(self.interp, [req_obj], 1, 1)
            elif callable(self.handler_fn):
                res = self.handler_fn(req_obj)
            else:
                res = {"status": 500, "body": "Handler is not callable"}
        except Exception as e:
            res = {"status": 500, "body": f"Handler error: {e}"}

        status_code = 200
        res_body = ""
        res_headers = {}

        if isinstance(res, dict):
            if "status" in res:
                status_code = int(res["status"])
                res_body = res.get("body", "")
                if isinstance(res_body, (dict, list)):
                    res_body = json.dumps(res_body)
                    res_headers["content-type"] = "application/json; charset=utf-8"
                else:
                    res_body = str(res_body)
                if "headers" in res and isinstance(res["headers"], dict):
                    res_headers.update({str(k).lower(): str(v) for k, v in res["headers"].items()})
            else:
                # Treat entire dict as JSON response
                status_code = 200
                res_body = json.dumps(res)
                res_headers["content-type"] = "application/json; charset=utf-8"
        elif isinstance(res, (list, bool, int, float)) or res is None:
            status_code = 200
            res_body = json.dumps(res)
            res_headers["content-type"] = "application/json; charset=utf-8"
        else:
            status_code = 200
            res_body = str(res)
            res_headers["content-type"] = "text/plain; charset=utf-8"

        body_encoded = res_body.encode("utf-8")
        if "content-length" not in res_headers:
            res_headers["content-length"] = str(len(body_encoded))

        self.send_response(status_code)
        for h_name, h_val in res_headers.items():
            self.send_header(h_name, h_val)
        self.end_headers()
        self.wfile.write(body_encoded)

    def do_GET(self) -> None:
        self._handle_request()

    def do_POST(self) -> None:
        self._handle_request()

    def do_PUT(self) -> None:
        self._handle_request()

    def do_DELETE(self) -> None:
        self._handle_request()

    def do_PATCH(self) -> None:
        self._handle_request()

    def do_OPTIONS(self) -> None:
        self._handle_request()

    def do_HEAD(self) -> None:
        self._handle_request()


class SikharHTTPServerInstance:
    """Manage an HTTP server lifecycle."""

    def __init__(self, interp: Any, port: int, handler_fn: Any, host: str = "127.0.0.1"):
        self.interp = interp
        self.host = host
        self.requested_port = port
        self.handler_fn = handler_fn
        self._server: Optional[HTTPServer] = None
        self._thread: Optional[threading.Thread] = None

        def handler_factory(*args, **kwargs):
            return SikharHTTPRequestHandler(self.interp, self.handler_fn, *args, **kwargs)

        self._server = HTTPServer((self.host, self.requested_port), handler_factory)
        self.port: int = self._server.server_port

    def start_background(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()

    def serve_forever(self) -> None:
        try:
            self._server.serve_forever()
        except KeyboardInterrupt:
            self.stop()

    def stop(self) -> None:
        if self._server:
            self._server.shutdown()
            self._server.server_close()


def create_http_module() -> SikharModule:
    exports = {}

    def _get(interp: Any, args: List[Any], line: int, col: int) -> Dict[str, Any]:
        if not args or len(args) > 3:
            raise SikharTypeError("std.http.get expects (url, [headers], [timeout])", filename=interp.filename, line=line, column=col)
        url = str(args[0])
        headers = _prepare_headers(args[1]) if len(args) >= 2 and args[1] is not None else {}
        timeout = float(args[2]) if len(args) >= 3 else 30.0
        return _perform_request("GET", url, headers=headers, timeout=timeout)

    def _post(interp: Any, args: List[Any], line: int, col: int) -> Dict[str, Any]:
        if not args or len(args) > 4:
            raise SikharTypeError("std.http.post expects (url, [body], [headers], [timeout])", filename=interp.filename, line=line, column=col)
        url = str(args[0])
        body = args[1] if len(args) >= 2 else None
        headers = _prepare_headers(args[2]) if len(args) >= 3 and args[2] is not None else {}
        timeout = float(args[3]) if len(args) >= 4 else 30.0
        return _perform_request("POST", url, body=body, headers=headers, timeout=timeout)

    def _put(interp: Any, args: List[Any], line: int, col: int) -> Dict[str, Any]:
        if not args or len(args) > 4:
            raise SikharTypeError("std.http.put expects (url, [body], [headers], [timeout])", filename=interp.filename, line=line, column=col)
        url = str(args[0])
        body = args[1] if len(args) >= 2 else None
        headers = _prepare_headers(args[2]) if len(args) >= 3 and args[2] is not None else {}
        timeout = float(args[3]) if len(args) >= 4 else 30.0
        return _perform_request("PUT", url, body=body, headers=headers, timeout=timeout)

    def _delete(interp: Any, args: List[Any], line: int, col: int) -> Dict[str, Any]:
        if not args or len(args) > 3:
            raise SikharTypeError("std.http.delete expects (url, [headers], [timeout])", filename=interp.filename, line=line, column=col)
        url = str(args[0])
        headers = _prepare_headers(args[1]) if len(args) >= 2 and args[1] is not None else {}
        timeout = float(args[2]) if len(args) >= 3 else 30.0
        return _perform_request("DELETE", url, headers=headers, timeout=timeout)

    def _patch(interp: Any, args: List[Any], line: int, col: int) -> Dict[str, Any]:
        if not args or len(args) > 4:
            raise SikharTypeError("std.http.patch expects (url, [body], [headers], [timeout])", filename=interp.filename, line=line, column=col)
        url = str(args[0])
        body = args[1] if len(args) >= 2 else None
        headers = _prepare_headers(args[2]) if len(args) >= 3 and args[2] is not None else {}
        timeout = float(args[3]) if len(args) >= 4 else 30.0
        return _perform_request("PATCH", url, body=body, headers=headers, timeout=timeout)

    def _request(interp: Any, args: List[Any], line: int, col: int) -> Dict[str, Any]:
        if len(args) < 2 or len(args) > 5:
            raise SikharTypeError("std.http.request expects (method, url, [body], [headers], [timeout])", filename=interp.filename, line=line, column=col)
        method = str(args[0])
        url = str(args[1])
        body = args[2] if len(args) >= 3 else None
        headers = _prepare_headers(args[3]) if len(args) >= 4 and args[3] is not None else {}
        timeout = float(args[4]) if len(args) >= 5 else 30.0
        return _perform_request(method, url, body=body, headers=headers, timeout=timeout)

    def _server(interp: Any, args: List[Any], line: int, col: int) -> Any:
        if len(args) not in (2, 3):
            raise SikharTypeError("std.http.server expects (port, handler, [host])", filename=interp.filename, line=line, column=col)
        port = int(args[0])
        handler = args[1]
        host = str(args[2]) if len(args) == 3 else "127.0.0.1"

        server_inst = SikharHTTPServerInstance(interp, port, handler, host)
        server_obj = {
            "port": server_inst.port,
            "host": server_inst.host,
            "listen": BuiltinFunction("listen", lambda _i, _a, _l, _c: server_inst.serve_forever()),
            "start": BuiltinFunction("start", lambda _i, _a, _l, _c: server_inst.start_background()),
            "stop": BuiltinFunction("stop", lambda _i, _a, _l, _c: server_inst.stop()),
        }
        return server_obj

    exports["get"] = BuiltinFunction("get", _get, arity=None)
    exports["lyaau"] = exports["get"]

    exports["post"] = BuiltinFunction("post", _post, arity=None)
    exports["pathaau"] = exports["post"]

    exports["put"] = BuiltinFunction("put", _put, arity=None)
    exports["delete"] = BuiltinFunction("delete", _delete, arity=None)
    exports["hatau"] = exports["delete"]

    exports["patch"] = BuiltinFunction("patch", _patch, arity=None)
    exports["request"] = BuiltinFunction("request", _request, arity=None)
    exports["server"] = BuiltinFunction("server", _server, arity=None)

    return SikharModule("std.http", exports)
