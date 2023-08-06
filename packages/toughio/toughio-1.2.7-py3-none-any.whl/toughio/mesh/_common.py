from string import ascii_uppercase

import meshio
import numpy

__all__ = [
    "vtk_to_meshio_type",
    "meshio_to_vtk_type",
    "vtk_type_to_numnodes",
    "meshio_type_to_ndim",
    "meshio_data",
    "get_meshio_version",
    "get_old_meshio_cells",
    "get_local_index",
    "labeler",
]


vtk_to_meshio_type = {
    0: "empty",
    1: "vertex",
    # 2: "poly_vertex",
    3: "line",
    # 4: "poly_line",
    5: "triangle",
    # 6: "triangle_strip",
    7: "polygon",
    # 8: "pixel",
    9: "quad",
    10: "tetra",
    # 11: "voxel",
    12: "hexahedron",
    13: "wedge",
    14: "pyramid",
    15: "penta_prism",
    16: "hexa_prism",
    21: "line3",
    22: "triangle6",
    23: "quad8",
    24: "tetra10",
    25: "hexahedron20",
    26: "wedge15",
    27: "pyramid13",
    28: "quad9",
    29: "hexahedron27",
    30: "quad6",
    31: "wedge12",
    32: "wedge18",
    33: "hexahedron24",
    34: "triangle7",
    35: "line4",
    #
    # 60: VTK_HIGHER_ORDER_EDGE,
    # 61: VTK_HIGHER_ORDER_TRIANGLE,
    # 62: VTK_HIGHER_ORDER_QUAD,
    # 63: VTK_HIGHER_ORDER_POLYGON,
    # 64: VTK_HIGHER_ORDER_TETRAHEDRON,
    # 65: VTK_HIGHER_ORDER_WEDGE,
    # 66: VTK_HIGHER_ORDER_PYRAMID,
    # 67: VTK_HIGHER_ORDER_HEXAHEDRON,
}
meshio_to_vtk_type = {v: k for k, v in vtk_to_meshio_type.items()}


vtk_type_to_numnodes = {
    0: 0,  # empty
    1: 1,  # vertex
    3: 2,  # line
    5: 3,  # triangle
    9: 4,  # quad
    10: 4,  # tetra
    12: 8,  # hexahedron
    13: 6,  # wedge
    14: 5,  # pyramid
    15: 10,  # penta_prism
    16: 12,  # hexa_prism
    21: 3,  # line3
    22: 6,  # triangle6
    23: 8,  # quad8
    24: 10,  # tetra10
    25: 20,  # hexahedron20
    26: 15,  # wedge15
    27: 13,  # pyramid13
    28: 9,  # quad9
    29: 27,  # hexahedron27
    30: 6,  # quad6
    31: 12,  # wedge12
    32: 18,  # wedge18
    33: 24,  # hexahedron24
    34: 7,  # triangle7
    35: 4,  # line4
}


meshio_type_to_ndim = {k: 3 for k in meshio_to_vtk_type.keys()}
meshio_type_to_ndim.update(
    {"empty": 0, "vertex": 1, "line": 2, "triangle": 2, "polygon": 2, "quad": 2}
)


meshio_data = {
    "material",
    "avsucd:material",
    "flac3d:zone",
    "gmsh:physical",
    "medit:ref",
}


alpha = list(ascii_uppercase)
numer = ["{:0>2}".format(i) for i in range(100)]
nomen = ["{:1}".format(i + 1) for i in range(9)] + alpha


def get_meshio_version():
    """
    Return :mod:`meshio` version as a tuple.

    Returns
    -------
    tuple
        :mod:`meshio` version as tuple (major, minor, patch).

    """
    return tuple(int(i) for i in meshio.__version__.split("."))


def get_old_meshio_cells(cells, cell_data=None):
    """
    Return old-style cells and cell_data (meshio < 4.0.0).

    Parameters
    ----------
    cells : list of namedtuple (type, data)
        New-style cells.
    cell_data : dict or None, optional, default None
        New-style cell data.

    Returns
    -------
    dict
        Old-style cells.
    dict
        Old-style cell data (only if `cell_data` is not None).

    """
    old_cells, cell_blocks = {}, {}
    for ic, c in enumerate(cells):
        if c.type not in old_cells.keys():
            old_cells[c.type] = [c.data]
            cell_blocks[c.type] = [ic]
        else:
            old_cells[c.type].append(c.data)
            cell_blocks[c.type].append(ic)
    old_cells = {k: numpy.concatenate(v) for k, v in old_cells.items()}

    if cell_data is not None:
        old_cell_data = (
            {
                cell_type: {
                    k: numpy.concatenate([cell_data[k][i] for i in iblock])
                    for k in cell_data.keys()
                }
                for cell_type, iblock in cell_blocks.items()
            }
            if cell_data
            else {}
        )
        return old_cells, old_cell_data
    else:
        return old_cells


def get_new_meshio_cells(cells, cell_data=None):
    """
    Return new-style cells and cell_data (meshio >= 4.0.0).

    Parameters
    ----------
    cells : dict
        Old-style cells.
    cell_data : dict or None, optional, default None
        Old-style cell data.

    Returns
    -------
    list of namedtuple (type, data)
        New-style cells.
    dict
        New-style cell data (only if `cell_data` is not None).

    """
    from ._mesh import CellBlock

    new_cells = [CellBlock(k, v) for k, v in cells.items()]

    if cell_data is not None:
        labels = numpy.unique([kk for k, v in cell_data.items() for kk in v.keys()])
        new_cell_data = {k: [] for k in labels}
        for k in new_cell_data.keys():
            for kk in cells.keys():
                new_cell_data[k].append(cell_data[kk][k])
        return new_cells, new_cell_data
    else:
        return new_cells


def get_local_index(mesh, i):
    """
    Convert global cell index to local tuple index.

    Parameters
    ----------
    mesh : toughio.Mesh
        Input mesh.
    i : int
        Global cell index.

    """
    n_cells = numpy.cumsum([len(c.data) for c in mesh.cells])
    idx = numpy.nonzero(n_cells > i)[0][0]

    return (0, i) if not idx else (idx, i - n_cells[idx - 1])


def labeler(i):
    """
    Return five-character long cell labels.

    - 1st: from A to Z
    - 2nd and 3rd: from 1 to 9 then A to Z
    - 4th and 5th: from 00 to 99
    Incrementation is performed from right to left.

    Parameters
    ----------
    i : int
        Cell general index in mesh.

    Returns
    -------
    str
        Label for cell `i`.

    Note
    ----
    Currently support up to 3,185,000 different cells.

    """
    q1, r1 = divmod(i, len(numer))
    q2, r2 = divmod(q1, len(nomen))
    q3, r3 = divmod(q2, len(nomen))
    _, r4 = divmod(q3, len(nomen))

    return "".join([alpha[r4], nomen[r3], nomen[r2], numer[r1]])
