import cadquery as cq

# Dimensions
top_length = 200
top_width = 100
top_height = 15
leg_diameter = 12
leg_height = 120
inset_distance = 15

# Create the rectangular top
top = (
    cq.Workplane("XY")
    .box(top_length, top_width, top_height)
)

# Create a single leg
leg = (
    cq.Workplane("XY")
    .circle(leg_diameter / 2)
    .extrude(leg_height)
)

# Position and add four legs to the table
result = top

for i in range(4):
    angle = i * 90  # Rotate each leg by 90 degrees
    positioned_leg = (
        leg
        .rotate((0, 0, 0), (0, 0, 1), angle)
        .translate((top_length / 2 - inset_distance, top_width / 2 - inset_distance, top_height))
    )
    result = result.union(positioned_leg)

# Store the final shape in 'result' variable