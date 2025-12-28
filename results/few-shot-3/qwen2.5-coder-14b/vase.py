import cadquery as cq

# Define the points for the vase profile
points = [
    (0, 30),   # Base radius at z=0
    (60, 22),  # Mid-height radius at z=60
    (120, 35)  # Top radius at z=120
]

# Create the vase profile by linearly interpolating between points
profile = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
)

# Revolve the profile around the Z-axis to create the vase
result = profile.revolve(axisStart=(0, 0, 0), axisEnd=(0, 0, 120))