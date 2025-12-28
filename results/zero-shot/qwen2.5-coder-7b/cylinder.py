import cadquery as cq

# Define parametric dimensions
diameter = 40
height = 60

# Create the cylinder using CadQuery API
result = cq.Workplane("XY").cylinder(d=diameter, h=height)

# Display the result (optional)
show_object(result)