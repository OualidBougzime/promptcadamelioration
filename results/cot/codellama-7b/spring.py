import cadquery as cq

# Create a workplane at the origin
wp = cq.Workplane()

# Create a circle with radius 1.5 mm
circle = wp.circle(radius=1.5)

# Create a right-hand helix with major radius 20 mm, pitch 8 mm, and total height 80 mm
helix = wp.helix(major_radius=20, pitch=8, height=80)

# Sweep the circle along the helix
result = circle.sweep(helix)