import cadquery as cq

# Define the major and minor radii of the torus
major_radius = 50.0  # mm
minor_radius = 8.0   # mm

# Create a new CadQuery object
result = cq.Workplane()

# Add a torus to the object
result = result.torus(major_radius, minor_radius)

# Display the final shape
print(result)