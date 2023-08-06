from typing import Any, Dict
from uuid import UUID, uuid4

from .serialization.json import from_json, to_json


class Message:
    def __init__(self, message_id: UUID, **kwargs):
        self._message_id = message_id
        self._body = kwargs

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]):
        return cls(message_id=dict["message_id"], **dict["body"])

    @classmethod
    def from_json(cls, data: str):
        return from_json(data)

    @classmethod
    def obtain(cls, *args, **kwargs):
        return cls(*args, **kwargs, message_id=uuid4())

    @property
    def message_id(self):
        return self._message_id

    @property
    def routing_key(self):
        raise NotImplementedError()

    def to_json(self):
        return to_json(self)

    @property
    def __dict__(self):
        return {
            "body": self._body,
            "message_id": self.message_id,
            "routing_key": self.routing_key,
        }

    def __str__(self):
        return str(self.__dict__)
