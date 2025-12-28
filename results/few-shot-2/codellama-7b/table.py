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
for i in range(4):
    leg = cq.Workplane("XY").circle(leg_diameter / 2).extrude(leg_height).translate((i * (top_width + leg_inset), 0))
    top = top.union(leg)

# Store the final shape in the 'result' variable
result = top