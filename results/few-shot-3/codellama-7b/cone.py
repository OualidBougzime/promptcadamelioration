import cadquery as cq

# Create a new CQ object
cq_obj = cq.Workplane("XY")

# Add a circle to the CQ object
circle = cq_obj.circle(50)

# Extrude the circle to create a cone
cone = circle.extrude((0, 0, 60))

# Store the final shape in the 'result' variable
result = cone