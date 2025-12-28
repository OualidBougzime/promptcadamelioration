import cadquery as cq

# Define key dimensions and parameters
radius = 40 / 2  # Diameter/2
height = 60      # Height

# Use CadQuery methods to generate shapes
result = cq.Cylinder(r=radius, h=height)