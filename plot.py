from main import Bundles, np
from matplotlib import pyplot as plt  # require this!

bundle = Bundles([
    (1, 564),
    (2, 540),
    (3, 504),
    (4, 491),
    (8, 472),
])

xx = range(3, 100)
prices = np.fromiter(map(bundle.solve, xx), int)

plt.figure()
plt.plot(xx, prices)
plt.grid('y')
plt.xlabel('total amount')
plt.ylabel('average price')
plt.show()
