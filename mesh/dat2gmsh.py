#!/usr/bin/python

# Aerofoil .dat to .geo file converter
""" firstly, we ask the user to provide us the name of the dat file"""
tries = 0

datfile = 'foil'
""" next, we create the new geo file"""
mesh = open(datfile + '.geo', 'r+')
aero = open(datfile + '.dat', 'r')
""" this section creates the points for the mesh and set up the spline"""
linecnt = 0
spline = []
mesh.write('Macro Foil\n')
mesh.write('th = 0.01;\n')
mesh.write('start = ce;\n')
for line in aero:
        new = line.strip().split(" ")
        mesh.write('Point(ce++) = {%s, %s, 0, th}; \n' % (str(new[0]),str(new[1])))
mesh.write('end = ce-1;\n')
mesh.write('Spline(1000) = {start:end,start}; \n')
linecnt += 1
mesh.write("Line Loop(1001)={1000}; \n" )
mesh.write("Results[0] = ce; \n" )

mesh.write('Return \n')
mesh.close()


