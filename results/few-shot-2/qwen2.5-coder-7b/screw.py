import cadquery as cq

# Define dimensions
shaft_radius = 4
shaft_length = 50
head_diameter = 12
head_height = 5

# Create the cylinder for the screw shaft
cylinder = (
    cq.Workplane("XY")
    .circle(shaft_radius)
    .extrude(shaft_length)
)

# Create the hexagonal head using a polygon
hexagon_points = [
    (0, 0),
    (head_diameter / 2, head_height / 2),
    (head_diameter / 2, -head_height / 2),
    (-head_diameter / 2, -head_height / 2),
    (-head_diameter / 2, head_height / 2),
    (0, 0)
]

hexagon = cq.Workplane("XY").polygon(6, head_diameter / 2).extrude(head_height)

# Combine the cylinder and hexagonal head
result = cylinder.union(hexagon)

# Optionally, chamfer the edges of the hexagonal head for a smoother finish
chamfer_distance = 1
result = result.faces("<Z").chamfer(chamfer_distance)