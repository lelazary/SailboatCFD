#!/usr/bin/python3

import gmsh
import numpy as np
from scipy.spatial.transform import Rotation as Rotation
import sys

gmsh.initialize()


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

def foil(fname, scale, dx, dy, aoa):
  foil = open(fname, 'r')
  lc = 0.1
  points = []

  rot_axis = np.array([0,0,1])
  rot_rad = np.radians(aoa)
  rot_vector = rot_axis * rot_rad
  rot = Rotation.from_rotvec(rot_vector)

  for line in foil:
    p_str = line.strip().split(" ")
    point = [scale*float(p_str[0]), scale*float(p_str[1]), 0]

    point = rot.apply(point)
    print(point)
    
    gp = gmsh.model.geo.add_point(point[0]+dx, point[1]+dy, point[2], lc)
    points.append(gp)
   
  spline = gmsh.model.geo.addSpline(points + [points[0]])


  l_loop = gmsh.model.geo.addCurveLoop([spline])

  return l_loop
 
  
wTunnel = windTunnel(40,20, 1)
mainSail = foil('foil.dat',scale=6.22, dx=0, dy=0, aoa=25)
headSail = foil('foil.dat',scale=6.20, dx=-5, dy=0, aoa=26)

sur_setup = gmsh.model.geo.addPlaneSurface([wTunnel,mainSail, headSail])

#addPlaneSurface returns the surface tag; extrude takes a list of (dim, tag) pairs as input. This is why (2,sur_setup)
#numElements=[1] is like Layers{1} in Extrude
ids = gmsh.model.geo.extrude([(2,sur_setup)], 0, 0, 1, numElements=[1], recombine=True)
print("IDS:", ids)

gmsh.model.geo.addPhysicalGroup(1, [1], name="outlet")
gmsh.model.geo.addPhysicalGroup(1, [2,4], name="walls")
gmsh.model.geo.addPhysicalGroup(1, [3], name="inlet")
gmsh.model.geo.addPhysicalGroup(1, [5,6], name="airfoil")
gmsh.model.geo.addPhysicalGroup(1, [38], name="1-1")
gmsh.model.geo.addPhysicalGroup(1, [17], name="1-2")
gmsh.model.geo.addPhysicalGroup(1, [21], name="1-3")
gmsh.model.geo.addPhysicalGroup(1, [25], name="1-4")
gmsh.model.geo.addPhysicalGroup(1, [29], name="1-5")
gmsh.model.geo.addPhysicalGroup(1, [33], name="1-6")
gmsh.model.geo.addPhysicalGroup(1, [37], name="1-7")


#Physical Surface("outlet") = {ids[2]};
#Physical Surface("walls") = {ids[{3, 5}]};
#Physical Surface("inlet") = {ids[4]};
#Physical Surface("airfoil") = {ids[{6,7}]};
#Physical Surface("frontAndBack") = {ids[0], TwoDimSurf};
#Physical Volume("volume") = {ids[1]};


# Create the relevant Gmsh data structures 
# from Gmsh model.
gmsh.model.geo.synchronize()
  
  
# Creates  graphical user interface
 
if "-nopopup" not in sys.argv:
  gmsh.fltk.run()
else:
  # Generate mesh:
  gmsh.model.mesh.generate()
  
  # Write mesh data:
  gmsh.write("GFG.msh")

# It finalize the Gmsh API
gmsh.finalize()

