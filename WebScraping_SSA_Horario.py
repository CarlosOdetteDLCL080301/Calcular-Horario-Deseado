import requests
from charset_normalizer import detect
from io import StringIO
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import random
from auxiliares.python.procesamiento import procesar_materias as extraer_materias_de_la_web
misMaterias = extraer_materias_de_la_web() 
longitudParaCentrar = 100
hora_entrada = 7
hora_salida = 13
# Esta es la columna que representa el cupo en el DataFrame
columna_cupo = 7
# Lista de claves que deseas conservar
claves_a_conservar = [1867,6867,1858,1765,2901,2914,2927,2928,2929,2930,2931,1866,2932,2934,2944,2945,2946,2947,2948.0674,2949,2950,1916,1018,2951,2952,'0757',2954,2955,2956,2957]
# Agregaremos materias ya cursadas para que no se considere en la entrega de horarios
materias_ya_cursadas = [2928,2958,2933]
# def formatoDeImpresion(resultados,nombreMateria,claveMateria):
#     print("#".center(longitudParaCentrar, "#"))
#     print(f"Materia: {nombreMateria} ({claveMateria})".center(longitudParaCentrar, " "))
#     print("#".center(longitudParaCentrar, "#"))
#     if resultados.empty:
#         print("No hay horarios disponibles".center(longitudParaCentrar, " "))
#     else:
#         print(resultados)
#     print("".center(longitudParaCentrar, "_"))
#     print("\n\n\n")

def formatoDeImpresion(resultados, nombreMateria, claveMateria):
    # Códigos ANSI para colores
    RESET = '\033[0m'  # Restablece el color a por defecto
    ROJO = '\033[31m'  # Rojo
    VERDE = '\033[32m'  # Verde
    AZUL = '\033[34m'  # Azul
    AMARILLO = '\033[33m'  # Amarillo

    # Definir longitud para centrar
    longitudParaCentrar = 100  # Puedes ajustar esto según sea necesario

    # Título de la materia
    print(AMARILLO+"".center(longitudParaCentrar, "#"))
    print(f"{VERDE}Materia: {nombreMateria} ({claveMateria})".center(longitudParaCentrar, " "))
    print(AMARILLO+"".center(longitudParaCentrar, "#"))

    # Mensaje si no hay horarios disponibles
    if resultados.empty:
        print(f"{ROJO}No hay horarios disponibles".center(longitudParaCentrar, " "))
    else:
        # Asignaremos un valor al encabezado de cada columna para que se vea más claro
        resultados.columns = ['Grupo', 'Profesor', 'Horario', 'Días', 'Cupo']
        print(f"{AZUL}{resultados}{RESET}")  # Coloca los resultados en azul
    
    # Línea final con un guion bajo
    print(AMARILLO+"".center(longitudParaCentrar, "_"))
    
    # Espacios adicionales
    print("\n\n\n")


# Filtrar los horarios antes de las 13:00
def es_hora_valida_salida(horario):
    # Extraer la hora de fin de la clase (antes del 'a'), ya que queremos que el horario
    # se ajuste a nuestra disponibilidad de tiempo
    hora_inicio = horario.split(' a ')[1]
    # Convertir la hora de inicio a formato de hora
    hora = datetime.strptime(hora_inicio, '%H:%M')
    return hora.hour <= hora_salida   # Filtra si la hora es antes de las 13:00

# Filtrar los horarios antes de las 13:00
def es_hora_valida_entrada(horario):
    # Extraer la hora de fin de la clase (antes del 'a'), ya que queremos que el horario
    # se ajuste a nuestra disponibilidad de tiempo
    hora_inicio = horario.split(' a ')[0]
    # Convertir la hora de inicio a formato de hora
    hora = datetime.strptime(hora_inicio, '%H:%M')

    return hora.hour >= hora_entrada # Filtra si la hora es antes de las 13:00

def filtrarTabla(df):
    # Seleccionar las columnas 1, 2, 4, 5 y columna_cupo
    columnas_seleccionadas = [1, 2, 4, 5, columna_cupo]
    columnas_disponibles = [col for col in columnas_seleccionadas if col < len(df.columns)]
    df_excluyendoColumnas = df.iloc[:, columnas_disponibles]
    
    # Eliminar la cadena "(PRESENCIAL)" de la columna de profesores (columna en posición 1)
    df_excluyendoColumnas.iloc[:, 1] = df_excluyendoColumnas.iloc[:, 1].str.replace(r" \(PRESENCIAL\)", "", regex=True)

    # Excluir los últimos dos renglones
    df_excluyendoRenglones = df_excluyendoColumnas.iloc[:-2, :]
    
    # Asegurar que la columna de interés sea numérica antes de la comparación
    df_excluyendoRenglones.iloc[:, -1] = pd.to_numeric(df_excluyendoRenglones.iloc[:, -1], errors='coerce')
    
    # Filtrar filas donde la columna 8 tenga valores mayores a 0
    df_filtrado = df_excluyendoRenglones[df_excluyendoRenglones.iloc[:, -1] > 0]

    # Aplicar el filtro a la columna de horarios para que sea antes de un horario específico
    df_filtrado = df_filtrado[df_filtrado.iloc[:, 2].apply(es_hora_valida_salida)]  # Asumiendo que la columna de horario está en la posición 2

    # Aplicar el filtro a la columna de horarios para que sea despues de un horario específico
    df_filtrado = df_filtrado[df_filtrado.iloc[:, 2].apply(es_hora_valida_entrada)]  # Asumiendo que la columna de horario está en la posición 2

    # Eliminar la cadena "(PRESENCIAL)" en la columna de profesores
    

    return df_filtrado

def imprimirMaterias(materiasPorMeter):
    resultados_por_materia = {}

    for materia in materiasPorMeter:
        # Obtener el valor correspondiente a la clave 'materia'
        nombreMateria = materiasPorMeter[materia]
        
        # Leer el contenido de la URL
        url = f"https://www.ssa.ingenieria.unam.mx/cj/tmp/programacion_horarios/{materia}.html"
        try:
            response = requests.get(url)
            detected_encoding = detect(response.content)['encoding']  # Detectar la codificación
            response.encoding = detected_encoding  # Aplicar la codificación detectada
            
            # Envolver el texto en un objeto StringIO antes de pasarlo a read_html
            html_content = StringIO(response.text)
            dfs = pd.read_html(html_content)  # Leer el HTML como texto literal desde StringIO
            df = dfs[0]  # Seleccionar la primera tabla
        except Exception as e:
            print(f"Error al leer la URL para la materia {materia}: {e}")
            continue
        
        # Filtrar el DataFrame para entregar solo las columnas deseadas
        #df_excluyendoRenglones = filtrarTabla(df)
        # Imprimir el Asignatura de la materia y el DataFrame seleccionado
        
        #formatoDeImpresion(df_excluyendoRenglones, nombreMateria, materia)
        df_filtrado = filtrarTabla(df)
        resultados_por_materia[materia] = (nombreMateria, df_filtrado)

    mostrar_resultados_combinados(resultados_por_materia)

def mostrar_resultados_combinados(resultados_por_materia):
    import tkinter as tk
    from tkinter import ttk

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

#claves_a_conservar = [1867]

# retiraremos las materias ya cursadas
claves_a_conservar = [clave for clave in claves_a_conservar if clave not in materias_ya_cursadas]
# La lista de enteros, la pasamos a una lista de strings
claves_a_conservar = list(map(str, claves_a_conservar))

# Filtra el diccionario
misMaterias_filtrado = {clave: misMaterias[clave] for clave in claves_a_conservar if clave in misMaterias}

imprimirMaterias(misMaterias_filtrado)
#Establecemos los horarios disponibles durante la semana
