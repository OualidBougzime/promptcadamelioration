import cadquery as cq

# Define the profile of the vase
profile = (
    cq.Workplane("XY")
    .circle(30)
    .moveTo(-22, 0)
    .lineTo(22, 0)
    .moveTo(0, -22)
    .lineTo(0, 22)
    .close()
)

# Revolve the profile to create the vase
result = cq.Workplane("XY").revolve(profile, angle=360, axis=(0, 1, 0), point=(0, 0, 0))