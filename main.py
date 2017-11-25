import numpy as np
# Weight Values
row_pos = [3.88, 4.64, 5.4, 6.37, 7.13, 7.89, 8.55, 9.55, 5.643, 10]
# Position Index Keys > 1,2,3,4,5,6,CO,CA,Fuel, Crew Baggage Position

A_mass = [[55, 63, 65], [66, 68, 70], [72, 74, 78], [78], [83, 86], [85], [0], [0], [835.2], [0]]
B_mass = [[0], [0], [63, 57, 84], [64, 65, 70], [72, 73, 74], [75, 80, 80], [85], [0], [650.8], [0]]
C_mass = [[50, 59, 53], [0], [67, 68, 68], [70, 70, 73], [78, 80, 82], [85], [0], [0], [814.2], [35, 6]]
D_mass = [[100, 88, 85], [77, 78, 79], [70, 75, 68], [52, 57, 85], [0], [0], [0], [0], [840.4], [35]]
E_mass = [[0], [62, 68, 69], [70, 72, 73], [73, 74, 88], [75, 84, 87], [62, 85], [0], [0], [642.8], [35]]
aircraft_data = [[4949, 27505]]


def cogcalc(masses, pos):
    mx = [aircraft_data[0][1]]
    m = [aircraft_data[0][0]]
    for posid, row in enumerate(masses):
        rowmass = 0
        for seat in row:
            rowmass += seat
        mx.append(rowmass*pos[posid])
        m.append(rowmass)
    cogpos = ((np.sum(mx)/np.sum(m)) - 5.149) * (100/1.717)
    return cogpos

print(str(cogcalc(A_mass, row_pos)))
print(str(cogcalc(B_mass, row_pos)))
print(str(cogcalc(C_mass, row_pos)))
print(str(cogcalc(D_mass, row_pos)))
print(str(cogcalc(E_mass, row_pos)))