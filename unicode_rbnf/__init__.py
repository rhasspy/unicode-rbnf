from pathlib import Path

from .engine import FormatOptions, FormatPurpose, FormatResult, RbnfEngine

_DIR = Path(__file__).parent

__version__ = (_DIR / "VERSION").read_text(encoding="utf-8").strip()

__all__ = [
    "__version__",
    "FormatOptions",
    "FormatPurpose",
    "FormatResult",
    "RbnfEngine",
]
