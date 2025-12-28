import cadquery as cq

# Define the parameters for the arc
radius = 60
sweep_angle = 210

# Create the arc using CadQuery API
result = (
    cq.Workplane("XY")
    .arc(0, radius, (radius * 2) * (sweep_angle / 360), radius)
)

# Display the result
show_object(result)