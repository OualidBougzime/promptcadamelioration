import cadquery as cq

diameter = 80
radius = diameter / 2

result = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(radius)
)

# Save the final shape in 'result' variable