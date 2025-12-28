import cadquery as cq

# Create a workplane at the origin
wp = cq.Workplane()

# Create a circle with radius 40 mm
circle = wp.circle(radius=40)

# Revolve the circle around the Z-axis to create a hemisphere
hemisphere = wp.revolve(circle, axis="Z")

# Create a shell with thickness of 3 mm
shell = hemisphere.shell(thickness=3)

# Display the result
result = cq.show(shell)