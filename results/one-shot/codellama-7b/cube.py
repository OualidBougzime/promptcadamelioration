import cadquery as cq

# Create a cube with dimensions 50 mm x 50 mm x 50 mm
result = (
    cq.Workplane("XY")
    .box(50, 50, 50)
)