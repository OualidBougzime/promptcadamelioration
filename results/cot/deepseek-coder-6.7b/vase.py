from cadquery import *
import math

# Define dimensions
base_radius = 30  # mm
mid_height = 60   # mm
top_radius = 35   # mm
vase_height = 120 # mm

# Create vase profile with smooth lines
pts = [(0, base_radius), (mid_height/2, top_radius), (mid_height, 0)]
profile = Workplane("XY").polyline(pts)

# Revolve the profile into a cylinder
vase = profile.revolve(origin=(0, 0))

# Extrude the vase to create height
result = vase.extrude(vase_height)