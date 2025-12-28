import cadquery as cq

# Define dimensions
diameter = 40
height = 60

# Calculate radius
radius = diameter / 2

# Create the cylinder
result = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(height)
)

# Store final shape in 'result' variable