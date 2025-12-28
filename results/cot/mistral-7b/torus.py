from cadquery import exporters, workplane, circle, extrude

# Define the major and minor radii of the torus
R = 50  # Major radius in millimeters
r = 8   # Minor radius in millimeters

# Create a new model object
result = workplane("XY").circle(d=2*R, r=r).extrude(h=2*R)

# Save or export the model as desired (e.g., STEP, STL, etc.)
exporters.export(result, "torus.stl")