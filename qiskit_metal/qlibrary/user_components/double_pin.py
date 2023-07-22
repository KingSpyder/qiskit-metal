import numpy as np

from qiskit_metal.toolbox_python.attr_dict import Dict
from qiskit_metal.qlibrary.core import QComponent


class DoublePin(QComponent):
    """Two pins back to back.
    Practical for lighter code when chip only has QRoutes and ModRoute.
    """

    default_options = Dict(
        layer=1,
        pos_x='0um',
        pos_y='0um',
        orientation='0',
        width=0.1
    )
    
    def make(self):
        p = self.p
        x_r = p.pos_x + np.cos(p.orientation*np.pi/180)
        y_r = p.pos_y + np.sin(p.orientation*np.pi/180)
        x_l = p.pos_x - np.cos(p.orientation*np.pi/180)
        y_l = p.pos_y - np.sin(p.orientation*np.pi/180)
        
        self.add_pin("left", [[x_r, y_r], [p.pos_x, p.pos_y]], width=p.width, input_as_norm=True)
        self.add_pin("right", [[x_l, y_l], [p.pos_x, p.pos_y]], width=p.width, input_as_norm=True)