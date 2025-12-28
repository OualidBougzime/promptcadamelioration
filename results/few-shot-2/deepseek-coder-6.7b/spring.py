import cadquery as cq

# Define parameters
radius = 1.5 # mm
major_radius = 20 # mm
pitch = 8 # mm
total_height = 80 # mm

# Create the helix profile
helix = (cq.Workplane("XY")
          .moveTo(0, 0)
          .lineTo(-major_radius, 0)
          .spline([(0, -pitch), (major_radius-2*radius, -total_height+pitch)])
          .closePath()
         )

# Create the spring by sweeping a circle along the helix profile
result = (cq.Workplane("XY")
           .circle(radius)
           .sweep(helix)
          )