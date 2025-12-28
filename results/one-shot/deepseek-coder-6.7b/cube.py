import cadquery as cq

# Define the size of the cube
size = 50

result = (
    cq.Workplane("XY")
     .box(size, size, size) # Create a box with given dimensions
)