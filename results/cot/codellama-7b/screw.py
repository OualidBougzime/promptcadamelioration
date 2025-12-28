import cadquery as cq

# Create a workplane at the origin
wp = cq.Workplane()

# Create the cylindrical shaft
cylinder = wp.cylinder(radius=4, length=50)

# Create the hexagonal head
hexagon = wp.hexagon(diameter=12, height=5, center=cylinder.endPoint())

# Combine the cylindrical shaft and hexagonal head into a single object
result = cq.Compound([cylinder, hexagon])