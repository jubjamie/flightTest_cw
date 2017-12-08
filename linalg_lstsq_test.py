import numpy as np
import matplotlib.pyplot as plt
x = np.array([0, 2, 3, 4, 5])
y = np.array([1, 2, 2.8, 2.9, 3.6])

filler = np.empty(len(x))
filler.fill(1/1.5)

A = np.vstack([x, filler]).T
print(A)

m, c = np.linalg.lstsq(A, y)[0]
print(m, c)

plt.plot(x, y, 'o')
plt.plot(x, m*x + c, 'r')
plt.show()
