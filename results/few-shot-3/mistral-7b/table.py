import cadquery as cq

top_width = 200
top_length = 100
top_height = 15
leg_diameter = 12
leg_height = 120
inset = 15

# Create rectangular top
result_top = (
    cq.Workplane("XY")
    .rect(top_width, top_length)
    .extrude(top_height)
)

# Create and position cylindrical legs
for i in range(4):
    for j in range(2):
        if i + j == 3:
            leg = (
                cq.Workplane("XY")
                .circle(leg_diameter / 2)
                .extrude(leg_height)
            )
            result_leg = leg.translate((i * (top_width + inset), j * (top_length + inset)))
        else:
            result_leg = cq.Workplane("Front").circle(leg_diameter / 2).extrude(leg_height) \
                .moveTo(cq.Vector(i * (top_width + inset), j * (top_length + inset)))
        if j == 0:
            result_leg = result_leg.mirrorPlane("XZ")
        elif i == 3:
            result_leg = result_leg.mirrorPlane("YZ")
        result_leg = result_top.cut(result_leg)

# Union all parts to create the final table shape
result = result_top.union(*[result_leg])