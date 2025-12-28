import cadquery as cq

# Define parameters
base_radius = 30.0  # mm
mid_radius = 22.0   # mm
top_radius = 35.0    # mm
mid_height = 60.0   # mm
total_height = 120.0 # mm

# Create the profile for the vase
profile = (
    cq.Workplane("XY")
    .moveTo(base_radius, 0)
    .lineTo(mid_radius, mid_height)
    .lineTo(top_radius, total_height)
)

# Revolve the profile to create the vase
result = profile.revolve(axisStart=(0, 0, 0), axisEnd=(0, 0, 1))

# Display the result (for Jupyter Notebook or similar environment)
if "show_object" in globals():
    show_object(result)