import cadquery as cq

# Diameter of the sphere
diameter = 80

# Create a sphere with the specified diameter
result = (
    cq.Workplane("XY")
    .sphere(diameter / 2)
)

# Store the final shape in the 'result' variable