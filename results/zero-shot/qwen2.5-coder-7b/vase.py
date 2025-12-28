import cadquery as cq

# Define parametric dimensions
base_radius = 30.0  # mm
mid_height = 60.0   # mm
top_radius = 35.0   # mm
total_height = 120.0  # mm

# Create the smooth profile
profile = cq.Workplane("XY") \
    .circle(base_radius) \
    .moveTo(0, mid_height / 2) \
    .lineTo(mid_height / 2, top_radius) \
    .lineTo(-mid_height / 2, top_radius) \
    .lineTo(0, -mid_height / 2) \
    .close()

# Revolve the profile around the Z-axis to create the vase
result = cq.Workplane("XY") \
    .center(0, total_height / 2) \
    .revolve(360, (0, 0, 0), (0, 0, 1))

# Display the result
show_object(result)