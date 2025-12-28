from cadquery import exporters, workplane, cylinder, revolve, circle, mesh, faces, bodies, vertices

# Initialize a new document
doc = workplane("XY")

# Create semicircle with radius 40 mm
arc_center = (0, 0, 0)
arc_radius = 40
semicircle = circle(arc_center, arc_radius).segment(180)

# Revolve the semicircle to create a hemisphere
hemisphere = revolve(semicircle, axis=(0, 0, arc_radius))

# Shell the hemisphere with a wall thickness of 3 mm
shelled_body = bodies.worksurface(faces.plane(vertices(hemisphere.edges()[0])), offset=3)
result = shelled_body + hemisphere

# Export the final shape as an STL file
exporters.write_stl(result, "bowl.stl")