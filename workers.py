import logging
from queue import Queue, Empty

from analyzers import Analyzer
from storages import Storage
from enums import ReputationScore


logger = logging.getLogger(__name__)


class Worker:
    def __init__(self, worker_id: int, tasks_queue: Queue, storage: Storage, analyzer: Analyzer):
        self._id = worker_id
        self._tasks_queue = tasks_queue
        self._analyzer = analyzer
        self._storage = storage
        self._is_running = True

    def run(self) -> None:
        while self._is_running:
            try:
                task_data = self._tasks_queue.get(timeout=1)
                if task_data is None:
                    break

                logger.debug(f'Worker {self._id} processing task {task_data}')
                status, reputation = self._analyzer.calc_reputation(task_data)
                logger.debug(f'Worker {self._id} finished task {task_data}: {status.name}')

                self._storage.update_status(task_data, status)
                if reputation is not ReputationScore.UNKNOWN:
                    self._storage.update_reputation(task_data, reputation)

                self._tasks_queue.task_done()
            except Empty as e:
                continue

    def stop(self) -> None:
        self._is_running = False
        logger.debug(f'Worker {self._id} is stopped.')
