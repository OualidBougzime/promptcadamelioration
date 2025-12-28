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
hexagon_points = [
    (0, head_diameter / 2),
    (-head_diameter * 0.5, 0),
    (0, -head_diameter / 2),
    (head_diameter * 0.5, 0),
    (0, head_height)
]

# Create the hexagon and extrude it to form the head
hexagon = cq.Workplane("XY").polygon(6, head_diameter / 2).extrude(head_height)

# Combine the shaft and the head
result = shaft.union(hexagon)