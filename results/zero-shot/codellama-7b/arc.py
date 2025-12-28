import cadquery as cq

# Define the radius and sweep angle of the arc
radius = 60.0
sweep_angle = 210.0

# Create a new CadQuery object
result = cq.Workplane()

# Add an arc to the object
result = result.moveTo(cq.Vector(0, 0))
result = result.addArc(radius, sweep_angle)

# Display the final shape
print(result)