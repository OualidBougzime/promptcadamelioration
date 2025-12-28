import cadquery as cq

major_radius = 20
pitch = 8
total_height = 80
circle_radius = 1.5

result = (
    cq.Workplane("XY")
    .circle(circle_radius)
    .extrude(total_height, startAngle=0, endAngle=2 * cq.pi)
    . helicalPath(majorRadius=major_radius, pitch=pitch, direction="R")
)