from cadquery import exporters, workplane, cube

def create_cube():
    result = cube(50, center=True)  # Create a centered cube of size 50mm x 50mm x 50mm
    return result

# Export the model to an .STL file
exporters.export(create_cube(), 'cube.stl')