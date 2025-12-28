import cadquery as cq
from math import pi

# Define the cylinder parameters
diameter = 60 * mm
height = 100 * mm
bottom_thickness = 3 * mm
wall_thickness = 2 * mm
fillet_radius = 1 * mm

# Create the cylinder shape
cylinder = cq.Workplane().cylinder(diameter, height)

# Hollow out the cylinder leaving the bottom and wall thickness
hollowed_cylinder = cylinder.cutThruAll(cq.Workplane(), bottom_thickness + wall_thickness)

# Add a fillet to the top rim of the cylinder
filleted_cylinder = hollowed_cylinder.faces(">Z").shell(fillet_radius, 1)

# Store the final shape in a variable named 'result'
result = filleted_cylinder