import cadquery as cq

shaft_radius = 4
shaft_length = 50
head_diameter = 12
head_height = 5

result = (
    cq.Workplane("XY")
    .workplane(cq.Plane("YZ", offset=shaft_radius))
    .circle(shaft_radius)
    .extrude(shaft_length)

    .faces(">Z")
    .workplane()
    .rect(head_diameter / 2, head_height / 2)
    .moveTo(cq.Vector(0, 0, shaft_radius))
    .rotate(cq.CAngle(90, cq.DEGREE))
    .hexagon()
    .extrude(head_height)
)