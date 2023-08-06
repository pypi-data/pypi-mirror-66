from .message import Message


class Publisher:
    def publish(self, msg: Message, routing_key: str, mandatory: bool = False) -> None:
        raise NotImplementedError()
