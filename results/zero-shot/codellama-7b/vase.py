import cadquery as cq

# Define the profile of the vase
profile = cq.Workplane().circle(radius=30)

# Revolve the profile to create the vase
result = profile.revolve(angle=120, axis=(0, 0, 1), center=(0, 0, 60))

# Display the result
cq.show_object(result)