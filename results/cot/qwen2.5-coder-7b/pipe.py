import cadquery as cq

# Define dimensions
outer_radius = 20
inner_radius = 15
length = 150
chamfer_size = 1

# Create the pipe
pipe = cq.Workplane("XY").cylinder(radius=outer_radius, height=length)

# Apply chamfers on both ends
result = pipe.faces("<Z").chamfer(chamfer_size)
result = result.faces(">Z").chamfer(chamfer_size)

# Show the result
show_object(result)