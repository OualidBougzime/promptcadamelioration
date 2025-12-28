import cadquery as cq

# Define dimensions
base_diameter = 50
height = 60

# Create a cone with the specified base diameter and height
result = (
    cq.Workplane("XY")
    .circle(base_diameter / 2)
    .extrude(height)
)

# Optionally, you can chamfer the edges if needed
chamfer_size = 1
result = result.faces(">Z").chamfer(chamfer_size)

# Store the final shape in 'result' variable