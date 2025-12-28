import cadquery as cq

# Define parametric dimensions
radius = 40.0  # Radius of the semicircle
thickness = 3.0  # Wall thickness

# Create a semicircle
semicircle = cq.Workplane("XY").circle(radius).workplane(offset=radius, invert=True).lineTo(0, radius * 2)

# Revolve the semicircle to form a hemisphere
hemisphere = semicircle.revolve(axisStart=(0, 0, 0), axisEnd=(0, 0, 1))

# Shell the hemisphere with the specified thickness
result = hemisphere.shell(thickness)

# Display the result (for visualization purposes)
show_object(result)