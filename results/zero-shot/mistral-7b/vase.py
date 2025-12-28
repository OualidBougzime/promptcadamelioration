from cadquery import exporters, workplane, cylinder, revolve, draftAngle, distancePointToLine, normalize, intersects, Workplane, Vector, Cylinder, assembly, faces

# Define the vase dimensions and angles
base_radius = 30
mid_height = 60
top_height = 120
bottom_height = mid_height
mid_radius = 22
top_radius = 35
draft_angle = draftAngle(45)

# Create a new workplane for the base
base_workplane = workplane("XY")

# Define the base cylinder
base_cylinder = cylinder(base_radius, height=bottom_height)

# Revolve the base cylinder to create the bottom part of the vase
bottom_part = revolve(base_cylinder, workplane=base_workplane, angle=180)

# Move the workplane up for the mid-section
mid_workplane = base_workplane.moveAxes(Vector(0, 0, mid_height))

# Define the mid-cylinder with a smaller radius
mid_cylinder = cylinder(mid_radius, height=top_height - mid_height)

# Revolve the mid-cylinder to create the middle part of the vase
middle_part = revolve(mid_cylinder, workplane=mid_workplane, angle=180)

# Define the top cylinder with a larger radius
top_cylinder = cylinder(top_radius, height=top_height - mid_height)

# Revolve the top cylinder to create the top part of the vase
top_part = revolve(top_cylinder, workplane=mid_workplane.moveAxes(Vector(0, 0, top_height)), angle=180)

# Combine all parts into a single assembly
result = assembly([bottom_part, middle_part, top_part])

# Apply draft angle to the edges of the vase
for face in result.faces():
    if intersects(face, cylinder(1, height=1)):
        normal = normalize(distancePointToLine(face.center(), face.edgeAt(0).start(), face.edgeAt(0).end()))
        drafted_face = face.draft(normal, draft_angle)
        result = result.cut(drafted_face)

# Export the final model as STEP file
exporters.step.exportFile(result, "vase.step")