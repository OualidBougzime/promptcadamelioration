import cadquery as cq

# Dimensions
table_width = 200
table_length = 100
table_thickness = 15
leg_diameter = 12
leg_height = 120
leg_inset = 15

# Create the table
result = (
    cq.Workplane("XY")
    .rect(table_width, table_length)
    .extrude(table_thickness)
)

# Create a function to create a leg
def create_leg(workplane, xofs, yofs):
    return (
        cq.Workplane("XY", origin=(xofs, yofs))
        .circle(leg_diameter/2)
        .extrude(leg_height)
        .translate((0, 0, -leg_inset))
    )

# Add the legs to the table
result = result.union(create_leg(cq.Workplane("XY"), -table_width/2 + leg_diameter/2, -table_length/2 + leg_diameter/2))  # Bottom left
result = result.union(create_leg(cq.Workplane("XY"), table_width/2 - leg_diameter/2, -table_length/2 + leg_diameter/2))   # Bottom right
result = result.union(create_leg(cq.Workplane("XY"), -table_width/2 + leg_diameter/2, table_length/2 - leg_diameter/2))  # Top left
result = result.union(create_leg(cq.Workplane("XY"), table_width/2 - leg_diameter/2, table_length/2 - leg_diameter/2))   # Top right