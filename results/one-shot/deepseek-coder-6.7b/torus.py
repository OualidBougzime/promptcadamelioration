import cadquery as cq

major_radius = 50
minor_radius = 8

# Create a torus with given major and minor radius.
result = (
    cq.Workplane("XY")
     .add(cq.Cylinder((major_radius, minor_radius)))
)