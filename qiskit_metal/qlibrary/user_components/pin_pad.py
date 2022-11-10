import numpy as np

from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent


class PinPad(QComponent):
    """A rectangle pad with a pin.
    If list as arguments make multiple rectangles (share pin border)
    May be used for patches to connect layers.
    """


    default_options = Dict(width='500um',
                           height='300um',
                           subtract='False',
                           helper='False')
    
    def make(self):
        p = self.p  # p for parsed parameters. Access to the parsed options.
        if not isinstance(p.width, list):
            p.width = [p.width]
        if not isinstance(p.height, list):
            p.height = [p.height]
        if not isinstance(p.layer, list):
            p.layer = [p.layer]
        if not isinstance(p.subtract, list):
            p.subtract = [p.subtract]
        if not(len(p.width) == len(p.height) and len(p.height)==len(p.layer) and len(p.layer)==len(p.subtract)):
            raise Exception("Don't know how to interpret mixed arguments (both list and scalar).")
        
        rects = []
        # create the geometry
        for width, height in zip(p.width, p.height):
            rect = draw.rectangle(width, height, 
                                  width/2-p.width[0]/2,
                                  0)
            rects.append(rect)
        rects = draw.rotate(rects, p.orientation, origin=(0,0))
        rects = draw.translate(rects, p.pos_x, p.pos_y)
        ##############################################
        # add qgeometry
        for rect, layer, subtract in zip(rects, p.layer, p.subtract):
            self.add_qgeometry('poly', {'rectangle': rect},
                                subtract=subtract,
                                helper=p.helper,
                                layer=layer,
                                chip=p.chip)
            
        self.add_pin("pad", rects[0].boundary.coords[3:5][::-1], width=0.1)