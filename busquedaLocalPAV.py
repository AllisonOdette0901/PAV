
"""
Búsqueda Local (Resultados)
@author: Odette
Parámetros:
ejemplo: matriz de distancias
tour: solución inicial
n_iter: número de iteraciones
n_base: nombre de la instancia
b_kn: su mejor valor conocido
printR = False: imprimir resultados    
"""

#import random
#import numpy as np
import time
#from Vecino_Mas_Cercano import nearest_neigbors
#from lector_arch_tsp import distancias_ciudades


def total_distancia(tour,g):
        dis = sum(g[tour[i]][tour[i+1]] for i in range(len(tour)-1))
        dis += g[tour[-1]][tour[0]]
        return dis
    
def dos_opciones(ejemplo, tour):
    sol_vecinas = []
    costos = []
    for i in range(0,len(ejemplo)-1):
      for j in range(i+1,len(tour)):
        tour_nuevo = tour.copy()
        tour_nuevo[i], tour_nuevo[j] = tour_nuevo[j], tour_nuevo[i]
        sol_vecinas.append(tour_nuevo)
        costos.append(total_distancia(tour_nuevo, ejemplo))
    return min(costos), sol_vecinas[costos.index(min(costos))]

def busqueda_Local(ejemplo, tour, n_iter, n_base, b_kn,printR = False):
    time_inicio = time.time()
    inicial = tour
    for i in range(n_iter):
      inicial = dos_opciones(ejemplo, inicial)[1]
    if(printR==True):
       return(inicial, total_distancia(inicial, ejemplo) )
    time_final = time.time()
    dis = round(total_distancia(inicial, ejemplo),2)
    print(f"Resultado {n_base}:-------------------------------")
    print("Distancia:", dis)
    print("Mejor ciclo hamiltoniano:",tour)
    #draw(tour)
    print('Tiempo:', round(time_final-time_inicio,5), 'seg')
    print('Tasa de error:', round(((dis-b_kn)/b_kn )*100,2), '%')

