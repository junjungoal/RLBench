import os
import numpy as np
from pyrep.objects.shape import Shape
from pyrep.backend import sim, utils
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
        resp = Shape.import_mesh(respondable, scaling_factor=0.015)
        vis = Shape.import_mesh(visual, scaling_factor=0.015)
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

def sample_shapenet_objects(task_base, num_samples, mass=0.1):
    ttm_assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              '../assets/shapenet_ttm_refined/')
    # ttm_assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    #                           '../assets/shapenet_ttm_small/')

    filenames = []
    for root, dirs, files in os.walk(ttm_assets_dir):
        for filename in files:
            if filename.endswith('.ttm'): filenames.append(os.path.join(root, filename))
    samples = np.random.choice(
        filenames, num_samples, replace=False)
    created = []
    for s in samples:
        # print(s)
        # filename = s[62:-4]
        # if os.path.exists(os.path.join(ttm_assets_dir, filename+'.ttm')):
        print(s)
        resp = utils.to_type(sim.simLoadModel(s))
        # object_name = os.path.join(ttm_assets_dir, filename)
        # object_name = filename
        # visual_name = object_name +'_visual'
        # respondable = Shape(object_name)
        # visual = Shape(visual_name)
        resp.set_parent(task_base)
        created.append(resp)
    # else:
        #     resp = Shape.import_mesh(s, scaling_factor=0.8)
        #     resp = Shape.import_mesh(s, scaling_factor=0.8)
        #     resp = resp.get_convex_decomposition(use_vhacd=True,
        #                                          vhacd_hull_downsample=16,
        #                                          vhacd_plane_downsample=16,
        #                                          vhacd_alpha=0.15, vhacd_beta=0.15,
        #                                          vhacd_concavity=0.00001)
        #     resp.set_color(np.random.rand(3).tolist())
        #     vis = Shape.import_mesh(s, scaling_factor=0.8)
        #     vis.set_color(np.random.rand(3).tolist())
        #     resp.set_renderable(False)
        #     vis.set_renderable(True)
        #     vis.set_parent(resp)
        #     vis.set_dynamic(False)
        #     vis.set_respondable(False)
        #     resp.set_dynamic(True)
        #     resp.set_mass(mass)
        #     resp.set_respondable(True)
        #     resp.set_model(True)
        #     resp.set_parent(task_base)
        #
        #     created.append(resp)
        #
        #     new_filename = os.path.join(ttm_assets_dir, s[62:-4] + '.ttm')
        #     # new_vis_filename = os.path.join(ttm_assets_dir, filename[62:-4] + '_visual' + '.ttm')
        #     dirname = os.path.dirname(new_filename)
        #     if not os.path.exists(dirname):
        #         os.makedirs(dirname)
        #     resp.save_model(new_filename)
        #     # vis.save_model(new_vis_filename)
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
