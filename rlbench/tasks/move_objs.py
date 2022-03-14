import numpy as np
from typing import List
from rlbench.backend.task import Task
from rlbench.backend.conditions import ConditionSet, DetectedCondition
from pyrep.objects.dummy import Dummy
from pyrep.objects.proximity_sensor import ProximitySensor
from pyrep.objects.shape import Shape
from rlbench.backend.spawn_boundary import SpawnBoundary
from pyrep.objects.vision_sensor import VisionSensor

from rlbench.backend.task_utils import sample_model_objects

class MoveObjs(Task):

    def init_task(self) -> None:
        #self.large_container = Shape('large_container')
        self._camera = VisionSensor('camera')
        self._camera_mask = VisionSensor('mask')
        self.arm_boundary = SpawnBoundary([Shape('arm_boundary')])
        self.spawn_boundary = SpawnBoundary([Shape('spawn_boundary')])
        self.success_sensor = ProximitySensor('success')
        self.register_success_conditions(
            [DetectedCondition(self.robot.arm.get_tip(), self.success_sensor)])
        self.bin_objects = []

        self.wp0 = Dummy('waypoint0')
        self.wp1 = Dummy('waypoint1')
        self.wp2 = Dummy('waypoint2')
        self._camera.set_resolution((450,450))
        self._camera_mask.set_resolution((450,450))

    def init_episode(self, index: int) -> List[str]:
        obj_num = np.random.choice([2,3,4])
        print('sampling objects')
        self.bin_objects = sample_model_objects(self.get_base(), obj_num)
        print('Sampeld objects')
        self.spawn_boundary.clear()
        for i, ob in enumerate(self.bin_objects):
            ob_bounding_box = ob.get_model_bounding_box()
            ob_height = ob_bounding_box[-1]-ob_bounding_box[-2]
            ob.set_position(
                [0.0, 0.0, 0.01+ob_height/2.], relative_to=self.get_base(),
                reset_dynamics=True)
            print('sample boundary {}/{}'.format(i, len(self.bin_objects)))
            self.spawn_boundary.sample(
                ob, ignore_collisions=False, min_distance=0.2,
                min_rotation=(0, 0, -3.14), max_rotation=(0, 0, 3.14))

        push_dir = np.random.choice([1,2,3])#1:left;2:right;3:bottom
        obj_pos = np.stack([obj.get_position() for obj in self.bin_objects],axis=0)
        #obj_pos: 1~3-3
        height = self.get_base().get_position()[2]
        if push_dir == 1:           
            which_obj = np.argmin(obj_pos[:,0])
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
            rot = np.array([0.,0.,0.5])*np.pi
            self.wp0.rotate(rot)
            self.wp1.rotate(rot)
            self.wp2.rotate(rot)
        if push_dir == 3:
            which_obj = np.argmax(obj_pos[:,1])
            obj_to_push = obj_pos[which_obj]
            start_point = obj_to_push + np.array([0.,0.15,0.])
            end_point = obj_to_push - np.array([0.,0.1,0.])
            #height = obj_pos[which_obj][2]*0.8
            start_point[2] = height
            end_point[2] = height
            start_point_pre = start_point.copy()
            start_point_pre[2] = start_point_pre[2]+0.3
            self.wp0.set_position(start_point_pre)
            self.wp1.set_position(start_point)
            self.wp2.set_position(end_point)
            rot = np.array([0.,0.,-0.5])*np.pi
            self.wp0.rotate(rot)
            self.wp1.rotate(rot)
            self.wp2.rotate(rot)
        return ['blahblahblah']
        
    def variation_count(self) -> int:
        # TODO: The number of variations for this task.
        return 1

    def cleanup(self) -> None:
        [ob.remove() for ob in self.bin_objects if ob.still_exists()]
        self.bin_objects = []
