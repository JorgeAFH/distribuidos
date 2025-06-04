import threading    # Módulo para hilos.
import time         # Simular tiempo. 
import random       # Genera valores aleatorios.

platillos = []      
platillos_a_preparar = 5  
contador_platillos = 1     # Para enumerar cada platillo
lock = threading.Lock()    # Para evitar conflictos al acceder a la lista y al contador.

# Evento para saber cuándo todos los cocineros han terminado
cocineros_terminaron = threading.Event()
cocineros_activos = 3  # Número de cocineros

def cocinero(id):           
    global platillos_a_preparar, contador_platillos, cocineros_activos
    while True:         
        with lock:      # Controla a los cocineros, 1 a la vez.
            if platillos_a_preparar <= 0:
                cocineros_activos -= 1
                if cocineros_activos == 0:
                    cocineros_terminaron.set()  # Señal de que todos terminaron
                break  # No hay platillos por hacer.
            platillo_id = contador_platillos
            contador_platillos += 1
            platillos_a_preparar -= 1   # Si hay platillos por hacer, se resta 1 

        nombre_platillo = f"Platillo-{platillo_id}"
        autor = f"Cocinero-{id}"
        print(f"{autor} preparando {nombre_platillo}...")

        time.sleep(random.randint(2, 5))  # Pausa y simula el tiempo de preparación.

        with lock:  # Accede a la lista de platillos.
            platillos.append((nombre_platillo, autor))  # Guarda el platillo junto con su autor.

        print(f"{nombre_platillo} listo por {autor}")

def mesero(id):     
    while True:
        with lock:  # Controla la lista de platillos. 
            if platillos:
                nombre_platillo, autor = platillos.pop(0)  # Toma el primer platillo.
                print(f"Mesero-{id} entregando {nombre_platillo} (hecho por {autor}) al cliente")
        if not platillos and cocineros_terminaron.is_set():
            break  # Si no hay platillos y los cocineros terminaron, salir
        time.sleep(1)  # Espera 1 seg antes de revisar otro platillo nuevo.

def restaurante_concurrente(): 
    inicio = time.time()  # Marca el tiempo de inicio
    
    cocinero_hilos = [threading.Thread(target=cocinero, args=(i+1,)) for i in range(3)]
    mesero_hilos = [threading.Thread(target=mesero, args=(i+1,)) for i in range(2)]

    # Inicia todos los hilos al mismo tiempo.
    for hilo in cocinero_hilos + mesero_hilos:
        hilo.start()
    # Todos los hilos terminan su ejecución.
    for hilo in cocinero_hilos + mesero_hilos:
        hilo.join()

    fin = time.time()  # Marca el tiempo de fin
    print(f"\nTiempo de ejecución concurrente: {fin - inicio:.2f} segundos")

# Ejecuta el restaurante
restaurante_concurrente()





