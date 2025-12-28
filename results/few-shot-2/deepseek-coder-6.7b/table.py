import cadquery as cq

# Define dimensions
top_width = 200
top_height = 100
top_thickness = 15
leg_diameter = 12
leg_height = 120
leg_inset = 15

# Create the top of the table
result = (
    cq.Workplane("XY")
    .rect(top_width, top_height)
    .extrude(top_thickness)
)

# Create and add four legs to the table
legs = (
    cq.Workplane("XY")
    .circle((leg_diameter / 2))
    .extrude(leg_height)
    .translate((-1 * top_width / 4, -1 * top_height / 4, 0)) # bottom left leg
    .union()
    .translate((top_width / 2, -1 * top_height / 4, 0)) # bottom right leg
    .union()
    .translate((-1 * top_width / 4, top_height / 2, 0)) # top left leg
    .union()
    .translate((top_width / 2, top_height / 2, 0)) # top right leg
)

result = result.add(legs)