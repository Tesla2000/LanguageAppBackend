import importlib
from pathlib import Path

__all__ = [
    module.name.partition(".")[0]
    for module in Path(__file__).parent.iterdir()
    if module.name not in ("__init__.py", "pycache") and not module.name.startswith("_")
]
tuple(importlib.import_module("." + module, __name__) for module in __all__)
