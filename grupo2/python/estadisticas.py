from typing import Dict, List, Callable, Any

"""
Clase para gestionar estadísticas del sistema
"""
class Estadisticas:
    def __init__(self):
        self.citas_registradas = 0
        self.citas_atendidas = 0
        self.tiempo_espera_total = 0.0
        self.tiempos_por_prioridad = {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0}
        self.citas_por_prioridad = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        self.callbacks: List[Callable] = []

    def registrar_cita(self):
        """Registra una nueva cita en las estadísticas"""
        self.citas_registradas += 1
        self._notificar_cambios()

    def registrar_atencion(self, cita, tiempo_espera):
        """Registra la atención de una cita en las estadísticas"""
        self.citas_atendidas += 1
        self.tiempo_espera_total += tiempo_espera
        
        # Actualizar estadísticas por prioridad
        prioridad = cita.prioridad
        self.tiempos_por_prioridad[prioridad] += tiempo_espera
        self.citas_por_prioridad[prioridad] += 1
        
        self._notificar_cambios()

    def agregar_callback(self, callback):
        """Agrega un callback para notificar cambios en las estadísticas"""
        self.callbacks.append(callback)

    def _notificar_cambios(self):
        """Notifica a los callbacks sobre cambios en las estadísticas"""
        informe = self.generar_informe()
        for callback in self.callbacks:
            callback(informe)

    def generar_informe(self) -> Dict[str, Any]:
        """Genera un informe con las estadísticas actuales"""
        # Calcular tiempo promedio general
        tiempo_promedio = 0.0
        if self.citas_atendidas > 0:
            tiempo_promedio = self.tiempo_espera_total / self.citas_atendidas
        
        # Calcular tiempos promedio por prioridad
        tiempos_promedio = {}
        for prioridad in range(1, 6):
            if self.citas_por_prioridad[prioridad] > 0:
                tiempos_promedio[prioridad] = self.tiempos_por_prioridad[prioridad] / self.citas_por_prioridad[prioridad]
            else:
                tiempos_promedio[prioridad] = 0.0
        
        return {
            "citasRegistradas": self.citas_registradas,
            "citasAtendidas": self.citas_atendidas,
            "tiempoEsperaPromedio": tiempo_promedio,
            "tiemposPorPrioridad": tiempos_promedio
        }
