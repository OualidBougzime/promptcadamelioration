import cadquery as cq

shaft_radius = 4    # in mm
shaft_length = 50   # in mm
head_diameter = 12  # in mm
head_height = 5      # in mm

# Create the shaft of the screw
result = (
    cq.Workplane("XY")
     .circle(shaft_radius)
     .extrude(shaft_length)
)

# Create the head of the screw
head = (
    cq.Workplane("XY").moveTo(-head_diameter/2, -head_height/2)
    .rect(head_diameter, head_height)
    .cutThruSlot((shaft_radius*2), (shaft_length-10))  # cut a slot in the top of hexagon for screw head to pass through
)

# Combine the shaft and head into one solid
result = result.union(head)