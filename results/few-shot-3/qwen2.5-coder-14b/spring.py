import cadquery as cq

# Parameters for the helical spring
circle_radius = 1.5
major_radius = 20
pitch = 8
total_height = 80

# Create a circle to be swept along the helix path
profile = (
    cq.Workplane("XY")
    .circle(circle_radius)
)

# Define the helix path
helix_path = (
    cq.Workplane("XZ")
    .circle(major_radius)
    .workplane(offset=total_height, centerOption="CenterOfMass")
    .helix(pitch=pitch, height=total_height, direction="+Z", angleDegrees=360)
)

# Sweep the circle along the helix path to create the spring
result = profile.sweep(helix_path, multisection=True)