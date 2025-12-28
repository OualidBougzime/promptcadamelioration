import cadquery as cq

arc_radius = 60
sweep_angle = 210

result = (
    cq.Workplane("XY")
    .arc(center=(0, 0), radius=arc_radius, start_angle=0, end_angle=sweep_angle)
    .workplane()
    .rotate(cq.Vector(0, 0, 1), 90)
    .extrude(cq.Workplane("XY").size((0, 0, arc_radius * sweep_angle / 360)))
)