import cadquery as cq

# Define dimensions
outer_diameter = 60
height = 100
bottom_thickness = 3
wall_thickness = 2
fillet = 1

# Create a cylinder with the given dimensions
result = (
    cq.Workplane("XY")
     .cylinder(r=outer_diameter/2, h=height)
     .cutThruSlot2D(depth=bottom_thickness, topOffset=wall_thickness)
     .edges('|Z').fillet(fillet)  # fillet on the rim
)