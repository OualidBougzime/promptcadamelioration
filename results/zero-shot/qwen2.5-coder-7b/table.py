import cadquery as cq

# Define parameters for easy modification
table_top_length = 200.0  # mm
table_top_width = 100.0   # mm
table_top_height = 15.0   # mm
leg_diameter = 12.0       # mm
leg_height = 120.0        # mm
leg_inset = 15.0          # mm

# Create the rectangular top of the table
top = cq.Workplane("XY").rect(table_top_length, table_top_width).extrude(table_top_height)

# Create four cylindrical legs
legs = (
    cq.Workplane("XZ")
    .circle(leg_diameter / 2)
    .extrude(leg_height)
    .translate((table_top_length / 2 - leg_inset, table_top_width / 2 - leg_inset, 0))
    .union(
        cq.Workplane("XZ")
        .circle(leg_diameter / 2)
        .extrude(leg_height)
        .translate((-table_top_length / 2 + leg_inset, table_top_width / 2 - leg_inset, 0))
    )
    .union(
        cq.Workplane("XZ")
        .circle(leg_diameter / 2)
        .extrude(leg_height)
        .translate((table_top_length / 2 - leg_inset, -table_top_width / 2 + leg_inset, 0))
    )
    .union(
        cq.Workplane("XZ")
        .circle(leg_diameter / 2)
        .extrude(leg_height)
        .translate((-table_top_length / 2 + leg_inset, -table_top_width / 2 + leg_inset, 0))
    )
)

# Union the top and legs to create the final shape
result = top.union(legs)

# Display the result (optional, for interactive use in a Jupyter notebook or similar environment)
show_object(result)