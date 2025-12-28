import cadquery as cq

diameter = 40
height = 60

result = (
    cq.Workplane("XY")
    .circle(diameter / 2)
    .extrude(height)
)

# Chamfers are not explicitly required for a cylinder, but if you want to add them:
# result = result.faces(">Z").chamfer(1)
# result = result.faces("<Z").chamfer(1)