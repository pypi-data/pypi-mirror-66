from limecore.util import T
from typing import Callable, Optional, Type

from .handler import Handler
from .subscription import Subscription


class SubscriptionBuilder:
    def __init__(self, callback: Callable[[Subscription], T]):
        self._callback = callback
        self._handler: Optional[Type[Handler]] = None
        self._queue: Optional[str] = None
        self._routing_key: Optional[str] = None

    def implemented_by(self, handler: Type[Handler]):
        self._handler = handler

        return self._self_or_parent()

    def routing_key(self, routing_key: str):
        self._routing_key = routing_key

        return self._self_or_parent()

    def using_queue(self, queue: str):
        self._queue = queue

        return self._self_or_parent()

    def _self_or_parent(self):
        if self._handler and self._queue and self._routing_key:
            return self._callback(
                Subscription(self._handler, self._queue, self._routing_key)
            )
        else:
            return self
