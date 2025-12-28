import cadquery as cq

# Define parametric dimensions
major_radius = 50.0  # major radius in mm
minor_radius = 8.0   # minor radius in mm

# Create the torus using parametric dimensions
torus = cq.Workplane("XY").revolve(360, (0, 0), (1, 0))

# Scale the torus to the desired dimensions
result = torus.scale(major_radius / torus.edges().boundingBox().sizeX)

# Display the result
show_object(result)