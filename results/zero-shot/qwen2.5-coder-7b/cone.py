import cadquery as cq

# Define parametric dimensions
base_diameter = 50.0  # in millimeters
height = 60.0  # in millimeters

# Calculate radius from diameter
radius = base_diameter / 2

# Create the cone using CadQuery API
result = cq.Workplane("XY").cone(radius, height)

# Display the result (optional)
show_object(result)