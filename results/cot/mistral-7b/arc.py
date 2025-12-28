from cadquery import exporters, workplane, arc, rotate, extrude

# Define the radius of the arc
radius = 60

# Create a new solid object (the result)
result = workplane("XY").arc(center=(0, 0), radius=radius, start_angle=0, end_angle=210).rotate(210).extrude(2*radius)

# Export the model to an .stl file (optional)
exporters.export(result, 'model.stl')