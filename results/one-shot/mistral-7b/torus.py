import cadquery as cq

major_radius = 50
minor_radius = 8

result = (
    cq.Workplane("XY")
    .torus(major_radius, minor_radius)
    .extrude(10)  # Adjust this value to control the height of the torus
)