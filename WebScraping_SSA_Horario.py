
from auxiliares.python.materiasFI import procesar_materias as extraer_materias_de_la_web
from auxiliares.python.procesamientoDataFrame import imprimirMaterias
from auxiliares.python.configuracionGUI import mostrar_resultados_combinados as visualizarGUI
from auxiliares.python.PantallaDeCarga import PantallaDeCarga
misMaterias = extraer_materias_de_la_web() 

hora_entrada = 7
hora_salida = 13
# Esta es la columna que representa el cupo en el DataFrame
columna_cupo = 7
# Lista de claves que deseas conservar
claves_a_conservar = [1867,6867,1858,1765,2901,2914,2927,2928,2929,2930,2931,1866,2932,2934,2944,2945,2946,2947,2948.0674,2949,2950,1916,1018,2951,2952,'0757',2954,2955,2956,2957]
# Agregaremos materias ya cursadas para que no se considere en la entrega de horarios
materias_ya_cursadas = [2928,2958,2933]

# Esta asignación de valor, existe unicamente para solo visualizar una materia y no traer todas las materias deseadas, solo funciona para test 
#claves_a_conservar = [1867]

# retiraremos las materias ya cursadas
claves_a_conservar = [clave for clave in claves_a_conservar if clave not in materias_ya_cursadas]
# La lista de enteros, la pasamos a una lista de strings
claves_a_conservar = list(map(str, claves_a_conservar))

# Filtra el diccionario, conservando solo las claves deseadas
misMaterias_filtrado = {clave: misMaterias[clave] for clave in claves_a_conservar if clave in misMaterias}

# Cremos la pantalla de carga
def procesar_materias_con_carga():
    global misMaterias_filtrado
    pantalla_carga = PantallaDeCarga(max_progreso=len(misMaterias_filtrado))
    def procesar_dataframe():
        resultados_filtrados_dataframe = imprimirMaterias(
            materiasPorMeter=misMaterias_filtrado,
            hora_entrada=hora_entrada,
            hora_salida=hora_salida,
            columna_cupo=columna_cupo,
            pantalla_carga=pantalla_carga
        )
        # Cerrar la pantalla de carga al finalizar
        pantalla_carga.cerrar()
        # Visualizamos la GUI enviandole el DataFrame filtrado por las características deseadas
        visualizarGUI(resultados_filtrados_dataframe)


    # Iniciar la pantalla de carga con la función de procesamiento
    pantalla_carga.iniciar(procesar_dataframe)

# Iniciar la pantalla de carga con la función de procesamiento
procesar_materias_con_carga()


