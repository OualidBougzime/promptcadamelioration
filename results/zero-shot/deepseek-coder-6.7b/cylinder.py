from cadquery import *

# Parametric Dimensions
diameter = 40   # in mm
height = 60     # in mm

# Create a cylinder with given dimensions
cylinder = cq.Cylinder(radius=diameter/2, height=height)
result = cylinder