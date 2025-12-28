import cadquery as cq

diameter = 40
height = 60

result = (
    cq.Workplane("XY")
    .circle(diameter / 2)
    .extrude(height)
)