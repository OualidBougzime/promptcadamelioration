from cadquery import exporters, workplane, cs, cone, verify
import cadquery as cq

# Initialize the cone design variables
base_diameter = 50
height = 60

# Create a new working plane
wp = workplane("XY")

# Generate the cone using CadQuery API
result = cone(base=cs.Circle(base_diameter / 2), height=height, start_angle=0, end_angle=180)

# Verify the model and export it as STEP file
verify(result).export(exporters.step("cone.step"))