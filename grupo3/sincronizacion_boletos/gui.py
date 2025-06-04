import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# Clase encargada de manejar la interfaz gráfica para la simulación
class LamportGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simulación de Reloj de Lamport")

        self.text_area = ScrolledText(self.root, width=80, height=20, state='disabled')
        self.text_area.pack(padx=10, pady=10)

    def log(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.yview(tk.END)
        self.text_area.config(state='disabled')

    def start(self):
        self.root.mainloop()
