import cadquery as cq

# Define parametric dimensions
circle_radius = 1.5  # mm
major_radius = 20    # mm
pitch = 8           # mm
total_height = 80   # mm

# Create a circle to be swept
circle = cq.Workplane("XY").circle(circle_radius)

# Define the helix path
helix_path = (
    cq.Workplane("YZ")
    .pointOnCurve((major_radius, 0), (0, pitch))
    .lineTo(major_radius, total_height)
    .close()
)

# Sweep the circle along the helix path
result = circle.sweep(helix_path, multisection=True)

# Display the result (for Jupyter Notebook or similar environment)
show_object(result)