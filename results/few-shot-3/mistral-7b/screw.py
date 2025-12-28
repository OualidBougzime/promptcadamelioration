import cadquery as cq

shaft_radius = 4
shaft_length = 50
head_diameter = 12
head_height = 5

# Create cylindrical shaft
shaft = (
    cq.Workplane("XY")
    .circle(shaft_radius)
    .extrude(shaft_length)
)

# Create hexagonal head
head = (
    cq.Workplane("XY")
    .polygon(6, head_diameter / 2)  # Hexagon with half the diameter
    .rotate(cq.Vector(0, 0, 1), head_height / 2)  # Rotate the polygon by half the height
    .translate((0, 0, shaft_length))  # Translate the rotated hexagon to the top of the shaft
    .polygon(6, head_diameter)  # Create a full hexagon on top of the rotated one
    .extrude(head_height)
)

# Combine shaft and head into final shape
result = shaft.union(head)