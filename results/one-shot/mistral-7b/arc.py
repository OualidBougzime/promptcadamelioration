import cadquery as cq

arc_radius = 60
sweep_angle = 210

result = (
    cq.Workplane("XY")
    .circle(arc_radius)
    .rotate(cq.CAngle(90, cq.Degrees))
    .sweepRev(cq.Arc(start=cq.Vector(0, 0, 0), end=cq.Vector(0, arc_radius*2*cq.Pi/3, 0), center=cq.Point(0, 0, 0)))
    .rotate(cq.CAngle(-90, cq.Degrees))
)