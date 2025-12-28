import cadquery as cq

# Define the parameters for the drinking glass
outer_diameter = 60
height = 100
bottom_thickness = 3
wall_thickness = 2
fillet_radius = 1

# Create a cylinder with the outer diameter and height specified
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(height)
)

# Hollow out the bottom of the glass leaving the desired thickness
result = result.faces("<Z").workplane().circle((outer_diameter / 2) - wall_thickness).cutBlind(-(height - bottom_thickness))

# Add a fillet to the top rim of the glass
result = result.edges(">Z").fillet(fillet_radius)