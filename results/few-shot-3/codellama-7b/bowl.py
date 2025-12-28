import cadquery as cq

# Create a semicircle with radius 40 mm
semicircle = (
    cq.Workplane("XY")
    .circle(40)
)

# Revolve the semicircle to create a hemisphere
hemisphere = semicircle.revolve()

# Shell the hemisphere with 3 mm wall thickness
result = hemisphere.shell(-3)