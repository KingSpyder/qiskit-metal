"""File contains dictionary for JJ_with_pads and the make()."""

from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent


class JJ_chain_with_pads(QComponent):
    """Josephson junction with pads. Orientation not implemented...

    Inherits QComponent class.

    The class will add default_options class Dict to QComponent class before calling make.
    """

    default_options = Dict(pads_size='75um',
                           pads_dist="20um",
                           jj_to_jj_dist="20um",
                           jj_lead_width="4um",
                           jj_bridge_length="2um",
                           jj_overlength_left='0.5um',
                           jj_bridge_width="300nm",
                           jj_to_bridge_length="4um",
                           undersize="2um",
                           under_spacing="50nm",
                           alignment_tol="1um",
                           layer=[1, 2, 3],
                           lateral_pads_period=20,
                           n_jj=400,
                           helper='False')
    """Default drawing options"""

    TOOLTIP = """A chain of configurable JJ with pads"""
    
    def make_cell(self, offset_x=0, offset_y=0, affix=None, fully_round=None):

        # self.p allows us to directly access parsed values (string -> numbers) form the user option
        p = self.p

        # since we will reuse these options, parse them once and define them as variables
        pos_x = p.pos_x + offset_x
        pos_y = p.pos_y + offset_y
        
        # create the geometry
        wire_length = p.jj_to_jj_dist/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length
        pad1 = draw.rectangle(wire_length, p.jj_lead_width, -p.jj_to_jj_dist/2 + wire_length/2)
        pad2 = draw.rectangle(wire_length, p.jj_lead_width, p.jj_to_jj_dist/2 - wire_length/2)
       
       
        jj_length = p.jj_to_bridge_length + p.alignment_tol
        x_jj_off = p.jj_bridge_width/2 + jj_length/2
        overbridge_length = p.jj_bridge_length + 2*p.jj_overlength_left
        
        
        underetch = draw.Polygon([
            [- p.jj_bridge_width/2 - p.undersize, -overbridge_length/2 - p.under_spacing],
            [- p.jj_bridge_width/2 + p.under_spacing, -overbridge_length/2 - p.under_spacing],
            [- p.jj_bridge_width/2 + p.under_spacing, overbridge_length/2 + p.under_spacing],
            [- p.jj_bridge_width/2 - p.undersize, overbridge_length/2 + p.under_spacing],
            [- p.jj_bridge_width/2 - p.undersize, p.jj_bridge_length/2 + p.undersize],
            [+ p.jj_bridge_width/2 + p.undersize, p.jj_bridge_length/2 + p.undersize],
            [+ p.jj_bridge_width/2 + p.undersize, p.jj_bridge_length/2 + p.under_spacing],
            [+ p.jj_bridge_width/2 - p.under_spacing, p.jj_bridge_length/2 + p.under_spacing],
            [+ p.jj_bridge_width/2 - p.under_spacing, -p.jj_bridge_length/2 - p.under_spacing],
            [+ p.jj_bridge_width/2 + p.undersize, -p.jj_bridge_length/2 - p.under_spacing],
            [+ p.jj_bridge_width/2 + p.undersize, -p.jj_bridge_length/2 - p.undersize],
            [- p.jj_bridge_width/2 - p.undersize, -p.jj_bridge_length/2 - p.undersize],
            [- p.jj_bridge_width/2 - p.undersize, -overbridge_length/2 - p.under_spacing]            
        ])
       
        
        jj1 = draw.rectangle(jj_length, overbridge_length, - x_jj_off)
        jj2 = draw.rectangle(jj_length, p.jj_bridge_length, + x_jj_off)
        
        polys = [pad1, pad2, jj1, jj2, underetch]
        polys = draw.rotate(polys, p.orientation)
        polys = draw.translate(polys, pos_x, pos_y)
        [pad1, pad2, jj1, jj2, underetch] = polys
        ##############################################
        # add qgeometry
        self.add_qgeometry('poly', {'pad1' + affix: pad1},
                           subtract=False,
                           helper=p.helper,
                           layer=p.layer[0],
                           chip=p.chip)
        self.add_qgeometry('poly', {'pad2' + affix: pad2},
                           subtract=False,
                           helper=p.helper,
                           layer=p.layer[0],
                           chip=p.chip)
        self.add_qgeometry('poly', {'jj1' + affix: jj1},
                           subtract=False,
                           helper=p.helper,
                           layer=p.layer[1],
                           chip=p.chip)
        self.add_qgeometry('poly', {'jj2' + affix: jj2},
                           subtract=False,
                           helper=p.helper,
                           layer=p.layer[1],
                           chip=p.chip)
        self.add_qgeometry('poly', {'underetch' + affix: underetch},
                           subtract=False,
                           helper=p.helper,
                           layer=p.layer[2],
                           chip=p.chip)
        
    def make_lead(self, offset_x, offset_y, rotation, affix):
        p = self.p
        
        pos_x = p.pos_x + offset_x
        pos_y = p.pos_y + offset_y
        
        lead = draw.rectangle(p.jj_lead_width, p.pads_dist,
                              0, -p.pads_dist/2)
        pad = draw.rectangle(p.pads_size, p.pads_size,
                             0, - p.pads_dist - p.pads_size/2)
        polys = [lead, pad]
        polys = draw.rotate(polys, rotation, origin=(0, 0))
        polys = draw.translate(polys, pos_x, pos_y)
        [lead, pad] = polys
        
        self.add_qgeometry('poly', {'lead' + affix: lead},
                           subtract=False,
                           helper=p.helper,
                           layer=p.layer[0],
                           chip=p.chip)
        self.add_qgeometry('poly', {'pad' + affix: pad},
                           subtract=False,
                           helper=p.helper,
                           layer=p.layer[0],
                           chip=p.chip)
        
        
    def make(self):
        p = self.p
        
        for i_jj in range(p.n_jj):
            off_x = i_jj*(p.jj_to_jj_dist)
            self.make_cell(off_x, 0, str(i_jj))
            
        #2 outer pads
        self.make_lead(-p.jj_to_jj_dist/2, 0, -90, "left")
        self.make_lead(p.jj_to_jj_dist*(p.n_jj-1/2), 0, 90, "right")
        
        #side pads
        for i_side in range(1, p.n_jj//p.lateral_pads_period):
            self.make_lead(p.jj_to_jj_dist*(i_side*p.lateral_pads_period - 1/2),
                           -p.jj_lead_width/2, 0, str(i_side))