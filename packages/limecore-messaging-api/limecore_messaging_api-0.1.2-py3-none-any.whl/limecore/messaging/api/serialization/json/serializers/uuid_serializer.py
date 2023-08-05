from typing import Any, Dict, Union
from uuid import UUID

from .base_serializer import BaseSerializer


class UUIDSerializer(BaseSerializer):
    def __init__(self):
        BaseSerializer.__init__(self, UUID)

    def _deserialize(self, json: Union[Dict[str, Any], str]) -> UUID:
        assert isinstance(json, str)

        return UUID(json)

    def _serialize(self, obj: object) -> str:
        assert isinstance(obj, UUID)

        return str(obj)
