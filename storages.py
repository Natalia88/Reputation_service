import logging
from abc import ABC, abstractmethod

from enums import ProgressStatus, ReputationScore


logger = logging.getLogger(__name__)


class Storage(ABC):
    @abstractmethod
    def add_request(self, request_id: str, hash_str: str) -> None:
        pass

    @abstractmethod
    def get_request_data(self, request_id: str) -> str | None:
        pass

    @abstractmethod
    def update_status(self, hash_str: str, status: ProgressStatus) -> None:
        pass

    @abstractmethod
    def get_status(self, hash_str: str) -> ProgressStatus:
        pass

    @abstractmethod
    def update_reputation(self, hash_str: str, reputation: ReputationScore) -> None:
        pass

    @abstractmethod
    def get_reputation(self, hash_str: str) -> ReputationScore:
        pass


class InMemoryStorage(Storage):
    def __init__(self):
        self._requests = {}
        self._data = {}

    def add_request(self, request_id: str, hash_str: str) -> None:
        self._requests[request_id] = hash_str
        if hash_str not in self._data:
            self._data[hash_str] = {"status": ProgressStatus.UNKNOWN,
                                    "reputation": ReputationScore.UNKNOWN}

    def get_request_data(self, request_id: str) -> str | None:
        return self._requests.get(request_id)

    def get_status(self, hash_str) -> ProgressStatus:
        data = self._data.get(hash_str)
        if data is None:
            return ProgressStatus.UNKNOWN

        return data["status"]

    def get_reputation(self, hash_str: str) -> ReputationScore:
        data = self._data.get(hash_str)
        if data is None:
            return ReputationScore.UNKNOWN

        return data["reputation"]

    def update_status(self, hash_str: str, status: ProgressStatus) -> None:
        try:
            self._data[hash_str]["status"] = status
        except KeyError as e:
            logger.error(f'Data for {hash_str} not found in the storage.')

    def update_reputation(self, hash_str: str, reputation: ReputationScore) -> None:
        try:
            self._data[hash_str]["reputation"] = reputation
        except KeyError as e:
            logger.error(f'Data for {hash_str} not found in the storage.')


class DBStorage(Storage):
    # TODO: implement
    pass