import cadquery as cq

# Create a new workplane at the origin
wp = cq.Workplane()

# Create a cylinder with the specified dimensions
cylinder = wp.cylinder(diameter=50, height=60)

# Get the result of the operation
result = cylinder.val()