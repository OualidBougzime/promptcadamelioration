from cadquery import *

# Parameters
outer_diameter = 60  # mm
height = 100  # mm
bottom_thickness = 3  # mm
wall_thickness = 2  # mm
fillet_radius = 1  # mm

# Create cylinder
cylinder = cq.Cylinder(r=outer_diameter/2, h=height)

# Cut out bottom and top to create a shell with the desired thickness
shell = cylinder.cut(cq.Cylinder(r=outer_diameter/2 - wall_thickness, h=bottom_thickness))
shell = shell.cut(cq.Cylinder(r=outer_diameter/2 - bottom_thickness, h=height - 2*bottom_thickness).translate((0,0,-1)))

# Fillet the top rim
result = shell.faces(">Z").workplane().circle(fillet_radius).cutThruSlot()