import cadquery as cq

# Create a cube with dimensions 50mm x 50mm x 50mm
result = (
    cq.Workplane("XY")
    .box(50, 50, 50)
)