import cadquery as cq

# Define parameters
radius = 40  # Radius of the semicircle in mm
wall_thickness = 3  # Wall thickness in mm

# Create a semicircle
semicircle = cq.Workplane("XY").circle(radius).revolve(180)

# Shell the semicircle to create a hemisphere
hemisphere = semicircle.shell(wall_thickness)

# Store the final shape in the variable 'result'
result = hemisphere