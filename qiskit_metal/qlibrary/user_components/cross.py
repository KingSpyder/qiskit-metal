"""File contains dictionary for Cross and the make()."""

from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent


class Cross(QComponent):
    """Alignement butterfly cross.

    Inherits QComponent class.

    The class will add default_options class Dict to QComponent class before calling make.

    Default Options:
        * size: '5um'
        * pocket_width: None
        * helper: False
    """

    default_options = Dict(size='5um',
                           pocket_width=None,
                           helper='False')
    """Default drawing options"""

    TOOLTIP = """A single configurable butterfly cross"""

    def make(self):
        """The make function implements the logic that creates the geoemtry
        (poly, path, etc.) from the qcomponent.options dictionary of
        parameters, and the adds them to the design, using
        qcomponent.add_qgeometry(...), adding in extra needed information, such
        as layer, subtract, etc."""
        p = self.p  # p for parsed parameters. Access to the parsed options.

        # create the geometry
        up_triangle = draw.shapely.geometry.Polygon([(0, 0), (-p.size/2, p.size/2), (p.size/2, p.size/2)])
        down_triangle = draw.shapely.geometry.Polygon([(0, 0), (-p.size/2, -p.size/2), (p.size/2, -p.size/2)])
        triangles = [up_triangle, down_triangle]
        triangles = draw.rotate(triangles, p.orientation)
        triangles = draw.translate(triangles, p.pos_x, p.pos_y)
        [up_triangle, down_triangle] = triangles
        ##############################################
        # add qgeometry
        self.add_qgeometry('poly', {'rectangle': up_triangle},
                           subtract=False,
                           helper=p.helper,
                           layer=p.layer,
                           chip=p.chip)
        self.add_qgeometry('poly', {'rectangle': down_triangle},
                           subtract=False,
                           helper=p.helper,
                           layer=p.layer,
                           chip=p.chip)
