import cadquery as cq

# Define parameters
radius = 1.5 # mm
major_radius = 20 # mm
pitch = 8 # mm
total_height = 80 # mm

# Create the helix workplane
helix = (cq.Workplane("XY")
          .moveTo(0, 0)
          .lineTo(-major_radius, 0))

# Sweep a circle along the helix
result = (cq.Workplane("YZ").placeSketch(
    cq.Sketch().addCircle((0, 0), radius)
).transformed(offset=(0, -major_radius/2)).sweep(helix))

# Extrude to total height
result = result.extrude(total_height)