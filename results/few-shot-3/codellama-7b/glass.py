import cadquery as cq

# Define the parameters for the drinking glass
outer_diameter = 60
height = 100
bottom_thickness = 3
wall_thickness = 2
fillet_radius = 1

# Create a cylinder with the desired outer diameter and height
cylinder = cq.Workplane("XY") \
    .circle(outer_diameter / 2) \
    .extrude(height)

# Hollow out the cylinder to create a hollow interior
hollowed_cylinder = cylinder.faces(">Z") \
    .workplane() \
    .circle((outer_diameter / 2) - wall_thickness) \
    .cutBlind(-(height - bottom_thickness)) \
    .edges(">Z") \
    .fillet(fillet_radius)

# Add a fillet to the top rim of the glass
result = hollowed_cylinder.faces("<Z") \
    .workplane() \
    .circle((outer_diameter / 2) - wall_thickness) \
    .cutBlind(-(height - bottom_thickness)) \
    .edges(">Z") \
    .fillet(fillet_radius)