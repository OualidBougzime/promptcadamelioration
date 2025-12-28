import cadquery as cq

radius = 30    # Convert to meters
angle_degrees = 210   # Sweep angle in degrees

# Create arc and store it in 'arc' variable
arc = (cq.Workplane("XY")
       .moveTo(radius, 0)
       .circle(radius, traversedPerimeter=False)
       .cutThruSlot2D((0, radius), angle_degrees))

# Store final shape in 'result' variable
result = arc