from json import JSONEncoder as _JSONEncoder

from .serializers import SERIALIZERS


class JsonEncoder(_JSONEncoder):
    def default(self, obj: object) -> object:
        for serializer in reversed(SERIALIZERS):
            if serializer.can_serialize(obj):
                return serializer.serialize(obj)

        return _JSONEncoder.default(self, obj)
