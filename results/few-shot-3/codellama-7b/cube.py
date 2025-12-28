import cadquery as cq

# Create a new workplane
wp = cq.Workplane("XY")

# Define the size of the cube
size = (50, 50, 50)

# Create the cube
cube = wp.box(size[0], size[1], size[2])

# Store the final shape in the 'result' variable
result = cube