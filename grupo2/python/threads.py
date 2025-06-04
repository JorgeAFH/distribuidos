import queue
import time
import threading
from config import Config
from models import Cita

"""
Hilos para la simulación del sistema
Equivalente a Recepcionista.java y Doctor.java
"""

class Recepcionista(threading.Thread):
    """Hilo productor que simula un recepcionista registrando citas médicas"""
    
    def __init__(self, id_recepcionista, estadisticas):
        super().__init__(name=f"Recepcionista-{id_recepcionista}")
        self.id_recepcionista = id_recepcionista
        self.estadisticas = estadisticas

    def run(self):
        print(f"Recepcionista {self.id_recepcionista} comienza su turno.")

        try:
            for i in range(Config.NUM_CITAS_POR_RECEPCIONISTA):
                # Verificar si la simulación está pausada
                Config.esperar_si_pausado()

                # Simular tiempo de registro de la cita
                tiempo_registro = (Config.RANDOM.randint(200, 500) * Config.FACTOR_VELOCIDAD) / 1000
                time.sleep(tiempo_registro)

                # Generar datos de la cita
                prioridad = Config.RANDOM.randint(1, 5)  # 1=emergencia, 5=rutina
                paciente = Config.RANDOM.choice(Config.NOMBRES_PACIENTES)
                sintomas = Config.RANDOM.choice(Config.SINTOMAS)

                # Crear objeto de cita
                cita = Cita(
                    self.id_recepcionista * 100 + i,
                    prioridad,
                    paciente,
                    sintomas,
                    time.time() * 1000  # Convertir a milisegundos como en Java
                )

                # Registrar la cita en la sala de espera correspondiente
                print(f"Recepcionista {self.id_recepcionista} registra: {cita}")
                Config.SALAS_ESPERA[prioridad].put(cita)

                # Notificar a la interfaz gráfica
                Config.notificar_nueva_cita(cita)

                # Actualizar estadísticas
                self.estadisticas.registrar_cita()

            print(f"Recepcionista {self.id_recepcionista} termina su turno.")
        except Exception as e:
            print(f"Recepcionista {self.id_recepcionista} error: {e}")
        finally:
            # Señalizar que este recepcionista ha terminado
            Config.FINALIZACION_RECEPCIONISTAS.release()


class Doctor(threading.Thread):
    """Hilo consumidor que simula un doctor atendiendo citas médicas"""
    
    def __init__(self, id_doctor, estadisticas):
        super().__init__(name=f"Doctor-{id_doctor}")
        self.id_doctor = id_doctor
        self.estadisticas = estadisticas

    def run(self):
        print(f"Doctor {self.id_doctor} comienza su turno.")
        citas_locales = 0
        citas_esperadas = Config.TOTAL_CITAS // Config.NUM_DOCTORES

        try:
            while citas_locales < citas_esperadas or not Config.JORNADA_TERMINADA:
                # Verificar si la simulación está pausada
                Config.esperar_si_pausado()

                # Buscar la próxima cita a atender, priorizando por nivel de urgencia
                cita = None

                # Revisar salas de espera por orden de prioridad (1=emergencia a 5=rutina)
                for prioridad in range(1, 6):
                    try:
                        # Intentar obtener una cita sin bloquear
                        cita = Config.SALAS_ESPERA[prioridad].get_nowait()
                        break
                    except queue.Empty:
                        continue

                # Si no hay citas disponibles, esperar un momento
                if cita is None:
                    # Si ya se atendieron todas las citas esperadas y se terminó la jornada, finalizar
                    if citas_locales >= citas_esperadas and Config.JORNADA_TERMINADA:
                        break

                    time.sleep(0.1 * Config.FACTOR_VELOCIDAD)
                    continue

                # Notificar a la interfaz gráfica que se está atendiendo la cita
                Config.notificar_atencion_cita(cita, self.id_doctor)

                # Simular tiempo de atención (varía según la prioridad)
                tiempo_atencion = (Config.RANDOM.randint(300, 700) * (cita.prioridad / 2.0) * Config.FACTOR_VELOCIDAD) / 1000
                time.sleep(tiempo_atencion)

                # Calcular tiempo de espera del paciente
                tiempo_espera = (time.time() * 1000 - cita.tiempo_registro) / 1000.0

                # Registrar la atención
                print(f"Doctor {self.id_doctor} atiende: {cita} - Tiempo de espera: {tiempo_espera:.2f}s")

                # Actualizar estadísticas
                self.estadisticas.registrar_atencion(cita, tiempo_espera)
                citas_locales += 1
                Config.incrementar_citas_atendidas()

            print(f"Doctor {self.id_doctor} termina su turno.")
        except Exception as e:
            print(f"Doctor {self.id_doctor} error: {e}")
