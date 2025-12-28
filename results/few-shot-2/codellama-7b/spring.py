import cadquery as cq

# Define parameters for helix sweep
major_radius = 20.0
pitch = 8.0
total_height = 80.0
minor_radius = major_radius - pitch

# Create a circle with radius 1.5 mm
circle = cq.Workplane("XY").circle(1.5)

# Sweep the circle along a right-hand helix
result = circle.sweep(cq.Workplane("YZ").right(major_radius), total_height, draft=False)

# Chamfer the top and bottom faces of the spring
chamfer_size = 1.0
result = result.faces(">Z").chamfer(chamfer_size).faces("<Z").chamfer(chamfer_size)

print(result)