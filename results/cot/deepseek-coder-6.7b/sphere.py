import cadquery as cq

# Define the dimensions
diameter = 80  # mm

# Create the workplane and add the sphere
result = (cq.Workplane('XY')
          .sphere(diameter / 2))