import cadquery as cq

# Define the parameters of the cone
diameter = 50
height = 60

# Create a workplane and add a circle to it
workplane = cq.Workplane("XY")
circle = workplane.circle(diameter / 2)

# Extrude the circle to create a cone
result = circle.extrude(height)

# Store the final shape in the 'result' variable
result = result

print(result)