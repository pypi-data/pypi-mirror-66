from .subscription import Subscription


class Subscriber:
    def add_subscription(self, subscription: Subscription):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()
