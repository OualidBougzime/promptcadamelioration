import cadquery as cq

# Define dimensions
top_width = 200
top_height = 100
top_thickness = 15
leg_diameter = 12
leg_height = 120
inset = 15

# Create the rectangular top
top = (
    cq.Workplane("XY")
    .rect(top_width, top_height)
    .extrude(top_thickness)
)

# Create the cylindrical legs
legs = []
for i in range(4):
    leg = (
        cq.Workplane("XY")
        .circle(leg_diameter / 2)
        .extrude(leg_height)
        .translate((i * (top_width - inset) / 2, (1 - i % 2) * (top_height - inset) / 2))
    )
    legs.append(leg)

# Union the top with all four legs
result = top
for leg in legs:
    result = result.union(leg)