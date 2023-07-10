from datetime import datetime
from main import convert_timestamp


def test_convert_timestamp():
    timestamp = 1688077800000
    assert convert_timestamp(timestamp) == datetime(year=2023,
                                                    month=6,
                                                    day=30,
                                                    hour=00,
                                                    minute=30,
                                                    second=00)
