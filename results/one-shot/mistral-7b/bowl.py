import cadquery as cq

radius = 40
wall_thickness = 3

result = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(height=radius)
    .faces(">Z")
    .revolve(angle=180, axis=(0, 0, 1))
    .shell(wall_thickness)
)