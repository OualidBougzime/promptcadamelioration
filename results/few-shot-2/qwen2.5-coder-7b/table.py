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
leg = (
    cq.Workplane("XY")
    .circle(leg_diameter / 2)
    .extrude(leg_height)
)

# Position the legs under the top
legs = (
    cq.Workplane("XY")
    .tag("origin")
    .rect(top_length, top_width)
    .vertices()
    .eachpoint(lambda loc: leg.translate((loc.x - inset, loc.y - inset, 0)), True)
)

# Union the top and legs
result = top.union(legs)