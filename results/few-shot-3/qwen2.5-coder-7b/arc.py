import cadquery as cq

# Define parameters
radius = 60
sweep_angle = 210

# Create the arc
arc = (
    cq.Workplane("XY")
    .circle(radius)
    .copyWorkplane()
    .rotate((0, 0, 0), (0, 0, 1), sweep_angle)
)

result = arc