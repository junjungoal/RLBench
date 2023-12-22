import numpy as np
import random
import copy
from typing import List
from rlbench.backend.task import Task
from rlbench.backend.conditions import ConditionSet, DetectedCondition
from pyrep.objects.dummy import Dummy
from pyrep.objects.proximity_sensor import ProximitySensor
from pyrep.objects.shape import Shape
from rlbench.backend.spawn_boundary import SpawnBoundary
from rlbench.backend.task_utils import sample_procedural_objects, sample_shapenet_objects
from pyrep.objects.vision_sensor import VisionSensor
from pyrep.objects.light import Light
from pyrep.objects.shape import Shape
from pyrep.const import RenderMode, PrimitiveShape
from pyrep.const import ObjectType, JointMode

from rlbench.backend.task_utils import sample_model_objects

class MoveObjs(Task):

    def init_task(self) -> None:
        #self.large_container = Shape('large_container')
        self._camera = VisionSensor('camera')
        self._camera_mask = VisionSensor('mask')
        # self._camera.set_render_mode(RenderMode.OPENGL3)
        self.arm_boundary = SpawnBoundary([Shape('arm_boundary')])
        self.spawn_boundary = SpawnBoundary([Shape('spawn_boundary')])
        self.success_sensor = ProximitySensor('success')
        self.register_success_conditions(
            [DetectedCondition(self.robot.arm.get_tip(), self.success_sensor)])
        self.bin_objects = []

        self._camera_position = self._camera.get_position()


        self.wp0 = Dummy('waypoint0')
        self.wp1 = Dummy('waypoint1')
        self.wp2 = Dummy('waypoint2')
        self._camera.set_resolution((128,128))
        self._camera_mask.set_resolution((128,128))

        self.lightA = Light('DefaultLightA')
        self.lightB = Light('DefaultLightB')
        self.lightC = Light('DefaultLightC')
        self.lightD = Light('DefaultLightD')

        self.colors = []
        self.sizes = []

        self.synthetic_colors = np.load('green_gray_white_color.npy')
        # self.synthetic_sizes = np.load('green_gray_size.npy')
        self.colors = np.load('color5.npy')
        self.sizes = np.load('size5.npy')
        # self.colors = np.load('color2.npy')
        # self.sizes = np.load('size2.npy')

        # self.colors = self.synthetic_colors
        # self.colors = np.concatenate([self.colors, self.synthetic_colors, self.synthetic_colors])
        self.colors = np.concatenate([self.colors, self.synthetic_colors])

        # self.arm_color_randamized_indices = [0, 1, 2, 4, 5, 8]
        self.arm_color_randamized_indices = [0, 1, 2, 4, 5, 8]

        self.random_diffuse = np.array([0.1, 0.2, 0.3, 0.4])

        self.robot_colors = [
            [0.6, 0.6, 0.6],
            [0.7, 0.7, 0.7],
            [0.8, 0.8, 0.8],
            [0.9, 0.9, 0.9],
            [0.9800000190734863, 0.9800000190734863, 0.9800000190734863],
            [1., 1., 1.],
        ]
        # self.colors = self.synthetic_colors


    def randomize_robot_color(self):
        arm_visuals = self.robot.arm.get_visuals()
        color = random.choice(self.robot_colors)
        for i, arm_visual in enumerate(arm_visuals):
            if i in self.arm_color_randamized_indices:
                arm_visual.set_color(color)

    def init_episode(self, index: int) -> List[str]:
        # self.randomize_robot_color()

        # new_camera_position = copy.deepcopy(self._camera_position) + np.random.uniform([-0.02, -0.05, -0.05], [0.05, 0.05, 0.05])
        # self._camera.set_position(new_camera_position)
        # self.lightA.turn_on()
        # self.lightB.turn_on()
        # self.lightC.turn_off()
        # self.lightD.turn_off()


        # diffuse_coeff = np.random.choice(self.random_diffuse)
        # diffuse_coeff = np.random.uniform(low=0.1, high=0.5, size=1)[0]
        # diffuse = np.ones(3) * diffuse_coeff
        # diffuse = np.ones(3) * 0.3
        # diffuse = np.ones(3) * 0.6
        # self.lightA.set_diffuse(diffuse)
        # self.lightB.set_diffuse(diffuse)
        # self.lightC.set_diffuse(diffuse)
        # self.lightD.set_diffuse(diffuse)

        #
        # if np.random.random() < 1.0:
        # # if np.random.random() < 0.25:
        # # if np.random.random() < 0.5:
        #     self.lightA.turn_on()
        #     # diffuse = (np.random.randint(2, 6) * 0.1) * np.ones(3)
        #     # diffuse = np.random.uniform(low=0.2, high=0.5, size=1)[0] * np.ones(3)
        #     diffuse = np.ones(3) * 0.35
        #     self.lightA.set_diffuse(diffuse)
        #     # self.lightA.set_specular(np.random.uniform(low=0.2, high=0.5, size=3))
        #     self.lightB.turn_off()
        #     self.lightC.turn_off()
        #     self.lightD.turn_off()
        # elif np.random.random() >= 0.25 and np.random.random() <0.5:
        # # if np.random.random() < 0.5:
        #     diffuse = np.ones(3) * 0.5
        #     self.lightB.turn_on()
        #     # diffuse = np.random.uniform(low=0.1, high=0.7, size=1)[0] * np.ones(3)
        #     self.lightB.set_diffuse(diffuse)
        #     self.lightB.set_specular(np.random.uniform(low=0.2, high=0.5, size=3))
        #     self.lightA.turn_off()
        #     self.lightC.turn_off()
        #     self.lightD.turn_off()
        # elif np.random.random() >= 0.5 and np.random.random() <0.75:
        # # if np.random.random() < 0.5:
        #     self.lightC.turn_on()
        #     # diffuse = np.random.uniform(low=0.1, high=0.7, size=1)[0] * np.ones(3)
        #     diffuse = np.ones(3) * 0.5
        #     self.lightC.set_diffuse(diffuse)
        #     self.lightC.set_specular(np.random.uniform(low=0.2, high=0.5, size=3))
        #     self.lightA.turn_off()
        #     self.lightB.turn_off()
        #     self.lightD.turn_off()
        # else:
        # # if np.random.random() < 0.5:
        #     self.lightD.turn_on()
        #     # diffuse = np.random.uniform(low=0.1, high=0.7, size=1)[0] * np.ones(3)
        #     diffuse = np.ones(3) * 0.5
        #     self.lightD.set_diffuse(diffuse)
        #     self.lightD.set_specular(np.random.uniform(low=0.2, high=0.5, size=3))
        #     self.lightA.turn_off()
        #     self.lightB.turn_off()
        #     self.lightC.turn_off()

        obj_num = np.random.choice([2,3,4])
        # self.bin_objects = sample_model_objects(self.get_base(), obj_num)
        # self.bin_objects = sample_procedural_objects(self.get_base(), obj_num)
        # self.bin_objects = sample_shapenet_objects(self.get_base(), obj_num)
        self.bin_objects = []
        for _ in range(obj_num):
            shapes = [PrimitiveShape.CUBOID]
            # obj = Shape.create(random.choice(shapes),size=np.random.uniform(0.05, 0.12, size=3).tolist(), color=np.random.uniform(0, 1, size=3).tolist())
            color_id = np.random.randint(len(self.colors))
            size_id = np.random.randint(len(self.sizes))
            obj = Shape.create(random.choice(shapes),size=self.sizes[size_id].tolist(), color=self.colors[color_id].tolist())
            obj.set_model(True)
            self.bin_objects.append(obj)

        self.spawn_boundary.clear()
        for i, ob in enumerate(self.bin_objects):
            ob_bounding_box = ob.get_model_bounding_box()
            ob_height = ob_bounding_box[-1]-ob_bounding_box[-2]
            ob.set_position(
                [0.0, 0.0, 0.01+ob_height/2.], relative_to=self.get_base(),
                reset_dynamics=True)
            self.spawn_boundary.sample(
                ob, ignore_collisions=False, min_distance=0.2,
                min_rotation=(0, 0, -3.14), max_rotation=(0, 0, 3.14))

        # push_dir = np.random.choice([1,2,3, 4])#1:left;2:right;3:bottom
        # push_dir = np.random.choice([5])#1:left;2:right;3:bottom
        push_dir = np.random.choice([4])#1:left;2:right;3:bottom
        obj_pos = np.stack([obj.get_position() for obj in self.bin_objects],axis=0)
        #obj_pos: 1~3-3
        height = self.get_base().get_position()[2]
        if push_dir == 1:
            # which_obj = np.argmin(obj_pos[:,0])
            which_obj = np.random.randint(len(self.bin_objects))
            obj_to_push = obj_pos[which_obj]
            start_point = obj_to_push - np.array([0.15,0.,0.])
            end_point = obj_to_push + np.array([0.1,0.,0.])
            #height = obj_pos[which_obj][2]*0.8
            start_point[2] = height
            end_point[2] = height
            start_point_pre = start_point.copy()
            start_point_pre[2] = start_point_pre[2]+0.3
            self.wp0.set_position(start_point_pre)
            self.wp1.set_position(start_point)
            self.wp2.set_position(end_point)
        if push_dir == 2:
            which_obj = np.argmin(obj_pos[:,1])
            obj_to_push = obj_pos[which_obj]
            start_point = obj_to_push - np.array([0.,0.15,0.])
            end_point = obj_to_push + np.array([0.,0.1,0.])
            #height = obj_pos[which_obj][2]*0.8
            start_point[2] = height
            end_point[2] = height
            start_point_pre = start_point.copy()
            start_point_pre[2] = start_point_pre[2]+0.3
            self.wp0.set_position(start_point_pre)
            self.wp1.set_position(start_point)
            self.wp2.set_position(end_point)
            # rot = np.array([0.,0.,0.5])*np.pi
            # self.wp0.rotate(rot)
            # self.wp1.rotate(rot)
            # self.wp2.rotate(rot)
        if push_dir == 3:
            which_obj = np.argmax(obj_pos[:,1])
            obj_to_push = obj_pos[which_obj]
            start_point = obj_to_push + np.array([0.,0.15,0.])
            end_point = obj_to_push - np.array([0.,0.1,0.])
            start_point[2] = height
            end_point[2] = height
            start_point_pre = start_point.copy()
            start_point_pre[2] = start_point_pre[2]+0.3
            self.wp0.set_position(start_point_pre)
            self.wp1.set_position(start_point)
            self.wp2.set_position(end_point)
            # rot = np.array([0.,0.,-0.5])*np.pi
            # self.wp0.rotate(rot)
            # self.wp1.rotate(rot)
            # self.wp2.rotate(rot)

        if push_dir == 4:
            y_coord = np.random.uniform(self.spawn_boundary._boundaries[0]._boundary_bbox.min_y-0.2,
                                        self.spawn_boundary._boundaries[0]._boundary_bbox.max_y+0.2, size=1)[0]
            start_point = np.array([0.05, y_coord, 0.])
            end_point = start_point + np.array([0.4, 0, 0.])
            start_point[2] = height
            end_point[2] = height
            start_point_pre = start_point.copy()
            start_point_pre[2] = start_point_pre[2]+0.3
            self.wp0.set_position(start_point_pre)
            self.wp1.set_position(start_point)
            self.wp2.set_position(end_point)

        # if push_dir == 5:
        #     x_coord = np.random.uniform(self.spawn_boundary._boundaries[0]._boundary_bbox.min_x+0.1,
        #                                 self.spawn_boundary._boundaries[0]._boundary_bbox.max_x-0.1, size=1)[0]
        #     start_point = np.array([x_coord, 0.4, 0.])
        #     end_point = start_point + np.array([0., -0.7, 0.])
        #     start_point[2] = height
        #     end_point[2] = height
        #     start_point_pre = start_point.copy()
        #     start_point_pre[2] = start_point_pre[2]+0.3
        #     self.wp0.set_position(start_point_pre)
        #     self.wp1.set_position(start_point)
        #     self.wp2.set_position(end_point)

        return ['blahblahblah']
        
    def variation_count(self) -> int:
        # TODO: The number of variations for this task.
        return 1

    def cleanup(self) -> None:
        [ob.remove() for ob in self.bin_objects if ob.still_exists()]
        self.bin_objects = []
