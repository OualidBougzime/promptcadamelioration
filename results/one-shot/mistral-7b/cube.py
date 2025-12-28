import cadquery as cq

cube_size = 50

result = (
    cq.Workplane("XY")
    .box(cq.Vector(cube_size, cube_size, cube_size))
)