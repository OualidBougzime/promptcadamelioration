import cadquery as cq

# Define the points for the smooth profile
points = [
    (0, 30),       # Base point
    (60, 22),      # Mid-height point
    (120, 35)      # Top point
]

# Create a workplane in the XY plane
result = (
    cq.Workplane("XY")
    .polyline(points)
    .sweep(cq.Vector(0, 0, 1))  # Revolve around the Z-axis
)

# Display the result
show_object(result)