import numpy as np
import matplotlib.pyplot as plt
x = np.array([0, 2, 3, 4, 5])
y = np.array([1, 2, 2.8, 2.9, 3.6])

A = np.vstack([x, np.ones(len(x))])

m, c = np.linalg.lstsq(A, y)[0]
print(m, c)

plt.plot(x, y, 'o')
plt.plot(x, m*x + c, 'r')
plt.show