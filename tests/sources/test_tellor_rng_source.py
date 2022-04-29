from datetime import datetime
from unittest import mock

import pytest
import requests

from telliot_feed_examples.sources import blockhash_aggregator
from telliot_feed_examples.sources.blockhash_aggregator import TellorRNGManualSource


@pytest.mark.asyncio
async def test_rng():
    """Retrieve random number."""
    blockhash_aggregator.input = lambda: "1649769707"  # BCT block num: 731547
    rng_source = TellorRNGManualSource()
    v, t = await rng_source.fetch_new_datapoint()

    assert v == (
        b"Ad\x81\xc2\x9d\xab\x8a\xf6\x8fN^\xcd\xb9g\xdf{"
        b"\xeap\xe4\xf8\xf2\xab\x89\xcb\xb0\xe6\x8cGR\x18\xf2+"
    )

    assert isinstance(v, bytes)
    assert isinstance(t, datetime)


@pytest.mark.asyncio
async def test_rng_failures(caplog):
    """Simulate API failures."""
    blockhash_aggregator.input = lambda: "1649769707"

    def conn_timeout(url, *args, **kwargs):
        raise requests.exceptions.ConnectTimeout()

    with mock.patch("requests.Session.get", side_effect=conn_timeout):
        rng_source = TellorRNGManualSource()
        v, t = await rng_source.fetch_new_datapoint()
        assert v is None
        assert t is None
        assert "Connection timeout" in caplog.text
