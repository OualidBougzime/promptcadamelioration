import cadquery as cq

# Define key dimensions
base_diameter = 50  # in mm
height = 60  # in mm

# Create a workplane for the shape to be built on
workplane = cq.Workplane('XY')

# Apply operations: create a cylinder with given diameter and height, then cut off excess material from both ends of the cylinder
result = (
    workplane.cylinder(radius=base_diameter/2, height=height)
)