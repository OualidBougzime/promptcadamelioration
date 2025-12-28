import cadquery as cq

# Define dimensions
diameter = 40
height = 60

# Create the cylinder
result = (
    cq.Workplane("XY")
    .circle(diameter / 2)
    .extrude(height)
)

# Store the final shape in 'result' variable