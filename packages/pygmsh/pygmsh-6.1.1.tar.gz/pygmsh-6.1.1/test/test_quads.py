import pygmsh
from helpers import compute_volume


def test():
    geom = pygmsh.built_in.Geometry()

    rectangle = geom.add_rectangle(0.0, 1.0, 0.0, 1.0, 0.0, 0.1)

    geom.add_raw_code("Recombine Surface {%s};" % rectangle.surface.id)

    ref = 1.0
    mesh = pygmsh.generate_mesh(geom, dim=2)
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    import meshio

    meshio.write("quads.vtu", test())
