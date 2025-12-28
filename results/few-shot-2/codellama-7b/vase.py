import cadquery as cq

# Define the profile
profile = cq.Workplane("XY") \
    .circle(30) \
    .moveTo(-60, 0) \
    .lineTo(60, 0) \
    .moveTo(0, -22) \
    .lineTo(0, 22) \
    .moveTo(-60, 0) \
    .lineTo(60, 0) \
    .moveTo(0, -35) \
    .lineTo(0, 35) \
    .close()

# Revolve the profile to create the vase
result = cq.Workplane("XY") \
    .revolve(profile, angle=120, axis=(0, 0, 1))