from cadquery import exporters, workplane, cube

# Importing necessary libraries
import cadquery as cq

# Creating a cube with parametric dimensions of 50 mm x 50 mm x 50 mm
result = cq.workplane("XY").cube(50)

# Export the model to an .stl file (optional)
result.export(exporters.stl, "my_model.stl")