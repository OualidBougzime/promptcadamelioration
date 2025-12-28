import cadquery as cq

# Define the dimensions of the table top
top_width = 200
top_length = 100
top_height = 15

# Define the dimensions of the legs
leg_diameter = 12
leg_height = 120
leg_inset = 15

# Create a rectangular top shape
top = cq.Workplane("XY").rect(top_width, top_length).extrude(top_height)

# Add four cylindrical legs to the top
legs = []
for i in range(4):
    x = leg_inset * (i % 2) - top_width / 2
    y = leg_inset * (i // 2) - top_length / 2
    legs.append(cq.Workplane("XY").circle(leg_diameter).extrude(leg_height).translate((x, y)))

# Union all parts
result = top.union(legs[0]).union(legs[1]).union(legs[2]).union(legs[3])