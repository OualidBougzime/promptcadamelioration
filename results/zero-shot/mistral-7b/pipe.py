from cadquery import exporters, workplane, cylinder, faces, vertices, edges, chamfer, cube, Workplane, Vector

# Define the outer and inner radii, length, and chamfer thickness
outer_radius = 20.0
inner_radius = 15.0
length = 150.0
chamfer_thickness = 1.0

# Create a new workplane for the pipe
wp = Workplane("XY")

# Define the pipe shape with the given dimensions
pipe = cylinder(point=(0, 0, length / 2), radius=outer_radius - chamfer_thickness, height=length)
inner_pipe = cylinder(point=(0, 0, (length + chamfer_thickness) / 2), radius=inner_radius, height=length - 2 * chamfer_thickness)

# Offset the outer pipe to create a shell with the inner pipe
pipe_shell = pipe.faces(">Z").offsetDistance(chamfer_thickness).cut(inner_pipe)

# Create chamfers on both ends of the pipe
end_chamfer = chamfer(pipe_shell, distance=chamfer_thickness)

# Export the final shape as an .stl file
exporters.export(end_chamfer, "pipe.stl", format="stl")

# Store the final shape in a variable named 'result'
result = end_chamfer