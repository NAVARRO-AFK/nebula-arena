import json, os, random, time, uuid
import requests
from gevent.lock import Semaphore
from locust import User, task, constant, events
from websocket import create_connection

ALLOCATOR_IP = os.environ.get("ALLOCATOR_IP", "172.18.0.2")
ALLOCATOR_PORT = os.environ.get("ALLOCATOR_PORT", "30617")
ALLOCATOR = f"https://{ALLOCATOR_IP}:{ALLOCATOR_PORT}/gameserverallocation"
PEDIDO = {"namespace": "default",
          "gameServerSelectors": [{"matchLabels": {"agones.dev/fleet": "nebula-fleet"}}]}
CERTS = {"cert": ("client.crt", "client.key"), "verify": False}

def medir(nombre, inicio, error=None):
    events.request.fire(request_type="WS", name=nombre,
                        response_time=(time.perf_counter() - inicio) * 1000,
                        response_length=0, exception=error)

class Jugador(User):
    wait_time = constant(0.05)  # 20 mensajes por segundo
    sala = {"addr": None, "cupo": 0}  # mini-matchmaker compartido
    candado = Semaphore()

    def pedir_servidor(self):
        with Jugador.candado:
            if Jugador.sala["cupo"] == 0:  # sala llena: pide otro servidor
                t0 = time.perf_counter()
                for intento in range(5):  # reintenta si el allocator responde 429
                    r = requests.post(ALLOCATOR, json=PEDIDO, timeout=10, **CERTS)
                    if r.status_code != 429:
                        break
                    time.sleep(0.5 * (intento + 1))
                r.raise_for_status()
                gs = r.json()
                medir("asignacion", t0)
                Jugador.sala = {"addr": f"{gs['address']}:{gs['ports'][0]['port']}",
                                "cupo": 10}
            Jugador.sala["cupo"] -= 1
            return Jugador.sala["addr"]

    def on_start(self):
        self.id, self.n = uuid.uuid4().hex[:8], 0
        self.x, self.y = random.uniform(0, 100), random.uniform(0, 100)
        self.ws = create_connection(f"ws://{self.pedir_servidor()}", timeout=5)

    @task
    def jugar(self):
        self.x += random.uniform(-1, 1)
        self.y += random.uniform(-1, 1)
        self.ws.send(json.dumps({"id": self.id, "x": self.x, "y": self.y,
                                 "dispara": random.random() < 0.1}))
        self.n += 1
        if self.n % 20 == 0:  # un ping por segundo
            t0 = time.perf_counter()
            try:
                self.ws.send(json.dumps({"ping": t0}))
                while json.loads(self.ws.recv()).get("pong") != t0:
                    pass  # descarta los snapshots acumulados
                medir("rtt", t0)
            except Exception as e:
                medir("rtt", t0, e)

    def on_stop(self):
        self.ws.close()
