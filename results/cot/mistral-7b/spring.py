from cadquery import exporters, workbench

# Initialize a new workbench
app = workbench.Workbench()

# Define the circular cross-section
circle_solid = app.workplane("XY").circle(1.5).extrude(2 * 1.5)

# Set up the workplane for the helix path
helix_wp = app.workplane("YZ", origin=(0, 0, 20))

# Generate the right-hand helix path
helix_path = helix_wp.helix(turns=80 / 8, pitch=8, direction="R")

# Perform the sweep operation to create the helical spring
result = circle_solid.sweep(helix_path)

# Export the model as STEP file
result.exportData(exporters.step(), "helical_spring.step")