import cadquery as cq

# Step 1: Create a workplane (optional)
# workplane = cq.Workplane("XY")

# Step 2: Create the sphere
radius = 40  # Radius is half of the diameter
result = cq.Workplane().sphere(radius)

# Display the result
show_object(result)