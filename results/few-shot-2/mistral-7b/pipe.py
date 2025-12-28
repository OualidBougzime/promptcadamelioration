import cadquery as cq

outer_radius = 20
inner_radius = 15
length = 150
chamfer = 1

result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(length)
    .faces(">Z").first()
    .chamfer(chamfer)
    .edges("|Z").first().back()
    .workplane()
    .rotate(180)
    .mirror(cq.Plane("XY", offset=(0, 0, length)))
    .faces("<Z").first()
    .chamfer(chamfer)
    .edges("|Z").last().back()
)