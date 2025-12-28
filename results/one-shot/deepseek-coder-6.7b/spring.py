import cadquery as cq

# Define dimensions
outer_radius = 1.5 # mm
length = 80 # mm
pitch = 8 # mm
major_radius = 20 # mm

# Create helix workplane
helix = (cq.Workplane("XY")
          .moveTo(0, 0)
          .circle(center=(0, major_radius))
          .sweep(cq.Vector(-length, 0), False)
         )

# Extrude helix to create spring
result = (helix.extrude(pitch)
           .faces(">Z")
           .chamfer(1)
           .edges("|Z")
           .fillet(1)
          )