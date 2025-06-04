import time
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Dict, List, Callable, Any
import threading
from datetime import datetime

from config import Config
from models import Cita

"""
Interfaz gráfica del sistema
Equivalente a InterfazGrafica.java
"""
class InterfazGrafica:
    def __init__(self, estadisticas, iniciar_simulacion_callback):
        self.estadisticas = estadisticas
        self.iniciar_simulacion_callback = iniciar_simulacion_callback

        # Estado de la simulación
        self.simulacion_iniciada = False
        self.simulacion_pausada = False

        # Datos
        self.citas_en_espera = {i: [] for i in range(1, 6)}
        self.citas_en_atencion = {}

        # Registrar callbacks
        Config.registrar_callback_nueva_cita(self.actualizar_nueva_cita)
        Config.registrar_callback_atencion_cita(self.actualizar_atencion_cita)
        estadisticas.agregar_callback(self.actualizar_estadisticas)

        # Crear la interfaz gráfica
        self.crear_interfaz()

    def crear_interfaz(self):
        """Crea la interfaz gráfica principal"""
        # Crear ventana principal
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Gestión de Citas Médicas")
        self.ventana.geometry("1000x700")
        self.ventana.protocol("WM_DELETE_WINDOW", self.confirmar_salida)

        # Crear pestañas
        self.pestanas = ttk.Notebook(self.ventana)
        self.pestanas.pack(fill=tk.BOTH, expand=True)

        # Crear paneles para cada pestaña
        self.panel_visualizacion = ttk.Frame(self.pestanas)
        self.panel_estadisticas = ttk.Frame(self.pestanas)
        self.panel_registro = ttk.Frame(self.pestanas)

        self.pestanas.add(self.panel_visualizacion, text="Visualización")
        self.pestanas.add(self.panel_estadisticas, text="Estadísticas")
        self.pestanas.add(self.panel_registro, text="Registro de Actividad")

        # Configurar cada panel
        self.configurar_panel_visualizacion()
        self.configurar_panel_estadisticas()
        self.configurar_panel_registro()

        # Configurar barra de control
        self.configurar_barra_control()

    def configurar_panel_visualizacion(self):
        """Configura el panel de visualización"""
        # Panel principal con scroll
        panel_scroll = ttk.Frame(self.panel_visualizacion)
        panel_scroll.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(panel_scroll)
        scrollbar = ttk.Scrollbar(panel_scroll, orient="vertical", command=canvas.yview)
        panel_contenido = ttk.Frame(canvas)

        panel_contenido.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=panel_contenido, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Panel para salas de espera
        panel_salas = ttk.LabelFrame(panel_contenido, text="Salas de Espera")
        panel_salas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Crear tablas para cada sala de espera
        niveles = ["", "EMERGENCIA", "URGENTE", "PRIORITARIO", "NORMAL", "RUTINA"]
        self.tablas_salas = {}

        for i in range(1, 6):
            panel_nivel = ttk.Frame(panel_salas)
            panel_nivel.pack(fill=tk.X, padx=5, pady=5)

            etiqueta = ttk.Label(panel_nivel, text=f"Sala {niveles[i]}:", font=("Arial", 10, "bold"))
            etiqueta.pack(side=tk.LEFT, padx=5)

            # Crear tabla
            tabla = ttk.Treeview(panel_nivel, columns=("id", "paciente", "sintomas"), show="headings", height=3)
            tabla.heading("id", text="ID")
            tabla.heading("paciente", text="Paciente")
            tabla.heading("sintomas", text="Síntomas")
            
            tabla.column("id", width=50)
            tabla.column("paciente", width=150)
            tabla.column("sintomas", width=250)
            
            tabla.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Agregar scrollbar horizontal
            scrollbar_x = ttk.Scrollbar(panel_nivel, orient="horizontal", command=tabla.xview)
            tabla.configure(xscrollcommand=scrollbar_x.set)
            scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
            
            self.tablas_salas[i] = tabla

        # Panel para consultas médicas
        panel_consultas = ttk.LabelFrame(panel_contenido, text="Consultas Médicas")
        panel_consultas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Crear paneles para cada doctor
        self.paneles_doctores = {}

        for i in range(1, Config.NUM_DOCTORES + 1):
            panel_doctor = ttk.Frame(panel_consultas)
            panel_doctor.pack(fill=tk.X, padx=5, pady=5)

            etiqueta = ttk.Label(panel_doctor, text=f"Doctor {i}:", font=("Arial", 10, "bold"))
            etiqueta.pack(side=tk.LEFT, padx=5)

            panel_paciente = ttk.Label(panel_doctor, text="Sin paciente", 
                                      background="#f0f0f0", relief="solid", 
                                      borderwidth=1, padding=5, width=50)
            panel_paciente.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            self.paneles_doctores[i] = panel_paciente

    def configurar_panel_estadisticas(self):
        """Configura el panel de estadísticas"""
        # Panel principal con scroll
        panel_scroll = ttk.Frame(self.panel_estadisticas)
        panel_scroll.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(panel_scroll)
        scrollbar = ttk.Scrollbar(panel_scroll, orient="vertical", command=canvas.yview)
        panel_contenido = ttk.Frame(canvas)

        panel_contenido.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=panel_contenido, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Panel para estadísticas generales
        panel_general = ttk.LabelFrame(panel_contenido, text="Estadísticas Generales")
        panel_general.pack(fill=tk.X, padx=10, pady=5)

        # Crear etiquetas para estadísticas
        self.lbl_citas_registradas = ttk.Label(panel_general, text="Citas registradas: 0")
        self.lbl_citas_atendidas = ttk.Label(panel_general, text="Citas atendidas: 0")
        self.lbl_tiempo_espera = ttk.Label(panel_general, text="Tiempo de espera promedio: 0.00s")

        self.lbl_citas_registradas.pack(anchor=tk.W, padx=10, pady=5)
        self.lbl_citas_atendidas.pack(anchor=tk.W, padx=10, pady=5)
        self.lbl_tiempo_espera.pack(anchor=tk.W, padx=10, pady=5)

        # Panel para tiempos por prioridad
        panel_tiempos = ttk.LabelFrame(panel_contenido, text="Tiempos de Espera por Prioridad")
        panel_tiempos.pack(fill=tk.X, padx=10, pady=5)

        # Crear etiquetas para tiempos por prioridad
        self.lbl_tiempos_prioridad = {}
        niveles = ["", "EMERGENCIA", "URGENTE", "PRIORITARIO", "NORMAL", "RUTINA"]
        
        for i in range(1, 6):
            lbl = ttk.Label(panel_tiempos, text=f"{niveles[i]}: 0.00s")
            lbl.pack(anchor=tk.W, padx=10, pady=5)
            self.lbl_tiempos_prioridad[i] = lbl

        # Panel para barra de progreso
        panel_progreso = ttk.LabelFrame(panel_contenido, text="Progreso de la Simulación")
        panel_progreso.pack(fill=tk.X, padx=10, pady=5)

        lbl_progreso = ttk.Label(panel_progreso, text="Progreso de citas:")
        lbl_progreso.pack(anchor=tk.W, padx=10, pady=5)

        self.barra_progreso = ttk.Progressbar(panel_progreso, orient="horizontal", length=400, mode="determinate")
        self.barra_progreso.pack(fill=tk.X, padx=10, pady=5)

    def configurar_panel_registro(self):
        """Configura el panel de registro de actividad"""
        # Crear área de texto con scroll
        self.txt_registro = scrolledtext.ScrolledText(self.panel_registro, wrap=tk.WORD, font=("Courier", 10))
        self.txt_registro.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.txt_registro.config(state=tk.DISABLED)  # Solo lectura

        # Mensaje inicial
        self.agregar_registro("Sistema de Gestión de Citas Médicas iniciado", "info")

    def configurar_barra_control(self):
        """Configura la barra de control"""
        panel_control = ttk.Frame(self.ventana)
        panel_control.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        # Botón para iniciar/detener simulación
        self.btn_iniciar = ttk.Button(panel_control, text="Iniciar Simulación", command=self.toggle_simulacion)
        self.btn_iniciar.pack(side=tk.LEFT, padx=5)

        # Botón para pausar/reanudar simulación
        self.btn_pausar = ttk.Button(panel_control, text="Pausar", command=self.toggle_pausa)
        self.btn_pausar.pack(side=tk.LEFT, padx=5)
        self.btn_pausar.config(state=tk.DISABLED)


    def toggle_simulacion(self):
        """Inicia o detiene la simulación"""
        if not self.simulacion_iniciada:
            # Iniciar simulación
            self.simulacion_iniciada = True
            self.btn_iniciar.config(text="Detener Simulación")
            self.btn_pausar.config(state=tk.NORMAL)

            # Llamar al callback para iniciar la simulación
            threading.Thread(target=self.iniciar_simulacion_callback).start()

            self.agregar_registro("Simulación iniciada", "info")
        else:
            # Preguntar si realmente quiere detener
            respuesta = messagebox.askyesno(
                "Detener Simulación",
                "¿Está seguro de que desea detener la simulación?"
            )

            if respuesta:
                # Detener simulación (cerrar la aplicación)
                self.ventana.quit()

    def toggle_pausa(self):
        """Pausa o reanuda la simulación"""
        if not self.simulacion_pausada:
            # Pausar simulación
            self.simulacion_pausada = True
            self.btn_pausar.config(text="Reanudar")
            Config.pausar_simulacion()
            self.agregar_registro("Simulación pausada", "info")
        else:
            # Reanudar simulación
            self.simulacion_pausada = False
            self.btn_pausar.config(text="Pausar")
            Config.reanudar_simulacion()
            self.agregar_registro("Simulación reanudada", "info")

    def confirmar_salida(self):
        """Confirma si el usuario desea salir de la aplicación"""
        if messagebox.askyesno("Salir", "¿Está seguro de que desea salir?"):
            self.ventana.destroy()

    def actualizar_nueva_cita(self, cita):
        """Callback que se llama cuando se registra una nueva cita"""
        # Agregar cita a la lista de espera
        self.citas_en_espera[cita.prioridad].append(cita)

        # Actualizar la interfaz (en el hilo de la interfaz gráfica)
        self.ventana.after(0, self.actualizar_interfaz)

        # Agregar al registro
        nivel_prioridad = cita.obtener_nivel_prioridad()
        mensaje = f"Nueva cita registrada: {cita.paciente} - {nivel_prioridad} - {cita.sintomas}"
        tipo = "recepcion"
        if cita.prioridad == 1:  # Emergencia
            tipo = "emergencia"
        self.agregar_registro(mensaje, tipo)

    def actualizar_atencion_cita(self, cita, doctor_id):
        """Callback que se llama cuando un doctor atiende una cita"""
        # Quitar cita de la lista de espera
        if cita in self.citas_en_espera[cita.prioridad]:
            self.citas_en_espera[cita.prioridad].remove(cita)

        # Agregar cita a la lista de atención
        self.citas_en_atencion[doctor_id] = cita

        # Actualizar la interfaz (en el hilo de la interfaz gráfica)
        self.ventana.after(0, self.actualizar_interfaz)

        # Agregar al registro
        nivel_prioridad = cita.obtener_nivel_prioridad()
        mensaje = f"Doctor {doctor_id} atiende a {cita.paciente} - {nivel_prioridad}"
        self.agregar_registro(mensaje, "atencion")

    def actualizar_estadisticas(self, informe):
        """Callback que se llama cuando cambian las estadísticas"""
        # Actualizar la interfaz (en el hilo de la interfaz gráfica)
        self.ventana.after(0, lambda: self.actualizar_panel_estadisticas(informe))

    def actualizar_interfaz(self):
        """Actualiza todos los elementos de la interfaz gráfica"""
        # Actualizar tablas de salas de espera
        for prioridad in range(1, 6):
            tabla = self.tablas_salas[prioridad]
            
            # Limpiar tabla
            for item in tabla.get_children():
                tabla.delete(item)

            # Agregar citas en espera
            for cita in self.citas_en_espera[prioridad]:
                tabla.insert("", "end", values=(cita.id, cita.paciente, cita.sintomas))

        # Actualizar paneles de doctores
        for doctor_id in range(1, Config.NUM_DOCTORES + 1):
            panel = self.paneles_doctores[doctor_id]
            if doctor_id in self.citas_en_atencion:
                cita = self.citas_en_atencion[doctor_id]
                texto = f"Atendiendo a: {cita.paciente} - {cita.obtener_nivel_prioridad()} - {cita.sintomas}"
                panel.config(text=texto, background=cita.obtener_color_prioridad())
            else:
                panel.config(text="Sin paciente", background="#f0f0f0")

    def actualizar_panel_estadisticas(self, informe):
        """Actualiza los elementos del panel de estadísticas"""
        # Actualizar etiquetas de estadísticas generales
        self.lbl_citas_registradas.config(text=f"Citas registradas: {informe['citasRegistradas']}")
        self.lbl_citas_atendidas.config(text=f"Citas atendidas: {informe['citasAtendidas']}")
        self.lbl_tiempo_espera.config(text=f"Tiempo de espera promedio: {informe['tiempoEsperaPromedio']:.2f}s")

        # Actualizar etiquetas de tiempos por prioridad
        tiempos_por_prioridad = informe['tiemposPorPrioridad']
        niveles = ["", "EMERGENCIA", "URGENTE", "PRIORITARIO", "NORMAL", "RUTINA"]
        for prioridad in range(1, 6):
            tiempo = tiempos_por_prioridad[prioridad]
            self.lbl_tiempos_prioridad[prioridad].config(text=f"{niveles[prioridad]}: {tiempo:.2f}s")

        # Actualizar barra de progreso
        total_citas = Config.NUM_RECEPCIONISTAS * Config.NUM_CITAS_POR_RECEPCIONISTA
        citas_atendidas = informe['citasAtendidas']
        progreso = (citas_atendidas * 100) // total_citas
        self.barra_progreso['value'] = progreso

    def agregar_registro(self, mensaje, tipo):
        """Agrega un mensaje al registro de actividad"""
        hora = datetime.now().strftime("%H:%M:%S")
        texto_formateado = f"[{hora}] {mensaje}\n"

        # Aplicar color según el tipo de mensaje
        color = "black"
        if tipo == "info":
            color = "black"
        elif tipo == "recepcion":
            color = "blue"
        elif tipo == "atencion":
            color = "green"
        elif tipo == "emergencia":
            color = "red"

        # Agregar texto con color
        self.txt_registro.config(state=tk.NORMAL)
        self.txt_registro.insert(tk.END, texto_formateado)
        
        # Aplicar etiqueta de color
        end_index = self.txt_registro.index(tk.END)
        start_index = f"{float(end_index) - len(texto_formateado)} linestart"
        end_index = f"{float(end_index) - 1.0} lineend"
        
        # Crear etiqueta si no existe
        tag_name = f"tag_{tipo}"
        if not tag_name in self.txt_registro.tag_names():
            self.txt_registro.tag_configure(tag_name, foreground=color)
        
        self.txt_registro.tag_add(tag_name, start_index, end_index)
        self.txt_registro.config(state=tk.DISABLED)

        # Desplazar al final
        self.txt_registro.see(tk.END)

    def iniciar(self):
        """Inicia la interfaz gráfica"""
        self.ventana.mainloop()
