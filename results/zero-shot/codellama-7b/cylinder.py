import cadquery as cq

# Define the cylinder parameters
diameter = 40e-3  # diameter of the cylinder (in meters)
height = 60e-3    # height of the cylinder (in meters)

# Create a new CadQuery object
cylinder = cq.Workplane().cylinder(diameter, height)

# Store the final shape in a variable named 'result'
result = cylinder