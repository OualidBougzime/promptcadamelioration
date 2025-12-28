import cadquery as cq

# Create a cylinder with diameter 40 mm and height 60 mm
result = cq.Workplane().cylinder(40, 60)

# Display the result
cq.show_object(result)