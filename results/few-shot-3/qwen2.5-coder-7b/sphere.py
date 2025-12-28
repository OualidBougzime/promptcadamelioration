import cadquery as cq

diameter = 80
radius = diameter / 2

result = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(diameter)  # Extrude to create a sphere by revolving the circle around the Z-axis
)