# -*- coding: utf-8 -*-

from numpy import array
from numpy import row_stack

def get_paths_from_n_files(
    prefix, 
    xmax, 
    ymax, 
    skip=0, 
    steps=500, 
    stride=1,
    scale=1, 
    postfix='*.2obj'
  ):

  from dddUtils.ioOBJ import load_2d as load
  from dddUtils.ddd import order_edges
  from glob import glob

  p = []

  for fn in sorted(glob(prefix + postfix))[skip:steps:stride]:
    print(fn)
    data = load(fn)
    vertices = data['vertices']
    vertices *= scale
    vertices[:,0] *= xmax
    vertices[:,1] *= ymax
    edges = data['edges']
    _,v_ordered = order_edges(edges)
    p.append(vertices[v_ordered,:])

  return p

def get_tris_from_file(
    fn, 
    xmax, 
    ymax, 
    scale=1, 
    postfix='*.2obj',
    spatial_sort = True
  ):

  from dddUtils.ioOBJ import load_2d as load
  from dddUtils.ddd import get_mid_2d as get_mid
  from dddUtils.ddd import get_distinct_edges_from_tris

  data = load(fn)
  vertices = data['vertices']

  vertices -= get_mid(vertices)                                                                                                                                                                                                                                                      
  vertices *= scale                                                                                                                                                                                                                                                                  
  vertices += array([[0.5]*2])  
  vertices[:,0] *= xmax
  vertices[:,1] *= ymax

  faces = data['faces']

  edges = get_distinct_edges_from_tris(faces)
  paths  = [row_stack(p) for p in vertices[edges,:]]

  if spatial_sort:
    from dddUtils.ddd import spatial_sort as ssort
    return ssort(paths)
  else:
    return paths

