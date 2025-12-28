from cadquery import exporters, workplane, cylinder, rect, union_all

def create_table():
    top = workplane("XY").rect(200, 100, 15)

    legs = []
    for corner in [(0, 0), (200, 0), (200, 100), (0, 100)]:
        legs.append(workplane("XY", origin=corner).move_to((0, 15)).cylinder(12, 120))

    result = union_all([top] + [leg.cut(top) for leg in legs])

    exporters.svgsave("table.svg", result)
    return result

create_table()