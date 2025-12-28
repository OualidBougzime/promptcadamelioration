import cadquery as cq

cylinder_diameter = 40
cylinder_height = 60

result = (
    cq.Workplane("XY")
    .circle(cylinder_diameter / 2)
    .extrude(cylinder_height)
)