package com.team.utils;

import com.team.interfaces.Cita;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
import java.util.function.Consumer;

/**
 * Clase para registrar y calcular estadísticas del sistema
 */
public class Estadisticas {
    private final Lock lock = new ReentrantLock();
    private int citasRegistradas = 0;
    private int citasAtendidas = 0;
    private double tiempoEsperaTotal = 0;
    private Map<Integer, List<Double>> tiemposPorPrioridad = new HashMap<>();
    private List<Consumer<Map<String, Object>>> callbacks = new ArrayList<>();

    public Estadisticas() {
        // Inicializar listas para cada nivel de prioridad
        for (int i = 1; i <= 5; i++) {
            tiemposPorPrioridad.put(i, new ArrayList<>());
        }
    }

    /**
     * Registra una nueva cita en las estadísticas
     */
    public void registrarCita() {
        lock.lock();
        try {
            citasRegistradas++;
            notificarCambios();
        } finally {
            lock.unlock();
        }
    }

    /**
     * Registra la atención de una cita y su tiempo de espera
     */
    public void registrarAtencion(Cita cita, double tiempoEspera) {
        lock.lock();
        try {
            citasAtendidas++;
            tiempoEsperaTotal += tiempoEspera;
            tiemposPorPrioridad.get(cita.getPrioridad()).add(tiempoEspera);
            notificarCambios();
        } finally {
            lock.unlock();
        }
    }

    /**
     * Genera un informe completo de estadísticas
     */
    public Map<String, Object> obtenerInforme() {
        lock.lock();
        try {
            Map<String, Object> informe = new HashMap<>();
            informe.put("citasRegistradas", citasRegistradas);
            informe.put("citasAtendidas", citasAtendidas);

            double tiempoPromedio = 0;
            if (citasAtendidas > 0) {
                tiempoPromedio = tiempoEsperaTotal / citasAtendidas;
            }
            informe.put("tiempoEsperaPromedio", tiempoPromedio);

            Map<Integer, Double> tiemposPromedioPorPrioridad = new HashMap<>();
            for (int prioridad = 1; prioridad <= 5; prioridad++) {
                List<Double> tiempos = tiemposPorPrioridad.get(prioridad);
                if (!tiempos.isEmpty()) {
                    double suma = 0;
                    for (double tiempo : tiempos) {
                        suma += tiempo;
                    }
                    tiemposPromedioPorPrioridad.put(prioridad, suma / tiempos.size());
                } else {
                    tiemposPromedioPorPrioridad.put(prioridad, 0.0);
                }
            }
            informe.put("tiemposPorPrioridad", tiemposPromedioPorPrioridad);

            return informe;
        } finally {
            lock.unlock();
        }
    }

    /**
     * Agrega un callback para ser notificado cuando cambien las estadísticas
     */
    public void agregarCallback(Consumer<Map<String, Object>> callback) {
        callbacks.add(callback);
    }

    /**
     * Notifica a todos los callbacks registrados sobre cambios en las estadísticas
     */
    private void notificarCambios() {
        Map<String, Object> informe = obtenerInforme();
        for (Consumer<Map<String, Object>> callback : callbacks) {
            callback.accept(informe);
        }
    }
}
