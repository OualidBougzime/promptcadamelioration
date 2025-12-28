import cadquery as cq

major_radius = 50
minor_radius = 8

result = (
    cq.Workplane("XY")
    .circle(major_radius + minor_radius)
    .extrude(2 * minor_radius)
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .circle(minor_radius)
    .cutThruAll()
)

# Display the result
show_object(result)