from importlib import import_module
from typing import Any, Callable, Dict, Optional

from .serializer import Serializer


class GenericSerializer(Serializer):
    def can_deserialize(self, json: Dict[str, Any]) -> bool:
        return (
            "__type__" in json and self._get_klass_loader(json["__type__"]) is not None
        )

    def can_serialize(self, obj: object) -> bool:
        return hasattr(obj, "__dict__")

    def deserialize(self, json: Dict[str, Any]) -> object:
        assert self.can_deserialize(json)

        klass_loader = self._get_klass_loader(json["__type__"])

        assert klass_loader is not None

        return klass_loader(json["__data__"])

    def serialize(self, obj: object) -> Dict[str, Any]:
        assert self.can_serialize(obj)

        return {
            "__type__": "%s.%s" % (obj.__class__.__module__, obj.__class__.__name__),
            "__data__": obj.__dict__,
        }

    def _get_klass_loader(self, name: str) -> Optional[Callable[[str], object]]:
        module_name, type_name = name.rsplit(".", 1)

        # Import the Specified module
        module = import_module(module_name)

        # Find the Type from inside the module
        klass = getattr(module, type_name)

        # Get the from_dict Method from the Type
        return getattr(klass, "from_dict") if hasattr(klass, "from_dict") else None
