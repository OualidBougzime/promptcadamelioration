import cadquery as cq

# Define dimensions
shaft_radius = 4    # mm
shaft_length = 50   # mm
head_diameter = 12  # mm
head_height = 5     # mm
chamfer = 1          # mm

# Create the shaft
result = (
    cq.Workplane("XY")
    .circle(shaft_radius)
    .extrude(shaft_length)
    .faces(">Z")
    .chamfer(chamfer)
    .faces("<Z")
    .chamfer(chamfer)
)

# Create the head
head = (
    cq.Workplane("XY").moveTo(-head_diameter/2, -head_height/2)
    .rect(head_diameter, head_height)
    .cutThruSlot((0, 0), (shaft_radius*2, shaft_length))
)

# Combine the two parts
result = result.union(head)