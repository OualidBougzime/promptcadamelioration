import cadquery as cq

# Create a new workplane (XY plane)
workplane = cq.Workplane("XY")

# Define the center of the arc and its radius
center = (0, 0)
radius = 60

# Draw the arc on the workplane
arc = workplane.arc(center, (radius, 0), (radius * cq.cos(210 * cq.pi / 180), radius * cq.sin(210 * cq.pi / 180)))

# Optionally, extrude the arc to create a 3D model
result = arc.extrude(10)  # Extrude by 10 mm

# Display the result
show_object(result)