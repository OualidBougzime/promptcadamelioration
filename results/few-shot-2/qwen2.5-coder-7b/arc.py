import cadquery as cq

# Define the parameters
radius = 60
sweep_angle = 210

# Create the arc
result = (
    cq.Workplane("XY")
    .arc((radius * (sweep_angle / 360)), radius, startAngle=0)
)

# Optionally, you can extrude or perform other operations on the arc if needed
# For example, extruding the arc to create a shape:
# result = result.extrude(10)  # Extrude along Z-axis by 10 mm