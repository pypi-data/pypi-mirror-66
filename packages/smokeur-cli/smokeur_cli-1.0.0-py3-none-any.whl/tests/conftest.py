"""
Tests configuration
"""
import pytest


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "match_on": ["method", "scheme", "host", "port", "path", "query", "body"],
        "filter_headers": [("authorization", "DUMMY")],
    }
