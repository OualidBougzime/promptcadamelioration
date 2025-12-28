import cadquery as cq

# Define the diameter parameter
diameter = 80.0

# Create a sphere with the specified diameter
result = cq.Workplane("XY").sphere(diameter / 2)

# Display the result (for Jupyter Notebook or similar environments)
show_object(result)