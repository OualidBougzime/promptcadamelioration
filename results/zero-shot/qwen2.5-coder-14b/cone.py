import cadquery as cq

# Define parametric dimensions
base_diameter = 50  # Base diameter in millimeters
height = 60         # Height in millimeters

# Create the cone using CadQuery API
result = (
    cq.Workplane("XY")
    .circle(base_diameter / 2)
    .extrude(height, taper=-base_diameter / height)
)

# Display the result (for Jupyter Notebook or similar environment)
# show_object(result)