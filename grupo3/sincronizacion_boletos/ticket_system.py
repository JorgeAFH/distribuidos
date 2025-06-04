
import threading
import time

import gui

class TicketSystem:
    def __init__(self):
        self.ticket_available = True
        #sigue comentado para NO usar sincronización
        self.lock = threading.Lock()

    def attempt_purchase(self, server_name, clock_time, elapsed_time, gui):
        with self.lock:
            if self.ticket_available:
                self.ticket_available = False
                gui.log(f"[{clock_time}] {server_name} ha comprado el boleto. "
                        f"Tiempo de compra: {elapsed_time:.4f} segundos.")
            else:
                gui.log(f"[{clock_time}] {server_name} intentó comprar, pero ya fue vendido.")
         
         # Versión sin lock:
        """ time.sleep(0.2)  # ← Esto fuerza que ambos hilos se crucen aquí (¡simula el error!)
        if self.ticket_available:
            gui.log(f"[{clock_time}] {server_name} compra el boleto SIN sincronización. "
                    f"Tiempo: {elapsed_time:.4f} segundos.")
            time.sleep(0.1)  # ← hace que el otro hilo aún alcance a entrar
            self.ticket_available = False
        else:
            gui.log(f"[{clock_time}] {server_name} ya no puede comprar. Boleto vendido. (SIN sincronización)") """