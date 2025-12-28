import cadquery as cq

radius = 40
height = 2 * radius  # The height of the hemisphere is twice its radius
shell_thickness = 3

result = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(height / 2)  # Extrude half the height to create a semicircle
    .revolve(angle=180, axis=(0, 0, 1))  # Revolve the semicircle around the Z-axis
    .faces(">Z")
    .workplane()
    .shell(thickness=shell_thickness)  # Shell the hemisphere with the specified thickness
)