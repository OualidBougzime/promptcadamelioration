import cadquery as cq

# Parameters
outer_diameter = 60
height = 100
bottom_thickness = 3
wall_thickness = 2
fillet = 1

# Create a cylinder with chamfered edges
result = (
    cq.Workplane("XY")
     .circle(outer_diameter / 2)
     .extrude(height)
     .faces(">Z")
     .chamfer(wall_thickness)
     .faces("<Z")
     .chamfer(bottom_thickness)
     .edges("|Z")
     .fillet(fillet)
)