import time
import threading
from config import Config
from models import Cita
from threads import Recepcionista, Doctor
from estadisticas import Estadisticas
from gui import InterfazGrafica

"""
Clase principal del Sistema de Gestión de Citas Médicas
Equivalente a SistemaCitasMedicas.java
"""
class SistemaCitasMedicas:
    @staticmethod
    def iniciar_simulacion():
        """Inicia la simulación del sistema"""
        # Asegurarse de que la simulación esté en marcha
        Config.reanudar_simulacion()

        # Registrar tiempo de inicio
        tiempo_inicio = time.time()

        # Crear y lanzar hilos recepcionistas
        hilos_recepcionistas = []
        for i in range(Config.NUM_RECEPCIONISTAS):
            hilo = Recepcionista(i + 1, estadisticas)
            hilo.start()
            hilos_recepcionistas.append(hilo)

        # Crear y lanzar hilos doctores
        hilos_doctores = []
        for i in range(Config.NUM_DOCTORES):
            hilo = Doctor(i + 1, estadisticas)
            hilo.start()
            hilos_doctores.append(hilo)

        try:
            # Esperar a que todos los recepcionistas terminen
            for _ in range(Config.NUM_RECEPCIONISTAS):
                Config.FINALIZACION_RECEPCIONISTAS.acquire()
            Config.JORNADA_TERMINADA = True

            # Esperar a que todos los doctores terminen
            for hilo in hilos_doctores:
                hilo.join()

            # Calcular tiempo de ejecución
            tiempo_ejecucion = time.time() - tiempo_inicio

            # Mostrar mensaje final
            print("\n=== SIMULACIÓN FINALIZADA ===")
            print(f"Tiempo total de la jornada: {tiempo_ejecucion:.2f} segundos")
        except Exception as e:
            print(f"Error en la simulación: {e}")

if __name__ == "__main__":
    # Crear instancia de estadísticas
    estadisticas = Estadisticas()

    # Crear y mostrar la interfaz gráfica
    interfaz = InterfazGrafica(estadisticas, SistemaCitasMedicas.iniciar_simulacion)
    interfaz.iniciar()
