import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from vpython import *

def run():
    file = 'accelerations.csv'
    df = pd.read_csv(file, header=None)
    data = df.to_numpy()

    # intervalos de tiempo
    dt = 1 / 60 # segundos
    t = np.cumsum(np.full(len(data), dt, dtype=np.float64))

    # calcular velocidades
    vx = [0]
    vy = [0]
    vz = [0]

    for i in np.arange(len(data) - 1):
        vx = vx + [vx[-1] + data[i][0]*dt]
        vy = vy + [vy[-1] + data[i][1]*dt]
        vz = vz + [vz[-1] + data[i][2]*dt]

    # plt.plot(t, vx, label='vx')
    # plt.plot(t, vy, label='vy')
    # plt.plot(t, vz, label='vz')

    # plt.xlabel('t (s)')
    # plt.ylabel('v (m/s)')

    # plt.legend()
    # plt.grid()
    # plt.show()

    # calcular posiciones
    x = [0]
    y = [0]
    z = [0]

    for i in np.arange(len(data) - 1):
        x = x + [x[-1] + vx[i]*dt]
        y = y + [y[-1] + vy[i]*dt]
        z = z + [z[-1] + vz[i]*dt]

    # print(x[:10], y[:10], z[:10])
    # print(t[:10])

    # plt.plot(t, x, label='x')
    # plt.plot(t, y, label='y')
    # plt.plot(t, z, label='z')

    # plt.xlabel('t (s)')
    # plt.ylabel('r (m)')

    # plt.legend()
    # plt.grid()
    # plt.show()

    plane = sphere(pos=vector(0, 0, 0), radius=5, color=color.yellow, make_trail=True)
    
    for i in range(len(t)):
        rate(100)
        plane.pos = vector(x[i], y[i], z[i])



if __name__ == '__main__':
    run()