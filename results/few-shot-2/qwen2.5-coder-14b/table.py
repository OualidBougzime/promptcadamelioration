import cadquery as cq

# Define dimensions
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

# Create a single leg
leg = (
    cq.Workplane("XY")
    .circle(leg_diameter / 2)
    .extrude(leg_height)
)

# Position and union all four legs to the table
result = top

for x_offset in [-1, 1]:
    for y_offset in [-1, 1]:
        result = (
            result
            .union(
                leg.translate((x_offset * (top_length / 2 - inset_distance), 
                               y_offset * (top_width / 2 - inset_distance), 
                               top_thickness))
            )
        )

# Store the final shape in 'result' variable