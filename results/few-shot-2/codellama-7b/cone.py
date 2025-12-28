import cadquery as cq

# Create a cone with base diameter of 50 mm and height of 60 mm
result = (
    cq.Workplane("XY")
    .circle(25)
    .extrude(60)
)