import re
# Intentaremos descargar el contenido directamente desde la URL proporcionada para procesarlo.
import requests

def extraer_materias_de_la_web():
    # URL de la página que contiene los datos
    url = "https://www.ssa.ingenieria.unam.mx/cj/tmp/programacion_horarios/listaAsignatura.js"

    # Descargar el contenido
    response = requests.get(url)
    js_data = response.text

    # Revisar una parte del contenido descargado
    #print(js_data[:200])
    #print(" FIN ".center(80, "="))
    return js_data

def procesar_materias():
    # Cadena JavaScript extraída del archivo o página
    js_data = extraer_materias_de_la_web()
    # Expresión regular para encontrar las claves y valores
    pattern = r"asignatura\['(\d+)'\] = '(.+?)';"
    matches = re.findall(pattern, js_data)

    # Convertir los resultados a un diccionario de Python
    misMaterias = {clave: valor for clave, valor in matches}

    # Imprimir el diccionario final
    #print(misMaterias)
    #print("FIN".center(80, "="))
    return misMaterias

