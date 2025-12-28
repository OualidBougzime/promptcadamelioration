import cadquery as cq

diameter = 40
height = 60

# Create a cylinder with given diameter and height
result = (
    cq.Workplane("XY")
     .circle(diameter / 2)
     .extrude(height)
     .faces(">Z")
     .chamfer(1)
)