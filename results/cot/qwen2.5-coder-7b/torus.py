import cadquery as cq

# Step 1: Define the workplane (XY plane)
workplane = cq.Workplane("XY")

# Step 2: Create the torus on the defined workplane
torus = workplane.torus(major_radius=50, minor_radius=8)

# Step 3: Assign the result to a variable
result = torus

# Display the result (optional)
show_object(result)