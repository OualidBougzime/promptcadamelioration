import cadquery as cq

# Define parametric dimensions
radius = 60.0  # Radius in millimeters
sweep_angle = 210.0  # Sweep angle in degrees

# Create an arc with the specified radius and sweep angle
result = cq.Workplane("XY").arc(0, 0, radius, startAngle=0, endAngle=sweep_angle)

# Display the result (optional)
show_object(result)