import os
import numpy as np

colors = []
sizes = []

colors.append(np.array([124, 252, 0]))
colors.append(np.array([50, 205, 50]))
colors.append(np.array([34, 139, 34]))
colors.append(np.array([0, 100, 0]))
colors.append(np.array([173, 255, 47]))
colors.append(np.array([154, 205, 50]))
colors.append(np.array([144, 238, 144]))


# gray
colors.append(np.array([220, 220, 220]))
colors.append(np.array([192, 192, 192]))
colors.append(np.array([169, 169, 169]))
colors.append(np.array([128, 128, 128]))
colors.append(np.array([105, 105, 105]))

colors.append(np.array([0, 0, 0]))
colors.append(np.array([255, 255, 255]))

colors = np.array(colors) / 255.

for _ in range(100):
    # sizes.append(np.random.uniform(0.04, 0.1, size=3))
    sizes.append(np.random.uniform(0.04, 0.10, size=3))

np.save('green_gray_white_color.npy', colors)
np.save('green_gray_white_size.npy', sizes)
