import cadquery as cq

# Define parameters
outer_diameter = 60.0  # mm
height = 100.0         # mm
bottom_thickness = 3.0 # mm
wall_thickness = 2.0   # mm
rim_fillet_radius = 1.0 # mm

# Calculate inner dimensions
inner_diameter = outer_diameter - 2 * wall_thickness

# Create the outer cylinder
outer_cylinder = cq.Workplane("XY").circle(outer_diameter / 2).extrude(height)

# Create the inner cylinder
inner_cylinder = cq.Workplane("XY").circle(inner_diameter / 2).extrude(height + bottom_thickness)

# Hollow out the glass by subtracting the inner cylinder from the outer cylinder
glass = outer_cylinder.cut(inner_cylinder)

# Add fillet to the top rim
result = glass.edges("|Z and >X").fillet(rim_fillet_radius)

# Display the result (for CadQuery GUI)
show_object(result)