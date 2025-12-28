import cadquery as cq

outer_diameter = 60
height = 100
bottom_thickness = 3
wall_thickness = 2
rim_fillet = 1

result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(height)
    .faces(">Z")
    .workplane()
    .circle((outer_diameter / 2) - wall_thickness)
    .cutBlind(-(height - bottom_thickness))
    .edges(">Z")
    .fillet(rim_fillet)
)