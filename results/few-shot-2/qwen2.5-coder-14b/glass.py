import cadquery as cq

# Define dimensions
diameter = 60
height = 100
bottom_thickness = 3
wall_thickness = 2
fillet_radius = 1

# Create the outer cylinder
result = (
    cq.Workplane("XY")
    .circle(diameter / 2)
    .extrude(height)
)

# Hollow out the interior to create the wall thickness
result = result.faces(">Z").workplane().circle((diameter / 2) - wall_thickness).cutBlind(-(height - bottom_thickness))

# Add a fillet on the top rim
result = result.edges("|Z and >X").fillet(fillet_radius)

# Store the final shape in 'result'