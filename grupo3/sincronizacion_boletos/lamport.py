from abc import ABC, abstractmethod
import threading  # Importa para manejar concurrencia con locks


class LamportInterface(ABC):
    @abstractmethod
    def tick(self):
        pass

    @abstractmethod
    def update(self, received_time):
        pass

class LamportClock(LamportInterface):
    def __init__(self):
        self.time = 0
        self.lock = threading.Lock()

    def tick(self):
        with self.lock:  # Bloquea acceso concurrente para evitar errores en entornos con hilos
            self.time += 1
            return self.time

    def update(self, received_time):
        with self.lock:
            self.time = max(self.time, received_time) + 1 # Reglas de Lamport para mantener orden causal
            return self.time   # Devuelve el nuevo valor del reloj


