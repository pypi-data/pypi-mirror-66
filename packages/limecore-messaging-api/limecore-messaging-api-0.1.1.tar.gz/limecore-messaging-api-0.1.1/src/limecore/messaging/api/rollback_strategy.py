from enum import Enum


class RollbackStrategy(Enum):
    RETRY_NOW = 1
    RETRY_LATER = 2
    QUARANTINE = 3
