from cadquery import exporters, workplane, cylinder, box, union

# Define the table top
top = box(size=(200, 100, 15))

# Define the leg dimensions and positioning
leg_diameter = 12
leg_height = 120
inset = 15

# Create the legs using workplane and cylinder functions
leg1 = cylinder(point=(inset, inset, top.Height()), radius=leg_diameter/2, height=leg_height)
leg2 = cylinder(point=(top.Width() - inset, inset, top.Height()), radius=leg_diameter/2, height=leg_height)
leg3 = cylinder(point=(inset, top.Depth() - leg_height - inset, top.Height()), radius=leg_diameter/2, height=leg_height)
leg4 = cylinder(point=(top.Width() - inset, top.Depth() - leg_height - inset, top.Height()), radius=leg_diameter/2, height=leg_height)

# Union the table top and legs to create the final model
result = union(top, leg1, leg2, leg3, leg4)