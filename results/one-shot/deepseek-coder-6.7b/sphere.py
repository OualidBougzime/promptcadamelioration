import cadquery as cq

diameter = 80

# Create a sphere with given diameter and store it in 'result' variable.
result = (
    cq.Workplane("XY")
     .circle(diameter / 2)
     .extrude(1) # extrude to create the 3D shape
)