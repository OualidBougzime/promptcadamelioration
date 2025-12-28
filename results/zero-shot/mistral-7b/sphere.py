from cadquery import exporters, workplane, cube, sphere, draft, mesh

# Import necessary modules
import cadquery as cq

# Create a sphere with a diameter of 80mm
result = cq.Workplane("XY").workplane(center=(0, 0, 40)).sphere(radius=40)

# Export the model to an .STL file
exporters.export(result, 'sphere.stl')