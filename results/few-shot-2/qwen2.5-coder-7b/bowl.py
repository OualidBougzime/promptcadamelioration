import cadquery as cq

# Define the parameters
radius = 40
wall_thickness = 3

# Create a semicircle
semicircle = (
    cq.Workplane("XY")
    .circle(radius)
    .lineTo(0, -radius)
    .close()
)

# Revolve the semicircle to form a hemisphere
hemisphere = semicircle.revolve()

# Shell the hemisphere with a wall thickness of 3 mm
result = (
    hemisphere
    .faces(">Z")
    .shell(wall_thickness)
)

# Display the result
show_object(result)