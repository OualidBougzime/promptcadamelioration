import cadquery as cq

# Define parametric dimensions
radius = 60  # Radius of the arc in millimeters
sweep_angle = 210  # Sweep angle in degrees

# Create an arc using CadQuery
result = (
    cq.Workplane("XY")
    .circle(radius)
    .workplane(offset=radius, centerOption="CenterOfMass")
    .moveTo(0, radius)
    .threePointArc((radius * cq.math.tan(cq.math.radians(sweep_angle / 2)), -radius), (0, -radius))
)

# Display the result (for interactive use in Jupyter Notebook or similar environments)
show_object(result)