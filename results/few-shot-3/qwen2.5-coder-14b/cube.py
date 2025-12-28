import cadquery as cq

# Define dimensions of the cube
side_length = 50

# Create a cube using CadQuery
result = (
    cq.Workplane("XY")
    .box(side_length, side_length, side_length)
)