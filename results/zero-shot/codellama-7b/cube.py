import cadquery as cq

# Define the size of the cube
size = 50

# Create a new empty object
obj = cq.Workplane()

# Add a cube to the object with the specified size
result = obj.box(size, size, size)