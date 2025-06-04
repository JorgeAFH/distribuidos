import time 
import random

platillos = [] # Lista donde se almacenan los platillos preparados

def cocinero():
    for i in range(5):
        platillo = f"Platillo cocinado {i+1}"
        print(f"Cocinero preparando {platillo}...")
        time.sleep(random.randint(2, 5))  # Este tiempo simula la preparación del platillo
        platillos.append(platillo)  # Agrega el platillo a la lista
        print(f"{platillo} listo")

def mesero():
    for i in range(5):
        if platillos:
            platillo = platillos.pop(0)  # El mesero toma el primer platillo de la lista
            print(f"Mesero entregando {platillo} al cliente")
        time.sleep(1)  # El mesero espera un segundo antes de entregar el siguiente platillo

def restaurante_secuencial():
    inicio = time.time()  # Marca el tiempo de inicio

    cocinero()  # El cocinero prepara los platillos uno tras otro
    mesero()    # El mesero entrega los platillos uno tras otro

    fin = time.time()  # Marca el tiempo de fin
    print(f"\nTiempo de ejecución secuencial: {fin - inicio:.2f} segundos")

restaurante_secuencial()


