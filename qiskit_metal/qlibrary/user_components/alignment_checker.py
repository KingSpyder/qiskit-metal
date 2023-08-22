"""File contains dictionary for Cross and the make()."""

from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent


class AlignementChecker(QComponent):
    """Alignement crosshair cross.

    Inherits QComponent class.

    The class will add default_options class Dict to QComponent class before calling make.

    Default Options:
        * size_small: '100nm'
        * size_big: '1000nm'
        * pocket_width: None
        * helper: False
    """

    default_options = Dict(size='2um',
                           distance="1um",
                           layer=[1, 2],
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
        rec1 = draw.rectangle(2*p.size, p.size, -p.size - p.distance/2)
        rec2 = draw.rectangle(2*p.size, p.size, p.size + p.distance/2)
        
        polys = [rec1, rec2]
        polys = draw.rotate(polys, p.orientation, origin=(0,0))
        polys = draw.translate(polys, p.pos_x, p.pos_y)
        [rec1, rec2] = polys
        ##############################################
        # add qgeometry
        self.add_qgeometry('poly', {'rec1': rec1},
                           subtract=p.subtract,
                           helper=p.helper,
                           layer=p.layer[0],
                           chip=p.chip)
        self.add_qgeometry('poly', {'rec2': rec2},
                        subtract=False,
                        helper=p.helper,
                        layer=p.layer[1],
                        chip=p.chip)
