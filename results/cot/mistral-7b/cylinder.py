from cadquery import exporters, workplane, cylinder

def create_cylinder(diameter=40, height=60):
    # Create a new workplane for the cylinder
    w = workplane("XY")

    # Define and create the cylinder
    result = cylinder(point=(0, 0, 0), diameter=diameter, height=height)

    # Export the model as an .stl file (optional)
    exporters.export(result, 'cylinder.stl')

    return result

# Create and display the cylinder
create_cylinder()