import socket
import datetime
import time
import threading
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Variables globales
historial_retardo = []
historial_diferencia = []
sincronizacion_activa = False
hilo_sincro = None

def sincronizar():
    try:
        T0 = time.time()

        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(('localhost', 5000))
        datos = cliente.recv(1024).decode()
        cliente.close()

        T1 = time.time()

        hora_servidor = datetime.datetime.strptime(datos, '%Y-%m-%d %H:%M:%S.%f')
        retardo_red = (T1 - T0) / 2
        hora_sincronizada = hora_servidor + datetime.timedelta(seconds=retardo_red)
        hora_local = datetime.datetime.now()
        diferencia_horas = abs((hora_sincronizada - hora_local).total_seconds())

        # Actualizar etiquetas
        lbl_hora_local.config(text=f"🕓 Hora Local del Cliente: {hora_local.strftime('%H:%M:%S.%f')[:-3]}")
        lbl_hora_servidor.config(text=f"🕒 Hora del Servidor: {hora_servidor.strftime('%H:%M:%S.%f')[:-3]}")
        lbl_hora_sinc.config(text=f"✅ Hora Sincronizada: {hora_sincronizada.strftime('%H:%M:%S.%f')[:-3]}")
        lbl_retardo.config(text=f"📶 Retardo estimado de red: {retardo_red:.6f} segundos")
        lbl_diferencia.config(text=f"📊 Diferencia entre Hora Local y Sincronizada: {diferencia_horas:.6f} segundos")

        # Guardar datos
        historial_retardo.append(retardo_red)
        historial_diferencia.append(diferencia_horas)
        tabla.insert('', 'end', values=(len(historial_retardo), f"{retardo_red:.6f}", f"{diferencia_horas:.6f}"))

        actualizar_grafico()

    except Exception as e:
        lbl_estado.config(text=f"⚠️ Error: {e}")

def sincronizar_automatica():
    global sincronizacion_activa
    while sincronizacion_activa:
        sincronizar()
        time.sleep(5)

def activar():
    global sincronizacion_activa, hilo_sincro
    if not sincronizacion_activa:
        sincronizacion_activa = True
        hilo_sincro = threading.Thread(target=sincronizar_automatica)
        hilo_sincro.daemon = True
        hilo_sincro.start()
        lbl_estado.config(text="🟢 Sincronización activa: El cliente está ajustando su reloj cada 5 segundos.")

def detener():
    global sincronizacion_activa
    sincronizacion_activa = False
    lbl_estado.config(text="🔴 Sincronización detenida. El cliente ya no está ajustando su reloj.")

def actualizar_grafico():
    ax1.clear()
    ax2.clear()

    eje_x = list(range(1, len(historial_retardo) + 1))

    ax1.plot(eje_x, historial_retardo, color='royalblue', marker='o')
    ax1.fill_between(eje_x, historial_retardo, color='lightblue', alpha=0.5)
    ax1.set_title("📶 Retardo estimado de red", fontsize=10)
    ax1.set_ylabel("Segundos")
    ax1.grid(True, linestyle="--", alpha=0.5)

    ax2.plot(eje_x, historial_diferencia, color='darkorange', marker='s')
    ax2.fill_between(eje_x, historial_diferencia, color='moccasin', alpha=0.5)
    ax2.set_title("📊 Diferencia entre Hora Local del Cliente y Hora Sincronizada", fontsize=10)
    ax2.set_xlabel("Intento")
    ax2.set_ylabel("Segundos")
    ax2.grid(True, linestyle="--", alpha=0.5)

    canvas.draw()

# Interfaz
ventana = tk.Tk()
ventana.title("⏰ Cliente de Sincronización de Relojes - Presentación Educativa")
ventana.geometry("1100x800")
ventana.configure(bg="#eef2f7")

# Título y explicación general
ttk.Label(ventana, text="📘 ¿Qué hace este sistema?",
          font=("Arial", 14, "bold"), background="#eef2f7").pack(pady=5)
ttk.Label(
    ventana,
    text="Este cliente simula cómo una computadora ajusta su reloj local según la hora de un servidor, "
         "usando el Algoritmo de Cristian. Esto es esencial en sistemas distribuidos donde "
         "la coordinación temporal entre dispositivos es crítica.",
    font=("Arial", 10), background="#eef2f7", wraplength=950, justify="center"
).pack(pady=5)

# Botones
frame_botones = ttk.Frame(ventana)
frame_botones.pack(pady=10)
ttk.Button(frame_botones, text="▶ Activar sincronización automática", command=activar).grid(row=0, column=0, padx=10)
ttk.Button(frame_botones, text="⏹ Detener sincronización", command=detener).grid(row=0, column=1, padx=10)
ttk.Button(frame_botones, text="🔄 Sincronizar solo una vez", command=sincronizar).grid(row=0, column=2, padx=10)

# Estado actual
lbl_estado = ttk.Label(ventana, text="⏸ Estado: Esperando acción del usuario...", font=("Arial", 11, "italic"),
                       background="#eef2f7")
lbl_estado.pack(pady=5)

# Datos actuales
lbl_hora_local = ttk.Label(ventana, text="", font=("Arial", 11), background="#eef2f7")
lbl_hora_local.pack()
lbl_hora_servidor = ttk.Label(ventana, text="", font=("Arial", 11), background="#eef2f7")
lbl_hora_servidor.pack()
lbl_hora_sinc = ttk.Label(ventana, text="", font=("Arial", 11), background="#eef2f7")
lbl_hora_sinc.pack()
lbl_retardo = ttk.Label(ventana, text="", font=("Arial", 11), background="#eef2f7")
lbl_retardo.pack()
lbl_diferencia = ttk.Label(ventana, text="", font=("Arial", 11), background="#eef2f7")
lbl_diferencia.pack(pady=5)

# Tabla
ttk.Label(ventana, text="📋 Historial de sincronizaciones", font=("Arial", 13, "bold"), background="#eef2f7").pack(pady=10)
ttk.Label(ventana, text="Cada fila representa un intento de sincronización realizado por el cliente.",
          background="#eef2f7", font=("Arial", 9)).pack()

tabla = ttk.Treeview(ventana, columns=('Intento', 'Retardo', 'Diferencia'), show='headings', height=6)
tabla.heading('Intento', text='Intento')
tabla.heading('Retardo', text='Retardo (s)')
tabla.heading('Diferencia', text='Diferencia Local vs Sincronizada (s)')
tabla.pack()

# Gráficos
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5))
fig.tight_layout(pad=4.0)
canvas = FigureCanvasTkAgg(fig, master=ventana)
canvas.get_tk_widget().pack(pady=10)

# Explicación de gráficos
ttk.Label(ventana, text="📈 Explicación de los gráficos", font=("Arial", 12, "bold"), background="#eef2f7").pack()
ttk.Label(ventana,
          text="• El primer gráfico muestra cuánto tarda en promedio una sincronización (retardo de red).\n"
               "• El segundo muestra qué tan bien está sincronizado el reloj local con el servidor. Una diferencia pequeña es ideal.",
          font=("Arial", 10), background="#eef2f7", justify="left", wraplength=950).pack(pady=10)

# Ejecutar ventana
ventana.mainloop()
