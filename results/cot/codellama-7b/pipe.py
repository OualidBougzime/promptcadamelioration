import cadquery as cq

# Define the dimensions of the pipe
R = 20  # outer radius
r = 15  # inner radius
L = 150  # length
w = 1  # chamfer width

# Create a new workplane at the origin
wp = cq.Workplane()

# Create the cylindrical shape with the given outer and inner radii and length
cylinder = wp.cylinder(R, r, L)

# Add chamfers to the ends of the cylinder
chamfered_cylinder = cylinder.chamfer(w)

# Display the resulting shape
result = cq.Display(chamfered_cylinder)