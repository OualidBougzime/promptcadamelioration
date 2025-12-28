import cadquery as cq

# Define parameters
shaft_radius = 4.0  # mm
shaft_length = 50.0  # mm
head_diameter = 12.0  # mm
head_height = 5.0  # mm

# Create the cylindrical shaft
shaft = (
    cq.Workplane("XY")
    .circle(shaft_radius)
    .extrude(shaft_length)
)

# Create the hexagonal head
head = (
    cq.Workplane("XY")
    .polygon(6, head_diameter / 2)  # Hexagon with given diameter
    .extrude(head_height)
)

# Combine shaft and head
result = (
    shaft
    .union(head.translate((0, 0, shaft_length)))
)

# Display the result (for Jupyter Notebook or similar environment)
# show_object(result)