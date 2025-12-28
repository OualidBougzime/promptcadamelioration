import cadquery as cq

# Define the diameter parameter
diameter = 80.0

# Create a sphere using the defined diameter
result = cq.Workplane("XY").sphere(diameter / 2)

# Display the result (optional, useful for interactive environments like Jupyter Notebook)
show_object(result)