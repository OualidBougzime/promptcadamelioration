import cadquery as cq

outer_diameter = 60
height = 100
bottom_thickness = 3
wall_thickness = 2
fillet_radius = 1

result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2 + wall_thickness)
    .extrude(height - bottom_thickness)
    .faces(">Z")
    .workplane()
    .circle((outer_diameter / 2 + wall_thickness) - wall_thickness)
    .cutBlind(-bottom_thickness)
    .edges(">Z")
    .fillet(fillet_radius)
)