import cadquery as cq

# Create an arc with radius 60 mm and sweep angle of 210 deg.
arc = (
    cq.Workplane("XY")
    .moveTo(cq.Vector(0, 0))
    .threePointArc((60, 0), (60, 210))
)

# Store the final shape in the 'result' variable.
result = arc