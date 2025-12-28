import cadquery as cq

# Parametric dimensions
base_diameter = 50 # mm
height = 60 # mm

# Create a cone with given parameters
cone = cq.Cylinder(r1=base_diameter/2, r2=0, h=height)
result = cone