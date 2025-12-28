import cadquery as cq

major_radius = 20
pitch = 8
circle_radius = 1.5
total_height = 80

result = (
    cq.Workplane("XY")
    .circle(circle_radius)
    .extrude(total_height)
    .faces(">Z")
    .revolve(2 * cq.pi, cq.Vector(pitch, 0, major_radius), direction="RIGHT")
    .faces("<Z")
    .revolve(2 * cq.pi, cq.Vector(-pitch, 0, -major_radius), direction="LEFT")
)