import cadquery as cq

# Define parameters
circle_radius = 1.5  # mm
major_radius = 20    # mm
pitch = 8          # mm
total_height = 80    # mm

# Create a circle with the specified radius
circle = cq.Workplane("XY").circle(circle_radius)

# Create a helix path
helix_path = cq.Workplane("XZ").lineTo(major_radius, total_height).close()

# Sweep the circle along the helix path to create the spring
result = circle.sweep(helix_path, multisection=True)

# Display the result (optional)
show_object(result)