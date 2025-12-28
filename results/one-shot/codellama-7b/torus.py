import cadquery as cq

# Define the parameters of the torus
major_radius = 50
minor_radius = 8

# Create a workplane and add a torus to it
result = (
    cq.Workplane("XY")
    .torus(major_radius, minor_radius)
)

# Display the final shape
print(result)