import cadquery as cq

# Define dimensions
outer_diameter = 60
inner_diameter = outer_diameter - 2 * 2  # Wall thickness is 2 mm
height = 100
bottom_thickness = 3
top_fillet_radius = 1

# Create the outer cylinder
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(height - bottom_thickness)  # Extrude to height minus bottom thickness
)

# Hollow out the cylinder
result = result.faces(">Z").workplane().circle(inner_diameter / 2).cutBlind(-height + bottom_thickness)

# Add fillet on top rim
result = result.edges("|Z and >X").fillet(top_fillet_radius)

# Display the result
show_object(result)