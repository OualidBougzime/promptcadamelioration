import cadquery as cq

# Define the radius of semi-circle (20mm) and wall thickness (3mm)
semi_circle_radius = 20  # in mm
wall_thickness = 3  # in mm

# Create a workplane for semicircle
semi_circle = cq.Workplane('XY').moveTo(semi_circle_radius, 0).lineTo(-semi_circle_radius, 0)

# Revolve the semi-circle to get hemisphere
hemisphere = semi_circle.revolve()

# Extrude the hemisphere to give it thickness
result = hemisphere.extrude(wall_thickness)