import cadquery as cq

top_width = 200
top_length = 100
top_height = 15
leg_diameter = 12
leg_height = 120
inset = 15

result = (
    cq.Workplane("XY")
    .rect(top_width, top_length)
    .extrude(top_height)

    # Create and position the legs
    .workplane()
    .for_each(lambda x: x.move((x.x(), x.y(), -inset)))
    .circle(leg_diameter / 2)
    .extrude(leg_height)

    # Union all parts to form the table
    .union()
)