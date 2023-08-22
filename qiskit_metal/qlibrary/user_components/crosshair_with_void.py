"""File contains dictionary for Cross and the make()."""

from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent


class CrosshairWithVoid(QComponent):
    """Alignement crosshair cross with a hole in the middle to do dot.
    Inherits QComponent class.

    The class will add default_options class Dict to QComponent class before calling make.

    Default Options:
        * size_small: '100nm'
        * size_big: '1000nm'
        * pocket_width: None
        * void_size: '600nm'
        * helper: False
    """

    default_options = Dict(size_small='100nm',
                           size_big='1000nm',
                           pocket_width=None,
                           void_size="600nm",
                           helper='False',
                           subtract='False')
    """Default drawing options"""

    TOOLTIP = """A single configurable crosshair cross"""

    def make(self):
        """The make function implements the logic that creates the geoemtry
        (poly, path, etc.) from the qcomponent.options dictionary of
        parameters, and the adds them to the design, using
        qcomponent.add_qgeometry(...), adding in extra needed information, such
        as layer, subtract, etc."""
        p = self.p  # p for parsed parameters. Access to the parsed options.

        # create the geometry
        if p.pocket_width is not None:
            pocket = draw.rectangle(p.pocket_width, p.pocket_width)
        
        big_left = draw.rectangle(3.125*p.size_big, p.size_big,
                                  -2*p.size_big - 3.125/2*p.size_big, 0)
        big_right = draw.rectangle(3.125*p.size_big, p.size_big,
                                  2*p.size_big + 3.125/2*p.size_big, 0)
        big_down = draw.rectangle(p.size_big, 3.125*p.size_big,
                                  0, -2*p.size_big - 3.125/2*p.size_big)
        big_up = draw.rectangle(p.size_big, 3.125*p.size_big,
                                  0, 2*p.size_big + 3.125/2*p.size_big)
        small_horiz = draw.rectangle(4*p.size_big, p.size_small)
        small_vertic = draw.rectangle(p.size_small, 4*p.size_big)
        small_45 = draw.rotate(draw.rectangle(4*p.size_big, p.size_small), 45, origin=(0, 0))
        small_m45 = draw.rotate(draw.rectangle(4*p.size_big, p.size_small), -45, origin=(0, 0))
        
        crosshair = draw.union(big_down, big_left, big_right, big_up, small_horiz, small_vertic, small_45, small_m45)
        crosshair = draw.subtract(
            crosshair,
            draw.shapely.geometry.Point(0, 0).buffer(p.void_size)
        )
        
        if p.pocket_width is not None:
            polys = [crosshair, pocket]
        else:
            polys = [crosshair]
        polys = draw.rotate(polys, p.orientation, origin=(0,0))
        polys = draw.translate(polys, p.pos_x, p.pos_y)
        if p.pocket_width is not None:
            [crosshair, pocket] = polys
        else:
            [crosshair] = polys
        ##############################################
        # add qgeometry
        self.add_qgeometry('poly', {'rectangle': crosshair},
                           subtract=p.subtract,
                           helper=p.helper,
                           layer=p.layer,
                           chip=p.chip)
        if p.pocket_width is not None:
            self.add_qgeometry('poly', {'pocket_cross': pocket},
                            subtract=True,
                            helper=p.helper,
                            layer=p.layer,
                            chip=p.chip)
