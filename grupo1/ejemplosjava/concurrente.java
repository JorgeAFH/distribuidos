package ejemplosjava;

import java.util.LinkedList;
import java.util.Queue;

public class concurrente {
    static Queue<String> platillos = new LinkedList<>();
    static int contadorPlatillos = 1;  // Contador de platillos
    static final int TOTAL_PLATILLOS = 5;  // Total de platillos a preparar
    static int platillosEntregados = 0;  // Control de cuántos platillos han sido entregados

    // Clase interna que representa al cocinero como un hilo (thread)
    public static class Cocinero extends Thread {
        private int id;

        public Cocinero(int id) {
            this.id = id;
        }

        public void run() {
            // El cocinero prepara platillos hasta que se llegue al total
            while (true) {
                String platillo;

                // Sincronizamos el acceso al contador de platillos para evitar problemas de concurrencia
                synchronized (concurrente.class) {
                    if (contadorPlatillos > TOTAL_PLATILLOS) {
                        break;  // Salir del ciclo cuando se alcanzan los 5 platillos
                    }
                    platillo = "Platillo cocinado " + contadorPlatillos++ + " por Cocinero " + id;
                }

                // Mostramos qué está haciendo el cocinero
                System.out.println("Cocinero " + id + " preparando " + platillo + "...");
                try {
                    // Simulamos el tiempo de preparación con una pausa entre 2 y 5 segundos
                    Thread.sleep((int) (Math.random() * 3000) + 2000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

                // Sección crítica: acceso sincronizado a la cola de platillos
                synchronized (platillos) {
                    platillos.add(platillo);
                    System.out.println(platillo + " listo");
                    platillos.notify();  // Notificar a los meseros que hay un platillo listo
                }
            }
        }
    }

    // Clase interna que representa al mesero como un hilo (thread)
    public static class Mesero extends Thread {
        private int id;

        public Mesero(int id) {
            this.id = id;
        }

        public void run() {
            // El mesero entrega platillos hasta que todos hayan sido entregados
            while (true) {
                String platillo = null;

                // Sección crítica: acceso sincronizado a la cola de platillos
                synchronized (platillos) {
                    // Si no hay platillos disponibles, el mesero espera
                    while (platillos.isEmpty()) {
                        try {
                            platillos.wait();  // Esperar hasta que un cocinero notifique
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                    }
                    // Extrae un platillo de la cola
                    platillo = platillos.poll();
                }

                // Si se obtuvo un platillo, lo entrega al cliente
                if (platillo != null) {
                    System.out.println("Mesero " + id + " entregando " + platillo + " al cliente");
                    synchronized (concurrente.class) {
                        platillosEntregados++;
                    }
                }

                // Simulamos el tiempo de entrega del platillo
                try {
                    Thread.sleep(1000);  // 1 segundo
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

                // Terminar cuando todos los platillos hayan sido entregados
                synchronized (concurrente.class) {
                    if (platillosEntregados >= TOTAL_PLATILLOS) {
                        break;  // Terminar cuando se hayan entregado los 5 platillos
                    }
                }
            }
        }
    }

    // Método principal que ejecuta el programa
    public static void main(String[] args) {
        long inicio = System.currentTimeMillis();  // Guardamos el tiempo de inicio

        // Crear cocineros
        Cocinero cocinero1 = new Cocinero(1);
        Cocinero cocinero2 = new Cocinero(2);
        Cocinero cocinero3 = new Cocinero(3);

        // Crear meseros
        Mesero mesero1 = new Mesero(1);
        Mesero mesero2 = new Mesero(2);

        // Iniciar hilos
        cocinero1.start();
        cocinero2.start();
        cocinero3.start();
        mesero1.start();
        mesero2.start();

        // Esperar a que todos los hilos terminen
        try {
            cocinero1.join();
            cocinero2.join();
            cocinero3.join();
            mesero1.join();
            mesero2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        long fin = System.currentTimeMillis();  // Guardamos el tiempo de fin
        System.out.printf("Tiempo total (concurrente): " + (fin - inicio) / 1000.0 + " segundos");
    }
}
