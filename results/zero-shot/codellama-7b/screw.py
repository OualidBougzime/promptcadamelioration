import cadquery as cq

# Define the screw parameters
radius = 4
length = 50
head_diameter = 12
height = 5

# Create a cylindrical shaft
shaft = cq.Workplane().cylinder(radius, length)

# Create a hexagonal head
head = cq.Workplane().hexagon(head_diameter / 2, height).translate((0, 0, length))

# Assemble the screw
result = shaft.union(head)