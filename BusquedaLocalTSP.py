
"""
Búsqueda Local (1)
@author: Odette
Parámetros:
tour: solución inicial
D: matriz de distancias
n_base: nombre de la base 
b_kn: mejor valor conocido
"""

#import random
import numpy as np
import time
#from Vecino_Mas_Cercano import nearest_neigbors
#from lector_arch_tsp import distancias_ciudades


def busqueda_Local(tour, D, n_base, b_kn):  
    time_inicio = time.time()
    def two_opt(D, initialH):
    
       change = False
       for i in range(len(initialH)-2):
           for j in range(i+2,len(initialH)-1):
               currentCost = D[initialH[i]][initialH[i+1]] + D[initialH[j]][initialH[j+1]]
               newCost = D[initialH[i]][initialH[j]] + D[initialH[i+1]][initialH[j+1]]
               difference = newCost - currentCost
               if (difference<0):
                   initialH[(i+1):j+1] = initialH[(i+1):j+1][::-1]
                   change = True
           if change:
            break
    
       tour = initialH
       return tour
    
    def total_distancia(tour,D):
        
        weight =  sum(D[tour[i]][tour[i+1]] for i in range(len(tour)-1))
        weight += D[tour[-1]][tour[0]]
        return weight
    
    def two_opt_iter(D, initialH):
        sol = initialH.copy()  
        cambio = 1   
        while cambio != 0:
            inicial = total_distancia(sol,D) 
            sol = two_opt(D,sol).copy() 
            final = total_distancia(sol,D)   
            cambio=np.abs(final-inicial) 
        return sol, total_distancia(sol,D)
    
 
    def busquedaLocal(tour, D):
        
        z = total_distancia(tour, D) 
        while 1:
            newz = two_opt_iter(D,tour)[1]
            if newz < z:
                z = newz
            else: 
                break
        return z
    time_final = time.time()
    dis = round(busquedaLocal(tour, D),2)
    print(f"Resultado {n_base}:-------------------------------")
    print("Distancia:", dis)
    print("Mejor ciclo hamiltoniano:",tour)
    #draw(tour)
    print('Tiempo:', round(time_final-time_inicio,5), 'seg')
    print('Tasa de error:', round(((dis-b_kn)/b_kn )*100,2), '%')


