import cadquery as cq

# Define parametric dimensions
length = 50.0  # Length of the cube in millimeters
width = 50.0   # Width of the cube in millimeters
height = 50.0  # Height of the cube in millimeters

# Create a cube using CadQuery
result = cq.Workplane("front").box(length, width, height)

# Display the result (optional)
show_object(result)