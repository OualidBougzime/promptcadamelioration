import cadquery as cq

# Define the dimensions of the table top
top_width = 200
top_length = 100
top_height = 15

# Define the dimensions of the legs
leg_diameter = 12
leg_height = 120
leg_inset = 15

# Create a rectangle for the table top
top = cq.Workplane("XY").rect(top_width, top_length).extrude(top_height)

# Add four cylindrical legs to the top
legs = []
for i in range(4):
    x = (i % 2) * leg_inset
    y = (i // 2) * leg_inset
    legs.append(top.faces(">Z").workplane().cylinder(diameter=leg_diameter, height=leg_height).translate((x, y, 0)))

# Union all parts
result = top.union(cq.Compound.makeCompound(legs))