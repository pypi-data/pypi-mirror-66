import pygmsh
from helpers import compute_volume


def test():
    geom = pygmsh.built_in.Geometry()

    poly = geom.add_polygon(
        [
            [0.0, 0.0, 0.0],
            [2.0, 0.0, 0.0],
            [3.0, 1.0, 0.0],
            [1.0, 2.0, 0.0],
            [0.0, 1.0, 0.0],
        ],
        lcar=0.1,
    )

    field0 = geom.add_boundary_layer(
        edges_list=[poly.line_loop.lines[0]],
        hfar=0.1,
        hwall_n=0.01,
        ratio=1.1,
        thickness=0.2,
        anisomax=100.0,
    )

    field1 = geom.add_boundary_layer(
        nodes_list=[poly.line_loop.lines[1].points[1]],
        hfar=0.1,
        hwall_n=0.01,
        ratio=1.1,
        thickness=0.2,
        anisomax=100.0,
    )

    geom.set_boundary_layers([field0, field1])

    ref = 4.0
    mesh = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    import meshio

    meshio.write("boundary_layers.vtu", test())
