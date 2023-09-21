""" --- Funciones del archivo ---
nearest_neigbors

result_nn
g: matriz de distanciade la base (np)
n_base: nombre de la base
b_nk: mejor valor conocido
current_node: vértice inicial
"""
import time
import matplotlib.pyplot as plt
plt.style.use('tableau-colorblind10')

def nearest_neigbors(g, current_node):
    path = [current_node]
    numOfCity = len(g)
    for _ in range(numOfCity-1):
        next_node = None
        min_edge = float("inf")
        for v in range(0,numOfCity):
            if v!= current_node and v not in path:
                if g[current_node][v] < min_edge:
                    next_node = v
                    min_edge = g[current_node][v]
                    
        assert  next_node is not None
        path.append(next_node)
        current_node = next_node
    path.append(path[0])
    weight =  sum(g[path[i]][path[i+1]] for i in range(len(path)-1))
    weight += g[path[-1]][path[0]]
    return weight,path

def result_nn(g, n_base, b_kn, current_node = 0):
    start_time = time.time()
    result = nearest_neigbors(g,current_node)
    print(f"Resultado {n_base}:-------------------------------")
    print("Mejor ciclo hamiltoniano:",result[1])
    print("Distancia:", round(result[0],2) )
    time_final = time.time()
    dis = round(result[0],2)
    print('Tasa de error:', round(((dis-b_kn)/b_kn )*100,2), '%')
    print('Tiempo:', round(time_final - start_time, 5) ) 



