import cadquery as cq

# Create a workplane for the top and legs
top = cq.Workplane("XY").rect(200, 100)

# Create a rectangular top
top_rect = top.rect(200, 100)

# Create four cylindrical legs inset 15 mm from each corner under the top
legs = []
for i in range(4):
    x = (i % 2) * 15
    y = (i // 2) * 15
    leg = top_rect.translate((x, y)).cylinder(d=12, h=120)
    legs.append(leg)

# Union all parts
result = cq.Union(top_rect, *legs)