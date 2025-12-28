from cadquery import exporters, workplane, circle, revolve, faces, worksurface, cq

# Create a semicircle on the XY plane
semicircle = circle((0, 0), radius=40).section(cq.Plane(z=-40)).reversed()

# Move to the Z=0 workplane
wp_z0 = workplane("XY").moveToZ(0)

# Revolve the semicircle around the Y-axis to form a hemisphere
hemisphere = revolve(semicircle, axis=(0, 0, 1))

# Shell the hemisphere with a 3mm thickness
result = worksurface(hemisphere).extrude(3)

# Export the model to an STL file
result.exportData("bowl.stl", exporters.STEP)