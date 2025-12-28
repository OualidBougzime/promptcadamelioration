import cadquery as cq

base_radius = 30
mid_radius = 22
top_radius = 35
height = 120
chamfer = 1

result = (
    cq.Workplane("XY")
    .circle(base_radius)
    .extrude(height / 2)
    .faces(">Z")
    .revolve(angle=cq.Cylinder(start=0, end=height, radius=base_radius).height())

    .worksurface()
    .circle(mid_radius)
    .extrude(height / 2 - height / 3)

    .faces(">Z")
    .revolve(angle=cq.Cylinder(start=(height / 2), end=(height / 2 + height / 3), radius=mid_radius).height())

    .worksurface()
    .circle(top_radius)
    .extrude(height / 2 - height)

    .faces(">Z")
    .chamfer(chamfer)
    .faces("<Z")
    .chamfer(chamfer)
)