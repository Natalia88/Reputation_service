import queue
import logging
import threading

from storages import Storage
from enums import ProgressStatus, ReputationScore
from workers import Worker
from analyzers import Analyzer


logger = logging.getLogger(__name__)


class ReputationService:
    lock = threading.Lock()

    def __init__(self, storage: Storage, queue: queue.Queue, analyzer: Analyzer) -> None:
        self._storage = storage
        self._tasks_queue = queue
        self._analyzer = analyzer
        self._workers = []

    def start_workers(self, workers_num):
        for i in range(workers_num):
            worker = Worker(i, self._tasks_queue, self._storage, self._analyzer)
            self._workers.append(worker)
            thread = threading.Thread(target=worker.run, args=(), daemon=True)
            thread.start()
            logger.debug(f'Started worker {i} in thread {thread.name}')

    def stop_workers(self):
        # for _ in range(0, len(self._workers)):
        #     self._tasks_queue.put(None)
        for worker in self._workers:
            worker.stop()

    def calc_reputation(self, hash_str: str) -> tuple[ProgressStatus, ReputationScore]:
        status = self._storage.get_status(hash_str)
        reputation = self._storage.get_reputation(hash_str)
        if reputation is not ReputationScore.UNKNOWN:
            logger.info(f'Reputation for {hash_str} is already calculated - {status}')
            return status, reputation

        if status is ProgressStatus.PENDING:
            logger.info(f'Reputation for {hash_str} is already sent to queue - {status}')
            return status, reputation

        logger.info(f'No reputation for {hash_str} was found. Creating a new task.')
        with ReputationService.lock:
            status = ProgressStatus.PENDING
            self._storage.update_status(hash_str, status)
            self._tasks_queue.put(hash_str)
        return status, reputation

    def is_reputation_ready(self, hash_str: str) -> tuple[ProgressStatus, ReputationScore]:
        status = self._storage.get_status(hash_str)
        reputation = self._storage.get_reputation(hash_str)
        if status is ProgressStatus.UNKNOWN:
            logger.warning(f'No task for {hash_str} was found.')
        else:
            logger.info(f'Calculating a reputation for {hash_str} - {status.name}')

        return status, reputation
