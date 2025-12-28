import cadquery as cq

# Parametric dimensions
shaft_radius = 4.0  # mm
shaft_length = 50.0  # mm
head_diameter = 12.0  # mm
head_height = 5.0  # mm

# Create the cylindrical shaft
shaft = cq.Workplane("XY").circle(shaft_radius).extrude(shaft_length)

# Create the hexagonal head
hexagon_points = [
    (0, head_diameter / 2),
    (-head_diameter * 0.866 / 2, -head_diameter / 4),
    (head_diameter * 0.866 / 2, -head_diameter / 4),
    (head_diameter / 2, 0),
    (head_diameter * 0.866 / 2, head_diameter / 4),
    (-head_diameter * 0.866 / 2, head_diameter / 4)
]

hexagon = cq.Workplane("XY").polygon(points=hexagon_points).extrude(head_height)

# Combine the shaft and the head
result = shaft.union(hexagon)

# Translate the head to be on top of the shaft
result = result.translate((0, 0, shaft_length))

# Show the resulting shape
show_object(result)