from .message import Message


class Handler:
    def handle_message(self, msg: Message):
        raise NotImplementedError()
