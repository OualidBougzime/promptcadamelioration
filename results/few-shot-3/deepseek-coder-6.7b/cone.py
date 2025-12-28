import cadquery as cq

diameter = 50
height = 60

# Create a cone with given diameter and height
cone = (
    cq.Workplane("XY")
    .circle(diameter / 2)
    .extrude(height)
)

result = cone