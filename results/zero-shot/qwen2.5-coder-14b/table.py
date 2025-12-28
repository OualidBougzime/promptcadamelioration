import cadquery as cq

# Define parametric dimensions
top_width = 200
top_length = 100
top_height = 15
leg_diameter = 12
leg_height = 120
inset_distance = 15

# Create the rectangular top
top = (
    cq.Workplane("XY")
    .box(top_width, top_length, top_height)
)

# Create a single cylindrical leg
leg = (
    cq.Workplane("XY")
    .circle(leg_diameter / 2)
    .extrude(leg_height)
)

# Add four legs to the table
legs = (
    leg
    .translate((inset_distance, inset_distance, top_height))
    .union(
        leg.translate((top_width - inset_distance, inset_distance, top_height))
    )
    .union(
        leg.translate((inset_distance, top_length - inset_distance, top_height))
    )
    .union(
        leg.translate((top_width - inset_distance, top_length - inset_distance, top_height))
    )
)

# Combine the top and legs
result = top.union(legs)

# Display the result (for visualization purposes)
show_object(result)