import cadquery as cq

# Define parameters
diameter = 40  # Diameter in millimeters
height = 60    # Height in millimeters

# Create a cylinder using CadQuery API
result = (
    cq.Workplane("XY")
    .circle(diameter / 2)
    .extrude(height)
)

# Display the result (for visualization purposes, not required for storing the shape)
show_object(result)