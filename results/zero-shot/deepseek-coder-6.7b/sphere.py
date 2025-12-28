import cadquery as cq

# Parametric dimension for the diameter
diameter = 80 #mm
radius = diameter / 2

# Create a sphere using CadQuery
sphere = cq.Workplane("XY").sphere(radius)
result = sphere