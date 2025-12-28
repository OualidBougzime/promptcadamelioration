import cadquery as cq

# Parameters
circle_radius = 1.5
major_radius = 20
pitch = 8
total_height = 80

# Create a helix path
helix_path = (
    cq.Workplane("XY")
    .circle(major_radius)
    .helix(pitch=pitch, height=total_height, direction="+Z", angle=360)
)

# Create a circle to sweep along the helix
sweep_circle = cq.Workplane("XY").circle(circle_radius)

# Sweep the circle along the helix path
result = (
    cq.Workplane("XY")
    .add(sweep_circle)
    .sweep(helix_path, multisection=True)
)

# Display the result (for Jupyter Notebook or similar environment)
show_object(result)