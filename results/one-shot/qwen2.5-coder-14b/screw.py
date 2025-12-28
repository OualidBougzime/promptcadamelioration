import cadquery as cq

# Define dimensions
shaft_radius = 4
shaft_length = 50
head_diameter = 12
head_height = 5

# Create the cylindrical shaft
result = (
    cq.Workplane("XY")
    .circle(shaft_radius)
    .extrude(shaft_length)
)

# Create the hexagonal head
hex_head = (
    cq.Workplane("XY")
    .polygon(6, head_diameter / 2)  # Hexagon with given diameter
    .extrude(head_height)
)

# Combine shaft and head
result = result.union(hex_head.translate((0, 0, shaft_length)))

# Store the final shape in 'result' variable