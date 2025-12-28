import cadquery as cq

# Create a sphere with diameter 80mm
sphere = cq.Workplane().circle(center=(0, 0, 0), radius=40).extrude(80)

# Store the final shape in a variable named 'result'
result = sphere