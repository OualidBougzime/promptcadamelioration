import cadquery as cq

# Define dimensions
r1 = 20  # outer radius
r2 = 15  # inner radius
l = 150  # length
d = 1  # chamfer radius

# Create a new sketch and apply geometric operations
result = (cq.Workplane("XY")
          .circle(r1)
          .extrude(l)
          .edges("|Z").fillet(d))