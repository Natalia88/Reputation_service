import os, sys
import unittest
import time
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app


class TestReputationService(unittest.TestCase):
    def setUp(self) -> None:
        pass
        # self.client = TestClient(app)

    def test_get_reputation_first_time(self):
        """
        The first request is expected to return PENDING status,
        UNKNOWN reputation and put a task to the queue.
        """
        with TestClient(app) as client:
            hash_str = "abc123"
            response = client.get(f'/getReputation/?hash_str={hash_str}')
            data = response.json()
            self.assertEqual(data["hash_str"], hash_str)
            self.assertEqual(data["status"], "PENDING")
            self.assertEqual(data["reputation"], "UNKNOWN")

    def test_get_reputation_same_hash_pending(self):
        """
        The same request for the existing hash before calculation is done.
        It is expected to return PENDING status,
        UNKNOWN reputation and NOT put a task to the queue.
        """
        with TestClient(app) as client:
            hash_str = "abc123"
            # first request
            response = client.get(f'/getReputation/?hash_str={hash_str}')
            # next request
            response = client.get(f'/getReputation/?hash_str={hash_str}')
            data = response.json()
            self.assertEqual(data["hash_str"], hash_str)
            self.assertEqual(data["status"], "PENDING")
            self.assertEqual(data["reputation"], "UNKNOWN")

    def test_get_reputation_same_hash_ready(self):
        """
        The same request for the existing hash after calculation is done.
        It is expected to return SUCCEED status,
        LOW|MEDIUM|HIGH|CRITICAL reputation.
        """
        with TestClient(app) as client:
            hash_str = "abc456"
            response = client.get(f'/getReputation/?hash_str={hash_str}')
            request_id = response.json()["request_id"]

            time.sleep(6)

            response = client.get(f'/isReputationReady/?request_id={request_id}')
            data = response.json()

            self.assertEqual(data["hash_str"], hash_str)
            self.assertEqual(data["status"], "SUCCEED")
            self.assertIn(data["reputation"], ["LOW","MEDIUM","HIGH","CRITICAL"])

    def test_get_reputation_unknown_request(self):
        """
        The request with invalid request_id is expected to return UNKNOWN status,
        UNKNOWN reputation.
        """
        with TestClient(app) as client:
            response = client.get(f'/isReputationReady/?request_id="invalid_id"')
            data = response.json()
            self.assertEqual(data["status"], "UNKNOWN")
            self.assertIn(data["reputation"],"UNKNOWN")
