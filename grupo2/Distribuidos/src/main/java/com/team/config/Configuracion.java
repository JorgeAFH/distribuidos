package com.team.config;

import com.team.interfaces.Cita;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.BiConsumer;
import java.util.function.Consumer;

/**
 * Clase que contiene la configuración global del sistema
 */
public class Configuracion {
    public static final int NUM_RECEPCIONISTAS = 3;     // Número de hilos productores
    public static final int NUM_DOCTORES = 2;           // Número de hilos consumidores
    public static final int NUM_CITAS_POR_RECEPCIONISTA = 10;
    public static final int TOTAL_CITAS = NUM_RECEPCIONISTAS * NUM_CITAS_POR_RECEPCIONISTA;

    public static double FACTOR_VELOCIDAD = 1.0;

    // Colas de espera por nivel de prioridad
    public static final Map<Integer, BlockingQueue<Cita>> SALAS_ESPERA = new HashMap<>();

    // Contador de citas atendidas
    public static final AtomicInteger CITAS_ATENDIDAS = new AtomicInteger(0);

    // Señal de finalización
    public static final CountDownLatch FINALIZACION_RECEPCIONISTAS = new CountDownLatch(NUM_RECEPCIONISTAS);
    public static volatile boolean JORNADA_TERMINADA = false;

    // Control de pausa
    public static final Object LOCK_PAUSA = new Object();
    public static volatile boolean SIMULACION_PAUSADA = false;

    // Generador de números aleatorios
    public static final Random RANDOM = new Random();

    // Datos para generar citas aleatorias
    public static final String[] NOMBRES_PACIENTES = {
            "Jordan Zambrano", "Yusmeli Vilela", "Maria Jose Sabando", "Angie Loor",
            "Jhonny Mero", "Yesenia Quishpe", "Anthony Caicedo", "Dayana Álava",
            "Kevin Pilay", "Yuleisi Vera", "Steven Quintero", "Byron Calderon"
    };

    public static final String[] SINTOMAS = {
            "Dolor de cabeza y fiebre", "Dolor abdominal intenso", "Mareos y náuseas",
            "Dificultad para respirar", "Dolor en el pecho", "Fractura expuesta",
            "Revisión rutinaria", "Seguimiento de tratamiento", "Dolor de garganta",
            "Erupción cutánea", "Dolor de espalda", "Presión arterial alta"
    };

    // Callbacks para notificar eventos a la interfaz gráfica
    private static final List<Consumer<Cita>> CALLBACKS_NUEVA_CITA = new ArrayList<>();
    private static final List<BiConsumer<Cita, Integer>> CALLBACKS_ATENCION_CITA = new ArrayList<>();

    // Inicializar las salas de espera
    static {
        for (int i = 1; i <= 5; i++) {
            SALAS_ESPERA.put(i, new LinkedBlockingQueue<>(10));
        }
    }

    /**
     * Registra un callback para ser notificado cuando se crea una nueva cita
     */
    public static void registrarCallbackNuevaCita(Consumer<Cita> callback) {
        CALLBACKS_NUEVA_CITA.add(callback);
    }

    /**
     * Notifica a todos los callbacks registrados sobre una nueva cita
     */
    public static void notificarNuevaCita(Cita cita) {
        for (Consumer<Cita> callback : CALLBACKS_NUEVA_CITA) {
            callback.accept(cita);
        }
    }

    /**
     * Registra un callback para ser notificado cuando se atiende una cita
     */
    public static void registrarCallbackAtencionCita(BiConsumer<Cita, Integer> callback) {
        CALLBACKS_ATENCION_CITA.add(callback);
    }

    /**
     * Notifica a todos los callbacks registrados sobre la atención de una cita
     */
    public static void notificarAtencionCita(Cita cita, int doctorId) {
        for (BiConsumer<Cita, Integer> callback : CALLBACKS_ATENCION_CITA) {
            callback.accept(cita, doctorId);
        }
    }

    /**
     * Pausa la simulación
     */
    public static void pausarSimulacion() {
        SIMULACION_PAUSADA = true;
    }

    /**
     * Reanuda la simulación
     */
    public static void reanudarSimulacion() {
        SIMULACION_PAUSADA = false;
        synchronized (LOCK_PAUSA) {
            LOCK_PAUSA.notifyAll();
        }
    }

    /**
     * Espera si la simulación está pausada
     */
    public static void esperarSiPausado() throws InterruptedException {
        if (SIMULACION_PAUSADA) {
            synchronized (LOCK_PAUSA) {
                while (SIMULACION_PAUSADA) {
                    LOCK_PAUSA.wait();
                }
            }
        }
    }

    /**
     * Establece la velocidad de la simulación
     */
    public static void establecerVelocidad(double factor) {
        FACTOR_VELOCIDAD = factor;
    }
}
