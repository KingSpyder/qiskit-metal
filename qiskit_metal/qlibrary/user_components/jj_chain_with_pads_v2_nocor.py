"""File contains dictionary for JJ_with_pads and the make()."""

from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent

def round_polygon(polygon, radius):
    return polygon.buffer(radius).buffer(-2*radius).buffer(radius)

class JJ_chain_with_pads(QComponent):
    """Josephson junction with pads. Orientation not implemented...

    Inherits QComponent class.

    The class will add default_options class Dict to QComponent class before calling make.
    """

    default_options = Dict(pads_size='75um',
                           pads_dist="20um",
                           jj_to_jj_dist="20um",
                           jj_lead_width="12um",
                           jj_wire_width="8um",
                           jj_bridge_length="8um",
                           jj_overlength_left='0um',
                           jj_bridge_width="330nm",
                           jj_to_bridge_length="7um",
                           jj_fine_length="2um",
                           undersize="0.45um",
                           under_spacing="50nm",
                           alignment_tol="1um",
                           layer=[1, 2, 3, 4],
                           lateral_pads_period=20,
                           n_jj=100,
                           side_lead_width="6um",
                           corner_rounding="200nm",
                           jj_t_size="1um",
                           al_patch_dist="2.235um",
                           fake_diel_patch_dist="10.2um",
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
        
        fake_diel_patch = draw.union(
            draw.rectangle(p.jj_to_jj_dist, p.jj_lead_width,
                           0, -p.fake_diel_patch_dist - p.jj_lead_width/2),
            draw.rectangle(p.jj_to_jj_dist, p.jj_lead_width,
                                         0, p.fake_diel_patch_dist + p.jj_lead_width/2)
            )
        
        pad1 = round_polygon(
                draw.subtract(
                    draw.rectangle(wire_length, p.jj_lead_width, -p.jj_to_jj_dist/2 + wire_length/2),
                    draw.Polygon([
                        [-p.jj_to_jj_dist/2 + wire_length, p.jj_t_size/2],
                        [-p.jj_to_jj_dist/2 + wire_length - p.jj_t_size, p.jj_t_size/2],
                        [-p.jj_to_jj_dist/2 + wire_length - p.jj_t_size, 3/2*p.jj_t_size],
                        [-p.jj_to_jj_dist/2 + wire_length - 2*p.jj_t_size, 3/2*p.jj_t_size],
                        [-p.jj_to_jj_dist/2 + wire_length - 2*p.jj_t_size, -3/2*p.jj_t_size],
                        [-p.jj_to_jj_dist/2 + wire_length - p.jj_t_size, -3/2*p.jj_t_size],
                        [-p.jj_to_jj_dist/2 + wire_length - p.jj_t_size, -p.jj_t_size/2],
                        [-p.jj_to_jj_dist/2 + wire_length, -p.jj_t_size/2],
                    ])
                ),
                p.corner_rounding
        )
        pad2 = round_polygon(
                draw.subtract(
                    draw.rectangle(wire_length, p.jj_lead_width, p.jj_to_jj_dist/2 - wire_length/2),
                    draw.Polygon([
                        [p.jj_to_jj_dist/2 - wire_length, p.jj_t_size/2],
                        [p.jj_to_jj_dist/2 - wire_length + p.jj_t_size, p.jj_t_size/2],
                        [p.jj_to_jj_dist/2 - wire_length + p.jj_t_size, 3/2*p.jj_t_size],
                        [p.jj_to_jj_dist/2 - wire_length + 2*p.jj_t_size, 3/2*p.jj_t_size],
                        [p.jj_to_jj_dist/2 - wire_length + 2*p.jj_t_size, -3/2*p.jj_t_size],
                        [p.jj_to_jj_dist/2 - wire_length + p.jj_t_size, -3/2*p.jj_t_size],
                        [p.jj_to_jj_dist/2 - wire_length + p.jj_t_size, -p.jj_t_size/2],
                        [p.jj_to_jj_dist/2 - wire_length, -p.jj_t_size/2],
                    ])
                ),
                p.corner_rounding
        )
        
        lead1 = draw.Polygon([
            [p.jj_bridge_width/2 + p.jj_fine_length, -p.jj_wire_width/2],
            [p.jj_bridge_width/2 + p.jj_fine_length, p.jj_wire_width/2],
            [p.jj_bridge_width/2 + p.jj_to_bridge_length + p.al_patch_dist, p.jj_wire_width/2],
            [p.jj_bridge_width/2 + p.jj_to_bridge_length + p.al_patch_dist, p.jj_lead_width/2],
            [p.jj_to_jj_dist/2, p.jj_lead_width/2],
            [p.jj_to_jj_dist/2, -p.jj_lead_width/2],
            [p.jj_bridge_width/2 + p.jj_to_bridge_length + p.al_patch_dist, -p.jj_lead_width/2],
            [p.jj_bridge_width/2 + p.jj_to_bridge_length + p.al_patch_dist, -p.jj_wire_width/2]            
        ])
        
        lead2 = draw.Polygon([
            [-p.jj_bridge_width/2 - p.jj_fine_length, -p.jj_wire_width/2],
            [-p.jj_bridge_width/2 - p.jj_fine_length, p.jj_wire_width/2],
            [-p.jj_bridge_width/2 - p.jj_to_bridge_length - p.al_patch_dist, p.jj_wire_width/2],
            [-p.jj_bridge_width/2 - p.jj_to_bridge_length - p.al_patch_dist, p.jj_lead_width/2],
            [-p.jj_to_jj_dist/2, p.jj_lead_width/2],
            [-p.jj_to_jj_dist/2, -p.jj_lead_width/2],
            [-p.jj_bridge_width/2 - p.jj_to_bridge_length - p.al_patch_dist, -p.jj_lead_width/2],
            [-p.jj_bridge_width/2 - p.jj_to_bridge_length - p.al_patch_dist, -p.jj_wire_width/2]            
        ])
       
       
        jj_length = p.jj_fine_length + p.alignment_tol
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
       
        
        jj_rects = [draw.rectangle(jj_length, p.jj_bridge_length, -jj_length/2-p.jj_bridge_width/2),
                    draw.rectangle(jj_length, p.jj_bridge_length, jj_length/2+p.jj_bridge_width/2)]
        
        jj_rects = draw.rotate(jj_rects, p.orientation)
        jj_rects = draw.translate(jj_rects, pos_x, pos_y)
        
        polys = [fake_diel_patch, pad1, pad2, lead1, lead2, underetch]
        polys = draw.rotate(polys, p.orientation)
        polys = draw.translate(polys, pos_x, pos_y)
        [fake_diel_patch, pad1, pad2, lead1, lead2, underetch] = polys
        ##############################################
        # add qgeometry
        
        self.add_qgeometry('poly', {f"jj_cut_L_bulk": jj_rects[0]},
                            subtract=False,
                            helper=p.helper,
                            layer=p.layer[3],
                            chip=p.chip)
        self.add_qgeometry('poly', {f"jj_cut_R_bulk": jj_rects[1]},
                            subtract=False,
                            helper=p.helper,
                            layer=p.layer[3],
                            chip=p.chip)
        
        self.add_qgeometry('poly', {'fake_diel': fake_diel_patch},
                           subtract=False,
                           helper=p.helper,
                           layer=p.layer[0],
                           chip=p.chip)
        self.add_qgeometry('poly', {'pad1': pad1},
                           subtract=False,
                           helper=p.helper,
                           layer=p.layer[0],
                           chip=p.chip)
        self.add_qgeometry('poly', {'pad2': pad2},
                           subtract=False,
                           helper=p.helper,
                           layer=p.layer[0],
                           chip=p.chip)
        self.add_qgeometry('poly', {'lead1': lead1},
                           subtract=False,
                           helper=p.helper,
                           layer=p.layer[1],
                           chip=p.chip)
        self.add_qgeometry('poly', {'lead2': lead2},
                           subtract=False,
                           helper=p.helper,
                           layer=p.layer[1],
                           chip=p.chip)
        self.add_qgeometry('poly', {'underetch': underetch},
                           subtract=False,
                           helper=p.helper,
                           layer=p.layer[2],
                           chip=p.chip)
        
    def make_lead(self, offset_x, offset_y, rotation, affix):
        p = self.p
        
        pos_x = p.pos_x + offset_x
        pos_y = p.pos_y + offset_y
        
        lead = draw.rectangle(p.side_lead_width, p.pads_dist,
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