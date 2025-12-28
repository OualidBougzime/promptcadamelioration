import cadquery as cq

major_radius = 50
minor_radius = 8

result = (
    cq.Workplane("XY")
    .circle(major_radius)
    .circle(minor_radius)
    .extrude(100)
)