import pygmsh
from helpers import compute_volume


def test():
    geom = pygmsh.built_in.Geometry()

    lcar = 0.1
    p1 = geom.add_point([0.0, 0.0, 0.0], lcar)
    p2 = geom.add_point([1.0, 0.0, 0.0], lcar)
    p3 = geom.add_point([1.0, 0.5, 0.0], lcar)
    p4 = geom.add_point([1.0, 1.0, 0.0], lcar)
    s1 = geom.add_bspline([p1, p2, p3, p4])

    p2 = geom.add_point([0.0, 1.0, 0.0], lcar)
    p3 = geom.add_point([0.5, 1.0, 0.0], lcar)
    s2 = geom.add_bspline([p4, p3, p2, p1])

    ll = geom.add_line_loop([s1, s2])
    geom.add_plane_surface(ll)

    ref = 0.9156598733673261 if pygmsh.get_gmsh_major_version() < 4 else 0.75
    mesh = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    import meshio

    meshio.write("bsplines.vtu", test())
