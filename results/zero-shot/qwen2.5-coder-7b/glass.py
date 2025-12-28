import cadquery as cq

# Define parameters for easy modification
outer_diameter = 60.0  # mm
height = 100.0  # mm
bottom_thickness = 3.0  # mm
wall_thickness = 2.0  # mm
rim_fillet_radius = 1.0  # mm

# Calculate inner dimensions based on the parameters
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = inner_diameter / 2
outer_radius = outer_diameter / 2

# Create the base cylinder with a hole for the hollow part
base_cylinder = cq.Workplane("XY").cylinder(height, outer_radius)

# Create the hollowed-out part of the glass
hollow_cylinder = cq.Workplane("XY").cylinder(height - bottom_thickness, inner_radius)

# Subtract the hollowed-out part from the base cylinder
result = base_cylinder.cut(hollow_cylinder)

# Add a fillet to the top rim
result = result.edges("|Z").fillet(rim_fillet_radius)

# Display the final shape (optional)
show_object(result)