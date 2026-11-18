import random
from locust import HttpUser, task, between

class Lector(HttpUser):
    wait_time = between(0.5, 1)

    @task(8)  # 80 % lecturas
    def leer_top(self):
        self.client.get("/top", name="GET /top")

    @task(2)  # 20 % escrituras
    def registrar(self):
        self.client.post("/score",
                         json={"jugador": f"j{random.randint(1, 500)}",
                               "puntos": random.randint(1, 100)},
                         name="POST /score")
