package ejemplosjava;
import java.util.LinkedList;
import java.util.Queue;

// Clase que simula un restaurante de forma secuencial
public class secuencial {

    // Cola para guardar los platillos preparados
    static Queue<String> platillos = new LinkedList<>();

    // El cocinero prepara 5 platillos uno por uno
    public static void cocinero() {
        for (int i = 1; i <= 5; i++) {
            String platillo = "Platillo cocinado " + i;
            System.out.println("Cocinero preparando " + platillo + "...");

            try {
                // Espera entre 2 y 5 segundos (simula el tiempo de preparación)
                Thread.sleep((int) (Math.random() * 3000) + 2000);
            } catch (InterruptedException e) {
                e.printStackTrace();  // Muestra error si se interrumpe el hilo
            }

            platillos.add(platillo);  // Agrega el platillo a la cola
            System.out.println(platillo + " listo");
        }
    }

    // El mesero entrega los platillos uno por uno
    public static void mesero() {
        for (int i = 1; i <= 5; i++) {
            if (!platillos.isEmpty()) {
                String platillo = platillos.poll();  // Saca el primer platillo de la cola
                System.out.println("Mesero entregando " + platillo + " al cliente");
            }

            try {
                Thread.sleep(1000);  // Espera 1 segundo entre entregas
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    // Método principal que ejecuta el programa
    public static void main(String[] args) {
        long inicio = System.currentTimeMillis();  // Tiempo inicial

        cocinero();  // Prepara los platillos
        mesero();    // Entrega los platillos

        long fin = System.currentTimeMillis();  // Tiempo final

        // Muestra cuánto tiempo tomó todo el proceso
        System.out.println("Tiempo total (secuencial): " + (fin - inicio) / 1000.0 + " segundos");
    }
}
