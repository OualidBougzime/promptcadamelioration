import cadquery as cq
from math import pi

# Define parameters
circle_radius = 1.5
major_radius = 20
pitch = 8
total_height = 80

# Calculate the number of turns for the helix
turns = total_height / pitch

# Create a helix path
helix_path = cq.Workplane("XY").lineTo(major_radius, 0).circle(circle_radius).close().extrude(total_height)

# Create a circle to sweep along the helix path
circle_to_sweep = cq.Workplane("YZ").circle(circle_radius)

# Sweep the circle along the helix path
result = (
    cq.Workplane("XY")
    .lineTo(major_radius, 0)
    .circle(circle_radius)
    .close()
    .extrude(total_height)
    .edges(">Z")
    .fillet(1)
    .sweep(circle_to_sweep, multisection=True)
)

# Rotate the helix to create a right-hand helix
result = result.rotate((0, 0, 0), (0, 0, 1), turns * 360 / turns)