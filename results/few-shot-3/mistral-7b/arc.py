import cadquery as cq

arc_radius = 60
sweep_angle = 210

result = (
    cq.Workplane("XY")
    .arc(center=(0, 0), radius=arc_radius, start_angle=0, end_angle=sweep_angle)
    .workplane()
    .rotate(90)
    .extrude(2 * cq.pi * arc_radius / 360 * sweep_angle)
)