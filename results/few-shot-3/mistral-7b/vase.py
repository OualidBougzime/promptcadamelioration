import cadquery as cq

base_radius = 30
mid_radius = 22
top_radius = 35
height = 120

result = (
    cq.Workplane("XY")
    .circle(base_radius)
    .extrude(height / 2)
    .revolve(cq.Vector(0, 0, 1), angle=cq.CADQ_TWO_PI)

    .worksurface()
    .moveTo(0, height / 2)
    .circle(mid_radius)
    .extrude(height / 2 - height / 4)

    .worksurface()
    .moveTo(0, height)
    .circle(top_radius)
    .extrude(height / 2 - height)
)

# To smooth the profile, you can use fillet() method at the end:
result = result.faces(">Z").fillet(1)