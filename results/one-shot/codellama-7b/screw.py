import cadquery as cq

# Define the dimensions of the screw
radius = 4
length = 50
head_diameter = 12
head_height = 5

# Create a cylindrical shaft
shaft = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(length)
)

# Create a hexagonal head
head = (
    cq.Workplane("YZ")
    .transformed(cq.Rotation.from_axis_angle((1, 0, 0), 30))
    .circle(head_diameter / 2)
    .extrude(head_height)
)

# Create a screw by combining the shaft and head
result = shaft.union(head)

# Store the final shape in the 'result' variable
result = result

# Print the resulting CAD model to STDOUT
print(result.wrapped.to_sat())