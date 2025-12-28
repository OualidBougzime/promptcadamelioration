import cadquery as cq

# Create a new workplane
wp = cq.Workplane()

# Apply the sphere method to create the sphere
sphere = wp.sphere(80)

# Move the sphere to its final location
sphere = sphere.translate((0, 0))

# Display the result
result = sphere.display()