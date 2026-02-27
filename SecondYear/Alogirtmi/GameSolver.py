stolpci = []
vrstice = []
skupaj = []
stol_skupaj = 0
vrst_skupaj = 0


def find_max(tabela):
    max = -1
    res = (-1, -1)

    for i in range(len(tabela)):
        for j in range(len(tabela[i])):
            if tabela[i][j] > max:
                max = tabela[i][j]
                res = (i, j)
                if max == 1:
                    return res

    return res


vhod = input("vpisite stolpec\n")
i = 0

while (vhod != ""):
    stolpci.append(int(vhod))
    stol_skupaj += int(vhod)
    i += 1
    vhod = input()

vhod = input("vpisite vrstico\n")
j = 0

while (vhod != ""):
    vrstice.append(int(vhod))
    vrst_skupaj += int(vhod)
    j += 1
    vhod = input()

reseno = [['.' for _ in range(i)] for _ in range(j)]

while (stol_skupaj > 0):
    skupaj = []

    for stol in range(len(stolpci)):
        temp = []
        for vrst in range(len(vrstice)):
            if reseno[vrst][stol] == '#':
                temp.append(-1)
            elif stolpci[stol] <= 0 or vrstice[vrst] <= 0:
                temp.append(-1)
            else:
                temp.append(round((stolpci[stol] / j + vrstice[vrst] / i) / 2, 3))
        skupaj.append(temp)

    max_i, max_j = find_max(skupaj)

    if max_i == -1 or max_j == -1:
        break

    reseno[max_j][max_i] = '#'
    stolpci[max_i] -= 1
    vrstice[max_j] -= 1
    stol_skupaj -= 1

for row in reseno:
    print(" ".join(row))