import cadquery as cq

arc_radius = 60
sweep_angle = 210

result = (
    cq.Workplane("XY")
    .circle(arc_radius)
    .workplane(offset=arc_radius, centerOption="CenterOfMass")
    .moveTo(0, arc_radius)
    .threePointArc((arc_radius * (1 - cq.util.cos(cq.util.toRadians(sweep_angle / 2))), 
                    arc_radius * (1 + cq.util.sin(cq.util.toRadians(sweep_angle / 2)))), 
                   (arc_radius * (1 - cq.util.cos(cq.util.toRadians(sweep_angle))), 0))
    .close()
)