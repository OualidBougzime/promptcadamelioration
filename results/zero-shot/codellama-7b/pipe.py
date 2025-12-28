import cadquery as cq

# Define the pipe parameters
outer_radius = 20.0
inner_radius = 15.0
length = 150.0
chamfer_width = 1.0

# Create a new CadQuery object
pipe = cq.Workplane("XY").moveTo(0, 0)

# Add the outer radius to the pipe
pipe = pipe.circle(outer_radius).extrude(length)

# Add the inner radius to the pipe
pipe = pipe.circle(inner_radius).cutThruAll()

# Add the chamfer to the ends of the pipe
pipe = pipe.edges("|Z").fillet(chamfer_width)

# Store the final shape in a variable named 'result'
result = pipe