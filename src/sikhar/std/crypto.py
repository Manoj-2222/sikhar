"""
Sikhar Standard Library: std.crypto
Cryptographic hashing, HMAC signatures, Base64 encoding, and secure random token generation.
"""

import base64
import hashlib
import hmac
import secrets
from typing import Any, List

from ..interpreter.values import BuiltinFunction, SikharModule
from ..errors.error_types import SikharTypeError, SikharRuntimeError


def create_crypto_module() -> SikharModule:
    exports = {}

    def _sha256(interp: Any, args: List[Any], line: int, col: int) -> str:
        if len(args) != 1 or not isinstance(args[0], (str, bytes)):
            raise SikharTypeError("std.crypto.sha256 expects 1 string argument", filename=interp.filename, line=line, column=col)
        data = args[0].encode("utf-8") if isinstance(args[0], str) else args[0]
        return hashlib.sha256(data).hexdigest()

    def _sha512(interp: Any, args: List[Any], line: int, col: int) -> str:
        if len(args) != 1 or not isinstance(args[0], (str, bytes)):
            raise SikharTypeError("std.crypto.sha512 expects 1 string argument", filename=interp.filename, line=line, column=col)
        data = args[0].encode("utf-8") if isinstance(args[0], str) else args[0]
        return hashlib.sha512(data).hexdigest()

    def _md5(interp: Any, args: List[Any], line: int, col: int) -> str:
        if len(args) != 1 or not isinstance(args[0], (str, bytes)):
            raise SikharTypeError("std.crypto.md5 expects 1 string argument", filename=interp.filename, line=line, column=col)
        data = args[0].encode("utf-8") if isinstance(args[0], str) else args[0]
        return hashlib.md5(data).hexdigest()

    def _hmac_sha256(interp: Any, args: List[Any], line: int, col: int) -> str:
        if len(args) != 2:
            raise SikharTypeError("std.crypto.hmac_sha256 expects 2 arguments: (key, message)", filename=interp.filename, line=line, column=col)
        key = str(args[0]).encode("utf-8")
        msg = str(args[1]).encode("utf-8")
        return hmac.new(key, msg, hashlib.sha256).hexdigest()

    def _base64_encode(interp: Any, args: List[Any], line: int, col: int) -> str:
        if len(args) != 1:
            raise SikharTypeError("std.crypto.base64_encode expects 1 argument", filename=interp.filename, line=line, column=col)
        data = str(args[0]).encode("utf-8")
        return base64.b64encode(data).decode("ascii")

    def _base64_decode(interp: Any, args: List[Any], line: int, col: int) -> str:
        if len(args) != 1 or not isinstance(args[0], str):
            raise SikharTypeError("std.crypto.base64_decode expects 1 base64 string", filename=interp.filename, line=line, column=col)
        try:
            raw = base64.b64decode(args[0].encode("ascii"))
            return raw.decode("utf-8", errors="replace")
        except Exception as e:
            raise SikharRuntimeError(f"Base64 decode error: {e}", filename=interp.filename, line=line, column=col)

    def _random_bytes(interp: Any, args: List[Any], line: int, col: int) -> str:
        count = int(args[0]) if args and isinstance(args[0], int) else 16
        return secrets.token_hex(count)

    def _random_token(interp: Any, args: List[Any], line: int, col: int) -> str:
        length = int(args[0]) if args and isinstance(args[0], int) else 32
        return secrets.token_urlsafe(length)

    exports["sha256"] = BuiltinFunction("sha256", _sha256, arity=1)
    exports["sha512"] = BuiltinFunction("sha512", _sha512, arity=1)
    exports["md5"] = BuiltinFunction("md5", _md5, arity=1)
    exports["hmac_sha256"] = BuiltinFunction("hmac_sha256", _hmac_sha256, arity=2)
    exports["base64_encode"] = BuiltinFunction("base64_encode", _base64_encode, arity=1)
    exports["base64_decode"] = BuiltinFunction("base64_decode", _base64_decode, arity=1)
    exports["random_bytes"] = BuiltinFunction("random_bytes", _random_bytes, arity=None)
    exports["random_token"] = BuiltinFunction("random_token", _random_token, arity=None)

    # Nepali aliases
    exports["hashing"] = exports["sha256"]
    exports["gupta"] = exports["hmac_sha256"]
    exports["chinno"] = exports["random_token"]

    return SikharModule("std.crypto", exports)
