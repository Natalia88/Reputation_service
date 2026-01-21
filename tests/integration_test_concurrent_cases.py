import os, sys
import threading
import unittest
import time
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app


class TestReputationService(unittest.TestCase):
    def setUp(self) -> None:
        pass
        # self.client = TestClient(app)

    def test_two_requests_same_hash(self):
        """
        Two concurrent requests with the same hash.
        The first request is expected to return PENDING status,
        UNKNOWN reputation and put a task to the queue. The second should
        not put the same task to the queue and update the status.
        """
        with TestClient(app) as client:
            hash_str = "abc123"
            responses = []

            def send_request():
                resp = client.get(f'/getReputation/?hash_str={hash_str}')
                responses.append(resp.json())

            thread1 = threading.Thread(target=send_request)
            thread2 = threading.Thread(target=send_request)

            thread1.start()
            thread2.start()
            thread1.join()
            thread2.join()

        self.assertEqual(len(responses), 2)
        for r in responses:
            self.assertEqual(r["hash_str"], hash_str)
            self.assertEqual(r["status"], "PENDING")
            self.assertEqual(r["reputation"], "UNKNOWN")

    def test_two_requests_different_hash(self):
        """
        Two concurrent requests with different hashes.
        The first request is expected to return PENDING status,
        UNKNOWN reputation and put a task to the queue. The second should
        do the same for the other hash.
        """
        with TestClient(app) as client:
            hash_str1 = "abc1234"
            hash_str2 = "def3456"
            responses = {}

            def send_request(hash_str):
                resp = client.get(f'/getReputation/?hash_str={hash_str}')
                responses[hash_str] = resp.json()

            thread1 = threading.Thread(target=send_request, args=(hash_str1,))
            thread2 = threading.Thread(target=send_request, args=(hash_str2,))

            thread1.start()
            thread2.start()
            thread1.join()
            thread2.join()

        self.assertEqual(len(responses), 2)
        for h, r in responses.items():
            self.assertEqual(r["hash_str"], h)
            self.assertEqual(r["status"], "PENDING")
            self.assertEqual(r["reputation"], "UNKNOWN")

        time.sleep(6)

        for h, r in responses.items():
            request_id = r["request_id"]
            res = client.get(f'/isReputationReady/?request_id={request_id}').json()
            self.assertEqual(res["hash_str"], h)
            self.assertEqual(res["status"], "SUCCEED")
            self.assertIn(res["reputation"], ["LOW", "MEDIUM", "HIGH", "CRITICAL"])

