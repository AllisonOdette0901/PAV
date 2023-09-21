import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import random
import math
import time
plt.style.use('tableau-colorblind10')

"""
Recocido Simulado
g : distancias (matriz o lista de distancias)
T0: temperatura inicial
alpha: tasa de decremento de la temperatura
nrep: número de repeticiones
Tf: temperatura final
n_base: nombre de la base para el plot
b_kn: mejor resultado conocido (para calcular tasa de error)
prinT: imprimir o no la distancia del tour por cada temperatura (T/F)
semilla: entero que fija semilla de resultados
"""

def RecocidoSimulado(g, T0, alpha, NREP, Tf, n_base, b_kn, prinT, semilla = 7):
    random.seed(semilla)
    T = T0
    def distancia_total(camino):
        dis = sum(g[camino[i]][camino[i+1]] for i in range(len(camino)-1))
        dis += g[camino[-1]][camino[0]]
        return dis
     
    numCiudades = len(g)          
    camino = [i for i in range(numCiudades)]
    random.shuffle(camino)    
    camino.append(camino[0])  
    dis = distancia_total(camino)    
    def vecino(camino, aleat_uno, aleat_dos):
        delta = (g[camino[aleat_uno-1]][camino[aleat_dos]] - g[camino[aleat_uno-1]][camino[aleat_uno]] \
                + g[camino[aleat_dos+1]][camino[aleat_uno]] - g[camino[aleat_dos+1]][camino[aleat_dos]] )
        return delta
    Temp = [] 
    Min_distancias = [] 
    time_inicio = time.time()
    cont = 0
    while(T > Tf):
        for i in range(NREP):
            aleat_uno = random.randint(1, len(camino)-3)
            aleat_dos = random.randint(aleat_uno+1, len(camino)-2)
            dE = vecino(camino, aleat_uno, aleat_dos)
            if dE <= 0 or random.random() < math.exp(-dE / T):
                camino[aleat_uno:aleat_dos+1] = camino[aleat_dos:aleat_uno-1:-1]
                dis = dis + dE 
        Temp = np.append(Temp,T)
        Min_distancias.append(dis)
        T = T*alpha
        cont += 1
        if(prinT == True):
            print('Iteración',cont,':', round(dis,2))         
        time_final = time.time()
    print("-----------------------")
    print('Mejor distancia:',round(dis,2))
    print('Mejor tour:', camino)
    print('Tiempo:', round(time_final-time_inicio,5), 'seg')
    print('Tasa de error:', round(((dis-b_kn)/b_kn )*100,2), '%')

    plt.scatter(np.arange(0,len(Min_distancias)),Min_distancias, c = np.arange(0,len(Min_distancias)), cmap="plasma")
    plt.plot(np.arange(0,len(Min_distancias)),np.array(Min_distancias), alpha = 0.5, color = mcolors.CSS4_COLORS['navy'])
    plt.axhline(y=b_kn, color = mcolors.CSS4_COLORS['dodgerblue'], linestyle='-')
    plt.title('Recocido Simulado'+' '+ str(n_base))
    plt.xlabel('Iteraciones')
    plt.ylabel('Distancia')
    plt.legend([ "Distancias de RS","Mejor distancia {}".format(b_kn)])
    plt.show()
    
