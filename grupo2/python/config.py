import queue
import random
import threading
from typing import List, Dict, Callable, Any, Tuple

"""
Clase que contiene la configuración global del sistema
Equivalente a Configuracion.java
"""
class Config:
    # Configuración de la simulación
    NUM_RECEPCIONISTAS = 3
    NUM_DOCTORES = 2
    NUM_CITAS_POR_RECEPCIONISTA = 10
    TOTAL_CITAS = NUM_RECEPCIONISTAS * NUM_CITAS_POR_RECEPCIONISTA

    # Velocidad de simulación (factor de multiplicación para los tiempos de espera)
    # Un valor menor hace que la simulación vaya más rápido
    FACTOR_VELOCIDAD = 1.0

    # Colas de espera por nivel de prioridad
    SALAS_ESPERA: Dict[int, queue.Queue] = {}

    # Contador de citas atendidas
    CITAS_ATENDIDAS = 0
    CITAS_ATENDIDAS_LOCK = threading.Lock()

    # Señal de finalización
    FINALIZACION_RECEPCIONISTAS = threading.Semaphore(0)
    JORNADA_TERMINADA = False

    # Control de pausa
    LOCK_PAUSA = threading.Condition()
    SIMULACION_PAUSADA = False

    # Generador de números aleatorios
    RANDOM = random.Random()

    # Datos para generar citas aleatorias
    NOMBRES_PACIENTES = [
        "Jordan Zambrano", "Yusmeli Vilela", "Maria Jose Sabando", "Angie Loor",
        "Jhonny Mero", "Yesenia Quishpe", "Anthony Caicedo", "Dayana Álava",
        "Kevin Pilay", "Yuleisi Vera", "Steven Quintero", "Byron Calderon"
    ]

    SINTOMAS = [
        "Dolor de cabeza y fiebre", "Dolor abdominal intenso", "Mareos y náuseas",
        "Dificultad para respirar", "Dolor en el pecho", "Fractura expuesta",
        "Revisión rutinaria", "Seguimiento de tratamiento", "Dolor de garganta",
        "Erupción cutánea", "Dolor de espalda", "Presión arterial alta"
    ]

    # Callbacks para notificar eventos a la interfaz gráfica
    _CALLBACKS_NUEVA_CITA: List[Callable] = []
    _CALLBACKS_ATENCION_CITA: List[Callable] = []

    @classmethod
    def inicializar(cls):
        """Inicializar las salas de espera"""
        for i in range(1, 6):
            cls.SALAS_ESPERA[i] = queue.Queue(maxsize=10)

    @classmethod
    def registrar_callback_nueva_cita(cls, callback):
        """Registra un callback para ser notificado cuando se crea una nueva cita"""
        cls._CALLBACKS_NUEVA_CITA.append(callback)

    @classmethod
    def notificar_nueva_cita(cls, cita):
        """Notifica a todos los callbacks registrados sobre una nueva cita"""
        for callback in cls._CALLBACKS_NUEVA_CITA:
            callback(cita)

    @classmethod
    def registrar_callback_atencion_cita(cls, callback):
        """Registra un callback para ser notificado cuando se atiende una cita"""
        cls._CALLBACKS_ATENCION_CITA.append(callback)

    @classmethod
    def notificar_atencion_cita(cls, cita, doctor_id):
        """Notifica a todos los callbacks registrados sobre la atención de una cita"""
        for callback in cls._CALLBACKS_ATENCION_CITA:
            callback(cita, doctor_id)

    @classmethod
    def pausar_simulacion(cls):
        """Pausa la simulación"""
        cls.SIMULACION_PAUSADA = True

    @classmethod
    def reanudar_simulacion(cls):
        """Reanuda la simulación"""
        cls.SIMULACION_PAUSADA = False
        with cls.LOCK_PAUSA:
            cls.LOCK_PAUSA.notify_all()

    @classmethod
    def esperar_si_pausado(cls):
        """Espera si la simulación está pausada"""
        if cls.SIMULACION_PAUSADA:
            with cls.LOCK_PAUSA:
                while cls.SIMULACION_PAUSADA:
                    cls.LOCK_PAUSA.wait()

    @classmethod
    def establecer_velocidad(cls, factor):
        """Establece la velocidad de la simulación"""
        cls.FACTOR_VELOCIDAD = factor

    @classmethod
    def incrementar_citas_atendidas(cls):
        """Incrementa el contador de citas atendidas de forma segura"""
        with cls.CITAS_ATENDIDAS_LOCK:
            cls.CITAS_ATENDIDAS += 1
            return cls.CITAS_ATENDIDAS

# Inicializar las salas de espera
Config.inicializar()
