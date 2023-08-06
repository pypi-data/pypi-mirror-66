class Serializer:
    def can_deserialize(self, json: dict) -> bool:
        raise NotImplementedError()

    def can_serialize(self, obj: object) -> bool:
        raise NotImplementedError()

    def deserialize(self, json: dict) -> object:
        raise NotImplementedError()

    def serialize(self, obj: object) -> dict:
        raise NotImplementedError()
