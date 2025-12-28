import cadquery as cq

radius = 40
wall_thickness = 3

# Create semicircle
semicircle = cq.Workplane("XY").circle(radius).sectionPlane(cq.Plane("Z", offset=radius)).cutBlind(-radius)

# Revolve the semicircle to form a hemisphere
bowl = semicircle.revolve(angle=180, axis=(0, 0, 1))

# Shell the hemisphere with specified wall thickness
result = bowl.faces(">Z").workplane().circle(radius - wall_thickness).cutBlind(-wall_thickness * 2).shell()