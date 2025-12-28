import cadquery as cq

diameter = 60
height = 100
bottom_thickness = 3
wall_thickness = 2

result = (
    cq.Workplane("XY")
    .circle(diameter / 2)
    .extrude(height)
    .faces(">Z")
    .workplane()
    .circle((diameter / 2) - wall_thickness)
    .cutBlind(-(height - bottom_thickness))
    .edges(">Z")
    .fillet(1)
)