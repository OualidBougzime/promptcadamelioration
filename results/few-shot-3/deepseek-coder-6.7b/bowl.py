import cadquery as cq

# Define parameters
radius = 40
wall_thickness = 3

# Create a semicircle workplane
semi_circle = (
    cq.Workplane("XY")
    .moveTo(radius, 0)
    .lineTo(-radius, 0)
    .close()
)

# Revolve the semi-circle to create a hemisphere
result = semi_circle.revolve(360)

# Add shell with thickness of wall_thickness
result = result.shell(wall_thickness)