import cadquery as cq

base_diameter = 50
height = 60

result = (
    cq.Workplane("XY")
    .circle(base_diameter / 2)
    .extrude(height, taper=1.0)  # Taper parameter is set to 1.0 for a cone shape
)