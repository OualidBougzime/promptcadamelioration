import cadquery as cq

diameter = 80

result = (
    cq.Workplane("XY")
    .sphere(diameter / 2)
)