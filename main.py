import uuid
import queue
import logging
import uvicorn
from fastapi import FastAPI

from reputation_service import ReputationService
from storages import InMemoryStorage
from analyzers import AnalyzerMock


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


WORKERS_NUM = 3     # TODO: get from config
STORAGE = InMemoryStorage()     # TODO: get from config
ANALYZER = AnalyzerMock()       # TODO: get from config
TASKS_QUEUE = queue.Queue()
REPUTATION_SERVICE = ReputationService(STORAGE, TASKS_QUEUE, ANALYZER)

app = FastAPI()


@app.on_event("startup")
def startup() -> None:
    REPUTATION_SERVICE.start_workers(WORKERS_NUM)


@app.on_event("shutdown")
def shutdown() -> None:
    REPUTATION_SERVICE.stop_workers()


@app.get("/getReputation/")
def get_reputation(hash_str: str) -> dict:
    request_id = str(uuid.uuid4())
    STORAGE.add_request(request_id, hash_str)
    status, reputation = REPUTATION_SERVICE.calc_reputation(hash_str)
    response = {"request_id": request_id,
                "hash_str": hash_str,
                "reputation": reputation.name,
                "status": status.name}
    return response


@app.get("/isReputationReady/")
def is_reputation_ready(request_id: str) -> dict:
    hash_str = STORAGE.get_request_data(request_id)
    if not hash_str:
        logger.warning(f'Unknown request {request_id}.')

    status, reputation = REPUTATION_SERVICE.is_reputation_ready(hash_str)

    response = {"request_id": request_id,
                "hash_str": hash_str,
                "reputation": reputation.name,
                "status": status.name}

    logger.info(f'Sending response for {request_id}.')
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)