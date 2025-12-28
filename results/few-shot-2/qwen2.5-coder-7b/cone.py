import cadquery as cq

# Define dimensions
base_diameter = 50
height = 60

# Create the cone
result = (
    cq.Workplane("XY")
    .circle(base_diameter / 2)
    .extrude(height)
)

# Store the final shape in 'result' variable