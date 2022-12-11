from kraken.common._metadata import KrakenMetadata, metadata


def test_capture_kraken_metadata() -> None:
    assert metadata() == KrakenMetadata()
    assert metadata(index_url="http://foo/simple") == KrakenMetadata(index_url="http://foo/simple")
    assert metadata(requirements=["a"]) == KrakenMetadata(requirements=["a"])
    assert metadata(extra_index_urls=["b"]) == KrakenMetadata(extra_index_urls=["b"])

    with KrakenMetadata.capture() as future:
        metadata(index_url="c")

    assert future.result() == KrakenMetadata(index_url="c")
