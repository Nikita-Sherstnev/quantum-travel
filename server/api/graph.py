import math
import json

from api import base
from solver import qubo_tsp, tsp

from qboard import Solver
import numpy as np

PARAMS = {
    "remote_addr": "https://remote.qboard.tech",
    "access_key": "pass"
}


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class Graph(base.ApiResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.post_parser = base.RequestParser()
        self.post_parser.add_argument('graph', location='json', required=True)

    def post(self):
        args = self.post_parser.parse_args()
        nodes = json.loads(args.graph)

        n = 0
        for i in nodes:
            if i[0] > i[1] and i > n:
                n = i[0]
            elif i[1] > n:
                n = i[1]
        n += 1

        # Номера станций
        # 0 - Краснопресенская
        # 1 - Кропоткинская
        # 2 - Библиотека Имени Ленина
        # 3 - Охотный ряд
        # 4 - Третьяковская
        # Подготавливаем матрицу весов и сохраняем
        max = 1

        for el in nodes:
            if el[0] > max:
                max = el[0] + 1

            if el[1] > max:
                max = el[1] + 1

        adjacency_array = [[0 for x in range(max)] for y in range(max)]

        for el in nodes:
            adjacency_array[el[0]][el[1]] = el[2]

        adjacency = np.asarray(adjacency_array)
        i_lower = np.tril_indices(5, -1)
        adjacency[i_lower] = adjacency.T[i_lower]

        np.save("adjacency.npy", adjacency)

        # Инициализируем Solver
        s = Solver(mode="remote:gurobi", params=PARAMS)

        # Определяем матрицу QUBO
        Q = qubo_tsp(nodes, n)

        np.save("Q.npy", Q)

        i_lower = np.tril_indices(25, -1)
        Q[i_lower] = Q.T[i_lower]
        spins, energy = s.solve_qubo(Q, timeout=30)

        ans = list(chunks(list(map(int, spins.tolist())), 5))
        path = []

        try:
            # Определяем номер станции по one-hot вектору
            for a in ans:
                path.append(a.index(1))
        except ValueError:
            print('Решение классическим методом.')
            path = tsp(nodes, n)
        
        return [int(p) for p in path]
