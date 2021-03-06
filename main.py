"""
This is the main script for generating the graphs.
"""

import numpy as np
import matplotlib.pyplot as plt

#Graph Utility
point_bank = ['rD', 'bo', 'cx', 'gs', 'm^', 'rp', 'bx', 'cx', 'gx', 'mx']

# Constants
aircraft_data = [4949, 27505]
Sw = 25.083  # m2
c_bar = 1.717  # m
mass_empty = 4949  # kg
g = 9.80665  # m/s2
rho0 = 1.225  # kg/m2
P0 = 101325  # N/m2
T0 = 288.15  # K


# Weight Values
row_pos = [3.88, 4.64, 5.4, 6.37, 7.13, 7.89, 8.55, 9.55, 5.643, 10]
# Position Index Keys > 1,2,3,4,5,6,CO,CA,Fuel, Crew Baggage Position

"""
DATA Format
Mass:> Each element is a row, each inner, element is a mass (kg)/seat.
Static:> Each element is a test. Test structure -> [Elevator Tab Angle (deg), Elevator Angle (deg), Airspeed EAS(kts)]
Man:> Each element is a test. Test structure -> [Elevator Angle (deg), Link Force (N), Normal Acceleration (g)]
Link:> Link Force (N), P_spring.
"""

A_mass = [[55, 63, 65], [66, 68, 70], [72, 74, 78], [78], [83, 86], [85], [0], [0], [835.2], [0]]
A_static = [[6.2, -3.1, 145], [8.1, -4.3, 134], [9.7, -4.6, 125], [5, -2.6, 156], [3.6, -2.2, 164]]
A_man = [[-2.2, -137, 1], [-3.1, -67, 1.16], [-4.2, -14, 1.32], [-5.2, 70, 1.56], [-7, 224, 1.97]]
A_link = -191

B_mass = [[0], [0], [63, 57, 84], [64, 65, 70], [72, 73, 74], [75, 80, 80], [85], [0], [650.8], [0]]
B_static = [[2.7, -0.8, 145], [3.4, -0.8, 136], [5, -1.1, 127], [1.9, -0.3, 156], [1.5, -0.1, 165]]
B_man = [[-0.1, -239, 1], [-0.8, -199, 1.18], [-1.1, -157, 1.3], [-1.5, -82, 1.47], [-3.7, 74, 2.09]]
B_link = -197

C_mass = [[50, 59, 63], [0], [67, 68, 68], [70, 70, 73], [78, 80, 82], [85], [0], [0], [814.2], [35, 6]]
C_static = [[4.3, -1.8, 144], [3.5, -1.4, 154], [2.6, -1.2, 166], [5.2, -2.2, 136], [6.8, -2.8, 127]]
C_man = [[-0.8, -171, 1], [-1.8, -119, 1.14], [-2.6, -83, 1.29], [-4.2, 48, 1.67], [-5.6, 170, 1.96]]
C_link = -164

D_mass = [[100, 88, 85], [77, 78, 79], [70, 75, 68], [52, 57, 85], [0], [0], [0], [0], [840.4], [35]]
D_static = [[6.5, -3.7, 146], [8.2, -4.2, 135], [10.8, -5.6, 124], [5.3, -3.1, 157], [4.2, -2.6, 167]]
D_man = [[-2.7, -90, 0.99], [-3.7, -20, 1.16], [-4.6, 47, 1.32], [-6.4, 172, 1.64], [-7.1, 242, 1.84]]
D_link = -157

E_mass = [[0], [62, 68, 69], [70, 72, 73], [73, 74, 88], [75, 84, 87], [62, 85], [0], [0], [642.8], [35]]
E_static = [[3.8, -1.4, 147], [5.1, -1.8, 137], [6.4, -2.1, 128], [2.8, -1.0, 155], [2.0, -0.8, 164]]
E_man = [[-0.8, -194, 0.96], [-1.5, -129, 1.18], [-1.7, -116, 1.22], [-2.6, -48, 1.4], [-4.2, 99, 1.9]]
E_link = -133


def cogcalc(masses, pos):
    mx = [aircraft_data[1]]
    m = [aircraft_data[0]]
    for posid, row in enumerate(masses):
        rowmass = 0
        for seat in row:
            rowmass += seat
        mx.append(rowmass*pos[posid])
        m.append(rowmass)
    cogpos = ((np.sum(mx)/np.sum(m)) - 5.149) * (100/1.717)
    return cogpos


def knts2ms(v):
    return v * 0.51444


def stickforce(pl, pspring):
    return 0.4 * 0.64 * (pl - pspring)


def cl(masses, v):
    top_load = 2 * (np.sum(np.sum(masses))+aircraft_data[0]) * g
    bottom_dyn = rho0 * knts2ms(v)**2 * Sw
    c_l = top_load/bottom_dyn
    return c_l


def matrix_static_stick_fixed(masses_list, data_list):
    # create empty matrix to fill
    m = np.matrix(np.zeros((25, 6)))
    m[:, 0] = 1
    eta = np.matrix(np.zeros((25, 1)))
    cog_list = []
    c_l_record = []
    angle_record = []
    gradient_record = []
    max_c_l = []
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(1, 1, 1)
    ax.xaxis.set_ticks_position('bottom')

    for data_id, masses in enumerate(masses_list):
        cog_list.append(cogcalc(masses, row_pos))
        c_l = []
        angle = []
        for test_id, test in enumerate(data_list[data_id]):
            eta[(5*data_id) + test_id] = test[1]
            m[(5*data_id) + test_id, data_id+1] = cl(masses, test[2])
            c_l.append(cl(masses, test[2]))
            angle.append(test[1])
        c_l_record.append(c_l)
        angle_record.append(angle)
    sol = np.dot(m.I, eta)
    print(m)
    print(eta)
    print("Solution")
    print(sol)

    #record gradients for backwards compat
    for gd in range(1, 6):
        gradient_record.append(sol[gd, 0])
    for data_id, masses in enumerate(masses_list):
        z = [gradient_record[data_id], sol[0, 0]]
        c_l = c_l_record[data_id]
        angle = angle_record[data_id]
        plt.plot(c_l, angle, point_bank[data_id % len(point_bank)],
                 label=r'$\eta$' + '=[' + str(format(z[0], '.3f')) + r'$C_L$' + ' + ' +
                       str(format(z[1], '.3f')) + ']  CoG: ' + str(format(cogcalc(masses, row_pos), '.2f')) +
                       '% ' + r'$\bar{c}$')
        lobf = np.poly1d(z)
        plt.plot([0, np.max(c_l)], [lobf(0), lobf(np.max(c_l))], 'k-')
        max_c_l.append(np.max(c_l))
    plt.xlabel(r'$C_L$')
    plt.ylabel('Elevator Angle (' + r'$\eta^\circ$' + ')')
    plt.legend(loc='lower left', shadow=True)
    plt.grid(True)
    step = 0.1
    end = step * (int(np.max(max_c_l)/step) + 2)
    print(end)
    ax.xaxis.set_ticks(np.arange(0, end, step))
    plt.xlim(0, end-step)
    plt.plot([0, end-step], [0, 0], 'k-')
    plt.title("Static Stability, Controls Fixed")
    plt.savefig('graphs/staticstabilityFixed.png')

    fig2 = plt.figure(figsize=(8, 6))
    ax = fig2.add_subplot(1, 1, 1)
    plt.plot(cog_list, gradient_record, 'ro')
    z1 = np.polyfit(cog_list, gradient_record, 1)
    lobf1 = np.poly1d(z1)
    # find x intercept
    x_int = (0 - z1[1]) / z1[0]
    print(x_int)
    plt.plot([np.min(cog_list), x_int + 2], [lobf1(np.min(cog_list)), lobf1(x_int + 2)], 'k-')
    plt.plot(x_int, 0, 'rx', label='Stick Fixed Neutral Point ' + r'$h_n$' + ' : ' + str(format(x_int, '.2f')) + '%')
    plt.xlabel('CoG % of ' + r'$\bar{c}$')
    plt.ylabel('Elevator Gradient (' + r'd$\eta$/d$C_L$' + ')')
    plt.legend(loc='lower right', shadow=True)
    plt.grid(True)
    step = 5
    start = step * (int(np.min(cog_list) / step) - 2)
    print(start)
    end = step * (int(x_int / step) + 2)
    print(end)
    ax.xaxis.set_ticks(np.arange(0, end, step))
    plt.xlim(start, end - step)
    plt.plot([start, end-step], [0, 0], 'k-')
    plt.title("Graph to Detirmine Neutral Point, Controls Fixed")
    plt.savefig('graphs/neutralpointStaticFixed.png')
    plt.show()

def matrix_static_stick_free(masses_list, data_list):
    # create empty matrix to fill
    m = np.matrix(np.zeros((25, 6)))
    m[:, 0] = 1
    eta = np.matrix(np.zeros((25, 1)))
    cog_list = []
    c_l_record = []
    angle_record = []
    gradient_record = []
    max_c_l = []
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(1, 1, 1)
    ax.xaxis.set_ticks_position('bottom')

    for data_id, masses in enumerate(masses_list):
        cog_list.append(cogcalc(masses, row_pos))
        c_l = []
        angle = []
        for test_id, test in enumerate(data_list[data_id]):
            eta[(5*data_id) + test_id] = test[0]
            m[(5*data_id) + test_id, data_id+1] = cl(masses, test[2])
            c_l.append(cl(masses, test[2]))
            angle.append(test[0])
        c_l_record.append(c_l)
        angle_record.append(angle)
    sol = np.dot(m.I, eta)
    print("Solution")
    print(sol)

    #record gradients for backwards compat
    for gd in range(1, 6):
        gradient_record.append(sol[gd, 0])
    for data_id, masses in enumerate(masses_list):
        z = [gradient_record[data_id], sol[0, 0]]
        c_l = c_l_record[data_id]
        angle = angle_record[data_id]
        plt.plot(c_l, angle, point_bank[data_id % len(point_bank)],
                 label=r'$\beta$' + '=[' + str(format(z[0], '.3f')) + r'$C_L$' + ' + ' +
                       str(format(z[1], '.3f')) + ']  CoG: ' + str(format(cogcalc(masses, row_pos), '.2f')) +
                       '% ' + r'$\bar{c}$')
        lobf = np.poly1d(z)
        plt.plot([0, np.max(c_l)], [lobf(0), lobf(np.max(c_l))], 'k-')
        max_c_l.append(np.max(c_l))
    plt.xlabel(r'$C_L$')
    plt.ylabel('Elevator Tab Angle (' + r'$\beta^\circ$' + ')')
    plt.legend(loc='upper left', shadow=True)
    plt.grid(True)
    step = 0.1
    end = step * (int(np.max(max_c_l)/step) + 2)
    print(end)
    ax.xaxis.set_ticks(np.arange(0, end, step))
    plt.xlim(0, end-step)
    plt.plot([0, end-step], [0, 0], 'k-')
    plt.title("Static Stability, Controls Free")
    plt.savefig('graphs/staticstabilityFree.png')

    fig2 = plt.figure(figsize=(8, 6))
    ax = fig2.add_subplot(1, 1, 1)
    plt.plot(cog_list, gradient_record, 'ro')
    z1 = np.polyfit(cog_list, gradient_record, 1)
    lobf1 = np.poly1d(z1)
    # find x intercept
    x_int = (0 - z1[1]) / z1[0]
    print(x_int)
    plt.plot([np.min(cog_list), x_int], [lobf1(np.min(cog_list)), 0], 'k-')
    plt.plot(x_int, 0, 'rx',
             label='Stick Free Neutral Point ' + r'$h^\prime_n $' + ' : ' + str(format(x_int, '.2f')) + '%')
    plt.xlabel('CoG % of ' + r'$\bar{c}$')
    plt.ylabel('Elevator Tab Gradient (' + r'd$\beta$/d$C_L$' + ')')
    plt.legend(loc='upper right', shadow=True)
    plt.grid(True)
    step = 5
    start = step * (int(np.min(cog_list) / step) - 2)
    print(start)
    end = step * (int(x_int / step) + 2)
    print(end)
    ax.xaxis.set_ticks(np.arange(0, end, step))
    plt.xlim(start, end - step)
    plt.plot([start, end-step], [0, 0], 'k-')
    plt.title("Graph to Detirmine Neutral Point, Controls Free")
    plt.savefig('graphs/neutralpointStaticFree.png')
    plt.show()


def matrix_man_stick_fixed(masses_list, data_list):
    # create empty matrix to fill
    m = np.matrix(np.zeros((25, 6)))
    m[:, 0] = 1
    eta = np.matrix(np.zeros((25, 1)))
    cog_list = []
    gee_record = []
    angle_record = []
    gradient_record = []
    max_gee = []
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(1, 1, 1)

    for data_id, masses in enumerate(masses_list):
        cog_list.append(cogcalc(masses, row_pos))
        gee = []
        angle = []
        for test_id, test in enumerate(data_list[data_id]):
            eta[(5*data_id) + test_id] = test[0]
            m[(5*data_id) + test_id, data_id+1] = test[2]
            gee.append(test[2])
            angle.append(test[0])
        gee_record.append(gee)
        angle_record.append(angle)
    sol = np.dot(m.I, eta)
    print("Solution")
    print(sol)

    #record gradients for backwards compat
    for gd in range(1, 6):
        gradient_record.append(sol[gd, 0])
    for data_id, masses in enumerate(masses_list):
        z = [gradient_record[data_id], sol[0, 0]]
        gee = gee_record[data_id]
        angle = angle_record[data_id]
        plt.plot(gee, angle, point_bank[data_id % len(point_bank)],
                 label=r'$\eta$' + '=[' + str(format(z[0], '.3f')) + 'g + ' +
                       str(format(z[1], '.3f')) + ']  CoG: ' + str(format(cogcalc(masses, row_pos), '.2f')) +
                       '% ' + r'$\bar{c}$')
        lobf = np.poly1d(z)
        plt.plot([0, np.max(gee)], [lobf(0), lobf(np.max(gee))], 'k-')
        max_gee.append(np.max(gee))
    plt.xlabel('Normal Acceleration (' + r'$n_z$' + ' g)')
    plt.ylabel('Elevator Angle (' + r'$\eta^\circ$' + ')')
    plt.legend(loc='lower left', shadow=True)
    plt.grid(True)
    step = 0.25
    end = step * (int(np.max(max_gee)/step) + 2)
    print(end)
    ax.xaxis.set_ticks(np.arange(0, end, step))
    plt.xlim(0, end-step)
    plt.plot([0, end-step], [0, 0], 'k-')
    plt.title("Manoeuvre Stability, Controls Fixed")
    plt.savefig('graphs/manstabilityFixed.png')

    fig2 = plt.figure(figsize=(8, 6))
    ax = fig2.add_subplot(1, 1, 1)
    plt.plot(cog_list, gradient_record, 'ro')
    z1 = np.polyfit(cog_list, gradient_record, 1)
    lobf1 = np.poly1d(z1)
    # find x intercept
    x_int = (0 - z1[1]) / z1[0]
    print(x_int)
    plt.plot([np.min(cog_list), x_int + 2], [lobf1(np.min(cog_list)), lobf1(x_int + 2)], 'k-')
    plt.plot(x_int, 0, 'rx', label='Stick Fixed Manoeuvre Point ' + r'$h_m$' + ' : ' + str(format(x_int, '.2f')) + '%')
    plt.xlabel('CoG % of ' + r'$\bar{c}$')
    plt.ylabel('Elevator Gradient (' + r'd$\eta$/d$n_z$' + ')')
    plt.legend(loc='lower right', shadow=True)
    plt.grid(True)
    step = 5
    start = step * (int(np.min(cog_list) / step) - 2)
    print(start)
    end = step * (int(x_int / step) + 2)
    print(end)
    ax.xaxis.set_ticks(np.arange(0, end, step))
    plt.xlim(start, end - step)
    plt.plot([start, end-step], [0, 0], 'k-')
    plt.title("Graph to Determine Manoeuvre Point, Controls Fixed")
    plt.savefig('graphs/manpointManFixed.png')
    plt.show()


def matrix_man_stick_free(masses_list, data_list, p_spring):
    # create empty matrix to fill
    m = np.matrix(np.zeros((25, 6)))
    m[:, 0] = 1
    eta = np.matrix(np.zeros((25, 1)))
    cog_list = []
    gee_record = []
    pn_record = []
    gradient_record = []
    max_gee = []
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(1, 1, 1)

    for data_id, masses in enumerate(masses_list):
        cog_list.append(cogcalc(masses, row_pos))
        gee = []
        pn = []
        for test_id, test in enumerate(data_list[data_id]):
            eta[(5*data_id) + test_id] = stickforce(test[1], p_spring[data_id])
            m[(5*data_id) + test_id, data_id+1] = test[2]
            gee.append(test[2])
            pn.append(stickforce(test[1], p_spring[data_id]))
        gee_record.append(gee)
        pn_record.append(pn)
    sol = np.dot(m.I, eta)
    print("Solution")
    print(sol)

    #record gradients for backwards compat
    for gd in range(1, 6):
        gradient_record.append(sol[gd, 0])
    for data_id, masses in enumerate(masses_list):
        z = [gradient_record[data_id], sol[0, 0]]
        gee = gee_record[data_id]
        pn = pn_record[data_id]
        plt.plot(gee, pn, point_bank[data_id % len(point_bank)],
                 label=r'$P_n$' + '=[' + str(format(z[0], '.3f')) + 'g + ' +
                       str(format(z[1], '.3f')) + ']  CoG: ' + str(format(cogcalc(masses, row_pos), '.2f')) +
                       '% ' + r'$\bar{c}$')
        lobf = np.poly1d(z)
        plt.plot([0, np.max(gee)], [lobf(0), lobf(np.max(gee))], 'k-')
        max_gee.append(np.max(gee))
        plt.xlabel('Normal Acceleration (' + r'$n_z$' + ' g)')
    plt.ylabel('Stick Force (' + r'$P_\eta$' + ' N)')
    plt.legend(loc='lower right', shadow=True)
    plt.grid(True)
    step = 0.25
    end = step * (int(np.max(max_gee)/step) + 2)
    print(end)
    ax.xaxis.set_ticks(np.arange(0, end, step))
    plt.xlim(0, end-step)
    plt.plot([0, end-step], [0, 0], 'k-')
    plt.title("Manoeuvre Stability, Controls Free")
    plt.savefig('graphs/manstabilityFree.png')

    fig2 = plt.figure(figsize=(8, 6))
    ax = fig2.add_subplot(1, 1, 1)
    plt.plot(cog_list, gradient_record, 'ro')
    z1 = np.polyfit(cog_list, gradient_record, 1)
    lobf1 = np.poly1d(z1)
    # find x intercept
    x_int = (0 - z1[1]) / z1[0]
    print("16% Stick Force: " + str(lobf1(16)))
    print("37% Stick Force: " + str(lobf1(37)))
    plt.plot([np.min(cog_list), x_int + 2], [lobf1(np.min(cog_list)), lobf1(x_int + 2)], 'k-')
    plt.plot(x_int, 0, 'rx',
             label='Stick Free Manoeuvre Point ' + r'$h^\prime_m$' + ' : ' + str(format(x_int, '.2f')) + '%')
    plt.xlabel('CoG % of ' + r'$\bar{c}$')
    plt.ylabel('Stick Force Gradient (' + r'd$P_\eta$/d$n_z$' + ')')
    plt.legend(loc='lower left', shadow=True)
    plt.grid(True)
    step = 5
    start = step * (int(np.min(cog_list) / step) - 2)
    print(start)
    end = step * (int(x_int / step) + 2)
    print(end)
    ax.xaxis.set_ticks(np.arange(0, end, step))
    plt.xlim(start, end - step)
    plt.plot([start, end-step], [0, 0], 'k-')
    plt.title("Graph to Determine Manoeuvre Point, Controls Free")
    plt.savefig('graphs/manpointManFree.png')
    plt.show()


matrix_static_stick_fixed([A_mass, B_mass, C_mass, D_mass, E_mass], [A_static, B_static, C_static, D_static, E_static])

matrix_static_stick_free([A_mass, B_mass, C_mass, D_mass, E_mass], [A_static, B_static, C_static, D_static, E_static])

matrix_man_stick_fixed([A_mass, B_mass, C_mass, D_mass, E_mass], [A_man, B_man, C_man, D_man, E_man])

matrix_man_stick_free([A_mass, B_mass, C_mass, D_mass, E_mass], [A_man, B_man, C_man, D_man, E_man], [A_link, B_link, C_link, D_link, E_link])
