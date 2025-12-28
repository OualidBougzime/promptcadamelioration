import cadquery as cq

# Create a new workplane (XY plane)
workplane = cq.Workplane("XY")

# Create a cube with dimensions 50 mm x 50 mm x 50 mm
cube = workplane.box(50, 50, 50)

# Finalize the construction and assign it to the result variable
result = cube.finalize()