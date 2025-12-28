import cadquery as cq

# Define the size of the cube
size = 50

# Create the cube
result = (
    cq.Workplane("XY")
    .box(size, size, size)
)