import json
import os

# Ruta al archivo JSON
DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "./../../auxiliares/textos/horario_estudios.json"))

def cargar_datos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return data
    else:
        print(f"El archivo {DATA_FILE} no existe.")
        return None

def recuperarJSON():
    datos = cargar_datos()

    if datos:
        # Reasignar valores a variables
        materias_seleccionadas = datos.get("materias_seleccionadas", [])
        hora_entrada = datos.get("hora_entrada", "")
        hora_salida = datos.get("hora_salida", "")
        dias_sise_estudio = datos.get("dias_sise_estudio", [])

        # Imprimir valores cargados
        print("Datos cargados del archivo JSON:")
        print(f"Materias seleccionadas: {materias_seleccionadas}")
        print(f"Horario de entrada: {hora_entrada}")
        print(f"Horario de salida: {hora_salida}")
        print(f"Días que sí se quiere asistir: {dias_sise_estudio}")
        return datos
    else:
        print("No se pudieron cargar los datos.")
        return None

if __name__ == "__main__":
    recuperarJSON()
