from enum import Enum


class ProgressStatus(Enum):
    UNKNOWN = 0
    PENDING = 1
    SUCCEED = 2
    FAILED = 3


class ReputationScore(Enum):
    UNKNOWN = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


    @classmethod
    def get_score(cls, score: int):
        if score in range(0, 30):
            return cls.LOW
        if score in range(30,60):
            return cls.MEDIUM
        if score in range(60, 90):
            return cls.HIGH
        if score in range(90, 101):
            return cls.CRITICAL
        return cls.UNKNOWN



