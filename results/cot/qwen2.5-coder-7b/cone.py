import cadquery as cq

# Step 1: Create a workplane (XY plane)
workplane = cq.Workplane("XY")

# Step 2: Use the cone method to create the cone
cone = workplane.cone(bottomRadius=50 / 2, topRadius=0, height=60)

# Assign the result to the variable 'result'
result = cone

# Optionally, you can visualize the result using a viewer
show_object(result)