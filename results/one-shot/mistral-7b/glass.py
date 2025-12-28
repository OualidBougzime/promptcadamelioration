import cadquery as cq

outer_diameter = 60
height = 100
bottom_thickness = 3
wall_thickness = 2
top_fillet = 1

result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2 - wall_thickness)
    .extrude(height - bottom_thickness)
    .faces(">Z")
    .cut(cq.Workplane("XY").rect(outer_diameter, bottom_thickness))
    .faces(">Z")
    .fillet(top_fillet)
)