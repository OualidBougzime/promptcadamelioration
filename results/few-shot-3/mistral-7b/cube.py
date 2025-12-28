import cadquery as cq

size = 50

result = (
    cq.Workplane("XY")
    .box(size, size, size)
)