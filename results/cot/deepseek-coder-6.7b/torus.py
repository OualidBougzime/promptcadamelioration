import cadquery as cq

# Define workplane (optional)
workplane = cq.Workplane('XY')

# Create torus using defined parameters
torus_shape = workplane.add(cq.Torus(50, 8))

# Extract edges of the torus
result = torus_shape.edges()