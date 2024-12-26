"""
El siguiente archivo contiene la clase PantallaDeInicio, la cual tiene como proposito ser un tipo login, donde
se cuestionará si se meterá nuevamente los parametros de inscripción o se cargará un archivo que igual se creará despues de 
guardar por primera vez los parametros de inscripción.
"""
import tkinter as tk
from auxiliares.python.ArchivoConfig import ArchivoConfig
def pantallaDeInicio():
    """
    Función que crea una ventana de inicio, donde se cuestionará si se meterá nuevamente los parametros de inscripción o se cargará un archivo que igual se creará despues de 
    guardar por primera vez los parametros de inscripción.
    """
    ventana = tk.Tk()
    ventana.title("Pantalla de Inicio")
    ventana.geometry("300x300")
    ventana.resizable(False, False)
    tk.Label(ventana, text="¿Deseas meter nuevamente los parametros de inscripción?").pack(pady=10)
    tk.Button(ventana, text="Si", command=lambda: ventana.destroy()).pack(pady=10)
    archivoConfig = ArchivoConfig('auxiliares\textos\ExigenciasEstudiante.json')
    
    if archivoConfig.existe():
        tk.Button(ventana, text="No", command=lambda: ventana.destroy()).pack(pady=10)
    ventana.mainloop()