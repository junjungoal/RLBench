import os
import numpy as np
from pyrep.objects.shape import Shape
from pyrep.backend import sim

def sample_procedural_objects(task_base, num_samples, mass=0.1):
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              '../assets/procedural_objects')
    samples = np.random.choice(
        os.listdir(assets_dir), num_samples, replace=False)
    created = []
    for s in samples:
        respondable = os.path.join(assets_dir, s, s + '_coll.obj')
        visual = os.path.join(assets_dir, s, s + '.obj')
        resp = Shape.import_mesh(respondable, scaling_factor=0.005)
        vis = Shape.import_mesh(visual, scaling_factor=0.005)
        resp.set_renderable(False)
        vis.set_renderable(True)
        vis.set_parent(resp)
        vis.set_dynamic(False)
        vis.set_respondable(False)
        resp.set_dynamic(True)
        resp.set_mass(mass)
        resp.set_respondable(True)
        resp.set_model(True)
        resp.set_parent(task_base)
        created.append(resp)
    return created

def sample_model_objects(task_base, num_samples):
    print('sampling function called')
    assets_dir = os.path.join(os.environ['COPPELIASIM_ROOT'],'models/ycb_grasp/')#objects/good_3d
    samples = np.random.choice(
        os.listdir(assets_dir), num_samples, replace=False)
    created = []
    print(samples)
    for s in samples:
        model_fn = os.path.join(assets_dir, s)
        print('loading')
        print(s)
        sim.simLoadModel(model_fn)
        print('loaded')
        object_name = s[:-4]
        visual_name = object_name +'_visual'
        print(object_name,visual_name)
        respondable = Shape(object_name)
        visual = Shape(visual_name)
        respondable.set_parent(task_base)
        created.append(respondable)
    return created

def get_model_objects(task_base, names):
    assets_dir = os.path.join(os.environ['COPPELIASIM_ROOT'],'models/objects/good_3d/')
    created = []
    for s in names:
        model_fn = os.path.join(assets_dir, s)
        sim.simLoadModel(model_fn)
        object_name = s[:-4]
        visual_name = object_name +'_visual'
        print(object_name,visual_name)
        respondable = Shape(object_name)
        visual = Shape(visual_name)
        respondable.set_parent(task_base)
        created.append(respondable)
    return created
