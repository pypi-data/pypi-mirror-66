import pyg4ometry
from   pyg4ometry.pycgal.core import CSG as _CSG1
import cgal

def test() :
    reg = pyg4ometry.geant4.Registry()
    b = pyg4ometry.geant4.solid.Box("b1", 10, 10, 10, reg, "mm", True)

    mesh1 = _CSG1.fromPolygons(b.pycsgmesh().toPolygons())

    ph   = mesh1.polyhedron
    nefp = cgal.polyhedron_to_nefpolyhedron(ph)
    sm   = cgal.nefpolyhedron_to_surfacemesh(nefp)

    cgal.polyhedron_write(ph,"test.pol3")
    cgal.nefpolyhedron_write(nefp,"test.nef3")
    cgal.surfacemesh_write(sm,"test.sm3")

    cgal.surfacemesh_print(sm)

    cgal.delete_polyhedron(ph)
    cgal.delete_nefpolyhedron(nefp)
    cgal.delete_surfacemesh(sm)