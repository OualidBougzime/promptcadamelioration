import cadquery as cq

# Dimensions
top_length = 200
top_width = 100
top_height = 15
leg_diameter = 12
leg_height = 120
inset = 15

# Create the top of the table
top = (
    cq.Workplane("XY")
    .rect(top_length, top_width)
    .extrude(top_height)
)

# Create the legs of the table
leg_radius = leg_diameter / 2
leg_positions = [
    (inset, inset),
    (top_length - inset, inset),
    (inset, top_width - inset),
    (top_length - inset, top_width - inset)
]

legs = cq.Workplane("XY").union(
    cq.Workplane("XY")
    .translate(pos)
    .circle(leg_radius)
    .extrude(leg_height)
    for pos in leg_positions
)

# Union the top and legs to form the final table
result = top.union(legs)