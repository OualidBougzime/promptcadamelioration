import cadquery as cq

base_radius = 30
mid_radius = 22
top_radius = 35
height = 120
fillet_radius = 1

result = (
    cq.Workplane("XY")
    .circle(base_radius)
    .revolve(height, axis=(0, 0, 1))
    .faces(">Z")
    .workplane()
    .circle(mid_radius)
    .extrude(60, tangent=True)
    .revolve(height - 60, axis=(0, 0, 1))
    .faces(">Z")
    .workplane()
    .circle(top_radius)
    .extrude(60, tangent=True)
    .revolve(height - 120, axis=(0, 0, 1))
    .edges().fillet(fillet_radius)
)