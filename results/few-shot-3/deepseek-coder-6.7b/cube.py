import cadquery as cq

# Define dimensions
width = 50
height = 50
depth = 50

# Create the cube and store it in 'result' variable
result = (
    cq.Workplane("XY")  # Set up a workplane in XY plane
    .box(width, height, depth)  # Create a box with given dimensions
)