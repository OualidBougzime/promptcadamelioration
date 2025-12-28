import cadquery as cq

major_radius = 50
minor_radius = 8

result = (
    cq.Workplane("XY")
    .circle(major_radius)
    .rotate(cq.Pi * 2)
    .circle(minor_radius)
    .extrude(2 * cq.Pi * major_radius)
)