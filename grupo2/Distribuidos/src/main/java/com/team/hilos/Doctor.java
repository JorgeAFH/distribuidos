package com.team.hilos;

import com.team.config.Configuracion;
import com.team.interfaces.Cita;
import com.team.utils.Estadisticas;

/**
 * Hilo consumidor que simula un doctor atendiendo citas médicas
 */
public class Doctor implements Runnable {
    private final int idDoctor;
    private final Estadisticas estadisticas;

    public Doctor(int idDoctor, Estadisticas estadisticas) {
        this.idDoctor = idDoctor;
        this.estadisticas = estadisticas;
    }

    @Override
    public void run() {
        System.out.println("Doctor " + idDoctor + " comienza su turno.");
        int citasLocales = 0;
        int citasEsperadas = Configuracion.TOTAL_CITAS / Configuracion.NUM_DOCTORES;

        try {
            while (citasLocales < citasEsperadas || !Configuracion.JORNADA_TERMINADA) {
                // Verificar si la simulación está pausada
                Configuracion.esperarSiPausado();

                // Buscar la próxima cita a atender, priorizando por nivel de urgencia
                Cita cita = null;

                // Revisar salas de espera por orden de prioridad (1=emergencia a 5=rutina)
                for (int prioridad = 1; prioridad <= 5; prioridad++) {
                    cita = Configuracion.SALAS_ESPERA.get(prioridad).poll();
                    if (cita != null) {
                        break;
                    }
                }

                // Si no hay citas disponibles, esperar un momento
                if (cita == null) {
                    // Si ya se atendieron todas las citas esperadas y se terminó la jornada, finalizar
                    if (citasLocales >= citasEsperadas && Configuracion.JORNADA_TERMINADA) {
                        break;
                    }

                    Thread.sleep((long) (100 * Configuracion.FACTOR_VELOCIDAD));
                    continue;
                }

                // Notificar a la interfaz gráfica que se está atendiendo la cita
                Configuracion.notificarAtencionCita(cita, idDoctor);

                // Simular tiempo de atención (varía según la prioridad)
                double tiempoAtencion = (Configuracion.RANDOM.nextInt(400) + 300) * (cita.getPrioridad() / 2.0) * Configuracion.FACTOR_VELOCIDAD;
                Thread.sleep((long) tiempoAtencion);

                // Calcular tiempo de espera del paciente
                double tiempoEspera = (System.currentTimeMillis() - cita.getTiempoRegistro()) / 1000.0;

                // Registrar la atención
                System.out.println("Doctor " + idDoctor + " atiende: " + cita +
                        " - Tiempo de espera: " + String.format("%.2f", tiempoEspera) + "s");

                // Actualizar estadísticas
                estadisticas.registrarAtencion(cita, tiempoEspera);
                citasLocales++;
                Configuracion.CITAS_ATENDIDAS.incrementAndGet();
            }

            System.out.println("Doctor " + idDoctor + " termina su turno.");
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.out.println("Doctor " + idDoctor + " interrumpido.");
        }
    }
}
