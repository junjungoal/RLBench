import os
import numpy as np
from pyrep.objects.shape import Shape
from pyrep.backend import sim
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
from tools.a3d.move_objs import LoadedTask

pr = PyRep()
ttt_file = '/home/jun/projects/RLBench/tools/a3d/move_objs_zoom.v4_wood.ttt'
pr.launch(ttt_file, responsive_ui=True)
pr.step_ui()
pr.set_simulation_timestep(0.005)
pr.step_ui()

ttm_assets_dir = 'rlbench/assets/shapenet_ttm/'

filenames = []
for root, dirs, files in os.walk(ttm_assets_dir):
    for filename in files:
        if filename.endswith('.ttm'): filenames.append(os.path.join(root, filename))
# samples = np.random.choice(
#     filenames, num_samples, replace=False)
created = []
for filename in filenames[10:]:
    print(filename)
    # filename = s[62:-4]
    # if os.path.exists(os.path.join(ttm_assets_dir, filename+'.ttm')):
    sim.simLoadModel(os.path.join(ttm_assets_dir, filename))
    # object_name = os.path.join(ttm_assets_dir, filename)
    object_name = filename
    visual_name = object_name +'_visual'
    respondable = Shape(object_name)
    visual = Shape(visual_name)
    respondable.set_parent(task_base)
    created.append(respondable)
