import cadquery as cq

# Step 1: Create a workplane
result = cq.Workplane("XY")

# Step 2: Draw a rectangle (base of the cylinder)
diameter = 40
radius = diameter / 2
height = 60

# The rectangle's width should be equal to the diameter and height to form a circle when extruded
rectangle = result.rect(diameter, height)

# Step 3: Extrude the rectangle to form a cylinder
cylinder = rectangle.extrude(height)

# Assign the final result to the 'result' variable
result = cylinder

# Display the result (optional)
show_object(result)