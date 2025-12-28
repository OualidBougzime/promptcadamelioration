from cadquery import *
import math

# Parametric dimensions
shaft_radius = 4  # in mm
length = 50  # in mm
head_diameter = 12  # in mm
height = 5  # in mm

# Create the shaft of the screw
shaft = cq.Cylinder(r=shaft_radius, h=length)

# Calculate the angle at which to rotate the head so that it fits snugly around the cylinder
angle = math.degrees(math.atan2(height / 2, shaft_radius))

# Create the hexagonal head of the screw
head = cq.Workplane().move(-length/2,0).box(head_diameter, height, shaft_radius)

# Rotate and position the head on top of the cylinder
head = head.rotate((0, 0, angle))

# Combine the two parts into a single solid
result = shaft.union(head)