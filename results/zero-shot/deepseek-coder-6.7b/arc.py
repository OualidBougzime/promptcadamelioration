import cadquery as cq
from math import pi

# Define parametric dimensions
radius = 60 # mm
sweep_angle = 210 # deg

# Create arc
arc = cq.Workplane("XY").moveTo(0, 0).circle(radius)
result = arc.revolve(360 - sweep_angle / (2 * pi))