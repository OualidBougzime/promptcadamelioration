import cadquery as cq

# Step 1: Define the workplane
base = cq.Workplane("XY")

# Step 2: Create the smooth profile
profile = (
    base.circle(30)  # Base circle at radius 30 mm
    .lineTo(0, 60)  # Line to mid-height point (x=0, y=60)
    .circle(22)      # Mid-height circle at radius 22 mm
    .lineTo(0, 120) # Line to top point (x=0, y=120)
    .circle(35)      # Top circle at radius 35 mm
)

# Step 3: Revolve the profile to create the vase
result = profile.revolve()

# Display the result
show_object(result)