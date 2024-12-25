import tkinter as tk
from tkinter import ttk

class PantallaDeCarga:
    def __init__(self, titulo="Cargando Datos", mensaje="Por favor espere...", max_progreso=100):
        self.ventana = tk.Tk()
        self.ventana.title(titulo)

        # Dimensiones de la ventana
        ancho_ventana = 800
        alto_ventana = 200

        # Obtener dimensiones de la pantalla
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()

        # Calcular posición para centrar
        x_centro = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y_centro = (alto_pantalla // 2) - (alto_ventana // 2)

        # Establecer posición centrada
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x_centro}+{y_centro}")

        # Etiqueta y barra de progreso
        self.etiqueta = ttk.Label(self.ventana, text=mensaje, anchor="center")
        self.etiqueta.pack(pady=20)

        self.barra_progreso = ttk.Progressbar(self.ventana, orient=tk.HORIZONTAL, mode='determinate', length=300)
        self.barra_progreso.pack(pady=20)

        self.progreso = tk.DoubleVar()
        self.barra_progreso["maximum"] = max_progreso
        self.barra_progreso["variable"] = self.progreso

    def actualizar_progreso(self, valor, mensaje=None):
        """Actualiza el progreso y el mensaje de la pantalla de carga."""
        self.progreso.set(valor)
        if mensaje:
            self.etiqueta.config(text=mensaje)
        self.ventana.update_idletasks()

    def cerrar(self):
        """Cierra la ventana de carga."""
        self.ventana.destroy()

    def iniciar(self, funcion_procesamiento, *args, **kwargs):
        """Inicia el procesamiento con la pantalla de carga visible."""
        self.ventana.after(100, funcion_procesamiento, *args, **kwargs)
        self.ventana.mainloop()
