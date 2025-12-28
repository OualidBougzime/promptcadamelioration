import cadquery as cq

# Define parametric dimensions
major_radius = 50.0  # Major radius in millimeters
minor_radius = 8.0   # Minor radius in millimeters

# Create the torus
result = cq.Workplane("XY").torus(major_radius, minor_radius)

# Display the result (for Jupyter Notebook or similar environment)
show_object(result)