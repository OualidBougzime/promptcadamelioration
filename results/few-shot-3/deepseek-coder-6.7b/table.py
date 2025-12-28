import cadquery as cq

# Define dimensions
top_width = 200
top_height = 100
top_thickness = 15
leg_diameter = 12
leg_height = 120
leg_inset = 15

# Create the top of the table
table_top = (
    cq.Workplane("XY")
    .box(top_width, top_height, top_thickness)
)

# Create a single leg
single_leg = (
    cq.Workplane("XY")
    .cylinder(leg_diameter/2, leg_height)
    .translate((0, 0, -leg_height/2)) # center the cylinder on the workplane
)

# Create four legs by translating the single leg to each corner of the table
leg1 = single_leg.translate((top_width/2-leg_inset, top_height/2-leg_inset, 0))
leg2 = single_leg.translate((-top_width/2+leg_inset, top_height/2-leg_inset, 0))
leg3 = single_leg.translate((-top_width/2+leg_inset, -top_height/2+leg_inset, 0))
leg4 = single_leg.translate((top_width/2-leg_inset, -top_height/2+leg_inset, 0))

# Combine all parts into the result variable
result = table_top.union(leg1).union(leg2).union(leg3).union(leg4)