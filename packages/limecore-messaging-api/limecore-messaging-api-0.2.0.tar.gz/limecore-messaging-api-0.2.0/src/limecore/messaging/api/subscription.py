from typing import Type

from .handler import Handler


class Subscription:
    def __init__(self, handler: Type[Handler], queue: str, routing_key: str):
        self._handler = handler
        self._queue = queue
        self._routing_key = routing_key

    @property
    def handler(self):
        return self._handler

    @property
    def queue(self):
        return self._queue

    @property
    def routing_key(self):
        return self._routing_key
