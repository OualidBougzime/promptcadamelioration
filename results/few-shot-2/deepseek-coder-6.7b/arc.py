import cadquery as cq

radius = 30 # Convert from mm to units of workplane (assuming units are mm)
angle = 210 # Degrees

# Create a new workplane at z=0 with the XY plane
result = (cq.Workplane("XY")
          .moveTo(0, 0) # Move to the origin
          .lineTo(radius, 0) # Draw a line from the origin to the right by radius
          .threePointArc((2*radius, radius), (radius, -2*radius)) # Draw an arc with the given center and endpoints
          .closePath() # Close the path
         )