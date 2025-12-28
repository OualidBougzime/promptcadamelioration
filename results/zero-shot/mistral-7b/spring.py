from cadquery import exporters, workplane, cylinder, helix, rotate, translate, mesh, Workplane

# Set up the parameters for the helical spring
circle_radius = 1.5  # Radius of the circle used to sweep along the helix
major_radius = 20.0  # Major radius of the helix
pitch = 8.0  # Pitch of the helix
total_height = 80.0  # Total height of the helical spring
number_of_turns = total_height / pitch  # Number of turns based on the total height

# Initialize a new workplane and create the helix
app = Workplane("XY")
helix_path = helix(start=(0, 0, 0), direction="Z", radius=major_radius, pitch=pitch, turns=number_of_turns)

# Create a circle at each point along the helix path and sweep it to form the helical spring
result = mesh(workplane().circles(circle_radius).translate(helix_path).extrude(2 * circle_radius))

# Export the final shape as an .stl file
exporters.export(result, "helical_spring.stl", format="stl")