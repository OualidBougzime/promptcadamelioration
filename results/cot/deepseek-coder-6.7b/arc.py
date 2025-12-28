from cadquery import *

# Define dimensions and parameters
r = 60  # Radius of circle in mm
a = 210  # Sweep angle of arc in degrees

# Create a workplane
w = Workplane('XY').circle(r)

# Create an arc with the given sweep angle
result = w.arcTo(startAngle=0, endAngle=a, radius=r)