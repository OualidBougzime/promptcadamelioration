import cadquery as cq

diameter = 80

# Create a sphere with given diameter
sphere = (
    cq.Workplane("XY")
    .circle(diameter / 2)
    .extrude(1) # extrude in z-direction to create the sphere
)

result = sphere