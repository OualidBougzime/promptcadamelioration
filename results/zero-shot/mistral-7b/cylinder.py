from cadquery import exporters, workplane, cylinder, CQ, Workplane

# Initialize the CadQuery workspace
cq = CQ()

# Create a workplane for the model
wp_base = workplane("XY")

# Define the cylinder with parametric dimensions
cylinder_diameter = 40.0
cylinder_height = 60.0
cylinder_obj = wp_base.workplane(center=(0, 0, cylinder_height / 2)).cylinder(radius=cylinder_diameter / 2, height=cylinder_height)

# Store the final shape in the 'result' variable
result = cylinder_obj

# Export the model to an .stl file (optional)
exporters.export(result, "cylinder.stl", format="stl")