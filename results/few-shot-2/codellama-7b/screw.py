import cadquery as cq

# Define the parameters for the screw
radius = 4
length = 50
head_diameter = 12
head_height = 5

# Create the cylindrical shaft
shaft = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(length)
)

# Create the hexagonal head
head = (
    cq.Workplane("XY")
    .circle(head_diameter / 2)
    .extrude(head_height)
)

# Assemble the screw
result = shaft.union(head)

# Store the final shape in the 'result' variable
result = result

print("The screw has a radius of", radius, "mm and a length of", length, "mm.")
print("The head has a diameter of", head_diameter, "mm and a height of", head_height, "mm.")