import unittest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.monitor import monitor_middleware

class TestMonitorMiddleware(unittest.TestCase):
    def setUp(self):
        self.app = FastAPI()
        
        @self.app.middleware("http")
        async def add_monitor(request, call_next):
            return await monitor_middleware(request, call_next)

        @self.app.get("/ping")
        async def ping():
            return {"msg": "pong"}

        self.client = TestClient(self.app)

    def test_monitor_updates_metrics(self):
        for _ in range(3):
            res = self.client.get("/ping")
            self.assertEqual(res.status_code, 200)
        
        app_state = self.app.state
        self.assertEqual(app_state.request_count, 3)
        self.assertIsInstance(app_state.last_latency, float)
        self.assertEqual(len(app_state.latency_history), 3)
        self.assertTrue(all(isinstance(x, float) for x in app_state.latency_history))

    def test_latency_history_limit(self):
        for _ in range(60):  # Go beyond the 50-history limit
            self.client.get("/ping")

        self.assertEqual(len(self.app.state.latency_history), 50)

if __name__ == "__main__":
    unittest.main()
