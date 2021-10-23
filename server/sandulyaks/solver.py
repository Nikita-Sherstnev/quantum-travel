from xml.etree.ElementTree import QName

from qboard import Solver
import numpy as np

# Access parameters
PARAMS = {
    "remote_addr": "https://remote.qboard.tech",
    "access_key": "a0062a5e-d3ae-4a17-8499-f4d40358de94"
}


def qubo_tsp(array, metro_count) -> np.ndarray:
    # Количество станций метро
    n = metro_count
    # Штраф за нарушение органичений
    penalty_A = 15
    penalty_B = 25

    q = np.zeros((n, n, n, n))

    # Каждая станция встречается один раз в цикле
    for i in range(n):
        q[i, :, i, :] = penalty_A * (np.ones((n, n)) - np.eye(n))

    # Добавление весов
    for el in array:
        q[el[0], :, el[1], :] = penalty_B * el[2] * (np.ones((n, n)) - np.eye(n))

    # Станция в j цикле не может встретиться в другом цикле с таким же номер
    for i in range(n):
        q[:, i, :, i] = penalty_A * (np.ones((n, n)) - np.eye(n))

    # Раскрывает 4-матрицу в 2-матрицу
    return q.reshape((n * n, n * n))


if __name__ == '__main__':
    # Номера станций
    # 0 - Краснопресенская
    # 1 - Кропоткинская
    # 2 - Библиотека Имени Ленина
    # 3 - Охотный ряд
    # 4 - Третьяковская

    # Узлы графа, [Номер станции, номер станции, расстояние в минутах]
    nodes = [
        [0, 1, 15],
        [0, 2, 17],
        [0, 3, 16],
        [0, 4, 16],
        [1, 2, 3],
        [1, 3, 4],
        [1, 4, 16],
        [2, 3, 3],
        [2, 4, 15],
        [3, 4, 12],
    ]

    # Сохраняем весовой граф в файл
    np.save("adjacency.npy", nodes)

    # Инициализируем Solver
    s = Solver(mode="remote:simcim", params=PARAMS)

    # Определяем матрицу QUBO
    Q = qubo_tsp(nodes, 5)
    np.save("Q.npy", Q)

    # Получаем результат
    spins, energy = s.solve_qubo(Q, timeout=30)
    print(spins, energy)
