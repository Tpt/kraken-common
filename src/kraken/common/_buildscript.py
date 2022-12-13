import enum
from concurrent.futures import Future
from contextlib import contextmanager
from dataclasses import dataclass, field
from threading import local
from typing import Iterator, List, Sequence


@dataclass
class BuildscriptMetadata:
    """
    Metadata for a Kraken build and its runtime environment.
    """

    index_url: "str | None" = None
    extra_index_urls: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
    additional_sys_paths: List[str] = field(default_factory=list)

    def requires(self, requirement: str) -> None:
        self.requirements.append(requirement)

    def extra_index_url(self, url: str) -> None:
        self.extra_index_urls.append(url)

    def additional_sys_path(self, path: str) -> None:
        self.additional_sys_paths.append(path)

    @staticmethod
    @contextmanager
    def capture() -> Iterator["Future[BuildscriptMetadata]"]:
        """
        A context manager that will ensure calling :func:`metadata` will raise a :class:`KrakenMetadataException` and
        catch that exception to return the metadata.
        """

        future: "Future[BuildscriptMetadata]" = Future()
        _global.mode = _Mode.RAISE
        try:
            yield future
        except BuildscriptMetadataException as exc:
            future.set_result(exc.metadata)
        else:
            exception = RuntimeError("No KrakenMetadataException was raised, did metadata() get called?")
            future.set_exception(exception)
            raise exception
        finally:
            _global.mode = _Mode.PASSTHROUGH


class BuildscriptMetadataException(BaseException):
    """
    This exception is raised by the :func:`metadata` function.
    """

    def __init__(self, metadata: BuildscriptMetadata) -> None:
        self.metadata = metadata

    def __str__(self) -> str:
        return (
            "If you are seeing this message, something has gone wrong with catching the exception. This "
            "exception is used to abort and transfer Kraken metadata to the caller."
        )


class _Mode(enum.Enum):
    PASSTHROUGH = 0
    RAISE = 1


class _ModeGlobal(local):
    mode: _Mode = _Mode.PASSTHROUGH


_global = _ModeGlobal()


def buildscript(
    *,
    index_url: "str | None" = None,
    extra_index_urls: "Sequence[str] | None" = None,
    requirements: "Sequence[str] | None" = None,
    additional_sys_paths: "Sequence[str] | None" = None,
) -> BuildscriptMetadata:
    """
    This function creates a :class:`BuildscriptMetadata` object and returns it.

    When called from inside the context of :meth:`BuildscriptMetadata.capture()`, the function raises a
    :class:`BuildscriptMetadataException` instead.
    """

    metadata = BuildscriptMetadata(
        index_url=index_url,
        extra_index_urls=list(extra_index_urls or ()),
        requirements=list(requirements or ()),
        additional_sys_paths=list(additional_sys_paths or ()),
    )

    if _global.mode == _Mode.RAISE:
        raise BuildscriptMetadataException(metadata)

    return metadata
