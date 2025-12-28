import cadquery as cq

diameter = 80

result = (
    cq.Workplane("XY")
    .circle(diameter / 2)
    .extrude(diameter / 2)
)