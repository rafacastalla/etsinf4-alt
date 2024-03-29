# -*- coding: utf-8 -*-
import numpy as np

'''
Nombre: Carlos S. Galindo Jiménez
Nombre: José Antonio Pérez
Fecha: 17/11/2017
'''

def create_graph(N,maxvalue=1000):
  G = np.random.randint(maxvalue, size=(N, N))
  for i in range(N):
    G[i][i] = 0
  return G

def process_graph(G):
  # EJERCICIO 2
  N = G.shape[0]
  for x in range(0, N-1):
    for y in range(x+1, N):
      if (G[x, y] > G[y, x]):
        G[x, y] -= G[y, x]
        G[y, x] = 0
      else:
        G[y, x] -= G[x, y]
        G[x, y] = 0

def generate_random_ordering(G):
  # let's assume that G is a square Numpy matrix of integers
  N = G.shape[0]
  return np.random.permutation(N)

def generate_greedy_ordering(G, infty = 1e9):
  # let's assume that G is a square Numpy matrix of integers
  N = G.shape[0]
  # EJERCICIO 1
  res = []
  # Compute initial score (if the vertex was first) for all vertices
  remaining = []
  for i in range(N):
    score = sum(G[i, x] for x in range(N)) - sum(G[x, i] for x in range(N))
    remaining.append((score, i))

  # Add vertices to res, modifying the score of the remaining ones
  while len(res) < N:
    remaining = sorted(remaining, reverse=True)
    _, v = remaining.pop(0)
    res.append(v)
    for i, (score, rv) in enumerate(remaining):
      # Ahora que el vertice ha pasado delante de estos
      # Tenemos que quitar del score la cantidad que supone el orden rv, v
      # Y añadir la cantidad que supone el orden v, rv
      # Como estas cantidades son la misma pero con distinto signo, basta con sumar
      # 2 * cantidad por orden v, rv
      score = score + 2 * (G[v, rv] - G[rv, v])
      remaining[i] = (score, rv)
  return res

def evaluate(G,ordering):
  # assume that G.shape is of type (N,N) and ordering.shape is of type
  # (N) and is a permutation of values 0,...,N-1
  N = G.shape[0]
  return sum(G[ordering[i]][ordering[j]]-G[ordering[j]][ordering[i]]
             for i in range(N) for j in range(i+1,N))

def show_evaluate(G,ordering):
  N = G.shape[0]
  positivos = list(G[ordering[i]][ordering[j]] for i in range(N) for j in range(i+1,N))
  negativos = list(G[ordering[j]][ordering[i]] for i in range(N) for j in range(i+1,N))
  vpos = sum(positivos)
  vneg = sum(negativos)
  resul = vpos-vneg
  print("(" + ",".join(map(str,positivos))+") - (" + ",".join(map(str,negativos))+
        ") = ",vpos, "-", vneg, "=", resul)
  return resul


# si pruebas con este grafo:
G= np.asarray([[0, 8, 3, 2, 9],
               [3, 0, 3, 8, 2],
               [0, 2, 0, 6, 2],
               [4, 4, 8, 0, 0],
               [7, 7, 6, 2, 0]],dtype=np.int)
# el algoritmo voraz hace estos pasos:
# [] [(8, 0), (-5, 1), (-10, 2), (-2, 3), (9, 4)]
# [4] [(4, 0), (5, 1), (-2, 2), (2, 3)]
# [4, 1] [(-6, 0), (0, 2), (10, 3)]
# [4, 1, 3] [(-2, 0), (4, 2)]
# [4, 1, 3, 2] [(-8, 0)]
# y termina dando como resultado:
# [4, 1, 3, 2, 0]
# con valor 10

# este trozo prueba ejemplos aleatorios:
N = 30
G = create_graph(N,100)
#print("G=",G)
random_ordering = generate_random_ordering(G)
greedy_ordering = generate_greedy_ordering(G)
print("random",evaluate(G,random_ordering),random_ordering)
print("greedy",evaluate(G,greedy_ordering),greedy_ordering)

