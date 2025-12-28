import cadquery as cq

# Define the outer diameter and height of the cylinder
outer_diameter = 60
height = 100

# Define the bottom thickness and wall thickness of the hollowed out cylinder
bottom_thickness = 3
wall_thickness = 2

# Define the fillet radius on the top rim
fillet_radius = 1

# Create a new CadQuery object
result = cq.Workplane("XY")

# Add a cylinder to the object with the given outer diameter and height
cylinder = result.cylinder(outer_diameter, height)

# Hollow out the cylinder leaving the bottom thickness and wall thickness
hollowed_cylinder = cylinder.faces(">Z").workplane().hollow(bottom_thickness + wall_thickness)

# Add a fillet to the top rim of the hollowed cylinder
filleted_cylinder = hollowed_cylinder.faces("<Z").workplane().transformed(offset=(-1, 0, 0)).fillet(fillet_radius).val()

# Assign the final shape to the 'result' variable
result = filleted_cylinder

print("The resulting shape is:")
print(result)