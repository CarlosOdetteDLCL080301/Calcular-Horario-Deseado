from datetime import datetime
import pandas as pd
from io import StringIO
import requests
from charset_normalizer import detect

longitudParaCentrar = 100

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
def es_hora_valida_salida(horario, hora_salida):
    # Extraer la hora de fin de la clase (antes del 'a'), ya que queremos que el horario
    # se ajuste a nuestra disponibilidad de tiempo
    hora_inicio = horario.split(' a ')[1]
    # Convertir la hora de inicio a formato de hora
    hora = datetime.strptime(hora_inicio, '%H:%M')
    return hora.hour <= hora_salida   # Filtra si la hora es antes de las 13:00

# Filtrar los horarios antes de las 13:00
def es_hora_valida_entrada(horario, hora_entrada):
    # Extraer la hora de fin de la clase (antes del 'a'), ya que queremos que el horario
    # se ajuste a nuestra disponibilidad de tiempo
    hora_inicio = horario.split(' a ')[0]
    # Convertir la hora de inicio a formato de hora
    hora = datetime.strptime(hora_inicio, '%H:%M')

    return hora.hour >= hora_entrada # Filtra si la hora es antes de las 13:00

def filtrarTabla(df,columna_cupo,hora_entrada,hora_salida):
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
    df_filtrado = df_filtrado[df_filtrado.iloc[:, 2].apply(lambda x: es_hora_valida_salida(x,hora_salida))]  # Asumiendo que la columna de horario está en la posición 2

    # Aplicar el filtro a la columna de horarios para que sea despues de un horario específico
    df_filtrado = df_filtrado[df_filtrado.iloc[:, 2].apply(lambda x: es_hora_valida_entrada(x,hora_entrada))]  # Asumiendo que la columna de horario está en la posición 2

    # Eliminar la cadena "(PRESENCIAL)" en la columna de profesores
    

    return df_filtrado

def imprimirMaterias(materiasPorMeter,hora_entrada,hora_salida,columna_cupo, pantalla_carga=None):
    resultados_por_materia = {}
    # Registraremos cuantas materias se buscaran en la red
    materias_por_leer = len(materiasPorMeter)
    for idx, materia in enumerate(materiasPorMeter):
        # Actualizamos la pantalla de carga si esta disponible
        if pantalla_carga:
            mensaje = f"Cargando {materiasPorMeter[materia]} ({idx + 1}/{materias_por_leer})"
            pantalla_carga.actualizar_progreso(idx + 1, mensaje)


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
        df_filtrado = filtrarTabla(df,columna_cupo,hora_entrada,hora_salida)
        resultados_por_materia[materia] = (nombreMateria, df_filtrado)
    return resultados_por_materia
    #mostrar_resultados_combinados(resultados_por_materia)
"""
hora_entrada = 7
hora_salida = 13
# Esta es la columna que representa el cupo en el DataFrame
columna_cupo = 7
"""