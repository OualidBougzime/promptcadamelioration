import cadquery as cq

# Define parameters
outer_radius = 20.0  # mm
inner_radius = 15.0  # mm
length = 150.0       # mm
chamfer_size = 1.0   # mm

# Create the pipe with chamfers on both ends
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(length)
    .faces(">Z")
    .edges()
    .fillet(chamfer_size)
    .faces("<Z")
    .edges()
    .fillet(chamfer_size)
)

# Optionally, you can add a hollow core to make it a pipe
result = result.cut(
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(length)
)

# Display the result (for Jupyter Notebook or similar environment)
# show_object(result)