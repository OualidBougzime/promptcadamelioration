import cadquery as cq

# Define dimensions
outer_diameter = 60
height = 100
bottom_thickness = 3
wall_thickness = 2
fillet_radius = 1

# Create the outer cylinder
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(height)
)

# Hollow out the interior
result = result.faces(">Z").workplane().circle((outer_diameter / 2) - wall_thickness).cutBlind(-(height - bottom_thickness))

# Add fillet on top rim
result = result.edges(">Z").fillet(fillet_radius)

# Store final shape in 'result' variable