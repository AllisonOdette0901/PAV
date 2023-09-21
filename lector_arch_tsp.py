
""" --- Funciones del archivo ---
read_tsp: Función que convierte archivo tsp en listas de coordenadas
distancias_ciudades: devuelve la lista de distancias entre las n ciudades
"""


import re

class ciudad:
    def __init__(self, numCiudad, x, y):
        self.numCiudad = numCiudad
        self.x = x
        self.y = y

def read_tsp(filename):
    """
    Lectura de datos .tsp convirtiendolo a pandas DataFrame
    """
    with open(filename) as file:
        ciudades = []
        eureka = False
        for linea in file.readlines()[0:-1]:
            if linea.startswith('EOF'):
                break
            if linea.startswith('NODE_COORD_SECTION'): 
                eureka = True
            elif eureka == True:
                info = re.split('[ ]+', linea.strip())
                ciudades.append(ciudad(info[0], float(info[1]), float(info[2])))
    return ciudades

def distancias_ciudades(filename):
    ciudades = read_tsp(filename)
    distancias = [] 
    for i in range(len(ciudades)):
        node = []
        for j in range(len(ciudades)):
            node.append(((ciudades[i].x - ciudades[j].x)**2 + (ciudades[i].y - ciudades[j].y)**2)**0.5 )
        distancias.append(node)
    return distancias