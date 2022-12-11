from . import path
from ._fs import atomic_file_swap, safe_rmpath
from ._generic import flatten, not_none
from ._metadata import KrakenMetadata, KrakenMetadataException, metadata, metadata_capturing
from ._terminal import get_terminal_width
from ._text import inline_text, lazy_str, pluralize

__all__ = [
    # _fs
    "atomic_file_swap",
    "safe_rmpath",
    # _generic
    "flatten",
    "not_none",
    # _importlib
    "import_class",
    "appending_to_sys_path",
    # _metadata
    "metadata",
    "metadata_capturing",
    "KrakenMetadata",
    "KrakenMetadataException",
    # _terminal
    "get_terminal_width",
    # _text
    "pluralize",
    "inline_text",
    "lazy_str",
    # global
    "path",
]
__version__ = "0.1.0"
