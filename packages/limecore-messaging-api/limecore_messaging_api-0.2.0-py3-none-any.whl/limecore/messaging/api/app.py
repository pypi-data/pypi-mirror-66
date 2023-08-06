from injector import inject

from .worker import Worker


class App:
    @inject
    def __init__(self, worker: Worker):
        self._worker = worker

    def start(self):
        self._worker.run()
