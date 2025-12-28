import cadquery as cq

# Parameters
arc_radius = 60
sweep_angle = 210

# Create an arc with a sweep angle of 210 degrees
result = (
    cq.Workplane("XY")
    .circle(arc_radius)
    .workplane(offset=arc_radius, centerOption="CenterOfMass")
    .moveTo(0, -arc_radius)
    .threePointArc((arc_radius * (1 - cq.math.tan(cq.math.radians(sweep_angle / 2))), 0), (0, arc_radius))
)

# Display the result
show_object(result)