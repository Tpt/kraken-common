from datetime import datetime, timezone

from kraken.common._date import date_to_iso8601, iso8601_to_date


def test__date_to_iso8601() -> None:
    assert date_to_iso8601(datetime(2022, 12, 6, 12, 5, 32, 103)) == "2022-12-06T12:05:32.000103"
    assert (
        date_to_iso8601(datetime(2022, 12, 6, 12, 5, 32, 103, tzinfo=timezone.utc)) == "2022-12-06T12:05:32.000103+0000"
    )


def test__iso8601_to_date() -> None:
    assert iso8601_to_date("2022-12-06T12:05:32.000103") == datetime(2022, 12, 6, 12, 5, 32, 103)
    assert iso8601_to_date("2022-12-06T12:05:32.000103+0000") == datetime(
        2022, 12, 6, 12, 5, 32, 103, tzinfo=timezone.utc
    )
