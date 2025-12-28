import cadquery as cq

# Define the profile of the vase
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(30, 0)
    .lineTo(35, 60)
    .lineTo(22, 120)
    .close()
)

# Revolve the profile to create a vase
result = cq.Workplane("XY").revolve(profile, angle=360, axis=(0, 0, 1), point=(0, 0, 0))

# Store the final shape in the 'result' variable
result = result.val()