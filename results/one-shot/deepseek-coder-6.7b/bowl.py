import cadquery as cq

# Define parameters
semi_radius = 40
wall_thickness = 3

# Create a semicircle and revolve it to form a hemisphere
result = (
    cq.Workplane("XY")
     .moveTo(0, -semi_radius) # Move the workplane to the bottom of the semicircle
     .circle(semi_radius)      # Draw a circle at the current location
     .revolve()                # Rotate around the Z-axis
)

# Extrude the shape to create a bowl and shell it with 3mm wall thickness
result = (
    result.edges(">Z")         # Select all edges pointing upwards
     .fillet(wall_thickness/2) # Fillet these edges by half of the wall thickness
     .extrude(length=semi_radius*2, both=True)  # Extrude in the direction of the Z-axis and also extrude to create a shell with thickness of 3mm
)