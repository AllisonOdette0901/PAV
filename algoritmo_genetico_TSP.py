'''
Experimentos usando algoritmos genéticos
Parámetros de la función:
AlgoritmoGenetico(POPSIZE, MAXGENS, PXOVER, PMUTATION,filename, n_base)
POPSIZE: tamaño de la población
MAXGENS: número de iteraciones
probaCruce: probabilidad de cruce 
PMUTATION: probabilidad de mutación
distance: objeto que tiene las distancias de la lista de coordenadas
filename: nombre del archivo .tsp
n_base: nombre de la base para el plot
seed: semilla establecida
prinT: TRUE si se requiere imprimir los resultados, FALSE si no
'''

from sys import float_info
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import time
from tqdm import tqdm
import random
#from lector_arch_tsp import distancias_ciudades
plt.style.use('tableau-colorblind10')


def AlgoritmoGenetico(POPSIZE, MAXGENS, probaCruce, PMUTATION,distance,b_kn, n_base,seed=2, prinT = False):    
    random.seed(seed)
    numCiudades = len(distance)   
    def poblacionInicial(distance, numCiudades):
        poblacion = []
        individuo = [i for i in range(numCiudades)]
        for _ in range(int(POPSIZE * 2 / 10)):
            random.shuffle(individuo)
            poblacion.append(individuo[:])
        for _ in range(int(POPSIZE - len(poblacion))):
            inicio = random.randint(0, numCiudades-1)
            gIndividuo = []
            gIndividuo.append(inicio)
            j = 1
            while j < numCiudades:
                mixDis = float_info.max #infinito
                i, bestId = 0, 0
                while i < numCiudades:
                    if (i not in gIndividuo) and i != gIndividuo[-1] and distance[gIndividuo[-1]][i] < mixDis:
                        bestId = i
                        mixDis = distance[gIndividuo[-1]][i]
                    i += 1
                j = j + 1
                gIndividuo.append(bestId)
            poblacion.append(gIndividuo[:]) 
            
        random.shuffle(poblacion)
        return poblacion
    
    def total_distancia(individuo):
        weight =  sum(distance[individuo[i]][individuo[i+1]] for i in range(len(individuo)-1))
        weight += distance[individuo[-1]][individuo[0]]
        return weight

    def seleccion(poblacion, numCiudades):
        poblacionN = []
        best = float_info.max
        bestId = 0
        aptitud = []
        sumApt = 0.0
    
        for i in range(POPSIZE):
            apt = total_distancia(poblacion[i])
            aptitud.append(1 / apt)
            sumApt += 1 / apt
            if (best > apt) :
                best = apt
                bestId = i
    
        poblacionN.append(poblacion[bestId])
    
        probaAcum = []
        for i in range(POPSIZE):
            if i == 0:
                probaAcum.append(aptitud[i] / sumApt)
            else:
                probaAcum.append(aptitud[i] / sumApt + probaAcum[i-1])       
        
        for i in range(POPSIZE-1):
            pro = random.random() 
            for j in range(POPSIZE):
                if probaAcum[j] >= pro:
                    poblacionN.append(poblacion[j])
                    break
        return poblacionN
    
    def OperadorCruce(poblacion, numCiudades):
        poblacionN = []
        for i in range(POPSIZE):
            if random.random() <= probaCruce:
                first = random.randint(0, POPSIZE - 1)
                second = random.randint(0, POPSIZE - 1)
                while first == second:
                    second = random.randint(0, POPSIZE - 1)
                start = random.randint(0, numCiudades - 2)
                end = random.randint(start + 1, numCiudades - 1)
                hijo_i = []
                hijo_j = []
                k = 0
                for j in range(numCiudades):
                    if j >= start and j < end:
                        hijo_i.append(poblacion[first][j])
                        j = end
                    else:
                        while k < numCiudades:
                            if poblacion[second][k] not in poblacion[first][start:end]:
                                hijo_i.append(poblacion[second][k])
                                k += 1
                                break
                            k += 1
                k = 0      
                for j in range(numCiudades):
                    if poblacion[second][j] in poblacion[first][start:end]:
                        hijo_j.append(poblacion[second][j])
                    else:
                        if k == start:
                            k = end
                        hijo_j.append(poblacion[first][k])
                        k += 1
                poblacionN.append(hijo_i[:])
                poblacionN.append(hijo_j[:])
        
        poblacionN.sort(key = lambda x: total_distancia(x))
        for i in range(len(poblacionN)):
            for j in range(POPSIZE):
                if total_distancia(poblacionN[i]) < total_distancia(poblacion[j]):
                    poblacion[j] = poblacionN[i]
                    break
    
        return poblacion
    
    def OperadorMutacion(poblacion, numCiudades):
        for i in range(len(poblacion)):
            if random.random() <= PMUTATION:
                first = random.randint(1,numCiudades-2)
                second = random.randint(first+1, numCiudades-1)
                poblacion[i][first:second] = poblacion[i][second-1:first-1:-1]
            if random.random() <= PMUTATION:
                first = random.randint(0,numCiudades-1)
                second = random.randint(0, numCiudades-1)
                while first == second:
                    second = random.randint(0, numCiudades-1)
                poblacion[i][first], poblacion[i][second] = poblacion[i][second], poblacion[i][first]
        return poblacion
    
    population = poblacionInicial(distance, numCiudades)
    result = []
    tours = []
    time_inicio = time.time()
    curGen = 0
    pbar = tqdm(total=MAXGENS) 
    while curGen < MAXGENS:
        random.shuffle(population)
        population = seleccion(population, numCiudades)
        population = OperadorCruce(population, numCiudades)
        population = OperadorMutacion(population, numCiudades)   
        population.sort(key = lambda x: total_distancia(x))
        result.append(total_distancia(population[0]))
        tours.append(population[0]) 
        if(prinT == True):
            print("Generación ", curGen, ":", total_distancia(population[0]))        
        else: 
            pbar.update(n=1)
        curGen += 1
        time_final = time.time() 
    
    print(f"Resultado {n_base}:---------------")
    print('Distancia del mejor tour:', round(min(result),2))
    print('Tiempo', round(time_final-time_inicio,2))
    print('Tasa de error:', round(((min(result)-b_kn)/b_kn )*100,2), '%')
    print('menor tour', tours[result.index(min(result))])
    plt.scatter(np.arange(0,len(result)),result, c = np.arange(0,len(result)), cmap="plasma")
    plt.plot(np.arange(0,len(result)),np.array(result), alpha = 0.5, color = mcolors.CSS4_COLORS['navy'])
    plt.axhline(y=b_kn, color = mcolors.CSS4_COLORS['dodgerblue'], linestyle='-')
    plt.title('Algoritmo genético'+' '+ str(n_base))
    plt.xlabel('Iteraciones')
    plt.ylabel('Distancia')
    plt.legend([ "Distancias de AG","Mejor distancia {}".format(b_kn)])
    plt.show()
    
