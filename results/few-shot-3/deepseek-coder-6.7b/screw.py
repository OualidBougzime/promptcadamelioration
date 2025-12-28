import cadquery as cq

shaft_radius = 4
shaft_length = 50
head_diameter = 12
head_height = 5

# Create the shaft of the screw
shaft = (
    cq.Workplane("XY")
    .circle(shaft_radius)
    .extrude(shaft_length)
)

# Create the head of the screw
head = (
    cq.Workplane("XY")
    .polygon(6, head_diameter / 2) # divide by 2 to get radius for polygon method
    .extrude(head_height)
)

# Combine shaft and head into one solid
result = shaft.union(head.translate((0, 0, shaft_length)))