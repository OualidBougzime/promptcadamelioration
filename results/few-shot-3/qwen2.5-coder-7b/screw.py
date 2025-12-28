import cadquery as cq

# Define dimensions
shaft_radius = 4
shaft_length = 50
head_diameter = 12
head_height = 5

# Create the cylindrical shaft
shaft = (
    cq.Workplane("XY")
    .circle(shaft_radius)
    .extrude(shaft_length)
)

# Create the hexagonal head
head = (
    cq.Workplane("XY")
    .polygon(6, head_diameter)
    .extrude(head_height)
)

# Combine the shaft and head into a single shape
result = shaft.union(head.translate((0, 0, shaft_length)))