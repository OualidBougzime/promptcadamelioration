from cadquery import exporters, workplane, cylinder, faces, vertices, fillet, offset, bodies, merge

# Import necessary modules
import cadquery as cq

# Define the parameters for the drinking glass
outer_diameter = 60.0
height = 100.0
bottom_thickness = 3.0
wall_thickness = 2.0
top_fillet_radius = 1.0

# Create a new working plane at the origin
glass_body = workplane("XY")

# Create the outer cylinder of the glass
outer_cylinder = cylinder(point=(0, 0, height), radius=outer_diameter / 2 - wall_thickness)

# Offset the outer cylinder to create the inner wall
inner_wall = offset(wall_thickness)(outer_cylinder)

# Subtract the bottom thickness from the base of the glass
bottom_base = bodies.worksurface(vertices=inner_wall.edges("|Z").vertices()).extrude(bottom_thickness)
glass_body = glass_body - bottom_base

# Add a fillet on the top rim of the glass
top_rim = faces('|Z', inner_wall).first()
top_fillet = fillet(top_rim, radius=top_fillet_radius)
glass_body = glass_body.cut(top_fillet)

# Export the final shape as an .stl file
exporters.export(cq.worksessions["default"].active(), "drinking_glass.stl", format="stl")

# Store the final shape in a variable named 'result'
result = glass_body