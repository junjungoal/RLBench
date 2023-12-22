import numpy as np

colors = []
sizes = []

for _ in range(1500):
    colors.append(np.random.uniform(0, 1, size=3))
    sizes.append(np.random.uniform(0.04, 0.1, size=3))

np.save('color5.npy', np.array(colors))
np.save('size5.npy', np.array(sizes))
