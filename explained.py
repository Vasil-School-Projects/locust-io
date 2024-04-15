"""
Simple locust.io demo testing file.
"""

from locust import HttpUser, task, between, tag


class ApiUser(HttpUser):
    """
    A locust class to test the FastAPI application
    """

    wait_time = between(0.25, 0.5)  # Hoe lang te wachten tussen requests
    token = None

    def on_start(self):  # Wat te doen wanneer een gebruiker begint
        with self.client.post(  # Client houdt de sessie bij (dus cookies worden bewaard)
            "/login", json={"username": "username", "password": "password"}
        ) as response:
            if response.status_code == 200:
                self.token = response.json().get("token")

    def on_stop(self):  # Wat te doen wanneer een gebruiker stopt
        with self.client.post("/logout") as response:
            if response.status_code == 200:
                self.token = None

    @tag("fast")  # Tag een task om alleen tasks met bepaalde tags uit te voeren
    @task(3)  # De 3 staat voor de kans om deze task uit te voeren
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


# class MobileUser(HttpUser): # Een ander soort gebruiker is een eigen class
#     """
#     Demo user class for mobile users
#     """

#     fixed_count: 10  # Het aantal van dit soort gebruikers om te "spawnen"
#     weight: 5  # Hoe groot de kans is dat dit soort gebruiker "gespawned" wordt
