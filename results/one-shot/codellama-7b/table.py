import cadquery as cq

# Define the dimensions of the table
top_width = 200
top_length = 100
leg_diameter = 12
leg_height = 120
inset = 15

# Create the top of the table as a rectangular solid
top = (
    cq.Workplane("XY")
    .rect(top_width, top_length)
    .extrude(15)
)

# Create the legs of the table as four cylinders
legs = []
for i in range(4):
    x = (i % 2) * (top_width / 2 - inset)
    y = (i // 2) * (top_length / 2 - inset)
    legs.append(
        cq.Workplane("XY")
        .transformed(offset=(-x, -y))
        .cylinder(diameter=leg_diameter, height=leg_height)
    )

# Union the top and legs of the table
result = top.union(legs)

# Store the final shape in the 'result' variable
result = result.val()