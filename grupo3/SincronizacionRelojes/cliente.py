# cliente.py
import socket
import datetime
import time

HOST = 'localhost'
PORT = 5000

# Tomar T0 (inicio)
T0 = time.time()

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

datos = cliente.recv(1024).decode()
cliente.close()

# Tomar T1 (respuesta)
T1 = time.time()

# Procesar datos
hora_servidor = datetime.datetime.strptime(datos, '%Y-%m-%d %H:%M:%S.%f')
retardo_red = (T1 - T0) / 2
hora_sincronizada = hora_servidor + datetime.timedelta(seconds=retardo_red)

# Mostrar resultados
print(f"Hora local:      {datetime.datetime.now()}")
print(f"Hora servidor:   {hora_servidor}")
print(f"Hora ajustada:   {hora_sincronizada}")
print(f"Retardo estimado: {retardo_red:.6f} segundos")
