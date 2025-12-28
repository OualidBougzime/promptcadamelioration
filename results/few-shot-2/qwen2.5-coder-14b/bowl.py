import cadquery as cq

radius = 40
wall_thickness = 3

# Create a semicircle and revolve it to form a hemisphere
hemisphere = (
    cq.Workplane("XY")
    .circle(radius)
    .workplane(offset=radius, centerOption="CenterOfMass")
    .lineTo(0, -radius)
    .close()
    .revolve()
)

# Shell the hemisphere with a wall thickness of 3 mm
result = (
    hemisphere
    .shell(wall_thickness)
)