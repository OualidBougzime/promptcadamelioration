from cadquery import exporters, workplane, circle, center, sphere

def create_sphere(diameter):
    # Define the workplane
    wp = workplane("XY")

    # Create a circle with half of the diameter as radius
    circle_radius = diameter / 2
    circle_obj = wp.circle(center=(0, 0), radius=circle_radius)

    # Generate the sphere using the center and radius of the circle
    result = sphere(circle_obj.center(), circle_obj.radius())

    return result

# Create a sphere with diameter 80mm
result = create_sphere(80)

# Export the model to an .STL file
exporters.export(result, 'sphere.stl')