import cadquery as cq

# Define dimensions
shaft_radius = 4  # in mm
shaft_length = 50  # in mm
head_diameter = 12  # in mm
head_height = 5  # in mm

# Create cylindrical shaft
shaft = cq.Cylinder(shaft_radius, shaft_length)

# Define hexagonal head parameters
points = [(0, -head_diameter / 2), (head_diameter * 3 ** 0.5 / 4, -head_height / 2), 
          (head_diameter * 3 ** 0.5 / 4, head_height / 2), (0, head_diameter / 2)]
faces = [(0, 1, 2, 3)]

# Create hexagonal head and subtract it from shaft
head = cq.Workplane().polyhedron(points=points, faces=faces)
result = shaft.cut(head)