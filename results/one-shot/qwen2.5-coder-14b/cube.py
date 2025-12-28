import cadquery as cq

# Define the size of the cube
size = 50

# Create the cube
result = (
    cq.Workplane("XY")
    .box(size, size, size)
)

# Display the result (for visualization purposes, not required for storing the shape)
show_object(result)