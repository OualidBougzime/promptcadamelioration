import cadquery as cq

# Define the cone parameters
base_diameter = 50e-3   # base diameter (mm)
height = 60e-3         # height (mm)

# Create a new shape using the CadQuery API
result = cq.Workplane().moveTo(0, 0, -height / 2).moveTo(-base_diameter / 2, 0, 0).arcCW(base_diameter / 2, height)

# Display the final shape
print(result)