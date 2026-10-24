from __future__ import annotations

import io
from collections import OrderedDict

import pytest

from coilmq.util.frames import (
    EmptyBuffer,
    parse_headers,
)


@pytest.mark.parametrize(
    ["frame", "expectation"],
    [
        (
            b"DISCONNECT\n\n\x00",
            ("DISCONNECT", OrderedDict()),
        ),
        (
            b"BEGIN\ntransaction:tx1\n\n\x00",
            ("BEGIN", OrderedDict([("transaction", "tx1")])),
        ),
        # The following case demonstrates https://github.com/coilmq/coilmq/issues/99:
        pytest.param(
            b"SEND\ndestination:/queue/foo\n foo : bar \n\n\x00",
            ("SEND", OrderedDict([("destination", "/queue/foo"), (" foo ", " bar ")])),
            marks=[pytest.mark.xfail],
        ),
    ],
)
def test_parse_headers(
    frame: bytes,
    expectation: tuple[str, OrderedDict[str, str]],
) -> None:
    """Verify that `parse_headers` returns the expected value.

    :param frame: the frame to parse
    :param expectation: the value that `parse_headers` is expected to return

    """
    assert parse_headers(io.BytesIO(frame)) == expectation


@pytest.mark.parametrize(
    ["frame"],
    [
        (b"",),
        (b"\n\n\0",),
    ],
)
def test_parse_headers_empty_buffer(
    frame: bytes,
) -> None:
    """Verify that `parse_headers` raises the expected error.

    :param frame: the frame to parse

    """
    with pytest.raises(EmptyBuffer):
        parse_headers(io.BytesIO(frame))
