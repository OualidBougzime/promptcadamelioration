import cadquery as cq

# Define the parameters for the torus
major_radius = 50
minor_radius = 8

# Create the torus using CadQuery API methods
result = (
    cq.Workplane("XY")
    .circle(minor_radius)
    .extrude(major_radius * 2)  # Extrude to create a tube with diameter equal to major radius
    .faces(">Z")
    .workplane(centered=(0, minor_radius))
    .circle(minor_radius)
    .cutBlind(-(major_radius * 2))  # Cut the tube to form the torus shape
)

# Display the result (optional, for visualization in a Jupyter notebook or similar environment)
show_object(result)