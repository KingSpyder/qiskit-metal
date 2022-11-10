from qiskit_metal.qlibrary.core import QRoute
from qiskit_metal import draw, Dict
import numpy as np

class QRoute_mm(QRoute):
    
    def make_elements(self, pts: np.ndarray):
        """Turns the CPW points into design elements, and add them to the
        design object.

        Args:
            pts (np.ndarray): Array of points
        """

        # prepare the routing track
        line = draw.LineString(pts)

        # compute actual final length
        p = self.p
        
        if not isinstance(p.layer, list):
            p.layer = [p.layer]
        if len(p.layer)==1:
            p.layer = p.layer*2
            
        self.options._actual_length = str(
            line.length - self.length_excess_corner_rounding(line.coords)
        ) + ' ' + self.design.get_units()

        # expand the routing track to form the substrate core of the cpw
        self.add_qgeometry('path', {'trace': line},
                            width=p.trace_width,
                            fillet=p.fillet,
                            layer=p.layer[1])
        if self.type == "CPW":
            # expand the routing track to form the two gaps in the substrate
            # final gap will be form by this minus the trace above
            self.add_qgeometry('path', {'cut': line},
                                width=p.trace_width + 2 * p.trace_gap,
                                fillet=p.fillet,
                                layer=p.layer[0],
                                subtract=True)