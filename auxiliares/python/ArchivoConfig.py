import os
import json

class ArchivoConfig:
    def __init__(self, archivo):
        """
        Inicializa la clase con el nombre del archivo.
        """
        self.archivo = archivo

    def guardar(self, datos):
        """
        Guarda los datos en el archivo en formato JSON.
        :param datos: Diccionario con las variables a almacenar.
        """
        try:
            with open(self.archivo, 'w') as f:
                json.dump(datos, f, indent=4)
            print(f"Datos guardados exitosamente en {self.archivo}.")
        except Exception as e:
            print(f"Error al guardar los datos: {e}")

    def cargar(self):
        """
        Carga los datos desde el archivo y los devuelve como un diccionario.
        :return: Diccionario con los datos cargados o None si no se pudo cargar.
        """
        if not self.existe():
            print(f"El archivo {self.archivo} no existe.")
            return None

        try:
            with open(self.archivo, 'r') as f:
                datos = json.load(f)
            print(f"Datos cargados exitosamente desde {self.archivo}.")
            return datos
        except Exception as e:
            print(f"Error al cargar los datos: {e}")
            return None

    def existe(self):
        """
        Comprueba si el archivo existe.
        :return: True si el archivo existe, False en caso contrario.
        """
        print("La respuesta es: ",os.path.isfile(self.archivo))
        return os.path.isfile(self.archivo)
    
    def crear_si_no_existe(self):
        """
        Crea el archivo si no existe, inicializándolo con un objeto JSON vacío.
        """
        try:
            with open(self.archivo, 'w') as f:
                json.dump({}, f)  # Inicializar con un objeto vacío
            print(f"Archivo {self.archivo} creado exitosamente.")
        except Exception as e:
            print(f"Error al crear el archivo: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    # Crear instancia de ArchivoConfig
    config = ArchivoConfig("config.json")

    # Definir variables a almacenar
    datos_a_guardar = {
        "hora_entrada": 7,
        "hora_salida": 13,
        "claves_a_conservar": [
            1867, 6867, 1858, 1765, 2901, 2914, 2927, 2928, 2929, 2930, 2931, 
            1866, 2932, 2934, 2944, 2945, 2946, 2947, 2948.0674, 2949, 2950, 
            1916, 1018, 2951, 2952, '0757', 2954, 2955, 2956, 2957
        ]
    }

    # Guardar datos en el archivo
    config.guardar(datos_a_guardar)

    # Verificar si el archivo existe
    if config.existe():
        print("El archivo existe.")
    else:
        print("El archivo no existe")
        config.crear_si_no_existe()
    # Cargar datos desde el archivo
    datos_cargados = config.cargar()
    if datos_cargados:
        print("Datos cargados:", datos_cargados)
