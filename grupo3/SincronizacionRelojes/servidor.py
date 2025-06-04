# servidor.py
import socket
import datetime

HOST = 'localhost'
PORT = 5000

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()

print(f"[Servidor de Tiempo] Esperando conexiones en {HOST}:{PORT}...")

while True:
    conn, addr = servidor.accept()
    print(f"[Conexión] Cliente conectado desde {addr}")
    hora_actual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    conn.sendall(hora_actual.encode())
    conn.close()
