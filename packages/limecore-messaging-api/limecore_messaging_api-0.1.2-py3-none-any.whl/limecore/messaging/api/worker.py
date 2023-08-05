from injector import Injector, inject
from typing import List, Type

from .subscriber import Subscriber
from .subscription import Subscription
from .subscription_builder import SubscriptionBuilder


class Worker:
    @inject
    def __init__(self, injector: Injector):
        self._injector = injector
        self._subscriber = Subscriber
        self._subscriptions: List[Subscription] = []

    def register(self, impl):
        return impl(self)

    def run(self):
        subscriber = self._injector.get(self._subscriber)

        # Register the Subscriptions
        for subscription in self._subscriptions:
            subscriber.add_subscription(subscription)

        # Run the Subscriber
        subscriber.run()

    def subscribe_to(self):
        return SubscriptionBuilder(self._add_subscription)

    def using_subscriber(self, subscriber: Type[Subscriber]):
        self._subscriber = subscriber

        return self

    def _add_subscription(self, subscription: Subscription):
        self._subscriptions.append(subscription)

        return self
