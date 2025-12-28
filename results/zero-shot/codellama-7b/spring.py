import cadquery as cq
from math import pi

# Define the helix parameters
major_radius = 20.0
pitch = 8.0
total_height = 80.0

# Create a circle with radius 1.5 mm
circle = cq.Workplane().circle(radius=1.5)

# Sweep the circle along the helix
result = circle.sweep(cq.Workplane(), angle=360, pitch=pitch, height=total_height, axis="Z")

# Rotate the swept shape to align with the major radius of the helix
result = result.rotate((0, 0, pi/2), center=(0, 0, 0))

# Translate the swept shape to the origin
result = result.translate((0, 0, -total_height/2))

# Store the final shape in a variable named 'result'
result = result.val()