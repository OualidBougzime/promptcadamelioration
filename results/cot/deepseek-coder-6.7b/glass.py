import cadquery as cq

# Define the key dimensions
outer_diameter = 60  # in mm
height = 100  # in mm
bottom_thickness = 3  # in mm
wall_thickness = 2  # in mm

# Create a cylinder for the base
base = cq.Cylinder(radius=outer_diameter/2, height=height)

# Cut a hole to leave space at the bottom
cut = base.cut(cq.Cylinder(radius=outer_diameter/2 - bottom_thickness))

# Fillet the top rim
result = cut.faces(">Z").fillet(wall_thickness)