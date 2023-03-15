from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent
from shapely.geometry import Polygon
import shapely

class Diamond(QComponent):
    """A single configurable diamond
    
    Default Options:
        * width: '500um'
        * height_left: '300um'
        * height_right: '300um'
        * subtract: 'False'
        * helper: 'False'
    """

    default_options = Dict(width='500um',
                           height_left='300um',
                           height_right='300um',
                           subtract='False',
                           helper='False')
    """Default drawing options"""

    TOOLTIP = """A single configurable diamond"""

    def make(self):
        p = self.p  # p for parsed parameters. Access to the parsed options.

        # create the geometry
        pad = f"""POLYGON (({-p.width/2} {-p.height_left/2},
                            {+p.width/2} {-p.height_right/2},
                            {+p.width/2} {+p.height_right/2},
                            {-p.width/2} {+p.height_left/2},
                            {-p.width/2} {-p.height_left/2}))"""  # last  point has to close on self

        diam = Polygon(shapely.wkt.loads(pad))
        diam = draw.translate(diam, p.pos_x, p.pos_y)
        diam = draw.rotate(diam, p.orientation)
        ##############################################
        # add qgeometry
        self.add_qgeometry('poly', {'diamond': diam},
                           subtract=p.subtract,
                           helper=p.helper,
                           layer=p.layer,
                           chip=p.chip)