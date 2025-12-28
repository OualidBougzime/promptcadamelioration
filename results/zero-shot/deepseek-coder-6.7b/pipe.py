import cadquery as cq

# Parameters
outer_radius = 20  # mm
inner_radius = 15  # mm
length = 150  # mm
chamfer_size = 1  # mm

# Create the pipe body
result = (cq.Workplane("XY")
          .circle(outer_radius)
          .extrude(length)
          .edges(f">Z and <Z")
          .fillet(chamfer_size))