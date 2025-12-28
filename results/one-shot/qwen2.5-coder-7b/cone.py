import cadquery as cq

# Define dimensions
base_diameter = 50
height = 60

# Create the cone
result = (
    cq.Workplane("XY")
    .cone(base_diameter / 2, base_diameter / 2, height)
)

# Optionally, you can extrude a small amount to give it a solid shape if needed
# result = result.extrude(1e-3)  # Uncomment this line if you need a solid cone