import enum
from concurrent.futures import Future
from contextlib import contextmanager
from dataclasses import dataclass, field
from threading import local
from typing import Iterator, List, Sequence


@dataclass
class KrakenMetadata:
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
    def capture() -> Iterator["Future[KrakenMetadata]"]:
        """
        A context manager that will ensure calling :func:`metadata` will raise a :class:`KrakenMetadataException` and
        catch that exception to return the metadata.
        """

        future: "Future[KrakenMetadata]" = Future()
        _metadata_mode.mode = MetadataMode.RAISE
        try:
            yield future
        except KrakenMetadataException as exc:
            future.set_result(exc.metadata)
        else:
            exception = RuntimeError("No KrakenMetadataException was raised, did metadata() get called?")
            future.set_exception(exception)
            raise exception
        finally:
            _metadata_mode.mode = MetadataMode.PASSTHROUGH


class KrakenMetadataException(BaseException):
    """
    This exception is raised by the :func:`metadata` function.
    """

    def __init__(self, metadata: KrakenMetadata) -> None:
        self.metadata = metadata

    def __str__(self) -> str:
        return (
            "If you are seeing this message, something has gone wrong with catching the exception. This "
            "exception is used to abort and transfer Kraken metadata to the caller."
        )


class MetadataMode(enum.Enum):
    PASSTHROUGH = 0
    RAISE = 1


class _MetadataModelGlobal(local):
    mode: MetadataMode = MetadataMode.PASSTHROUGH


_metadata_mode = _MetadataModelGlobal()


def metadata(
    *,
    index_url: "str | None" = None,
    extra_index_urls: "Sequence[str] | None" = None,
    requirements: "Sequence[str] | None" = None,
    additional_sys_paths: "Sequence[str] | None" = None,
) -> KrakenMetadata:
    """
    This function creates a :class:`KrakenMetadata` object and returns it. If :func:`get_metadata_mode` returns
    :data:`MetadataMode.RAISE`, the function raises a :class:`KrakenMetadataException`. Otherwise, the metadata
    object is returned.
    """

    metadata = KrakenMetadata(
        index_url=index_url,
        extra_index_urls=list(extra_index_urls or ()),
        requirements=list(requirements or ()),
        additional_sys_paths=list(additional_sys_paths or ()),
    )

    if _metadata_mode.mode == MetadataMode.RAISE:
        raise KrakenMetadataException(metadata)

    return metadata
