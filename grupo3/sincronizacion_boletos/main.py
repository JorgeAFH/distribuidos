import threading
import time
import random
from lamport import LamportClock  # Importa la clase que implementa el reloj lógico de Lamport
from ticket_system import TicketSystem # Importa el sistema que maneja la compra de boletos
from gui import LamportGUI     # Importa la interfaz gráfica que muestra los eventos

# Esta función representa el comportamiento de un servidor (A o B)
def server_behavior(server_name, lamport_clock, ticket_system, gui):
    for _ in range(random.randint(1, 3)):
        time.sleep(random.uniform(0.1, 0.3))
        t = lamport_clock.tick()
        gui.log(f"[{t}] {server_name} ejecutó un evento local.")

# Espera antes de intentar comprar un boleto
    time.sleep(random.uniform(0.1, 0.2))
    start_time = time.time()
     # Genera un nuevo tick para el intento de compra
    sent_time = lamport_clock.tick()
    gui.log(f"[{sent_time}] {server_name} intenta comprar el boleto...")
    # Se actualiza el reloj Lamport usando su propio valor 
    received_time = lamport_clock.update(sent_time)
    elapsed_time = time.time() - start_time

    ticket_system.attempt_purchase(server_name, received_time, elapsed_time, gui)

def run_simulation(gui, simulation_number):
    gui.log(f"\n--- Simulación #{simulation_number} ---")
    lamport_a = LamportClock()
    lamport_b = LamportClock()
    ticket_system = TicketSystem()  # Nuevo sistema por cada simulación
    # Se crean hilos para los dos servidores con su comportamiento independiente
    thread_a = threading.Thread(target=server_behavior, args=("Servidor A", lamport_a, ticket_system, gui))
    thread_b = threading.Thread(target=server_behavior, args=("Servidor B", lamport_b, ticket_system, gui))
    # Inicia ambos hilos
    thread_a.start()
    thread_b.start()
    # Espera a que ambos hilos terminen antes de continua
    thread_a.join()
    thread_b.join()

if __name__ == "__main__":
    gui = LamportGUI()

    def run_all_simulations():
        for i in range(1, 21):  # Ejecuta 20 veces
            run_simulation(gui, i)
            time.sleep(0.5)  # Espera entre simulaciones

    # Lanza todo desde un hilo para no bloquear el GUI
    threading.Thread(target=run_all_simulations).start()
    gui.start()
