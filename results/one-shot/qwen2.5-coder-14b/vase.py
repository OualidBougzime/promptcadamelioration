import cadquery as cq

# Define the points for the profile
points = [
    (0, 30),   # Base radius at z=0
    (60, 22),  # Mid-height radius at z=60
    (120, 35)  # Top radius at z=120
]

# Create a workplane and make a spline from the points
result = (
    cq.Workplane("XY")
    .spline(points)
    .revolve()
)

# Display the result
show_object(result)