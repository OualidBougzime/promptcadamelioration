import cadquery as cq

length = 50

result = (
    cq.Workplane("XY")
    .box(cq.Vector(length, length, length))
)