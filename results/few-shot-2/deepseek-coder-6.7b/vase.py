import cadquery as cq

# Define dimensions
base_radius = 30  # mm
mid_height_radius = 22  # mm
top_radius = 35  # mm
vase_height = 120  # mm

# Create a profile for the vase
profile = (
    cq.Workplane("XY")
    .moveTo(base_radius, 0)
    .lineTo(mid_height_radius, vase_height/2)
    .lineTo(top_radius, vase_height)
    .lineTo(base_radius, vase_height)
    .close()
)

# Revolve the profile to create a vase
result = (
    cq.Workplane("YZ")  # YZ plane for revolving around y-axis
    .placeSketch(profile)
    .revolve(180, (0, 0, 0), (True, False, False))  # Rotate the profile 180 degrees about y-axis
)