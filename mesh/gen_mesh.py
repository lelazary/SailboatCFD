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

def foil(fname, scale, pos, aoa, lc = 0.1):
  foil = open(fname, 'r')
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
 
def gen_sail(pos, aoa, chord=1, camber=0.10, draft=0.50, leading_angle=50, trailing_angle=70, lc = 0.01):


  dx = pos[0]
  dy = pos[1]

  rot_axis = np.array([0,0,1])
  rot_rad = np.radians(aoa)
  rot_vector = rot_axis * rot_rad
  rot = Rotation.from_rotvec(rot_vector)

  Yd = chord * camber
  Xd = chord * draft
  
  c2 =  Yd/np.tan((90-leading_angle)*np.pi/180)
  c3 =  Yd/np.tan((90-trailing_angle)*np.pi/180)
  
  thickness = 0.01
  
  p1 = gmsh.model.geo.addPoint(0,0,0, lc)
  p2 = gmsh.model.geo.addPoint(c2,Yd,0, lc)
  p3 = gmsh.model.geo.addPoint(Xd,Yd,0, lc)
  
  p4 = gmsh.model.geo.addPoint(Xd,Yd,0, lc)
  p5 = gmsh.model.geo.addPoint(chord-c3,Yd,0, lc)
  p6 = gmsh.model.geo.addPoint(chord,0,0, lc)
  
  p7 = gmsh.model.geo.addPoint(0,0+thickness,0, lc)
  p8 = gmsh.model.geo.addPoint(c2,Yd+thickness,0, lc)
  p9 = gmsh.model.geo.addPoint(Xd,Yd+thickness,0, lc)
  
  p10 = gmsh.model.geo.addPoint(Xd,Yd+thickness,0, lc)
  p11 = gmsh.model.geo.addPoint(chord-c3,Yd+thickness,0, lc)
  p12 = gmsh.model.geo.addPoint(chord,0+thickness,0, lc)


  aoa_rad = np.radians(aoa)
  
  b1 = gmsh.model.geo.addBezier([p1, p2,p3]) 
  b2 = gmsh.model.geo.addBezier([p4, p5,p6,p12])
  
  b3 = gmsh.model.geo.addBezier([p12, p11,p10])
  b4 = gmsh.model.geo.addBezier([p9, p8,p7,p1])
  
  cbs = gmsh.model.geo.addCompoundBSpline([b1,b2,b3,b4])
  gmsh.model.geo.rotate([(1,cbs)], 0, 0, 1, 0, 0, 1, aoa_rad)
  gmsh.model.geo.translate([(1,cbs)], dx, dy, 0)

  l_loop = gmsh.model.geo.addCurveLoop([cbs])

  return l_loop
  
awa = -35
mainSailPos = [0,0,0]
headSailPos = [-6/6.20,0,0]

rot_axis = np.array([0,0,1])
rot_rad = np.radians(awa)
rot_vector = rot_axis * rot_rad
rot = Rotation.from_rotvec(rot_vector)
mainSailPos = rot.apply(mainSailPos)
headSailPos = rot.apply(headSailPos)

surfaces = []
wTunnel = windTunnel(20,20, 1.0)
surfaces.append(wTunnel)
#mainSail = foil('mesh/foil.dat',scale=6.22, pos=mainSailPos, aoa=awa+8)
#headSail = foil('mesh/headsail.dat',scale=6.20, pos=headSailPos, aoa=awa+15)
#mainSail = foil('mesh/foil_NACA1408.dat',scale=1, pos=mainSailPos, aoa=-10, lc=0.01)
#surfaces.append(mainSail)

headSail = gen_sail(pos=headSailPos, aoa=-20)
surfaces.append(headSail)

mainSail = gen_sail(pos=mainSailPos, aoa=-20)
surfaces.append(mainSail)

#headSail = foil('mesh/headsail.dat',scale=1, pos=headSailPos, aoa=awa+15)
#surfaces.append(headSail)

surface_2d = gmsh.model.geo.addPlaneSurface(surfaces)

#addPlaneSurface returns the surface tag; extrude takes a list of (dim, tag) pairs as input. This is why (2,surface_2d)
#numElements=[1] is like Layers{1} in Extrude
#ids = gmsh.model.geo.extrude([(2,surface_2d)], 0, 0, 10, numElements=[1], recombine=True)
#print("IDS:", ids)

#gmsh.model.geo.addPhysicalGroup(3, [ ids[1][1] ], name="volume")
#gmsh.model.geo.addPhysicalGroup(2, [ ids[0][1], surface_2d ], name="frontAndBack")
#gmsh.model.geo.addPhysicalGroup(2, [ ids[2][1] ], name="outlet")
#gmsh.model.geo.addPhysicalGroup(2, [ ids[3][1], ids[5][1] ], name="walls")
#gmsh.model.geo.addPhysicalGroup(2, [ ids[4][1] ], name="inlet")
##gmsh.model.geo.addPhysicalGroup(2, [ ids[6][1] ], name="mainsail")
##gmsh.model.geo.addPhysicalGroup(2, [ ids[7][1] ], name="headsail")


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

