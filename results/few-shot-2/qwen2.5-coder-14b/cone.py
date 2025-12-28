import cadquery as cq

base_diameter = 50
height = 60

result = (
    cq.Workplane("XY")
    .circle(base_diameter / 2)
    .extrude(height)
)