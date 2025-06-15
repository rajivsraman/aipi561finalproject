import unittest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

class TestMainEndpoints(unittest.TestCase):

    def test_signup_and_login_flow(self):
        # ---- Sign up a new user ----
        response = client.post("/signup", data={"username": "unittestuser", "password": "unittestpass"})
        self.assertIn(response.status_code, [200, 400])  # 400 if already exists

        # ---- Login the user ----
        login = client.post("/login", data={"username": "unittestuser", "password": "unittestpass"})
        self.assertEqual(login.status_code, 200)
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # ---- Get metrics ----
        metrics = client.get("/metrics", headers=headers)
        self.assertEqual(metrics.status_code, 200)
        self.assertIn("requests", metrics.json())
        self.assertIn("last_latency_sec", metrics.json())
        self.assertIn("latency_history", metrics.json())

if __name__ == "__main__":
    unittest.main()
