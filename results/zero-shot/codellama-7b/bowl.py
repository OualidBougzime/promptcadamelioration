import cadquery as cq

# Define the semicircle radius
radius = 40.0

# Create a semicircle using the CadQuery API
semicircle = cq.Workplane().circle(radius=radius)

# Revolve the semicircle to form a hemisphere
hemisphere = semicircle.revolve()

# Shell the hemisphere with a 3mm wall thickness
result = hemisphere.shell(thickness=3.0, chamfer_size=0)