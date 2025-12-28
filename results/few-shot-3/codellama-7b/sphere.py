import cadquery as cq

sphere_diameter = 80

result = (
    cq.Workplane("XY")
    .circle(sphere_diameter / 2)
    .extrude(sphere_diameter / 2)
)