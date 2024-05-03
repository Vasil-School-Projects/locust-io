"""
Simple locust.io demo testing file.

Run using locust -f main.py
"""

from locust import HttpUser, task, between, tag


class ApiUser(HttpUser):
    """
    A locust class to test the FastAPI application
    """

    wait_time = between(0.25, 0.5)
    token = None

    def on_start(self):
        with self.client.post(
            "/login", json={"username": "username", "password": "password"}
        ) as response:
            if response.status_code == 200:
                self.token = response.json().get("token")

    def on_stop(self):
        with self.client.post("/logout") as response:
            if response.status_code == 200:
                self.token = None

    @tag("fast")
    @task(3)
    def fast(self):
        """
        Sends a GET request to the /fast route
        """
        self.client.get("/fast", headers={"login-token": self.token})

    @tag("slow")
    @task
    def slow(self):
        """
        Sends a GET request to the /slow route
        """
        self.client.get("/slow", headers={"login-token": self.token})


# class MobileUser(HttpUser):
#     """
#     Demo user class for mobile users
#     """

#     fixed_count: 10
#     weight: 5
