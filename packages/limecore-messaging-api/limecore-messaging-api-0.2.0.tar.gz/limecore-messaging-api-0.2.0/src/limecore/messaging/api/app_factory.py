import re

from argparse import ArgumentParser
from injector import Module, provider, singleton
from limecore.core.configuration import Configuration
from types import ModuleType
from typing import Dict, List, Type

from .app import App
from .handler import Handler
from .worker import Worker


class AppFactory(Module):
    def __init__(self, profile: str = "default"):
        self._handlers: Dict[str, Type[Handler]] = {}
        self._profile = profile

    def add(self, module: ModuleType) -> "AppFactory":
        for name in module.__all__:
            obj = getattr(module, name)

            if issubclass(obj, Handler):
                self._handlers[f"{module.__name__}.{name}"] = obj

        return self

    def create_argument_parser(self, argument_parser: ArgumentParser):
        return argument_parser

    @singleton
    @provider
    def provide_app(self, configuration: Configuration, worker: Worker) -> App:
        patterns = self._build_patterns(configuration)

        for name, handler in self._handlers.items():
            if any(p.match(name) for p in patterns):
                for message_type in handler.handles:
                    worker.subscribe_to().routing_key(
                        message_type.routing_key
                    ).implemented_by(handler).using_queue(handler.queue)

        return App(worker)

    def _build_pattern(self, pattern: str) -> re.Pattern:
        return re.compile(f"^{pattern.replace('*', '.*')}")

    def _build_patterns(self, configuration: Configuration) -> List[re.Pattern]:
        profile = configuration.section(
            "limecore", "messaging", "profiles", self._profile
        )

        return list(
            self._build_pattern(h.get_string("pattern"))
            for h in profile.get_list("handlers")
        )
