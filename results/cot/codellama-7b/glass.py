import cadquery as cq

# Create a new workplane
wp = cq.Workplane()

# Create the cylinder
cylinder = wp.cylinder(d=60, h=100)

# Hollow out the cylinder to leave 3 mm at the bottom and 2 mm on the walls
hollowed_cylinder = cq.HollowCylinder(cylinder, b=3, w=2)

# Add a fillet to the top rim of the cylinder
filleted_cylinder = hollowed_cylinder.fillet(1)

# Display the final result
result = filleted_cylinder.show()