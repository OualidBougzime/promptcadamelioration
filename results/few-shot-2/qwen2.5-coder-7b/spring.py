import cadquery as cq

# Define the parameters
circle_radius = 1.5
major_radius = 20
pitch = 8
total_height = 80

# Calculate the number of turns in the helix
num_turns = total_height / pitch

# Create a helix path
helix_path = cq.Workplane("XY").rect(2 * major_radius, num_turns * circle_radius).extrude(pitch)

# Create the spring shape by sweeping a circle along the helix path
result = (
    cq.Workplane("XZ")
    .circle(circle_radius)
    .translate((major_radius, 0, 0))
    .rotate((0, 0, 1), angle=360 * num_turns)
    .extrude(total_height)
)

# Optionally, you can fillet the edges to smooth them out
result = result.edges().fillet(0.5)