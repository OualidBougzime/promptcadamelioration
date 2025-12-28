import cadquery as cq

# Define parameters
radius = 1.5
major_radius = 20
pitch = 8
height = 80

# Create a right-hand helix
helix = (
    cq.Workplane("XY")
    .circle(major_radius)
    .sweep(cq.Vector(0, 1, 0), pitch)
    .extrude(height)
)

# Create a circle with radius 1.5 mm along the helix
circle = (
    cq.Workplane("XY")
    .circle(radius)
    .sweep(helix)
)

# Store final shape in 'result' variable
result = circle