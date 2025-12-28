import cadquery as cq

radius = 40
wall_thickness = 3

# Create a semicircle
semicircle = (
    cq.Workplane("XY")
    .circle(radius)
    .workplane(offset=radius, centerOption="CenterOfMass")
    .lineTo(0, -radius)
)

# Revolve the semicircle to form a hemisphere
hemisphere = semicircle.revolve()

# Shell the hemisphere with 3 mm wall thickness
result = hemisphere.shell(wall_thickness)