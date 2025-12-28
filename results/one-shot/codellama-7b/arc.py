import cadquery as cq

# Define the parameters for the arc
radius = 60
sweep_angle = 210

# Create a workplane and add an arc to it
result = (
    cq.Workplane("XY")
    .moveTo(cq.Vector(0, 0))
    .arc(radius, sweep_angle)
)

# Display the final shape
print(result)