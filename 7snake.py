import csv
import sys
from tqdm import tqdm

matrix_rs = []
pos_avail = []
sum_snk = []
snk = []
snks = []
v_snk = [0, 0, 0, 0, 0, 0, 0]
var_end = False

file = sys.argv[1]

with open(file) as csvfile:
    reader = csv.reader(csvfile)
    matrix_rs = [[int(value) for value in row] for row in reader]

n_rows = len(matrix_rs)
n_cols = len(matrix_rs[0])

pos_avail = [(j, i) for j in range(n_cols) for i in range(n_rows)]

def get_adjacent(cell, variant, i_cell=(0,0)):
    global pos_avail, snk, n_cols, n_rows
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

def find_dups_sum(seq, item):
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

        
def remove_from_list(cell):
    global pos_avail
    while cell in pos_avail:
        pos_avail.remove(cell)

def add_snake():
    global matrix_rs, sum_snk, snk, snks
    sum = 0
    snks.append(list(snk))
    for ind in snk:
        sum = sum + matrix_rs[ind[0]][ind[1]]
    sum_snk.append(sum)

def generate_all_snakes():
    global var_end, snk, v_snk, pos_avail, n_rows, n_cols
    if not snk:
        for _ in range(7):
            snk.append(0)
            
    for row in tqdm(range(n_rows)):
        for col in range(n_cols):
            v_snk = [0, 0, 0, 0, 0, 0, 0]
            snk[0] = (row, col)
            if snk[0] in pos_avail:
                remove_from_list(snk[0])
            generate_sections(1)
            if var_end:
                break
            add_snake()
            while not var_end:
                generate_sections()
                if not var_end:
                    add_snake()
                else:
                    break
            var_end = False
            for it in snk:
                if it != 0 and not it in pos_avail:
                    pos_avail.append(it)
                    
        for it in snk:
            if it != 0 and not it in pos_avail:
                pos_avail.append(it)
        var_end = False
        
def generate_sections(seg=6):
    global var_end, v_snk, pos_avail, snk
    if v_snk[seg] < 4 :
        v_snk[seg] = v_snk[seg] + 1
        cell = get_adjacent(snk[seg - 1], v_snk[seg], snk[0])
        if cell != -1:
            if snk[seg] != 0 and not snk[seg] in pos_avail:
                pos_avail.append(snk[seg])
            snk[seg] = cell
            remove_from_list(cell)
            if seg + 1 <= 6:
                v_snk[seg + 1] = 0
                generate_sections(seg + 1)
        else:
            generate_sections(seg)
    else:
        if seg - 1 > 0:
            if snk[seg] != 0 and not snk[seg] in pos_avail:
                pos_avail.append(snk[seg])
                snk[seg] = 0
            generate_sections(seg - 1)
        else:
            var_end = True

def main():
    global sum_snk, snks
    generate_all_snakes()
    sn7_1 = []
    sn7_2 = []
    for it_sum in sum_snk:
        indx = find_dups_sum(sum_snk, it_sum)
        for cell, index in enumerate(indx):
            for cell_b in indx[index:]:
                var = set(snks[cell]) & set(snks[cell_b])
                if not var:
                    sn7_1 = snks[cell]
                    sn7_2 = snks[cell_b]
                    break
            if sn7_1 and sn7_2:
                break
        if sn7_1 and sn7_2:
            break
    if not sn7_1 or not sn7_2:
        print('FAIL')
    else:
        print('Snake A: ' + str(sn7_1))
        print('Snake B: ' + str(sn7_2))
    
if __name__ == '__main__':
    main()