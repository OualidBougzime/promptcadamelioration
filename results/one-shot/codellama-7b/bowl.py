import cadquery as cq

# Create a semicircle with radius 40 mm
semicircle = (
    cq.Workplane("XY")
    .circle(40)
    .extrude(100)
)

# Shell the semicircle with a thickness of 3 mm
result = (
    semicircle
    .faces(">Z")
    .shell(thickness=3, draftAngle=25)
)

# Display the final shape
show(result)