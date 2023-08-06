from .serializers import SERIALIZERS


class JsonDecoder:
    @classmethod
    def decode(cls, json: dict) -> object:
        if "__type__" in json:
            for serializer in SERIALIZERS:
                if serializer.can_deserialize(json):
                    return serializer.deserialize(json)

            raise RuntimeError("Unknown Serialized Type: %s" % (json["__type__"]))

        return json
