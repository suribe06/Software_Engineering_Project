import random
"""
Este archivo es para agregar las funciones adicionales que se probaran en el proyecto de Pruebas de Software
"""

def calcular_riesgo(edad, estrato, salidas_recientes):
    factor = 0
    #Tomando en cuenta la edad
    if edad < 10:
        factor += 6
    elif edad > 60:
        factor += 12
    else:
        factor += 3
    #tomando en cuenta el estrato
    if estrato <= 2:
        factor += 10
    elif estrato > 2 and estrato <= 4:
        factor += 5
    elif estrato > 4 and estrato <= 6:
        factor += 3
    #tomando en cuenta la cantidad de salidas recientes
    if salidas_recientes <= 4:
        factor += 3
    elif salidas_recientes > 4 and salidas_recientes <= 8:
        factor += 6
    elif salidas_recientes > 8 and salidas_recientes <= 12:
        factor += 10
    else:
        factor += 15
    #factor de infeccion aleatorio
    factor += random.randint(1, 5)

    riesgo = None
    if factor <= 8:
        riesgo = 'Bajo'
    elif factor > 8 and factor <= 16:
        riesgo = 'Normal'
    elif factor > 16 and factor <= 24:
        riesgo = 'Alto'
    elif factor > 24:
        riesgo = 'Muy Alto'

    return riesgo
