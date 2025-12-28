import cadquery as cq

# Create a cylinder with diameter 40 mm and height 60 mm
result = (
    cq.Workplane("XY")
    .circle(40)
    .extrude(60)
)