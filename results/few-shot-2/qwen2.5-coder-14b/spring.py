import cadquery as cq

# Define parameters for the helical spring
circle_radius = 1.5
major_radius = 20
pitch = 8
total_height = 80

# Create a circle that will be swept to form the helix
profile = cq.Workplane("XY").circle(circle_radius)

# Define the path of the helix
path = (
    cq.Workplane("XZ")
    .circle(major_radius)
    .extrude(total_height, twist=360 * (total_height / pitch))
)

# Sweep the profile along the helical path to create the spring
result = profile.sweep(path, multisection=True)