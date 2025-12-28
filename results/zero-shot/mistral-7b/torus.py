from cadquery import exporters, workplane, torus, cm

# Initialize a new model
model = cadquery.Workplane("XY")

# Create the torus with major radius 50 mm and minor radius 8 mm
result = model.workplane("YZ").torus(50 * cm, 8 * cm)

# Save the final shape in the 'result' variable
result