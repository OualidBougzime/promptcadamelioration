import cadquery as cq

diameter = 50
height = 60

# Create a cone with base diameter and height
result = (
    cq.Workplane("XY")
     .circle(diameter / 2) # create the circle for bottom face of cone
     .extrude(height)       # extrude it to get the cone's height
     .edges(">Z").fillet(1)   # fillet edges on top to make a smooth edge
)