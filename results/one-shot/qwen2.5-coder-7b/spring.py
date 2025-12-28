import cadquery as cq

# Define the parameters
circle_radius = 1.5  # Radius of the wire forming the spring
major_radius = 20    # Major radius of the helix
pitch = 8            # Pitch of the helix
total_height = 80    # Total height of the helix

# Create a circle that will be swept along the helix
circle_profile = cq.Workplane("XY").circle(circle_radius)

# Define the helix path
helix_path = cq.Workplane("XZ").lineTo(major_radius, total_height).lineTo(-major_radius, total_height).close()

# Sweep the circle profile along the helix path to create the spring
result = (
    cq.Workplane("XY")
    .circle(circle_radius)
    .extrude(total_height / 2)  # Extrude half of the height to form a helical shape
    .rotate((0, 0, 0), (0, 1, 0), total_height / (2 * pitch))  # Rotate to create the helix
)

# Optionally, you can add more operations if needed