import cadquery as cq

major_radius = 20
pitch = 8
total_height = 80
circle_radius = 1.5

result = (
    cq.Workplane("XY")
    .circle(circle_radius)
    .extrude(total_height, start_solid=True, tapered=cq.Helix(start_angle=0, end_angle=2 * cq.pi, major_radius=major_radius, pitch=pitch))
    .faces(">Z")
    .chamfer(1)
    .faces("<Z")
    .chamfer(1)
)