from cadquery import exporters, workplane, circle, extrude, cone

def make_cone(diameter=50, height=60):
    # Create a new workplane at the origin (0, 0, 0)
    w = workplane()

    # Define the base circle with the given diameter
    base_circle = w.circle(diameter / 2)

    # Extrude the base circle to form a cylinder of the specified height
    cone_base = base_circle.extrude(height)

    # Convert the cylinder into a cone with the given height
    result = cone(cone_base, height=height)

    return result

# Generate the cone and export it as an STL file
result = make_cone()
result.export('cone.stl', exporters.stl)