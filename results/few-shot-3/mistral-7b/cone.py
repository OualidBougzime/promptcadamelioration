import cadquery as cq

base_diameter = 50
height = 60
cone_height = height - (base_diameter / 2)

result = (
    cq.Workplane("XY")
    .circle(base_diameter / 2)
    .extrude(cone_height)
)