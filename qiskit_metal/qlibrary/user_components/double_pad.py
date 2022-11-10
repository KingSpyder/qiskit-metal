from qiskit_metal.toolbox_python.attr_dict import Dict
from qiskit_metal.qlibrary.core import QComponent
from qiskit_metal import draw, Dict


class DoublePad(QComponent):
    """Two pins out of a two layers rectangle. Practical for 2 materials junction.
    """

    default_options = Dict(
        layer=[1,2],
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
        if len(p.layer)!=2:
            raise NotImplementedError(f"A double pad should have options layer as\
                [n1,n2] where n1 and n2 are two ints, got {p.layer}")
        pad = draw.rectangle(p.width, p.height)
        pocket = draw.rectangle(p.pocket_width, p.pocket_heigth)
        polys = [pad, pocket]
        polys = draw.rotate(polys, p.orientation, origin=(0,0))
        polys = draw.translate(polys, p.pos_x, p.pos_y)
        [pad, pocket] = polys
        
        pad_name = "double_pad"
        pocket_name = "double_pad_pocket"
        chip = p.chip
        self.add_qgeometry('poly',{pad_name+"1": pad},
                           chip=chip, layer=p.layer[0])
        self.add_qgeometry('poly',{pad_name+"2": pad},
                           chip=chip, layer=p.layer[1])
        self.add_qgeometry('poly',{pocket_name: pocket},
                           chip=chip, layer=p.layer[0], subtract=True)
        self.add_pin("right", pad.boundary.coords[1:3][::-1], width=p.width)
        self.add_pin("left", pad.boundary.coords[3:5][::-1], width=p.width)