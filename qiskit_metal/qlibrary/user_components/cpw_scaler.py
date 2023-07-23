from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent
from shapely.geometry import Polygon
import shapely

class CPWScaler(QComponent):
    """Scaler to go from one set of CPW dimensions to another
    IN (0,0)==>-- OUT
    Default Options:
        * width_in: '500um'
        * gap_in: '300um'
        * width_out: '500um'
        * gap_out: '300um'
        * scaler_length: '100um'
        * in_compensation: ['0um', '0um'] (bottom & top)
        * helper: 'False'
    """

    default_options = Dict(width_in='500um',
                           gap_in='300um',
                           width_out='500um',
                           gap_out='300um',
                           scaler_length='100um',
                           in_compensation=['0um', '0um'],
                           helper='False')
    """Default drawing options"""

    TOOLTIP = """CPW Scaler"""

    def make(self):
        p = self.p  # p for parsed parameters. Access to the parsed options.

        # create the geometry
        gap = draw.Polygon([
            [0, -p.width_in/2 - p.gap_in - p.in_compensation[0]],
            [0, +p.width_in/2 + p.gap_in + p.in_compensation[1]],
            [p.in_compensation[1], +p.width_in/2 + p.gap_in],
            [p.scaler_length, +p.width_out/2 + p.gap_out],
            [p.scaler_length, -p.width_out/2 - p.gap_out],
            [p.in_compensation[0], -p.width_in/2 - p.gap_in],
        ])
        
        trace = draw.Polygon([
            [0, -p.width_in/2],
            [0, +p.width_in/2],
            [p.scaler_length, +p.width_out/2],
            [p.scaler_length, -p.width_out/2],
        ])
            

        polys = [gap, trace]
        polys = draw.rotate(polys, p.orientation, origin=(0,0))
        polys = draw.translate(polys, p.pos_x, p.pos_y)
        [gap, trace] = polys
        ##############################################
        # add qgeometry
        self.add_qgeometry('poly', {'scaler_gap': gap},
                           subtract=True,
                           helper=p.helper,
                           layer=p.layer,
                           chip=p.chip)
        self.add_qgeometry('poly', {'scaler_trace': trace},
                           helper=p.helper,
                           layer=p.layer,
                           chip=p.chip)
    
        # Pins
        in_pin = draw.LineString([(p.scaler_length, 0),
                                  (0, 0)])
        out_pin = draw.LineString([(0,0),
                                  (p.scaler_length, 0)])
        
        pins = [in_pin, out_pin]
        pins = draw.rotate(pins, p.orientation, origin=(0,0))
        pins = draw.translate(pins, p.pos_x, p.pos_y)
        [in_pin, out_pin] = pins
                
        self.add_pin("in",
                     points=in_pin.coords,
                     width=p.width_in,
                     input_as_norm=True,
                     chip=p.chip)
        self.add_pin("out",
                     points=out_pin.coords,
                     width=p.width_out,
                     input_as_norm=True,
                     chip=p.chip)