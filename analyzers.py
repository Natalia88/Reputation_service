import time
import logging
from random import randint
from abc import ABC, abstractmethod
from enums import ProgressStatus, ReputationScore


logger = logging.getLogger(__name__)


class Analyzer(ABC):
    @abstractmethod
    def calc_reputation(self, hash_str: str) -> tuple[ProgressStatus, ReputationScore]:
        pass


class AnalyzerMock(Analyzer):
    def calc_reputation(self, hash_str: str) -> tuple[ProgressStatus, ReputationScore]:
        try:
            time.sleep(randint(1, 5))    # sleep to simulate delay at real analyzer
            score = ReputationScore.get_score(int(hash_str, 16) % 101)
            return ProgressStatus.SUCCEED, score
        except Exception as e:
            logger.error(f'Reputation calculating for {hash_str} failed: {str(e)}')
            return ProgressStatus.FAILED, ReputationScore.UNKNOWN
