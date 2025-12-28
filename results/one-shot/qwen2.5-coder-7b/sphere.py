import cadquery as cq

# Diameter of the sphere
diameter = 80
radius = diameter / 2

# Create the sphere
result = (
    cq.Workplane("XY")
    .sphere(radius)
)

# Display the result (optional, for visualization in a Jupyter notebook or similar environment)
show_object(result)