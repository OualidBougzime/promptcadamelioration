import cadquery as cq

# Dimensions
outer_diameter = 60
inner_diameter = outer_diameter - 2 * 2  # 3 mm bottom thickness + 2 mm wall thickness
height = 100
fillet_radius = 1

# Create the base cylinder with chamfered top rim
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(height)
    .faces(">Z")
    .chamfer(fillet_radius)  # Fillet on top rim
)

# Hollow out the cylinder leaving the specified thickness
result = result.faces("<Z").cut(
    cq.Workplane("XY")
    .circle(inner_diameter / 2)
    .extrude(height)
)

# Store final shape in 'result' variable