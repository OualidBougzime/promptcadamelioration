import cadquery as cq

# Define the parameters for the helix
major_radius = 20
minor_radius = 1.5
pitch = 8
height = 80

# Create a circle to sweep along the helix
circle = cq.Workplane("XY").circle(major_radius)

# Sweep the circle along the helix
result = circle.sweep(cq.Workplane("YZ").helix(pitch, height), both=True)

# Chamfer the ends of the spring
chamfer_size = 1
result = result.faces(">Z").chamfer(chamfer_size).faces("<Z").chamfer(chamfer_size)

# Store the final shape in the 'result' variable
result = result

# Print the resulting CAD object
print(result)