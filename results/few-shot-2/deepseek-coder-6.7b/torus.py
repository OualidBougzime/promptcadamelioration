import cadquery as cq

major_radius = 50
minor_radius = 8

result = (
    cq.Workplane("XY")
    .moveTo(major_radius, 0)
    .circle(minor_radius)
    .extrude(2 * major_radius)
)