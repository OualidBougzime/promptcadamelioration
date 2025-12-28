import cadquery as cq

# Define parameters for the pipe
outer_radius = 20.0  # mm
inner_radius = 15.0  # mm
length = 150.0       # mm
chamfer_size = 1.0    # mm

# Create a workplane in the XY plane
workplane = cq.Workplane("XY")

# Draw an outer circle and then subtract the inner circle to create the pipe shape
pipe_shape = (
    workplane.circle(outer_radius)
    .circle(inner_radius, mode="s")
    .extrude(length)
)

# Add chamfers to both ends of the pipe
result = pipe_shape.faces("<Z").chamfer(chamfer_size)
result = result.faces(">Z").chamfer(chamfer_size)

# Display the final shape
show_object(result)