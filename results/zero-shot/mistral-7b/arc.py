from cadquery import exporters, workplane, cs, circle, arc, sweep

# Initialize a new CAD model
model = workplane("XY")

# Create the circular arc with a radius of 60mm and sweeping angle of 210 degrees
result = sweep(circle(radius=60), arc((0, 0), (0, 0), 60, start_angle=-90, end_angle=270))

# Save the model to an .stl file
exporters.write_stl(result, "arc_sweep.stl")