# Importamos los módulos necesarios
import threading  
import time       

# Códigos ANSI para colorear la salida del terminal (mejor presentación visual)
ROJO = "\033[91m"
AZUL = "\033[94m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
RESET = "\033[0m"  # Código para resetear al color por defecto

# Declaración de los recursos compartidos (bloqueos)
# Simulan dispositivos físicos como una impresora y un escáner
# Ambos procesos deben adquirirlos para completar su tarea
impresora = threading.Lock()
escaner = threading.Lock()

# Función auxiliar que simula una barra de progreso al bloquear un recurso
# Imprime la etiqueta en color con una animación simple
def barra_progreso(etiqueta, color):
    for _ in range(3):
        print(f"{color}{etiqueta} [{'=' * (_ + 1):<3}]{RESET}", end='\r')  # Sobrescribe la línea
        time.sleep(0.3)  # Espera corta entre pasos de animación
    print()  # Salto de línea final

# Función auxiliar que imprime una línea separadora
def separador():
    print(f"{AMARILLO}" + "-" * 60 + f"{RESET}")

# Primer proceso (hilo): bloquea primero la impresora y luego el escáner
def proceso1():
    print(f"{ROJO}🔴 [Proceso 1] Iniciando...{RESET}")
    
    print(f"{ROJO}🔒 [Proceso 1] Intentando bloquear IMPRESORA...{RESET}")
    with impresora:  # Solicita acceso exclusivo a la impresora
        barra_progreso("🖨️  Bloqueando impresora", ROJO)
        print(f"{ROJO}✅ [Proceso 1] Impresora bloqueada.{RESET}")
        time.sleep(1)  # Simula trabajo con la impresora

        print(f"{ROJO}🔒 [Proceso 1] Intentando bloquear ESCÁNER...{RESET}")
        with escaner:  # Solicita acceso al escáner luego de tener la impresora
            barra_progreso("📠  Bloqueando escáner", ROJO)
            print(f"{ROJO}✅ [Proceso 1] Escáner bloqueado.{RESET}")
            print(f"{ROJO}🧾 [Proceso 1] Usando impresora + escáner...{RESET}")
            time.sleep(1)  # Simula trabajo conjunto

        # Al salir del bloque 'with', el escáner se libera automáticamente
        print(f"{ROJO}🔓 [Proceso 1] Escáner liberado.{RESET}")

    # Al salir del primer bloque 'with', la impresora también se libera
    print(f"{ROJO}🔓 [Proceso 1] Impresora liberada.{RESET}")
    print(f"{ROJO}🏁 [Proceso 1] Finalizado.\n{RESET}")
    separador()

# Segundo proceso (hilo): también bloquea impresora primero, luego el escáner
# Al tener el mismo orden que el proceso1, se evita interbloqueo
def proceso2():
    print(f"{AZUL}🔵 [Proceso 2] Iniciando...{RESET}")
    
    print(f"{AZUL}🔒 [Proceso 2] Intentando bloquear IMPRESORA...{RESET}")
    with impresora:  # Bloquea la impresora como primer recurso
        barra_progreso("🖨️  Bloqueando impresora", AZUL)
        print(f"{AZUL}✅ [Proceso 2] Impresora bloqueada.{RESET}")
        time.sleep(1)

        print(f"{AZUL}🔒 [Proceso 2] Intentando bloquear ESCÁNER...{RESET}")
        with escaner:  # Luego accede al escáner
            barra_progreso("📠  Bloqueando escáner", AZUL)
            print(f"{AZUL}✅ [Proceso 2] Escáner bloqueado.{RESET}")
            print(f"{AZUL}🧾 [Proceso 2] Usando impresora + escáner...{RESET}")
            time.sleep(1)

        # Se libera escáner
        print(f"{AZUL}🔓 [Proceso 2] Escáner liberado.{RESET}")

    # Se libera impresora
    print(f"{AZUL}🔓 [Proceso 2] Impresora liberada.{RESET}")
    print(f"{AZUL}🏁 [Proceso 2] Finalizado.\n{RESET}")
    separador()

# Registro del tiempo inicial para calcular la duración total del programa
inicio_global = time.time()

# Se crean dos hilos, cada uno ejecutará un proceso
t1 = threading.Thread(target=proceso1)
t2 = threading.Thread(target=proceso2)

# Título inicial del programa
print(f"{VERDE}=== Simulación de procesos con orden consistente para evitar interbloqueo ==={RESET}")
separador()

# Se inicia la ejecución paralela de ambos procesos
t1.start()
t2.start()

# Espera a que ambos procesos terminen antes de continuar
t1.join()
t2.join()

# Registro del tiempo final
fin_global = time.time()

# Mensaje final indicando éxito y duración total
print(f"{VERDE}✅ Ambos procesos han finalizado correctamente sin interbloqueo.{RESET}")
print()
print(f"{VERDE}💡 Esto ocurrió porque ambos procesos solicitaron los recursos en el mismo orden:")
print(f"   primero la impresora y luego el escáner.")
print(f"   Al mantener este orden, se evita una espera circular,")
print(f"   una de las condiciones necesarias para que ocurra un interbloqueo.{RESET}")
print()
print(f"{VERDE}⏱️ Tiempo total del programa: {fin_global - inicio_global:.2f} segundos{RESET}")

