import cadquery as cq

# Define dimensions
radius = 40
thickness = 3

# Create a semicircle
semicircle = (
    cq.Workplane("XY")
    .circle(radius)
    .workplane(offset=radius, centerOption="CenterOfMass")
    .lineTo(0, -radius)
)

# Revolve the semicircle to form a hemisphere
hemisphere = semicircle.revolve(axisStart=(0, 0, 0), axisEnd=(0, 0, 1))

# Shell the hemisphere with the specified thickness
result = hemisphere.shell(thickness)