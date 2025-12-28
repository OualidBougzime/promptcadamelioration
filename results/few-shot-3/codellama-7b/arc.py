import cadquery as cq

# Create an arc with radius 60 mm and sweep angle 210 deg
arc = (
    cq.Workplane("XY")
    .circle(60)
    .sweep(210, "deg")
)

# Store the final shape in the 'result' variable
result = arc