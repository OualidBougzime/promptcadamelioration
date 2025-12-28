import cadquery as cq

outer_radius = 40
inner_radius = 20
length = 80
chamfer = 1

result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(length)
    .faces(">Z")
    .chamfer(chamfer)
    .faces("<Z")
    .chamfer(chamfer)
)