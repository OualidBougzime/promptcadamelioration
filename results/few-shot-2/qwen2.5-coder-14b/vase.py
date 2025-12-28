import cadquery as cq

# Define the profile points for the vase
profile_points = [
    (30, 0),   # Base radius at z=0
    (22, 60),  # Mid-height radius at z=60
    (35, 120)  # Top radius at z=120
]

# Create the profile by connecting the points with a smooth curve
profile = cq.Workplane("XY").polyline(profile_points).close()

# Revolve the profile around the Z-axis to create the vase shape
result = profile.revolve(axisStart=(0, 0, 0), axisEnd=(0, 0, 120))

# Optionally, you can add a fillet to smooth out the edges if needed
# result = result.edges("|Z").fillet(2)