import numpy as np
import os, sys
import matplotlib.pyplot as plt
import cv2
from core.utils.video import save_video

d = '/home/jun/projects/RLBench/datasets/3D_data/P2D_cuboid.dr.pre.v7/raw1'
new_d = '/home/jun/Downloads/samples/'

filenames = []
for root, dirs, files in os.walk(d):
    for filename in files:
        if filename.endswith('.npy'): filenames.append(os.path.join(root, filename))

filenames = filenames[:30]

for filename in filenames:
    data = np.load(filename, allow_pickle=True)
    # data = np.load('/home/jun/projects/RLBench/datasets/3D_data/P2D3D2_light/raw/{}.npy'.format(data_id), allow_pickle=True)

    video = []
    for i, d in enumerate(data):
        video.append(d['rgb'])
        # plt.imsave('/home/jun/Downloads/samples/img_{}.png'.format(i), d['rgb'])

    new_filename = 'video_' + os.path.basename(filename)[:-3] + '.mp4'
    new_filename = os.path.join(new_d, new_filename)
    save_video(video, new_filename)

