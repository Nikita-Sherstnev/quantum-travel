from qboard import Solver
import numpy as np

# Access parameters
PARAMS = {
    "remote_addr": "https://remote.qboard.tech", 
    "access_key": "a0062a5e-d3ae-4a17-8499-f4d40358de94"
}

if __name__ == '__main__':
    # Solver initialization
    s = Solver(mode="remote:simcim", params=PARAMS)

    # QUBO matrix definition
    Q = np.random.randn(5,5)

    # Getting results
    spins, energy = s.solve_qubo(Q, timeout=30)
