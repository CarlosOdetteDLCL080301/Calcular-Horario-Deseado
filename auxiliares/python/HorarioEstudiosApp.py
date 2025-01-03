"""
El siguiente archivo contiene la clase PantallaDeInicio, la cual tiene como proposito ser un tipo login, donde
se cuestionará si se meterá nuevamente los parametros de inscripción o se cargará un archivo que igual se creará despues de 
guardar por primera vez los parametros de inscripción.
"""
import os
import json
import tkinter as tk
from tkinter import messagebox
#from materiasFI import procesar_materias as extraer_materias_de_la_web
from auxiliares.python.materiasFI import procesar_materias as extraer_materias_de_la_web
# Diccionario de materias

materias = extraer_materias_de_la_web()

# Ruta al archivo JSON
DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../textos/horario_estudios.json"))

# Verificar que el directorio exista
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

class HorarioEstudiosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Horario de Estudios")

        # Variables
        self.clave_materia = tk.StringVar()
        self.hora_entrada = tk.StringVar()
        self.hora_salida = tk.StringVar()
        self.materias_seleccionadas = []
        self.dias_sise_estudio = []
        self.error_msg = tk.StringVar()

        # Sección Agregar Materia
        self.create_add_materia_section()

        # Sección Horario
        self.create_horario_section()

        # Sección Días que sí se quiere asistir
        self.create_dias_sise_estudio_section()

        # Botón de enviar
        submit_button = tk.Button(
            root, text="Enviar", command=self.handle_submit, bg="#4CAF50", fg="white", font=("Arial", 12, "bold")
        )
        submit_button.pack(pady=10)

    def create_add_materia_section(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10, fill="x")

        label = tk.Label(frame, text="Agregar Materia:", font=("Arial", 12))
        label.pack(anchor="w")

        input_frame = tk.Frame(frame)
        input_frame.pack(fill="x", pady=5)

        entry = tk.Entry(input_frame, textvariable=self.clave_materia, font=("Arial", 12))
        entry.pack(side="left", fill="x", expand=True)

        add_button = tk.Button(input_frame, text="Agregar", command=self.add_materia, bg="#007BFF", fg="white")
        add_button.pack(side="left", padx=5)

        self.materias_list = tk.Listbox(frame, font=("Arial", 12), height=5)
        self.materias_list.pack(fill="x", pady=5)

        # Habilitar la eliminación al hacer clic en una materia
        self.materias_list.bind("<Double-Button-1>", self.delete_selected_materia)

    def create_horario_section(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10, fill="x")

        tk.Label(frame, text="Horario de Entrada:", font=("Arial", 12)).pack(anchor="w")
        tk.Entry(frame, textvariable=self.hora_entrada, font=("Arial", 12)).pack(fill="x", pady=5)

        tk.Label(frame, text="Horario de Salida:", font=("Arial", 12)).pack(anchor="w")
        tk.Entry(frame, textvariable=self.hora_salida, font=("Arial", 12)).pack(fill="x", pady=5)

    def create_dias_sise_estudio_section(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10, fill="x")

        tk.Label(frame, text="Días que sí se quiere asistir:", font=("Arial", 12)).pack(anchor="w")

        self.dias_vars = {}
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        for dia in dias:
            var = tk.BooleanVar()
            self.dias_vars[dia] = var
            tk.Checkbutton(frame, text=dia, variable=var, font=("Arial", 12)).pack(anchor="w")

    def add_materia(self):
        clave = self.clave_materia.get()
        if clave in materias:
            if clave not in self.materias_seleccionadas:
                self.materias_seleccionadas.append(clave)
                self.update_materias_list()
                self.clave_materia.set("")
                self.error_msg.set("")
            else:
                messagebox.showerror("Error", "Esta materia ya está agregada.")
        else:
            messagebox.showerror("Error", "Clave de materia no válida.")

    def update_materias_list(self):
        self.materias_list.delete(0, tk.END)
        for clave in self.materias_seleccionadas:
            self.materias_list.insert(tk.END, f"{clave} - {materias[clave]}")

    def delete_selected_materia(self, event):
        # Obtener el índice del elemento seleccionado
        selection = self.materias_list.curselection()
        if selection:
            index = selection[0]
            # Eliminar la materia de la lista
            del self.materias_seleccionadas[index]
            self.update_materias_list()

    def guardar_datos(self):
        data = {
            "materias_seleccionadas": self.materias_seleccionadas,
            "hora_entrada": self.hora_entrada.get(),
            "hora_salida": self.hora_salida.get(),
            "dias_sise_estudio": [
                dia for dia, var in self.dias_vars.items() if var.get()
            ],
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)
        messagebox.showinfo("Guardado", "Datos guardados correctamente.")

    def cargar_datos(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
            self.materias_seleccionadas = data.get("materias_seleccionadas", [])
            self.hora_entrada.set(data.get("hora_entrada", ""))
            self.hora_salida.set(data.get("hora_salida", ""))
            for dia in data.get("dias_sise_estudio", []):
                if dia in self.dias_vars:
                    self.dias_vars[dia].set(True)
            self.update_materias_list()

    def handle_submit(self):
        # Validar horario
        if self.hora_entrada.get() >= self.hora_salida.get():
            messagebox.showerror("Error", "La hora de salida debe ser posterior a la hora de entrada.")
            return

        if not self.materias_seleccionadas:
            messagebox.showerror("Error", "Debe agregar al menos una materia.")
            return

        self.dias_sise_estudio = [dia for dia, var in self.dias_vars.items() if var.get()]
        if not self.dias_sise_estudio:
            messagebox.showerror("Error", "Debe seleccionar al menos un día para asistir.")
            return

        # Mostrar datos en consola (simulando el envío)
        #print("Materias seleccionadas:", self.materias_seleccionadas)
        #print("Horario de entrada:", self.hora_entrada.get())
        #print("Horario de salida:", self.hora_salida.get())
        #print("Días que sí se quiere asistir:", self.dias_sise_estudio)
        self.guardar_datos()
        messagebox.showinfo("Éxito", "Datos Capturados y Almacenados Correctamente")

# Crear la ventana principal
root = tk.Tk()
app = HorarioEstudiosApp(root)
root.mainloop()
