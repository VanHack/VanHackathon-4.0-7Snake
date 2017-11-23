import csv
import sys
from tqdm import tqdm

matrix_rs = []
pos_avail = []
sum_snk = []
snk = []
snks = []
vsnk = [0, 0, 0, 0, 0, 0, 0]
var_end = 0
t_pot = []

file = sys.argv[1]

with open(file) as csvfile:
    reader = csv.reader(csvfile)
    matrix_rs = [[int(value) for value in row] for row in reader]

n_rows = len(matrix_rs)
n_cols = len(matrix_rs[0])

pos_avail = [(j, i) for j in range(n_cols) for i in range(n_rows)]

def getAdjacent(cell, variant, i_cell=(0,0)):
    if (cell[1] + 1 < n_cols) and ((cell[0], cell[1] + 1) in pos_avail) and not ((cell[0], cell[1] + 1) in snk) and variant == 1:
        return (cell[0], cell[1] + 1)
    elif (cell[0] + 1 < n_rows) and ((cell[0] + 1, cell[1]) in pos_avail) and not ((cell[0] + 1, cell[1]) in snk) and variant == 2:
        return (cell[0] + 1, cell[1])
    elif (cell[1] - 1 >= 0) and ((cell[0], cell[1] - 1) in pos_avail) and not ((cell[0], cell[1] - 1) in snk) and variant == 3:
        return (cell[0], cell[1] - 1)
    elif (cell[0] - 1 >= i_cell[0]) and ((cell[0] - 1, cell[1]) in pos_avail) and not ((cell[0] - 1, cell[1]) in snk) and variant == 4:
        return (cell[0] - 1, cell[1])
    else:
        return -1

def findDupsSum(seq, item):
    st = -1
    lis_dup = []
    while True:
        try:
            it_lis = seq.index(item, st + 1)
        except ValueError:
            break
        else:
            lis_dup.append(it_lis)
            st = it_lis
    return lis_dup

        
def removeFromList(cell):
    while cell in pos_avail:
        pos_avail.remove(cell)

def addSnake():
    sum = 0
    snks.append(list(snk))
    for ind in snk:
        sum = sum + matrix_rs[ind[0]][ind[1]]
    sum_snk.append(sum)

def generateAllSnakes():
    i = 0
    global var_end
    global vsnk
    if not snk:
        for _ in range(7):
            snk.append(0)
            
    for row in tqdm(range(n_rows)):
        for col in range(n_cols):
            vsnk = [0, 0, 0, 0, 0, 0, 0]
            snk[0] = (row, col)
            if snk[0] in pos_avail:
                removeFromList(snk[0])
            generateSections(1)
            if var_end == 1:
                break
            addSnake()
            t_pot.append(len(pos_avail))
            while var_end != 1:
                generateSections()
                if var_end != 1:
                    addSnake()
                    t_pot.append(len(pos_avail))
                else:
                    break
            var_end = 0
            for it in snk:
                if it != 0 and not it in pos_avail:
                    pos_avail.append(it)
                    
        for it in snk:
            if it != 0 and not it in pos_avail:
                pos_avail.append(it)
        var_end = 0
        
def generateSections(seg=6):
    global var_end
    global vsnk
    if vsnk[seg] < 4 :
        vsnk[seg] = vsnk[seg] + 1
        cell = getAdjacent(snk[seg - 1], vsnk[seg], snk[0])
        if cell != -1:
            if snk[seg] != 0 and not snk[seg] in pos_avail:
                pos_avail.append(snk[seg])
            snk[seg] = cell
            removeFromList(cell)
            if seg + 1 <= 6:
                vsnk[seg + 1] = 0
                generateSections(seg + 1)
        else:
            generateSections(seg)
    else:
        if seg - 1 > 0:
            if snk[seg] != 0 and not snk[seg] in pos_avail:
                pos_avail.append(snk[seg])
                snk[seg] = 0
            generateSections(seg - 1)
        else:
            var_end = 1

def main():
    generateAllSnakes()
    sn7_1 = []
    sn7_2 = []
    for it_sum in tqdm(sum_snk):
        indx = findDupsSum(sum_snk, it_sum)
        for num, index in tqdm(enumerate(indx)):
            for num2 in indx[index:]:
                var = set(snks[num]) & set(snks[num2])
                if not var:
                    sn7_1 = snks[num]
                    sn7_2 = snks[num2]
                    break
            if sn7_1 and sn7_2:
                break
        if sn7_1 and sn7_2:
            break
    if not sn7_1 or not sn7_2:
        print('FAIL')
    else:
        print(sn7_1)
        print(sn7_2)
    
if __name__ == '__main__':
    main()