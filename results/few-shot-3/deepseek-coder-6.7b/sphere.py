import cadquery as cq

diameter = 80
radius = diameter / 2

# Create a sphere with given radius
sphere = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(1) # extrude in z-direction to create the volume of the shape
)

result = sphere