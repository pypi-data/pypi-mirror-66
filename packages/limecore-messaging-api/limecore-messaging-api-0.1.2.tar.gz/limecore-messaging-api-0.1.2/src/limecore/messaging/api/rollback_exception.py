from .rollback_strategy import RollbackStrategy


class RollbackException(Exception):
    def __init__(self, *args: object, rollback_strategy: RollbackStrategy):
        super().__init__(*args)

        self._rollback_strategy = rollback_strategy

    @property
    def rollback_strategy(self):
        return self._rollback_strategy
