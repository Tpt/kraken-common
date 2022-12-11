from ._fs import atomic_file_swap, safe_rmpath
from ._metadata import KrakenMetadata, KrakenMetadataException, metadata, metadata_capturing
from ._text import inline_text, lazy_str, pluralize

__all__ = [
    # _fs
    "atomic_file_swap",
    "safe_rmpath",
    # _metadata
    "metadata",
    "metadata_capturing",
    "KrakenMetadata",
    "KrakenMetadataException",
    # _text
    "pluralize",
    "inline_text",
    "lazy_str",
]
__version__ = "0.1.0"
