import cadquery as cq

radius = 60
sweep_angle = 210

result = (
    cq.Workplane("XY")
    .circle(radius)
    .workplane(offset=radius)
    .moveTo(0, radius)
    .threePointArc((radius * (1 - cq.util.cos(cq.util.toRadians(sweep_angle / 2))), 
                    radius * (1 + cq.util.sin(cq.util.toRadians(sweep_angle / 2)))), 
                   (radius * (1 - cq.util.cos(cq.util.toRadians(sweep_angle))), 0))
    .close()
)