```python
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
    .faces(">Z")
    .chamfer(chamfer)
    .faces("<Z")
    .chamfer(chamfer)
)