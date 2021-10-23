import math
import json

from api import base
from solver import qubo_tsp

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
        # Инициализируем Solver
        s = Solver(mode="remote:gurobi", params=PARAMS)

        # Определяем матрицу QUBO
        Q = qubo_tsp(nodes, n)

        i_lower = np.tril_indices(25, -1)
        Q[i_lower] = Q.T[i_lower]
        spins, energy = s.solve_qubo(Q, timeout=30)

        ans = list(chunks(list(map(int, spins.tolist())), 5))
        res = []
        
        for a in ans:
            res.append(a.index(0))

        return res