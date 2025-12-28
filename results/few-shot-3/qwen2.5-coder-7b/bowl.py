import cadquery as cq

# Define the parameters
semicircle_radius = 40
wall_thickness = 3

# Create a semicircle
semicircle = (
    cq.Workplane("XY")
    .circle(semicircle_radius)
    .lineTo(0, -semicircle_radius)
    .close()
)

# Revolve the semicircle to form a hemisphere
hemisphere = semicircle.revolve()

# Create an inner sphere for shelling
inner_sphere_radius = semicircle_radius - wall_thickness
inner_sphere = cq.Workplane("XY").sphere(inner_sphere_radius).translate((0, 0, -semicircle_radius))

# Shell the hemisphere by subtracting the inner sphere
result = hemisphere.cut(inner_sphere)

# Optionally, chamfer the edges to smooth out the transition
result = result.edges().chamfer(1)