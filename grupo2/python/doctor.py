import time
import random
import queue
import threading
from config import (
    salas_espera, 
    TOTAL_CITAS, 
    NUM_DOCTORES, 
    jornada_terminada,
    notificar_atencion_cita,
    esperar_si_pausado,
    FACTOR_VELOCIDAD,
    lock_citas,
    citas_en_espera,
    citas_en_atencion,
    simulacion_detenida
)

def doctor(id_doctor, estadisticas):
    """
    Hilo consumidor que simula un doctor atendiendo citas médicas.
    Los doctores atienden primero las citas de mayor prioridad.
    """
    print(f"Doctor {id_doctor} comienza su turno.")
    citas_atendidas = 0
    citas_esperadas = TOTAL_CITAS // NUM_DOCTORES
    
    try:
        # Continuar mientras no se haya detenido la simulación y
        # (no se hayan atendido todas las citas esperadas o no haya terminado la jornada)
        while not simulacion_detenida.is_set() and (citas_atendidas < citas_esperadas or not jornada_terminada.is_set()):
            # Verificar si la simulación está pausada
            esperar_si_pausado()
            
            # Buscar la próxima cita a atender, priorizando por nivel de urgencia
            cita = None
            
            # Revisar salas de espera por orden de prioridad (1=emergencia a 5=rutina)
            for prioridad in range(1, 6):
                try:
                    if not salas_espera[prioridad].empty():
                        cita = salas_espera[prioridad].get(block=False)
                        
                        # Eliminar la cita de la lista de espera para la interfaz gráfica
                        with lock_citas:
                            if cita in citas_en_espera[prioridad]:
                                citas_en_espera[prioridad].remove(cita)
                        
                        break
                except queue.Empty:
                    continue
            
            # Si no hay citas disponibles, esperar un momento y verificar de nuevo
            if cita is None:
                # Si ya se atendieron todas las citas esperadas y se terminó la jornada, finalizar
                if citas_atendidas >= citas_esperadas and jornada_terminada.is_set():
                    break
                    
                time.sleep(0.1 * FACTOR_VELOCIDAD)
                continue
                
            # Registrar que el doctor está atendiendo esta cita
            with lock_citas:
                citas_en_atencion[id_doctor] = cita
                
            # Notificar a la interfaz gráfica que se está atendiendo la cita
            notificar_atencion_cita(cita, id_doctor)
                
            # Simular tiempo de atención (varía según la prioridad)
            # Las emergencias se atienden más rápido, las citas rutinarias pueden tomar más tiempo
            tiempo_atencion = random.uniform(0.3, 0.7) * cita.prioridad / 2 * FACTOR_VELOCIDAD
            time.sleep(tiempo_atencion)
            
            # Calcular tiempo de espera del paciente
            tiempo_espera = time.time() - cita.tiempo_registro
            
            # Registrar la atención
            print(f"Doctor {id_doctor} atiende: {cita} - Tiempo de espera: {tiempo_espera:.2f}s")
            
            # Eliminar la cita de la lista de atención
            with lock_citas:
                if id_doctor in citas_en_atencion:
                    del citas_en_atencion[id_doctor]
            
            # Marcar cita como completada y actualizar estadísticas
            salas_espera[cita.prioridad].task_done()
            estadisticas.registrar_atencion(cita, tiempo_espera)
            citas_atendidas += 1
        
        print(f"Doctor {id_doctor} termina su turno. Atendió {citas_atendidas} citas.")
    except InterruptedError:
        print(f"Doctor {id_doctor} detenido.")
    except Exception as e:
        print(f"Error en doctor {id_doctor}: {e}")