import cadquery as cq

radius = 40
wall_thickness = 3

# Create a semicircle with radius 'radius'
semi_circle = (cq.Workplane("XY")
               .moveTo(radius, 0)
               .lineTo(-radius, 0))

# Revolve the semi-circle to create a hemisphere
result = semi_circle.revolve()

# Shell out the original shape by 'wall_thickness'
shell = result.faces(">Z").workplane().move(z=-wall_thickness).box(2*radius, 2*radius, wall_thickness)
result = shell.cutThruAll()