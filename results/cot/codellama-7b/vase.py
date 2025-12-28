import cadquery as cq

# Create a workplane at the origin
base = cq.Workplane()

# Move the workplane along the Z axis by 30 mm
base = base.transformed(offset=cq.Vector(z=30))

# Revolve the profile around the Z axis
result = base.revolve(profile=cq.Circle(radius=22), angle=180)

# Move the result along the Z axis by 60 mm
result = result.transformed(offset=cq.Vector(z=60))

# Revolve the profile around the Z axis again
result = result.revolve(profile=cq.Circle(radius=35), angle=180)

# Move the result along the Z axis by 90 mm
result = result.transformed(offset=cq.Vector(z=90))