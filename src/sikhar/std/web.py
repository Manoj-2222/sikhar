"""
Sikhar Standard Library: std.web
Official Sikhar Web Framework with routing, middleware, params, and static files.
"""

import json
import re
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
from urllib.parse import urlparse, parse_qs

from ..interpreter.values import BuiltinFunction, SikharModule, is_truthy
from ..errors.error_types import SikharTypeError
from .http import SikharHTTPServerInstance


def _compile_route_pattern(pattern: str) -> Tuple[re.Pattern, List[str]]:
    """Convert an express-like route pattern (/users/:id) to a compiled regex."""
    parts = pattern.strip("/").split("/") if pattern.strip("/") else []
    param_names = []
    regex_parts = []

    for part in parts:
        if part.startswith(":") and len(part) > 1:
            name = part[1:]
            param_names.append(name)
            regex_parts.append(f"(?P<{name}>[^/]+)")
        elif part.startswith("{") and part.endswith("}"):
            name = part[1:-1]
            param_names.append(name)
            regex_parts.append(f"(?P<{name}>[^/]+)")
        elif part == "*":
            param_names.append("wildcard")
            regex_parts.append("(?P<wildcard>.*)")
        else:
            regex_parts.append(re.escape(part))

    if not regex_parts:
        regex_str = r"^/?$"
    else:
        regex_str = r"^/" + r"/".join(regex_parts) + r"/?$"

    return re.compile(regex_str), param_names


class WebApp:
    """Official Sikhar Web Framework Application engine."""

    def __init__(self, interp: Any):
        self.interp = interp
        self.routes: List[Dict[str, Any]] = []
        self.middlewares: List[Any] = []
        self.static_mounts: List[Tuple[str, Path]] = []
        self._server_instance: Optional[SikharHTTPServerInstance] = None

    def add_route(self, method: str, pattern: str, handler: Any) -> None:
        regex, param_names = _compile_route_pattern(pattern)
        self.routes.append({
            "method": method.upper(),
            "pattern": pattern,
            "regex": regex,
            "param_names": param_names,
            "handler": handler,
        })

    def use(self, middleware_fn: Any) -> None:
        self.middlewares.append(middleware_fn)

    def static(self, prefix: str, dir_path: str) -> None:
        clean_prefix = "/" + prefix.strip("/")
        self.static_mounts.append((clean_prefix, Path(dir_path).resolve()))

    def _match_static(self, path: str) -> Optional[Dict[str, Any]]:
        for prefix, directory in self.static_mounts:
            if path == prefix or path.startswith(prefix + "/"):
                rel_path = path[len(prefix):].lstrip("/")
                if not rel_path:
                    rel_path = "index.html"
                file_path = (directory / rel_path).resolve()
                # Security check: prevent directory traversal
                if directory not in file_path.parents and file_path != directory:
                    return {"status": 403, "body": "Forbidden", "headers": {"content-type": "text/plain"}}
                if file_path.exists() and file_path.is_file():
                    content_type = "text/plain; charset=utf-8"
                    sfx = file_path.suffix.lower()
                    if sfx in (".html", ".htm"):
                        content_type = "text/html; charset=utf-8"
                    elif sfx == ".css":
                        content_type = "text/css; charset=utf-8"
                    elif sfx == ".js":
                        content_type = "application/javascript; charset=utf-8"
                    elif sfx == ".json":
                        content_type = "application/json; charset=utf-8"
                    elif sfx in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"):
                        content_type = f"image/{sfx.lstrip('.')}"

                    try:
                        content = file_path.read_text(encoding="utf-8")
                        return {"status": 200, "body": content, "headers": {"content-type": content_type}}
                    except UnicodeDecodeError:
                        return {"status": 500, "body": "Binary static file read not supported in text mode"}
        return None

    def handle(self, raw_req: Dict[str, Any]) -> Dict[str, Any]:
        raw_path = raw_req.get("path") or raw_req.get("url") or "/"
        parsed_url = urlparse(raw_path)
        path = parsed_url.path or "/"
        query_dict = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(parsed_url.query).items()}
        method = str(raw_req.get("method", "GET")).upper()
        headers = {str(k).lower(): str(v) for k, v in raw_req.get("headers", {}).items()}
        body = raw_req.get("body", "")

        # Auto-parse JSON body if content-type is json
        parsed_json_body = None
        if isinstance(body, str) and body.strip():
            try:
                parsed_json_body = json.loads(body)
            except Exception:
                parsed_json_body = None

        req_ctx = {
            "method": method,
            "path": path,
            "url": raw_path,
            "query": query_dict,
            "params": {},
            "headers": headers,
            "body": body,
            "data": parsed_json_body,
        }

        # 1. Execute middlewares
        for mw in self.middlewares:
            try:
                if hasattr(mw, "call"):
                    mw_res = mw.call(self.interp, [req_ctx], 1, 1)
                elif callable(mw):
                    mw_res = mw(req_ctx)
                else:
                    mw_res = None
            except Exception as e:
                return {"status": 500, "body": f"Middleware error: {e}", "headers": {"content-type": "text/plain"}}

            if mw_res is not None:
                # Middleware returned an early response
                return self._normalize_response(mw_res)

        # 2. Check static file mounts
        if method in ("GET", "HEAD"):
            static_res = self._match_static(path)
            if static_res is not None:
                return static_res

        # 3. Match routes
        for route in self.routes:
            if route["method"] != "ALL" and route["method"] != method:
                continue
            m = route["regex"].match(path)
            if m:
                req_ctx["params"] = m.groupdict()
                handler = route["handler"]
                try:
                    if hasattr(handler, "call"):
                        res = handler.call(self.interp, [req_ctx], 1, 1)
                    elif callable(handler):
                        res = handler(req_ctx)
                    else:
                        return {"status": 500, "body": "Route handler is not callable"}
                    return self._normalize_response(res)
                except Exception as e:
                    return {
                        "status": 500,
                        "body": f"Route error in {method} {path}: {e}",
                        "headers": {"content-type": "text/plain"},
                    }

        # 4. 404 Not Found
        return {
            "status": 404,
            "body": f"Not Found: {method} {path}",
            "headers": {"content-type": "text/plain"},
        }

    def _normalize_response(self, res: Any) -> Dict[str, Any]:
        if isinstance(res, dict):
            if "status" in res and "body" in res:
                status = int(res["status"])
                body = res["body"]
                headers = dict(res.get("headers", {}))
                if isinstance(body, (dict, list)):
                    body = json.dumps(body)
                    if "content-type" not in headers:
                        headers["content-type"] = "application/json; charset=utf-8"
                elif not isinstance(body, str):
                    body = str(body)
                if "content-type" not in headers:
                    headers["content-type"] = "text/plain; charset=utf-8"
                return {"status": status, "body": body, "headers": headers}
            else:
                # Treat dictionary as JSON
                return {
                    "status": 200,
                    "body": json.dumps(res),
                    "headers": {"content-type": "application/json; charset=utf-8"},
                }
        elif isinstance(res, list):
            return {
                "status": 200,
                "body": json.dumps(res),
                "headers": {"content-type": "application/json; charset=utf-8"},
            }
        elif res is None:
            return {"status": 204, "body": "", "headers": {}}
        else:
            body_str = str(res)
            is_html = body_str.strip().startswith("<") and body_str.strip().endswith(">")
            c_type = "text/html; charset=utf-8" if is_html else "text/plain; charset=utf-8"
            return {"status": 200, "body": body_str, "headers": {"content-type": c_type}}

    def listen(self, port: int, host: str = "127.0.0.1") -> None:
        self._server_instance = SikharHTTPServerInstance(self.interp, port, self.handle, host)
        print(f"Sikhar Web Server listening on http://{host}:{self._server_instance.port}")
        self._server_instance.serve_forever()

    def start_background(self, port: int = 0, host: str = "127.0.0.1") -> int:
        self._server_instance = SikharHTTPServerInstance(self.interp, port, self.handle, host)
        self._server_instance.start_background()
        return self._server_instance.port

    def stop(self) -> None:
        if self._server_instance:
            self._server_instance.stop()


def create_web_module() -> SikharModule:
    exports = {}

    def _create_app(interp: Any, args: List[Any], line: int, col: int) -> Dict[str, Any]:
        app = WebApp(interp)

        def _get(_i: Any, a: List[Any], l: int, c: int) -> Any:
            if len(a) != 2:
                raise SikharTypeError("app.get expects 2 arguments: (path, handler)", filename=interp.filename, line=l, column=c)
            app.add_route("GET", str(a[0]), a[1])
            return None

        def _post(_i: Any, a: List[Any], l: int, c: int) -> Any:
            if len(a) != 2:
                raise SikharTypeError("app.post expects 2 arguments: (path, handler)", filename=interp.filename, line=l, column=c)
            app.add_route("POST", str(a[0]), a[1])
            return None

        def _put(_i: Any, a: List[Any], l: int, c: int) -> Any:
            if len(a) != 2:
                raise SikharTypeError("app.put expects 2 arguments: (path, handler)", filename=interp.filename, line=l, column=c)
            app.add_route("PUT", str(a[0]), a[1])
            return None

        def _delete(_i: Any, a: List[Any], l: int, c: int) -> Any:
            if len(a) != 2:
                raise SikharTypeError("app.delete expects 2 arguments: (path, handler)", filename=interp.filename, line=l, column=c)
            app.add_route("DELETE", str(a[0]), a[1])
            return None

        def _patch(_i: Any, a: List[Any], l: int, c: int) -> Any:
            if len(a) != 2:
                raise SikharTypeError("app.patch expects 2 arguments: (path, handler)", filename=interp.filename, line=l, column=c)
            app.add_route("PATCH", str(a[0]), a[1])
            return None

        def _all(_i: Any, a: List[Any], l: int, c: int) -> Any:
            if len(a) != 2:
                raise SikharTypeError("app.all expects 2 arguments: (path, handler)", filename=interp.filename, line=l, column=c)
            app.add_route("ALL", str(a[0]), a[1])
            return None

        def _use(_i: Any, a: List[Any], l: int, c: int) -> Any:
            if len(a) != 1:
                raise SikharTypeError("app.use expects 1 middleware function", filename=interp.filename, line=l, column=c)
            app.use(a[0])
            return None

        def _static(_i: Any, a: List[Any], l: int, c: int) -> Any:
            if len(a) != 2:
                raise SikharTypeError("app.static expects 2 arguments: (url_prefix, directory_path)", filename=interp.filename, line=l, column=c)
            app.static(str(a[0]), str(a[1]))
            return None

        def _handle(_i: Any, a: List[Any], l: int, c: int) -> Dict[str, Any]:
            if len(a) != 1 or not isinstance(a[0], dict):
                raise SikharTypeError("app.handle expects 1 request map argument", filename=interp.filename, line=l, column=c)
            return app.handle(a[0])

        def _listen(_i: Any, a: List[Any], l: int, c: int) -> Any:
            if not a or len(a) > 2:
                raise SikharTypeError("app.listen expects (port, [host])", filename=interp.filename, line=l, column=c)
            port = int(a[0])
            host = str(a[1]) if len(a) == 2 else "127.0.0.1"
            app.listen(port, host)
            return None

        def _start(_i: Any, a: List[Any], l: int, c: int) -> int:
            port = int(a[0]) if a else 0
            host = str(a[1]) if len(a) >= 2 else "127.0.0.1"
            return app.start_background(port, host)

        def _stop(_i: Any, a: List[Any], l: int, c: int) -> Any:
            app.stop()
            return None

        return {
            "get": BuiltinFunction("get", _get, arity=2),
            "post": BuiltinFunction("post", _post, arity=2),
            "put": BuiltinFunction("put", _put, arity=2),
            "delete": BuiltinFunction("delete", _delete, arity=2),
            "patch": BuiltinFunction("patch", _patch, arity=2),
            "all": BuiltinFunction("all", _all, arity=2),
            "use": BuiltinFunction("use", _use, arity=1),
            "static": BuiltinFunction("static", _static, arity=2),
            "handle": BuiltinFunction("handle", _handle, arity=1),
            "listen": BuiltinFunction("listen", _listen, arity=None),
            "start": BuiltinFunction("start", _start, arity=None),
            "stop": BuiltinFunction("stop", _stop, arity=0),
        }

    exports["app"] = BuiltinFunction("app", _create_app, arity=0)
    exports["new_app"] = exports["app"]

    return SikharModule("std.web", exports)
