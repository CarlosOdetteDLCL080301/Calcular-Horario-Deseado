import tkinter as tk
from tkinter import ttk
import random
def mostrar_resultados_combinados(resultados_por_materia):
    ventana = tk.Tk()
    ventana.title("Resultados Horarios")

    frame = ttk.Frame(ventana)
    frame.pack(fill=tk.BOTH, expand=True)

    # Configurar la ventana para iniciar en pantalla completa
    ventana.attributes("-fullscreen", True)

    # Nombres de los encabezados a mostrar 
    tree = ttk.Treeview(frame, columns=("Clave", "Asignatura", "Grupo", "Profesor", "Horario", "Días", "Cupo"), show="headings")
    tree.heading("Clave", text="Clave")
    tree.heading("Asignatura", text="Asignatura")
    tree.heading("Grupo", text="Grupo")
    tree.heading("Profesor", text="Profesor")
    tree.heading("Horario", text="Horario")
    tree.heading("Días", text="Días")
    tree.heading("Cupo", text="Cupo")

    # Anchos de los encabezados y ubicación de los mismos  
    tree.column("Clave", width=10, anchor="center")
    tree.column("Asignatura", width=230, anchor="w")  
    tree.column("Grupo", width=10, anchor="center")
    tree.column("Profesor", width=200, anchor="w")
    tree.column("Horario", width=10, anchor="center")
    tree.column("Días", width=10, anchor="center")
    tree.column("Cupo", width=10, anchor="center")

    # Hace responsiva la ventana
    scrollbar_y = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar_y.set)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

     # Generar colores aleatorios para cada "Asignatura"
    def generar_color():
        return f'#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}'

    # Diccionario para asociar nombres con colores
    colores_por_nombre = {}

     # Aplicar colores y añadir datos
    for claveMateria, (nombreMateria, resultados) in resultados_por_materia.items():
        if not resultados.empty:
            # Asignar un color si aún no tiene uno
            if nombreMateria not in colores_por_nombre:
                colores_por_nombre[nombreMateria] = generar_color()
                tree.tag_configure(nombreMateria, background=colores_por_nombre[nombreMateria])

            for _, row in resultados.iterrows():
                tree.insert("", "end", values=(claveMateria, nombreMateria, *row.tolist()), tags=(nombreMateria,))

    # Función para aplicar el orden seleccionado
    def aplicar_orden():
        criterio = combobox.get()  # Obtener el criterio seleccionado
        if criterio in columnas_sencillas:
            ordenar_por_columna(tree, criterio, False)  # Ordenamiento sencillo
        elif criterio == "Asignatura y Horario":
            ordenar_por_asignatura_y_horario(tree)  # Ordenamiento complejo

    # Lista de opciones para el ordenamiento
    columnas_sencillas = ["Clave", "Asignatura", "Profesor", "Horario", "Días", "Cupo"]
    opciones = columnas_sencillas + ["Asignatura y Horario"]

    # Crear combobox para seleccionar el ordenamiento
    combobox = ttk.Combobox(ventana, values=opciones, state="readonly")
    combobox.set("Seleccione el ordenamiento")
    combobox.pack(pady=10)

    # Botón para aplicar el orden
    boton_ordenar = tk.Button(ventana, text="Ordenar", command=aplicar_orden)
    boton_ordenar.pack(pady=5)

    # Botón para cerrar la ventana
    tk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)
    ventana.mainloop()


def ordenar_por_columna(tree, columna, reverse):
    """
    Ordena los elementos en un Treeview según una columna específica.
    """
    datos = [(tree.set(k, columna), k) for k in tree.get_children("")]
    datos.sort(reverse=reverse)

    # Reorganizar los datos ordenados en el Treeview
    for index, (val, k) in enumerate(datos):
        tree.move(k, "", index)


def ordenar_por_asignatura_y_horario(tree):
    """
    Ordena los datos por asignatura (Asignatura) y luego por Horario.
    """
    datos = [(tree.set(k, "Asignatura"), tree.set(k, "Horario"), k) for k in tree.get_children("")]
    datos.sort(key=lambda x: (x[0], x[1]))  # Primero por Asignatura, luego por Horario

    # Reorganizar los datos ordenados en el Treeview
    for index, (Asignatura, horario, k) in enumerate(datos):
        tree.move(k, "", index)
