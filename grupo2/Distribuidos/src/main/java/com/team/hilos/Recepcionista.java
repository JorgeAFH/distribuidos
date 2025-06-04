package com.team.hilos;

import com.team.config.Configuracion;
import com.team.interfaces.Cita;
import com.team.utils.Estadisticas;

/**
 * Hilo productor que simula un recepcionista registrando citas médicas
 */
public class Recepcionista implements Runnable {
    private final int idRecepcionista;
    private final Estadisticas estadisticas;

    public Recepcionista(int idRecepcionista, Estadisticas estadisticas) {
        this.idRecepcionista = idRecepcionista;
        this.estadisticas = estadisticas;
    }

    @Override
    public void run() {
        System.out.println("Recepcionista " + idRecepcionista + " comienza su turno.");

        try {
            for (int i = 0; i < Configuracion.NUM_CITAS_POR_RECEPCIONISTA; i++) {
                // Verificar si la simulación está pausada
                Configuracion.esperarSiPausado();

                // Simular tiempo de registro de la cita
                Thread.sleep((long) ((long) (Configuracion.RANDOM.nextInt(300) + 200) * Configuracion.FACTOR_VELOCIDAD));

                // Generar datos de la cita
                int prioridad = Configuracion.RANDOM.nextInt(5) + 1;  // 1=emergencia, 5=rutina
                String paciente = Configuracion.NOMBRES_PACIENTES[Configuracion.RANDOM.nextInt(Configuracion.NOMBRES_PACIENTES.length)];
                String sintomas = Configuracion.SINTOMAS[Configuracion.RANDOM.nextInt(Configuracion.SINTOMAS.length)];

                // Crear objeto de cita
                Cita cita = new Cita(
                        idRecepcionista * 100 + i,
                        prioridad,
                        paciente,
                        sintomas,
                        System.currentTimeMillis()
                );

                // Registrar la cita en la sala de espera correspondiente
                System.out.println("Recepcionista " + idRecepcionista + " registra: " + cita);
                Configuracion.SALAS_ESPERA.get(prioridad).put(cita);

                // Notificar a la interfaz gráfica
                Configuracion.notificarNuevaCita(cita);

                // Actualizar estadísticas
                estadisticas.registrarCita();
            }

            System.out.println("Recepcionista " + idRecepcionista + " termina su turno.");
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.out.println("Recepcionista " + idRecepcionista + " interrumpido.");
        } finally {
            Configuracion.FINALIZACION_RECEPCIONISTAS.countDown();
        }
    }
}
