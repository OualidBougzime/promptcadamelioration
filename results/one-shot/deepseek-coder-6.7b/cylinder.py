import cadquery as cq

diameter = 40
height = 60

# Create a workplane for our 3D object. We'll use XY plane in this case
workplane = cq.Workplane("XY")

# Add a cylinder to the workplane with given diameter and height
result = (
    workplane.cylinder(diameter/2, height)
)