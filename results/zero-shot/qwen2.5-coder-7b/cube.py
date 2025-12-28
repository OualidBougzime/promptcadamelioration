import cadquery as cq

# Define the size of the cube using a parameter
cube_size = 50.0  # in millimeters

# Create the cube using the parametric dimension
result = cq.Workplane("XY").box(cube_size, cube_size, cube_size)

# Display the result (optional)
show_object(result)