"""
Sikhar Standard Library Registry
"""

from typing import Optional, Dict
from ..interpreter.values import SikharModule
from .math import create_math_module
from .text import create_text_module
from .list import create_list_module
from .map import create_map_module
from .time import create_time_module
from .file import create_file_module
from .system import create_system_module

_STD_CACHE: Dict[str, SikharModule] = {}


def get_std_module(name: str) -> Optional[SikharModule]:
    """Retrieve or instantiate a standard library module."""
    clean_name = name.strip()
    if clean_name.startswith("std."):
        clean_name = clean_name[4:]

    if clean_name in _STD_CACHE:
        return _STD_CACHE[clean_name]

    module: Optional[SikharModule] = None

    if clean_name == "math":
        module = create_math_module()
    elif clean_name == "text":
        module = create_text_module()
    elif clean_name == "list":
        module = create_list_module()
    elif clean_name == "map":
        module = create_map_module()
    elif clean_name == "time":
        module = create_time_module()
    elif clean_name == "file":
        module = create_file_module()
    elif clean_name == "system":
        module = create_system_module()
    elif clean_name in ("std", ""):
        # Aggregated root std module
        root_exports = {
            "math": get_std_module("math"),
            "text": get_std_module("text"),
            "list": get_std_module("list"),
            "map": get_std_module("map"),
            "time": get_std_module("time"),
            "file": get_std_module("file"),
            "system": get_std_module("system"),
        }
        module = SikharModule("std", root_exports)

    if module is not None:
        _STD_CACHE[clean_name] = module

    return module


__all__ = ["get_std_module"]
