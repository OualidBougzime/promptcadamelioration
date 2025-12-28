from cadquery import exporters, workplane, cylinder, translate, intersect, hexagon, cube, faces, fillet, Workplane, Vector

# Create a new CAD model
model = workplane("XY")

# Define the screw shaft
shaft = cylinder(point=(0, 0, 0), radius=4, height=50)

# Define the hexagonal head
head_radius = 6  # Adding a margin of 2mm for filleting
head = hexagon(size=(12 + 2 * head_radius, head_radius * 6))
head = translate((0, 0, 50 - head.height / 2))(head)
head = fillet(faces=head.edges, radius=head_radius)

# Intersect the shaft and head to create the screw body
screw_body = intersect(shaft, head)

# Define the hexagonal head cap
head_cap = cube((12 + 2 * head_radius, head_radius * 6, 5))
head_cap = translate((0, 0, -50))(head_cap)
head_cap = fillet(faces=head_cap.edges, radius=head_radius)

# Intersect the screw body and head cap to create the final screw shape
result = intersect(screw_body, head_cap)

# Export the model as an .stl file
exporters.export(result, 'screw.stl')