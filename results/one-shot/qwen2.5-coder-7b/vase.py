import cadquery as cq

# Define the points for the smooth profile
points = [
    (0, 30),       # Base point at radius 30 mm
    (60, 22),      # Mid-height point at radius 22 mm
    (120, 35)      # Top point at radius 35 mm
]

# Create a workplane in the XY plane
result = cq.Workplane("XY")

# Draw a spline through the defined points to create the smooth profile
profile = result.polyline(points).spline()

# Revolve the profile around the Z-axis to create the vase
result = profile.revolve(360)

# Optionally, you can chamfer the edges if needed
# result = result.edges().chamfer(chamfer_value)

# Display the final shape
show_object(result)