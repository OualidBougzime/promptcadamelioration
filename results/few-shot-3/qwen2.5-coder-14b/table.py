import cadquery as cq

# Dimensions for the table
top_length = 200
top_width = 100
top_thickness = 15
leg_diameter = 12
leg_height = 120
inset_distance = 15

# Create the rectangular top
top = (
    cq.Workplane("XY")
    .box(top_length, top_width, top_thickness)
)

# Function to create a leg
def make_leg():
    return (
        cq.Workplane("XY")
        .circle(leg_diameter / 2)
        .extrude(leg_height)
    )

# Create the four legs and position them
legs = []
for x in [-1, 1]:
    for y in [-1, 1]:
        leg_position = (x * (top_length / 2 - inset_distance), y * (top_width / 2 - inset_distance))
        leg = make_leg().translate(leg_position + (0,))
        legs.append(leg)

# Union all parts to form the final table
result = top.union(*legs)