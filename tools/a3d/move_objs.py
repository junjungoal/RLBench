import os
import numpy as np
from os.path import join, dirname, abspath, isfile
import sys
import traceback

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

CURRENT_DIR = dirname(abspath(__file__))


def print_fail(message, end='\n'):
    message = str(message)
    sys.stderr.write('\x1b[1;31m' + message.strip() + '\x1b[0m' + end)


class LoadedTask(object):

    def __init__(self, pr: PyRep, scene: Scene, robot: Robot):
        self.pr = pr
        self.scene = scene
        self.robot = robot
        self.task = self.task_class = self.task_file = None
        self._variation_index = 0

    def _load_task_to_scene(self):
        self.scene.unload()
        self.task = self.task_class(self.pr, self.robot)  # task constructor
        try:
            # Try and load the task
            scene.load(self.task)
        except FileNotFoundError as e:
            # The .ttt file must not exist
            handle = Dummy.create()
            handle.set_name(self.task_file.replace('.py', ''))
            handle.set_model(True)
            # Put the dummy at the centre of the workspace
            self.task.get_base().set_position(Shape('workspace').get_position())

    def _edit_new_task(self):
        task_file = input('What task would you like to edit?\n')
        if len(task_file) > 3 and task_file[-3:] != '.py':
            task_file += '.py'
        try:
            task_class = name_to_task_class(task_file)
        except:
            print('There was no task named: %s. '
                  'Would you like to create it?' % task_file)
            inp = input()
            if inp == 'y':
                self._create_python_file(task_file)
                task_class = name_to_task_class(task_file)
            else:
                print('Pick a defined task in that case...')
                task_class, task_file = self._edit_new_task()
        return task_class, task_file

    def _create_python_file(self, task_file: str):
        with open(join(CURRENT_DIR, '../assets', 'task_template.txt'), 'r') as f:
            file_content = f.read()
        class_name = self._file_to_class_name(task_file)
        file_content = file_content % (class_name,)
        new_file_path = join(CURRENT_DIR, '../../rlbench/tasks', task_file)
        if isfile(new_file_path):
            raise RuntimeError('File already exists. Will not override this.')
        with open(new_file_path, 'w+') as f:
            f.write(file_content)

    def _file_to_class_name(self, name):
        name = name.replace('.py', '')
        return ''.join([w[0].upper() + w[1:] for w in name.split('_')])

    def reload_python(self):
        try:
            task_class = name_to_task_class(self.task_file)
        except Exception as e:
            print_fail('The python file could not be loaded!')
            traceback.print_exc()
            return None, None
        self.task = task_class(self.pr, self.robot)  # task constructor
        self.scene.load(self.task)

    def new_task(self):
        self._variation_index = 0
        self.task_class, self.task_file = self._edit_new_task()
        self._load_task_to_scene()
        self.pr.step_ui()
        print('You are now editing: %s' % str(self.task_class))

    def reset_variation(self):
        self._variation_index = 0

    def new_variation(self):
        try:
            self._variation_index += 1
            descriptions = self.scene.init_episode(
                self._variation_index % self.task.variation_count())
            print('Task descriptions: ', descriptions)
        except (WaypointError, BoundaryError, Exception) as ex:
            traceback.print_exc()
        self.pr.step_ui()

    def new_episode(self):
        try:
            descriptions = self.scene.init_episode(
                self._variation_index % self.task.variation_count(),
                max_attempts=1)
            print('Task descriptions: ', descriptions)
        except (WaypointError, BoundaryError, Exception) as ex:
            traceback.print_exc()
            self.scene.reset()
        self.pr.step_ui()

    def new_demo(self):
        success = False
        try:
            demo=self.scene.get_demo(True, randomly_place=False)
            success = True
        except (WaypointError, NoWaypointsError, DemoError, Exception) as e:
            traceback.print_exc()
            success = False
        #success, terminate = self.task.success()
        #success=True
        if success:
            indx_num=len(os.listdir('/home/jun/projects/RLBench/datasets/3D_data/P2D3D2/raw'))
            np.save('/home/jun/projects/RLBench/datasets/3D_data/P2D3D2/raw/{}.npy'.format(indx_num),demo)
        
        self.scene.reset()
        self.pr.step_ui()
        self.pr.step_ui()

    def save_task(self):
        ttm_path = join(CURRENT_DIR, '../rlbench/task_ttms',
                        self.task_file.replace('.py', '.ttm'))
        self.task.get_base().save_model(ttm_path)
        print('Task saved to:', ttm_path)

    def run_task_validator(self):
        print('About to perform task validation.')
        print("What variation to test? Pick int in range: 0 to %d, or -1 to "
              "test all. Or press 'e' to exit."
              % self.task.variation_count())
        inp = input()
        if inp == 'e':
            return
        self.pr.start()
        try:
            v = int(inp)
            v = v if v < 0 else v % self.task.variation_count()
            task_smoke(self.task, self.scene, variation=v)
        except TaskValidationError as e:
            traceback.print_exc()
        self.pr.stop()

    def rename(self):
        print('Enter new name (or q to abort).')
        inp = input()
        if inp == 'q':
            return

        name = inp.replace('.py', '')
        python_file = name + '.py'

        # Change name of base
        handle = Dummy(self.task_file.replace('.py', ''))
        handle.set_name(name)

        # Change the class name
        old_file_path = join(CURRENT_DIR, '../rlbench/tasks', self.task_file)
        old_class_name = self._file_to_class_name(self.task_file)
        new_class_name = self._file_to_class_name(name)
        with open(old_file_path, 'r') as f:
            content = f.read()
        content = content.replace(old_class_name, new_class_name)
        with open(old_file_path, 'w') as f:
            f.write(content)

        # Rename python task file
        new_file_path = join(CURRENT_DIR, '../rlbench/tasks', python_file)
        os.rename(old_file_path, new_file_path)

        # Rename .ttt
        old_ttm_path = join(CURRENT_DIR, '../rlbench/task_ttms',
                        self.task_file.replace('.py', '.ttm'))
        new_ttm_path = join(CURRENT_DIR, '../rlbench/task_ttms',
                            python_file.replace('.py', '.ttm'))
        os.rename(old_ttm_path, new_ttm_path)

        self.task_file = python_file
        self.reload_python()
        self.save_task()
        print('Rename complete')


if __name__ == '__main__':

    pr = PyRep()
    ttt_file = '/home/jun/projects/RLBench/tools/a3d/move_objs.ttt'#join(CURRENT_DIR, TTT_FILE)
    pr.launch(ttt_file, responsive_ui=True)
    pr.step_ui()
    pr.set_simulation_timestep(0.005)
    pr.step_ui()

    robot = Robot(Panda(), PandaGripper())
    #cam_config = CameraConfig(rgb=True, depth=False, mask=False,
                              #render_mode=RenderMode.OPENGL)
    cam_config = CameraConfig(image_size=(450, 450))
    obs_config = ObservationConfig(cam_config)
    #obs_config.set_all(False)
    #obs_config.right_shoulder_camera = cam_config
    #obs_config.left_shoulder_camera = cam_config
    #obs_config.wrist_camera = cam_config

    scene = Scene(pr, robot, obs_config)
    loaded_task = LoadedTask(pr, scene, robot)

    print('  ,')
    print(' /(  ___________')
    print('|  >:===========`  Welcome to task builder!')
    print(' )(')
    print(' ""')

    loaded_task.new_task()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\n-----------------\n')
        print('The python file will be reloaded when simulation is restarted.')
        print('(q) to quit.')
        if pr.running:
            print('(+) stop the simulator')
            print('(v) for task variation.')
            print('(e) for episode of same variation.')
            print('(d) for demo.')
            print('(p) for running the sim for 100 steps.')
        else:
            print('(!) to run task validator.')
            print('(+) run the simulator')
            print('(n) for new task.')
            print('(s) to save the .ttm')
            print('(r) to rename the task')

        inp = input()

        if inp == 'q':
            break

        if pr.running:
            if inp == '+':
                pr.stop()
                pr.step_ui()
            elif inp == 'p':
                [pr.step() for _ in range(100)]
            elif inp == 'd':
                for i in range(2000):
                    loaded_task.new_demo()
            elif inp == 'v':
                loaded_task.new_variation()
            elif inp == 'e':
                loaded_task.new_episode()
        else:
            if inp == '+':
                loaded_task.reload_python()
                loaded_task.reset_variation()
                pr.start()
                pr.step_ui()
            elif inp == 'n':
                inp = input('Do you want to save the current task first?\n')
                if inp == 'y':
                    loaded_task.save_task()
                loaded_task.new_task()
            elif inp == 's':
                loaded_task.save_task()
            elif inp == '!':
                loaded_task.run_task_validator()
            elif inp == 'r':
                loaded_task.rename()

    pr.stop()
    pr.shutdown()
    print('Done. Goodbye!')
