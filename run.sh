#!/bin/sh

# Quit on error :
set -e

./mesh/gen_mesh.py -mesh
# Convert the mesh to OpenFOAM format:
gmshToFoam main.msh -case case
# Change the patches that gmsh generate so openfoam can read them
changeDictionary -case case
# Run Sim
simpleFoam -case case
