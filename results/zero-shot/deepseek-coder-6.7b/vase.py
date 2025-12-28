from cadquery import *
import math

# Define parameters for the vase
base_radius = 30  # in mm
mid_height = 60   # in mm
top_radius = 22    # in mm
vase_length = top_radius*2 + mid_height  # length of the vase is twice the radius at the top plus the height at the mid-point

# Create a smooth profile for the vase
profile = Workplane("XY").moveTo(0, -base_radius).circle(base_radius)

# Revolve this profile to create the vase shape
vase = profile.revolve(vase_length)

# Cut off the top and bottom of the vase to make it a perfect cylinder
cylinder = Workplane("XY").moveTo(-base_radius, 0).circle(top_radius)
result = vase.cut(cylinder)

# Add a hole for the neck of the vase
neck_height = 120   # in mm
hole_diameter = 5    # in mm
vase_width = math.sqrt((base_radius**2 - (mid_height/2)**2))*2  # width of the vase at mid-height
result = result.faces(">Z").workplane().moveTo(-(vase_width/2), -neck_height).circle(hole_diameter / 2)

# Store final shape in variable named 'result'
final_shape = result.extrude(mid_height + neck_height, combine=False)