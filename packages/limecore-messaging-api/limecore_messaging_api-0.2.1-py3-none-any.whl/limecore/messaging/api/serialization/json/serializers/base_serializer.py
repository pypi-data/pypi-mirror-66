from typing import Any, Dict, Union

from .serializer import Serializer


class BaseSerializer(Serializer):
    def __init__(self, type: type):
        self.__key = "%s.%s" % (type.__module__, type.__qualname__)
        self.__type = type

    def can_deserialize(self, json: dict) -> bool:
        return "__type__" in json and json["__type__"] == self.__key

    def can_serialize(self, obj: object) -> bool:
        return isinstance(obj, self.__type)

    def deserialize(self, json: dict) -> object:
        assert self.can_deserialize(json)

        return self._deserialize(json["__data__"])

    def serialize(self, obj: object) -> dict:
        assert self.can_serialize(obj)

        return {"__type__": self.__key, "__data__": self._serialize(obj)}

    def _deserialize(self, data: Union[Dict[str, Any], str]) -> object:
        raise NotImplementedError()

    def _serialize(self, obj: object) -> str:
        raise NotImplementedError()
