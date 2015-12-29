# -*- coding: utf-8 -*-

from numpy import array
from numpy import row_stack
from glob import glob

def get_bounding_box(xy):

  mi = xy.min(axis=0).squeeze()
  ma = xy.max(axis=0).squeeze()
  xd = ma[0]-mi[0]
  yd = ma[1]-mi[1]

  return mi, ma, xd, yd

def print_values(mi, ma, xd, yd):

  print('x: min {:0.08f} max {:0.08f} d {:0.08f}'.format(mi[0], ma[0], xd))
  print('y: min {:0.08f} max {:0.08f} d {:0.08f}'.format(mi[1], ma[1], yd))

def scale(xy):

  _,_,xd,yd = get_bounding_box(xy)
  xy/=max(xd,yd)

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

def get_paths_from_file(
    fn,
    smax,
    postfix='*.2obj',
    spatial_sort = True
  ):

  from dddUtils.ioOBJ import load_2d as load
  from dddUtils.ddd import get_mid_2d as get_mid

  data = load(fn)
  vertices = data['vertices']
  lines = data['lines']

  vertices -= get_mid(vertices)
  scale(vertices)
  vertices += array([[0.5]*2])
  vertices[:,:] *= smax

  print('scaled size:')
  print_values(*get_bounding_box(vertices))

  paths = [row_stack(vertices[l,:]) for l in lines]

  if spatial_sort:
    from dddUtils.ddd import spatial_sort_2d as sort
    return sort(paths)
  else:
    return paths

def get_tris_from_file(
    fn,
    smax,
    postfix='*.2obj',
    spatial_sort = True
  ):

  from dddUtils.ioOBJ import load_2d as load
  from dddUtils.ddd import get_mid_2d as get_mid
  from dddUtils.ddd import get_distinct_edges_from_tris

  data = load(fn)
  vertices = data['vertices']

  vertices -= get_mid(vertices)
  scale(vertices)
  vertices += array([[0.5]*2])
  vertices[:,:] *= smax

  print('scaled size:')
  print_values(*get_bounding_box(vertices))

  edges = get_distinct_edges_from_tris(data['faces'])
  paths = [row_stack(p) for p in vertices[edges,:]]

  if spatial_sort:
    from dddUtils.ddd import spatial_sort_2d as sort
    return sort(paths)
  else:
    return paths

