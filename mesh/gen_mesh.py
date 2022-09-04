#!/usr/bin/python3

import gmsh
import numpy as np
from scipy.spatial.transform import Rotation as Rotation
import sys

gmsh.initialize()
gmsh.option.setNumber("Mesh.MshFileVersion", 2)

def windTunnel(length, height, lc):
  p1 = gmsh.model.geo.addPoint(length/2, -height/2, 0,lc)
  p2 = gmsh.model.geo.addPoint(length/2, height/2, 0,lc)
  p3 = gmsh.model.geo.addPoint(-length/2, height/2, 0,lc)
  p4 = gmsh.model.geo.addPoint(-length/2, -height/2, 0,lc)

  l1 = gmsh.model.geo.addLine(p1, p2)
  l2 = gmsh.model.geo.addLine(p2, p3)
  l3 = gmsh.model.geo.addLine(p3, p4)
  l4 = gmsh.model.geo.addLine(p4, p1)

  l_loop = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])

  return l_loop

def foil(fname, scale, pos, aoa):
  foil = open(fname, 'r')
  lc = 0.1
  points = []

  dx = pos[0]
  dy = pos[1]

  rot_axis = np.array([0,0,1])
  rot_rad = np.radians(aoa)
  rot_vector = rot_axis * rot_rad
  rot = Rotation.from_rotvec(rot_vector)

  for line in foil:
    p_str = line.strip().split(" ")
    point = [scale*float(p_str[0]), scale*float(p_str[1]), 0]

    point = rot.apply(point)
    
    gp = gmsh.model.geo.add_point(point[0]+dx, point[1]+dy, point[2], lc)
    points.append(gp)
   
  spline = gmsh.model.geo.addSpline(points + [points[0]])


  l_loop = gmsh.model.geo.addCurveLoop([spline])

  return l_loop
 
  
awa = -35
mainSailPos = [0,0,0]
headSailPos = [-6,0,0]

rot_axis = np.array([0,0,1])
rot_rad = np.radians(awa)
rot_vector = rot_axis * rot_rad
rot = Rotation.from_rotvec(rot_vector)
mainSailPos = rot.apply(mainSailPos)
headSailPos = rot.apply(headSailPos)

wTunnel = windTunnel(80,50, 1.0)
mainSail = foil('mesh/foil.dat',scale=6.22, pos=mainSailPos, aoa=awa+8)
headSail = foil('mesh/headsail.dat',scale=6.20, pos=headSailPos, aoa=awa+15)

sur_setup = gmsh.model.geo.addPlaneSurface([wTunnel,mainSail, headSail])

#addPlaneSurface returns the surface tag; extrude takes a list of (dim, tag) pairs as input. This is why (2,sur_setup)
#numElements=[1] is like Layers{1} in Extrude
ids = gmsh.model.geo.extrude([(2,sur_setup)], 0, 0, 10, numElements=[1], recombine=True)
print("IDS:", ids)

gmsh.model.geo.addPhysicalGroup(3, [ ids[1][1] ], name="volume")
gmsh.model.geo.addPhysicalGroup(2, [ ids[0][1], sur_setup ], name="frontAndBack")
gmsh.model.geo.addPhysicalGroup(2, [ ids[2][1] ], name="outlet")
gmsh.model.geo.addPhysicalGroup(2, [ ids[3][1], ids[5][1] ], name="walls")
gmsh.model.geo.addPhysicalGroup(2, [ ids[4][1] ], name="inlet")
gmsh.model.geo.addPhysicalGroup(2, [ ids[6][1] ], name="mainsail")
gmsh.model.geo.addPhysicalGroup(2, [ ids[7][1] ], name="headsail")


# Create the relevant Gmsh data structures 
# from Gmsh model.
gmsh.model.geo.synchronize()
  
  
# Creates  graphical user interface
 
if "-mesh" not in sys.argv:
  gmsh.fltk.run()
else:
  # Generate mesh:
  gmsh.model.mesh.generate(dim=3)
  
  # Write mesh data:
  gmsh.write("main.msh")

# It finalize the Gmsh API
gmsh.finalize()

