import numpy as np

from qiskit_metal.toolbox_python.attr_dict import Dict
from qiskit_metal.qlibrary.core import QComponent
from qiskit_metal import draw, Dict


class QuadriPin(QComponent):
    """Four pins out of a rectangle (made in a layer). Practical for mega resistive networks.
    Multi layer supported if layer is a list. (make the pad on all layers).
    Always put the ground layer in first.
    """

    default_options = Dict(
        layer=1,
        pos_x='0um',
        pos_y='0um',
        orientation='0',
        width="50um",
        height="50um",
        pocket_width="50um",
        pocket_heigth="100um"
    )
    
    def make(self):
        p = self.p
        if not isinstance(p.layer, list):
            p.layer = [p.layer]
        if len(p.layer)==1:
            p.layer = p.layer*2

        quadri = draw.rectangle(p.width, p.height)
        pocket = draw.rectangle(p.pocket_width, p.pocket_heigth)
        polys = [quadri, pocket]
        polys = draw.rotate(polys, p.orientation, origin=(0,0))
        polys = draw.translate(polys, p.pos_x, p.pos_y)
        [quadri, pocket] = polys
        
        quadri_name = "quadri_pin"
        pocket_name = "quadri_pocket"
        chip = p.chip
        self.add_qgeometry('poly',{quadri_name: quadri},
                        chip=chip, layer=p.layer[1])
        self.add_qgeometry('poly',{pocket_name: pocket},
                           chip=chip, layer=p.layer[0], subtract=True)
        self.add_pin("bottom", quadri.boundary.coords[0:2][::-1], width=p.width)
        self.add_pin("right", quadri.boundary.coords[1:3][::-1], width=p.width)
        self.add_pin("top", quadri.boundary.coords[2:4][::-1], width=p.width)
        self.add_pin("left", quadri.boundary.coords[3:5][::-1], width=p.width)