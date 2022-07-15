import os
import numpy as np
import tqdm
from pyrep.objects.shape import Shape
from pyrep.const import RenderMode

from rlbench.backend.const import TTT_FILE
from pyrep import PyRep
from pyrep.robots.arms.panda import Panda
from pyrep.objects.shape import Shape
from pyrep.objects.dummy import Dummy
from pyrep.robots.end_effectors.panda_gripper import PandaGripper
from rlbench.backend.scene import Scene_reach as Scene
from rlbench.backend.exceptions import *
from rlbench.observation_config import ObservationConfig_min as ObservationConfig
from rlbench.observation_config import CameraConfig_min as CameraConfig
from rlbench.backend.robot import Robot
from rlbench.utils import name_to_task_class
from tools.task_validator import task_smoke, TaskValidationError

pr = PyRep()
ttt_file = '/home/jun/projects/RLBench/tools/a3d/move_objs_zoom.v7_wood.ttt'
pr.launch(ttt_file, responsive_ui=True)
pr.step_ui()
pr.set_simulation_timestep(0.005)
pr.step_ui()

assets_dir = os.path.join('./rlbench/assets/shapenet')
assets_base_dir = os.path.join('./rlbench/assets/shapenet_ttm_refined')
assets_new_dir = os.path.join('./rlbench/assets/shapenet_ttm_small')

filenames = []
for root, dirs, files in os.walk(assets_base_dir):
    for filename in files:
        if filename.endswith('.ttm'):
            filenames.append(os.path.join(root.replace('shapenet_ttm_refined', 'shapenet'), filename.replace('ttm', 'obj')))
created = []

mass = 0.15
# for filename in tqdm.tqdm(filenames[::-1]):
# for filename in tqdm.tqdm(filenames[(len(filenames)//2):]):
for filename in tqdm.tqdm(filenames):
    print(filename)
    new_filename = os.path.join(assets_new_dir, filename[26:-4] + '.ttm')
    # new_vis_filename = os.path.join(assets_new_dir, filename[26:-4] + '_visual' + '.ttm')
    if not os.path.exists(new_filename):
        # color = np.random.rand(3).tolist()
        resp = Shape.import_mesh(filename, scaling_factor=0.7)
        resp = resp.get_convex_decomposition(use_vhacd=True,
                                             vhacd_hull_downsample=16,
                                             vhacd_plane_downsample=16,
                                             vhacd_alpha=0.15, vhacd_beta=0.15,
                                             vhacd_concavity=0.00001)
        vis = Shape.import_mesh(filename, scaling_factor=0.82)
        # resp.set_name(os.path.basename(filename)[:-4])
        # vis.set_name(os.path.basename(filename)[:-4]+'_vis')
        resp.set_renderable(False)
        resp.set_transparency(0)
        vis.set_renderable(True)
        vis.set_parent(resp)
        vis.set_dynamic(False)
        vis.set_respondable(False)
        resp.set_dynamic(True)
        resp.set_mass(mass)
        resp.set_respondable(True)
        resp.set_model(True)

        dirname = os.path.dirname(new_filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        resp.save_model(new_filename)
        # pr.step_ui()
        # pr.set_simulation_timestep(0.005)
        # pr.step_ui()
        resp.remove()
        # vis.save_model(new_vis_filename)
