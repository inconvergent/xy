# -*- coding: utf-8 -*-

def get_paths(prefix, xmax, ymax, skip=0, steps=500, stride=1, scale=1, postfix='*.2obj'):

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

