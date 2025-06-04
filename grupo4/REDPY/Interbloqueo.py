import threading  # Para manejar hilos de ejecución simultánea
import time       # Para simular demoras con sleep()

# Colores ANSI para mejorar la salida en consola con colores
ROJO = "\033[91m"
AZUL = "\033[94m"
AMARILLO = "\033[93m"
VERDE = "\033[92m"
RESET = "\033[0m"  # Resetear el color a predeterminado

# Separadores visuales para la salida en consola
SEPARADOR = f"{AMARILLO}\n{'═'*60}{RESET}"  # Línea amarilla horizontal
TITULO = f"{AMARILLO}{'='*20} SIMULACIÓN DE INTERBLOQUEO {'='*20}{RESET}"

# Definición de los recursos compartidos simulados
# Estos podrían representar dispositivos físicos como una impresora y un escáner
impresora = threading.Lock()
escaner = threading.Lock()

# Proceso 1: solicita primero la impresora y luego el escáner
def proceso1():
    print(SEPARADOR)
    print(f"{ROJO}[Proceso 1] 🖨️ Solicitando acceso a la impresora...{RESET}")
    
    # Bloquea el recurso 'impresora'
    with impresora:
        print(f"{ROJO}[Proceso 1] 🔒 Impresora bloqueada con éxito.{RESET}")
        time.sleep(1)  # Simula trabajo con la impresora antes de pedir el siguiente recurso
        
        print(f"{ROJO}[Proceso 1] 📠 Solicitando acceso al escáner...{RESET}")
        
        # Intenta bloquear el recurso 'escaner'
        with escaner:
            print(f"{ROJO}[Proceso 1] 🔒 Escáner bloqueado con éxito.{RESET}")
            print(f"{ROJO}[Proceso 1] 🧾 Utilizando impresora y escáner...{RESET}")
        
        # Escáner se libera al salir del bloque 'with'
        print(f"{ROJO}[Proceso 1] 🔓 Escáner liberado.{RESET}")
    
    # Impresora se libera al salir del primer bloque 'with'
    print(f"{ROJO}[Proceso 1] 🔓 Impresora liberada. ✅ Proceso 1 finalizado.{RESET}")
    print(SEPARADOR)

# Proceso 2: solicita primero el escáner y luego la impresora (orden inverso al proceso1)
def proceso2():
    print(SEPARADOR)
    print(f"{AZUL}[Proceso 2] 📠 Solicitando acceso al escáner...{RESET}")
    
    # Bloquea el recurso 'escaner'
    with escaner:
        print(f"{AZUL}[Proceso 2] 🔒 Escáner bloqueado con éxito.{RESET}")
        time.sleep(1)  # Simula trabajo con el escáner antes de pedir el siguiente recurso
        
        print(f"{AZUL}[Proceso 2] 🖨️ Solicitando acceso a la impresora...{RESET}")
        
        # Intenta bloquear el recurso 'impresora'
        with impresora:
            print(f"{AZUL}[Proceso 2] 🔒 Impresora bloqueada con éxito.{RESET}")
            print(f"{AZUL}[Proceso 2] 🧾 Utilizando escáner e impresora...{RESET}")
        
        # Impresora se libera al salir del bloque 'with'
        print(f"{AZUL}[Proceso 2] 🔓 Impresora liberada.{RESET}")
    
    # Escáner se libera al salir del primer bloque 'with'
    print(f"{AZUL}[Proceso 2] 🔓 Escáner liberado. ✅ Proceso 2 finalizado.{RESET}")
    print(SEPARADOR)

# Crear los hilos que ejecutarán cada proceso en paralelo
t1 = threading.Thread(target=proceso1)
t2 = threading.Thread(target=proceso2)


print(TITULO)
print(f"{AMARILLO}🚦 Iniciando ejecución de procesos... Posible interbloqueo en camino.{RESET}")
print(SEPARADOR)

# Iniciar la ejecución concurrente de los procesos
t1.start()
t2.start()

# Esperamos hasta 5 segundos a que ambos hilos terminen
# Si se bloquean entre sí, seguirán vivos después del timeout
t1.join(timeout=5)
t2.join(timeout=5)

# Evaluamos si los procesos siguen vivos (lo que indica un posible interbloqueo)
print(SEPARADOR)
if t1.is_alive() or t2.is_alive():
    # Al menos uno no ha terminado => están esperando recursos entre sí (deadlock)
    print(f"{ROJO}🛑 INTERBLOQUEO DETECTADO{RESET}")
    print()
    print(f"{ROJO}🔄 Esto ocurrió porque los procesos adquirieron los recursos en distinto orden:{RESET}")
    print(f"{ROJO}   - Proceso 1 bloqueó primero la impresora y luego intentó acceder al escáner.{RESET}")
    print(f"{ROJO}   - Proceso 2 bloqueó primero el escáner y luego intentó acceder a la impresora.{RESET}")
    print()
    print(f"{ROJO}🧱 Esto provocó una espera circular: cada proceso quedó esperando un recurso{RESET}")
    print(f"{ROJO}   que el otro ya tenía bloqueado, sin posibilidad de continuar.{RESET}")
    print()
    print(f"{AMARILLO}💡 Sugerencia: para evitar este tipo de interbloqueos, se debe garantizar{RESET}")
    print(f"{AMARILLO}   que todos los procesos adquieran los recursos en el mismo orden.{RESET}")
else:
    # Ambos procesos lograron terminar sin quedar esperando
    print(f"{VERDE}✅ EJECUCIÓN EXITOSA: Ambos procesos finalizaron sin interbloqueo.{RESET}")
print(SEPARADOR)
