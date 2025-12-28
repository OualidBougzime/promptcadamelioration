import cadquery as cq

# Define the size of the cube
size = 50

# Create the cube using the extrude method
result = (
    cq.Workplane("XY")
    .rect(size, size)
    .extrude(size)
)

# Store the final shape in the 'result' variable