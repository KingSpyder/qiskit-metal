import numpy as np

from qiskit_metal.toolbox_python.attr_dict import Dict
from qiskit_metal.qlibrary.core import QComponent
from qiskit_metal import draw, Dict


class PrintedCapa(QComponent):
    """Multi-layer printed capa. With leads.
    """

    default_options = Dict(
        layer=[1,2,3],
        pos_x='0um',
        pos_y='0um',
        orientation='0',
        capa_width="50um",
        capa_height1="50um",
        capa_height2="50um",
        diel_width="50um",
        diel_height="100um",
        gap_width="70um",
        wire_length="20um",
        lead_width="60um",
        lead_length="100um",
        lead_gap="80um",
        overlap=True
    )
    
    def make(self):
        p = self.p

        diel = draw.rectangle(p.diel_width, p.diel_height)
        pocket = draw.Polygon([[-(p.capa_width/2+p.wire_length+p.lead_length), p.lead_gap/2],
                               [-(p.capa_width/2+p.wire_length), p.gap_width/2],
                               [p.capa_width/2+p.wire_length, p.gap_width/2],
                               [p.capa_width/2+p.wire_length+p.lead_length, p.lead_gap/2],
                               [p.capa_width/2+p.wire_length+p.lead_length, -p.lead_gap/2],
                               [p.capa_width/2+p.wire_length, -p.gap_width/2],
                               [-(p.capa_width/2+p.wire_length), -p.gap_width/2],
                               [-(p.capa_width/2+p.wire_length+p.lead_length), -p.lead_gap/2],
                               [-(p.capa_width/2+p.wire_length+p.lead_length), p.lead_gap/2]
                               ])
        layer1 = draw.Polygon([[-(p.capa_width/2+p.wire_length+p.lead_length), p.lead_width/2],
                               [-(p.capa_width/2+p.wire_length), p.capa_height1/2],
                               [p.capa_width/2, p.capa_height1/2],
                               [p.capa_width/2, -p.capa_height1/2],
                               [-(p.capa_width/2+p.wire_length), -p.capa_height1/2],
                               [-(p.capa_width/2+p.wire_length+p.lead_length), -p.lead_width/2],
                               [-(p.capa_width/2+p.wire_length+p.lead_length), p.lead_width/2]])
        layer2 = draw.Polygon([[p.capa_width/2+p.wire_length+p.lead_length, p.lead_width/2],
                               [p.capa_width/2+p.wire_length, p.capa_height2/2],
                               [-p.capa_width/2, p.capa_height2/2],
                               [-p.capa_width/2, -p.capa_height2/2],
                               [p.capa_width/2+p.wire_length, -p.capa_height2/2],
                               [p.capa_width/2+p.wire_length+p.lead_length, -p.lead_width/2],
                               [p.capa_width/2+p.wire_length+p.lead_length, p.lead_width/2]])
        layer1_overlap = draw.Polygon([[p.capa_width/2+p.wire_length+p.lead_length, p.lead_width/2],
                               [p.capa_width/2+p.wire_length, p.capa_height1/2],
                               [p.capa_width/2+p.wire_length, -p.capa_height1/2],
                               [p.capa_width/2+p.wire_length+p.lead_length, -p.lead_width/2],
                               [p.capa_width/2+p.wire_length+p.lead_length, p.lead_width/2]])
        
        polys = [diel, pocket, layer1, layer2, layer1_overlap]
        polys = draw.rotate(polys, p.orientation, origin=(0,0))
        polys = draw.translate(polys, p.pos_x, p.pos_y)
        [diel, pocket, layer1, layer2, layer1_overlap] = polys
        
        lay1_name = "capa_layer1"
        lay2_name = "capa_layer2"
        lay1_overlap_name = "capa_layer1_overlap"
        diel_name = "capa_diel"
        pocket_name = "capa_pocket"
        chip = p.chip
        
        self.add_qgeometry('poly', {lay1_name: layer1}, chip=chip, layer=p.layer[0])
        if p.overlap:
            self.add_qgeometry('poly', {lay1_overlap_name: layer1_overlap}, chip=chip, layer=p.layer[0])
        self.add_qgeometry('poly', {lay2_name: layer2}, chip=chip, layer=p.layer[1])
        self.add_qgeometry('poly', {diel_name: diel}, chip=chip, layer=p.layer[2])
        self.add_qgeometry('poly', {pocket_name: pocket}, chip=chip, layer=p.layer[0], subtract=True)
        
        self.add_pin("right", layer2.boundary.coords[-2:][::-1], width=p.lead_width)
        self.add_pin("left", layer1.boundary.coords[-2:], width=p.lead_width)