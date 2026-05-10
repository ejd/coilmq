from __future__ import annotations

from typing import TYPE_CHECKING, Generator

import pytest

from coilmq.engine import StompEngine
from tests.mock import (
    MockConnection,
    MockQueueManager,
    MockTopicManager,
)

if TYPE_CHECKING:
    from coilmq.protocol import STOMP11, STOMP12


@pytest.fixture
def engine(protocol: type[STOMP11 | STOMP12]) -> Generator[StompEngine, None, None]:
    engine = StompEngine(
        connection=MockConnection(),
        queue_manager=MockQueueManager(),
        topic_manager=MockTopicManager(),
        authenticator=None,
        protocol=protocol,
    )

    try:
        yield engine
    finally:
        engine.unbind()
