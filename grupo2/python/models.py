"""
Clase que representa una cita médica
Equivalente a Cita.java
"""
class Cita:
    def __init__(self, id, prioridad, paciente, sintomas, tiempo_registro):
        self.id = id                          # Identificador único de la cita
        self.prioridad = prioridad            # Nivel de urgencia (1=emergencia, 5=rutina)
        self.paciente = paciente              # Nombre del paciente
        self.sintomas = sintomas              # Descripción de los síntomas
        self.tiempo_registro = tiempo_registro  # Momento en que se registró la cita

    def obtener_nivel_prioridad(self):
        """Devuelve el nombre del nivel de prioridad"""
        niveles = ["", "EMERGENCIA", "URGENTE", "PRIORITARIO", "NORMAL", "RUTINA"]
        return niveles[self.prioridad]

    def obtener_color_prioridad(self):
        """Devuelve el color asociado al nivel de prioridad"""
        colores = ["", "#ff0000", "#ff6600", "#ffcc00", "#66cc00", "#00cc66"]
        return colores[self.prioridad]

    def __str__(self):
        """Representación en texto de la cita"""
        return f"Cita[ID={self.id}, Paciente='{self.paciente}', Prioridad={self.obtener_nivel_prioridad()}]"
