from imports import *


def gen_coords_c(N, M):  # generate graphene's coordinates
    a0 = 142.1
    s3 = (3.) ** 0.5
    coords = []
    full_topo = {}
    x0 = s3 * a0 / 2.
    x1 = 0.
    for m in range(M):
        y0 = 0.
        y1 = a0 / 2.
        y2 = a0 * 1.5
        y3 = a0 * 2.
        z = 0.
        for n in range(N):
            coords.append((x0, y0, z))
            full_topo[4 * N * m + 4 * n] = []
            full_topo[4 * N * m + 4 * n].append(4 * N * m + 4 * n + 1)  # connection wit this n
            if m < (M - 1):
                full_topo[4 * N * m + 4 * n].append(4 * N * (m + 1) + 4 * n + 1)  # connection wit next m
            if n > 0:
                full_topo[4 * N * m + 4 * n].append(4 * N * m + 4 * n - 1)  # connection wit previous n

            coords.append((x1, y1, z))
            full_topo[4 * N * m + 4 * n + 1] = []
            full_topo[4 * N * m + 4 * n + 1].append(4 * N * m + 4 * n)  # connection wit this n
            full_topo[4 * N * m + 4 * n + 1].append(4 * N * m + 4 * n + 2)  # connection wit this n
            if m > 0:
                full_topo[4 * N * m + 4 * n + 1].append(4 * N * (m - 1) + 4 * n)  # connection wit previous m

            coords.append((x1, y2, z))
            full_topo[4 * N * m + 4 * n + 2] = []
            full_topo[4 * N * m + 4 * n + 2].append(4 * N * m + 4 * n + 1)  # connection wit this n
            full_topo[4 * N * m + 4 * n + 2].append(4 * N * m + 4 * n + 3)  # connection wit this n
            if m > 0:
                full_topo[4 * N * m + 4 * n + 2].append(4 * N * (m - 1) + 4 * n + 3)  # connection wit previous m

            full_topo[4 * N * m + 4 * n + 3] = []
            coords.append((x0, y3, z))
            full_topo[4 * N * m + 4 * n + 3].append(4 * N * m + 4 * n + 2)  # connection wit this n
            if m < (M - 1):
                full_topo[4 * N * m + 4 * n + 3].append(4 * N * (m + 1) + 4 * n + 2)  # connection wit next m
            if n < (N - 1):
                full_topo[4 * N * m + 4 * n + 3].append(4 * N * m + 4 * (n + 1))  # connection wit next n

            y0 += 3. * a0
            y1 += 3. * a0
            y2 += 3. * a0
            y3 += 3. * a0
        x0 += s3 * a0
        x1 += s3 * a0

    return coords, full_topo


def calc_E1(g):
    A1 = [[0, 1., 1, 1, 0, 0, 0, 0, 0, 0],
          [1, 0, 0, 0, 1, 1, 0, 0, 0, 0],
          [1, 0, 0, 0, 0, 0, 1, 1, 0, 0],
          [1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]]

    A2 = [[0, 0, 0, 0, 1., 1, 1, 1, 1, 1],
          [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
          [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
          [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
          [1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
          [1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
          [1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
          [1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
          [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 1, 0]]
    A1 = np.array(A1)
    A2 = np.array(A2)
    Ef, a1, a2, b1, b2 = [-1.01077427, 0.27016959, 0.08816037, -0.83043493, 0.1652446]  # >40%
    Ef, a1, a2, b1, b2 = [-1.01025288, 0.28779231, 0.07563629, -0.84786808, 0.20291209]  # <50%
    Ef, a1, a2, b1, b2 = [-1.00070806, 0.27776472, 0.07930538, -0.86348635, 0.18097026]  # geneal
    E = np.sum(np.abs(g)) * Ef
    for i in range(len(g)):
        for j in range(i + 1, len(g)):
            E += a1 * A1[i][j] * g[i] * g[j] + a2 * A2[i][j] * g[i] * g[j] + b1 * A1[i][j] * np.abs(g[i] * g[j]) + b2 * \
                 A2[i][j] * np.abs(g[i] * g[j])
    return E


def calc_prob(i, coords, topo, fluor, beta,
              z,one_side):  # return an array (2,2) with structure [[orientaion of F(+1), probability],[orientaion of F(-1),probability]]
    bonded_with = list(topo[i])  # find all neighbor-carbons
    if len(bonded_with) == 3:  # we are not on the edge
        g = np.zeros(10)
        g[1] = fluor[bonded_with[0]]
        g[2] = fluor[bonded_with[1]]
        g[3] = fluor[bonded_with[2]]
        for j in [0, 1, 2]:
            g1 = list(topo[bonded_with[j]])
            g1.remove(i)
            for k in range(len(g1)):
                g[4 + 2 * j + k] = fluor[g1[k]]
        Ap = 2.
        Am = 2.
        for r in g[1:4]:
            if r == 1:
                Ap -= 0.39
                Am += 0.02
            elif r == -1:
                Am -= 0.39
                Ap += 0.02
        E0 = calc_E1(g)
        g[0] = 1
        E_p = calc_E1(g)

        # g=-g
        g[0] = -1

        E_m = calc_E1(g)
        P_plus = Ap * np.exp(-(E_p - E0) * beta)
        P_minus = one_side*Am * np.exp(-(E_m - E0) * beta)

    else:
        P_plus = 0.
        P_minus = 0.
    res = np.array([[1, P_plus], [-1, P_minus]])
    return res  # return a tuple (2,2) with structure [[orientaion of F(+1), probability],[orientaion of F(-1),probability]]


def probsAndZ_calc(zzz, ATOM, coords, topo, fluor, probabilities, beta,one_side):  # recalculate probabilities and Z
    zzz -= (probabilities[ATOM][0][1] + probabilities[ATOM][1][1])

    probabilities[ATOM] = [[1, 0.], [-1, 0.]]
    neighbours = list(topo[ATOM])  # find all neighbouring carbons
    second_order_neighbours = np.array(ATOM)

    for j in neighbours:
        second_order_neighbours = np.hstack(
            (second_order_neighbours, np.array(topo[j])))  # find all second-order neighboring carbons
    for j in second_order_neighbours:
        if j not in neighbours:
            neighbours.append(j)
    # print neighbours
    for element in neighbours:
        zzz -= (probabilities[element][0][1] + probabilities[element][1][1])  # subtract from Z old probabilities
        if fluor[element] != 0.:
            probabilities[element] = [[1, 0.], [-1, 0.]]
        else:
            probabilities[element] = calc_prob(element, coords, topo, fluor, beta, zzz,one_side)  # find new probabilities
            # print '#',probabilities[element]
        zzz += probabilities[element][0][1] + probabilities[element][1][1]  # add to Z new probabilities

    return zzz, probabilities


def fluorination(f_n, N, M, zz, c_free_array, coords, full_topo, fluor, f_prohibided, probabilities, beta, F_N,one_side):
    i = np.random.choice(c_free_array)  # set position of F atom
    if i not in f_prohibided:
        res = probabilities[
            i]  # return an array (2,2) with structure [[orientaion of F(+1), probability],[orientaion of F(-1),probability]]
        rv = np.random.rand()
        # print rv,res[0][1]/zz,res[1][1]/zz
        # print probabilities
        if 0. < rv < res[0][1] / zz:  # decide, will F be +1
            pmigr = [probabilities[i][0][1]]
            zmigr = probabilities[i][0][1]
            rv_m = np.random.rand()
            for k in full_topo[i]:
                zmigr += probabilities[k][0][1]
                pmigr.append(probabilities[k][0][1])
            if 0. < rv_m < pmigr[0] / zmigr:
                j = i
            elif pmigr[0] / zmigr < rv_m < (pmigr[0] + pmigr[1]) / zmigr:
                j = full_topo[i][0]
            elif (pmigr[0] + pmigr[1]) / zmigr < rv_m < (pmigr[0] + pmigr[1] + pmigr[2]) / zmigr:
                j = full_topo[i][1]
            elif (pmigr[0] + pmigr[1] + pmigr[2]) / zmigr < rv_m:
                j = full_topo[i][2]
            j = i
            fluor[j] = 1
            f_n += 1
            zz, probabilities = probsAndZ_calc(zz, j, coords, full_topo, fluor, probabilities,beta, one_side)
            updcircle(j, N, M, 1, f_n, F_N)
            c_free_array.remove(j)

        elif res[0][1]/zz < rv < res[0][1]/zz + res[1][1]/zz:
            pmigr = [probabilities[i][1][1]]
            zmigr = probabilities[i][1][1]
            rv_m = np.random.rand()
            for k in full_topo[i]:
                zmigr += probabilities[k][1][1]
                pmigr.append(probabilities[k][1][1])
            if 0. < rv_m < pmigr[0] / zmigr:
                j = i
            elif pmigr[0] / zmigr < rv_m < (pmigr[0] + pmigr[1]) / zmigr:
                j = full_topo[i][0]
            elif (pmigr[0] + pmigr[1]) / zmigr < rv_m < (pmigr[0] + pmigr[1] + pmigr[2]) / zmigr:
                j = full_topo[i][1]
            elif (pmigr[0] + pmigr[1] + pmigr[2]) / zmigr < rv_m:
                j = full_topo[i][2]
            j = i
            fluor[j] = -1
            f_n += 1
            zz, probabilities = probsAndZ_calc(zz, j, coords, full_topo, fluor, probabilities, beta,one_side)
            updcircle(j, N, M, -1, f_n, F_N)
            c_free_array.remove(j)

    return f_n, zz, c_free_array


def calc_fluor(coords, full_topo, N, M, fluor, F_N, zz, f_prohibided, probabilities, beta,one_side):
    f_n = 0
    c_free_array = list(range(len(fluor)))
    while f_n < F_N:
        f_n, zz, c_free_array = fluorination(f_n, N, M, zz, c_free_array, coords, full_topo, fluor, f_prohibided,
                                             probabilities, beta, F_N,one_side)

    return fluor, zz


def calcF(N, M, f_perc, beta,one_side):
    N = N + 2
    f_prohibided = []  # edge atoms

    for m in range(M):
        for k in range(4):
            f_prohibided.append(m * 4 * N + k)
            f_prohibided.append((m + 1) * 4 * N - k - 1)

    F_N = int((4 * N * M - len(f_prohibided) - N * 4 + 8) * f_perc)
    probabilities = np.zeros([4 * N * M, 2, 2], dtype=np.float32)
    fluor = np.zeros(4 * N * M)
    Z = 1.
    coords, full_topo = gen_coords_c(N, M)
    # print full_topo
    for i in range(4 * N * M):
        if i in f_prohibided:
            probabilities[i] = [[1, 0], [-1, 0]]
        else:
            probabilities[i] = calc_prob(i, coords, full_topo, fluor, beta, Z,one_side)

    for element in probabilities:
        Z += element[0][1] + element[1][1]
    # print Z
    fluor, Z = calc_fluor(coords, full_topo, N, M, fluor, F_N, Z, f_prohibided, probabilities, beta,one_side)
    return fluor, coords, full_topo
