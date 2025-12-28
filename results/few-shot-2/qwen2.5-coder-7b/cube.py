import cadquery as cq

# Define the dimensions of the cube
edge_length = 50

# Create the cube
result = (
    cq.Workplane("XY")
    .box(edge_length, edge_length, edge_length)
)