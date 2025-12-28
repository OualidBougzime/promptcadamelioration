import CadQuery as cq

# Create the pipe body without ends
body = ...

# Add chamfers to both ends
body = body.chamfer(cq.Workplane("Front").vector([-chamfer_size, 0]), chamfer_size)
body = body.mirror(cq.Plane("X", length))
body = body.chamfer(cq.Workplane("Front").vector([chamfer_size, 0]), chamfer_size)

# Final pipe object
result = cq.Workplane("Front").workplane().cutBlind(body).solid()