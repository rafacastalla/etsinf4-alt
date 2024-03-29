import numpy as np
import heapq # a priority queue
import math

'''
Nombre: Carlos S. Galindo Jiménez
Nombre: José Antonio Pérez
Fecha: 20/12/2017
'''

def create_graph(N,maxvalue=1000):
  G = np.random.randint(maxvalue, size=(N, N))
  for i in range(N):
    G[i][i] = 0
    for j in range(i+1,N):
      m = min(G[i][j],G[j][i])
      G[i][j] -= m
      G[j][i] -= m
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

def generate_greedy_ordering(G):
  # let's assume that G is a square Numpy matrix of integers
  N = G.shape[0]
  resul = []
  while len(resul)<N:
    noresul = list(set(range(N))-set(resul))
    aux = []
    for i in range(N):
      if i not in resul:
        score = (sum(G[j][i]-G[i][j] for j in resul) +
                 sum(G[i][j]-G[j][i] for j in noresul if j!=i))
        aux.append((score,i))
    print(resul,aux)
    score,choice = max(aux)
    resul.append(choice)
  return np.asarray(resul,dtype=np.int)

def evaluate_partial(G,ordering):
  # assume that G.shape is of type (N,N) and ordering.shape is of type
  # (N) and is a permutation of values 0,...,N-1
  N = len(ordering)
  return sum(G[ordering[i]][ordering[j]]-G[ordering[j]][ordering[i]]
             for i in range(N) for j in range(i+1,N))


def BranchAndBound(G):
  # ojo con graph <- "se mira pero no se toca"
  N = G.shape[0]

  def optimistic(s, p_score = float('nan')):
    # s es una lista de vertices entre 0 y N-1
    # Vertices no colocados en s
    rest = [i for i in range(N) if i not in s]
    if math.isnan(p_score):
      opt = 0
      # Aristas de vertices colocados a desconocidos
      opt += sum(G[i,j] for i in s for j in rest)
      opt -= sum(G[j,i] for i in s for j in rest)
      # Aristas entre vertices colocados
      opt += sum(G[i,j] for x,i in enumerate(s) for y,j in enumerate(s) if x < y)
      opt -= sum(G[j,i] for x,i in enumerate(s) for y,j in enumerate(s) if x < y)
      # Estimacion aristas entre vertices desconocidos (suma de todos sus pesos)
      opt += sum(G[i,j] for i in rest for j in rest)
      return opt
    else:
      return p_score - 2 * sum(G[i,s[-1]] for i in rest)

  def branch(s):
    return (s+[i] for i in range(N) if i not in s)

  def is_complete(s):
    return len(s) == N

  A = [] # empty priority queue
  x = generate_greedy_ordering(G)
  fx = optimistic(x) # equivale a evaluate quando is_complete(x)

  # anyadimos el estado inicial:
  s = []
  opt = optimistic(s)
  heapq.heappush(A,(-opt,s))
  iter = 0
  maxA = 0
  # bucle principal de ramificacion y poda:
  while len(A)>0 and -A[0][0] > fx: # PODA IMPLICITA
    iter += 1
    lenA = len(A)
    maxA = max(maxA,lenA)
    score_s, s = heapq.heappop(A)
    score_s = -score_s # ahora ya no está negado
    print("Iter. %04d |A|=%05d max|A|=%05d fx=%04d score_s=%04d" % \
      (iter,lenA,maxA,fx,score_s))
    for child in branch(s):
      fchild = optimistic(child, score_s)
      if is_complete(child): # si es terminal
        # seguro que es factible
        # falta ver si mejora la mejor solucion en curso
        if fchild > fx:
          x = child
          fx = fchild
      else: # no es terminal
        # lo metemos en el cjt de estados activos si supera
        # la poda por cota optimista:
        if fchild > fx:
          heapq.heappush(A,(-fchild, child))
  return x,fx

if __name__ == "__main__":
    N = 8
    G = create_graph(N,5)
#     G = np.asarray([[0, 1, 1, 1],
#                     [0, 0, 1, 1],
#                     [0, 0, 0, 1],
#                     [0, 0, 0, 0]], dtype=np.int)
    process_graph(G)
    print("G=",G)
    x,fx = BranchAndBound(G)
    greedy_ordering = generate_greedy_ordering(G)
    print("greedy ordering", greedy_ordering,evaluate(G,greedy_ordering))
    print("exacto",x,fx,evaluate(G,x))

