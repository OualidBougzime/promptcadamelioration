import cadquery as cq

# Create a semicircle radius 40 mm
semicircle = (
    cq.Workplane("XY")
    .circle(40)
    .extrude(100)
)

# Shell the semicircle with a wall thickness of 3 mm
result = (
    semicircle
    .faces(">Z")
    .workplane()
    .shell(thickness=3)
)