package com.team;

import com.team.config.Configuracion;
import com.team.hilos.Doctor;
import com.team.hilos.Recepcionista;
import com.team.utils.Estadisticas;
import com.team.utils.InterfazGrafica;

/**
 * Clase principal del Sistema de Gestión de Citas Médicas
 */
public class SistemaCitasMedicas {

    /**
     * Inicia la simulación del sistema
     */
    public static void iniciarSimulacion() {
        // Asegurarse de que la simulación esté en marcha
        Configuracion.reanudarSimulacion();

        // Registrar tiempo de inicio
        long tiempoInicio = System.currentTimeMillis();

        // Crear y lanzar hilos recepcionistas
        Thread[] hilosRecepcionistas = new Thread[Configuracion.NUM_RECEPCIONISTAS];
        for (int i = 0; i < Configuracion.NUM_RECEPCIONISTAS; i++) {
            hilosRecepcionistas[i] = new Thread(new Recepcionista(i + 1, estadisticas));
            hilosRecepcionistas[i].start();
        }

        // Crear y lanzar hilos doctores
        Thread[] hilosDoctores = new Thread[Configuracion.NUM_DOCTORES];
        for (int i = 0; i < Configuracion.NUM_DOCTORES; i++) {
            hilosDoctores[i] = new Thread(new Doctor(i + 1, estadisticas));
            hilosDoctores[i].start();
        }

        try {
            // Esperar a que todos los recepcionistas terminen
            Configuracion.FINALIZACION_RECEPCIONISTAS.await();
            Configuracion.JORNADA_TERMINADA = true;

            // Esperar a que todos los doctores terminen
            for (Thread hilo : hilosDoctores) {
                hilo.join();
            }

            // Calcular tiempo de ejecución
            double tiempoEjecucion = (System.currentTimeMillis() - tiempoInicio) / 1000.0;

            // Mostrar mensaje final
            System.out.println("\n=== SIMULACIÓN FINALIZADA ===");
            System.out.println("Tiempo total de la jornada: " + String.format("%.2f", tiempoEjecucion) + " segundos");
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.out.println("Simulación interrumpida");
        }
    }

    // Instancia de estadísticas compartida
    private static Estadisticas estadisticas;

    public static void main(String[] args) {
        // Crear instancia de estadísticas
        estadisticas = new Estadisticas();

        // Crear y mostrar la interfaz gráfica
        InterfazGrafica interfaz = new InterfazGrafica(estadisticas, SistemaCitasMedicas::iniciarSimulacion);
    }
}
