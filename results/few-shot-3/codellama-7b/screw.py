import cadquery as cq

# Define screw parameters
shaft_radius = 4
shaft_length = 50
head_diameter = 12
head_height = 5

# Create shaft
shaft = (
    cq.Workplane("XY")
    .circle(shaft_radius)
    .extrude(shaft_length)
)

# Create hexagonal head
head = (
    cq.Workplane("XY")
    .polygon(6, head_diameter)
    .extrude(head_height)
)

# Union shaft and head
result = shaft.union(head.translate((0, 0, shaft_length)))

# Store final shape in 'result' variable
result = result

# Print the resulting CQ object
print(result)