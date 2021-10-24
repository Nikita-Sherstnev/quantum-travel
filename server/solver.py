import numpy as np
import networkx as nx
from networkx.algorithms.approximation import traveling_salesman_problem


def qubo_tsp(array, metro_count) -> np.ndarray:
    # Количество станций метро
    n = metro_count
    # Штраф за нарушение органичений
    penalty_a = 10
    penalty_b = 50

    q = np.zeros((n, n, n, n))

    # Каждая станция встречается один раз в цикле
    for i in range(n):
        q[i, :, i, :] = penalty_a * (np.ones((n, n)) - np.eye(n))

    # Добавление весов
    for el in array:
        q[el[0], :, el[1], :] = penalty_b * el[2] * (np.ones((n, n)) - np.eye(n))

    # Станция в j цикле не может встретиться в другом цикле с таким же номер
    for i in range(n):
        q[:, i, :, i] = penalty_a * (np.ones((n, n)) - np.eye(n))

    # Раскрывает 4-матрицу в 2-матрицу
    return q.reshape((n * n, n * n))


def tsp(nodes, n):
    G = nx.Graph()
    G.add_nodes_from(np.arange(0,n,1))
    G.add_weighted_edges_from(nodes)

    return traveling_salesman_problem(G)