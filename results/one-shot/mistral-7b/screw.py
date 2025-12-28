import cadquery as cq

shaft_radius = 4
shaft_length = 50
head_diameter = 12
head_height = 5

result = (
    cq.Workplane("XY")
    .workplane(cq.Plane("Y", offset=shaft_radius))
    .circle(shaft_radius)
    .extrude(shaft_length)

    # Create hexagonal head
    .worksurface()
    .rect(head_diameter / 2, head_height)
    .workplane(cq.Plane("X", offset=-head_diameter / 2))
    .polyline([[0, 0], [head_diameter / 2, -head_height / 2],
               [head_diameter, 0], [-head_diameter / 2, head_height / 2],
               [0, head_height]])
    .workplane(cq.Plane("Y", offset=shaft_radius))
    .extrude(shaft_length)
)