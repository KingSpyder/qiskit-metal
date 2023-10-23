"""File contains dictionary for JJ_with_pads and the make()."""

from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent

def round_polygon(polygon, radius):
    return polygon.buffer(radius).buffer(-2*radius).buffer(radius)

class JJ_chain_with_buffer(QComponent):
    """Josephson junction with pads.

    Inherits QComponent class.

    The class will add default_options class Dict to QComponent class before calling make.
    """

    default_options = Dict(pads_size='75um',
                           pads_dist="50um",
                           jj_to_jj_dist="20um",
                           lead_width="12um",
                           jj_lead_width="3um",
                           jj_left_width="0.4um",
                           jj_right_width="0.4um",
                           jj_bridge_width="2um",
                           jj_to_bridge_length="7um",
                           jj_left_wire_width="0.625um",
                           jj_fine_length="2um",
                           small_aperture_dist="4um",
                           undercut_height="4.1um",
                           undercut_width="2.5um",
                           under_spacing="60nm",
                           alignment_tol="1000nm",
                           layer=[1, 2, 3, 4, 5],
                           jj_t_size="1um",
                           lateral_pads_period=20,
                           n_jj=100,
                           side_lead_width="6um",
                           corner_rounding="200nm",
                           al_patch_dist="2.235um",
                           fake_diel_patch_dist="10.2um",
                           buffer_size="10um",
                           helper='False')
    """Default drawing options"""

    TOOLTIP = """A single configurable JJ with pads"""

    def make_cell(self, offset_x, offset_y, affix=""):
        """The make function implements the logic that creates the geoemtry
        (poly, path, etc.) from the qcomponent.options dictionary of
        parameters, and the adds them to the design, using
        qcomponent.add_qgeometry(...), adding in extra needed information, such
        as layer, subtract, etc."""
        p = self.p  # p for parsed parameters. Access to the parsed options.

        # create the geometry
        wire_length = p.jj_to_jj_dist/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length
        
        fake_diel_patch = draw.union(
            draw.rectangle(p.jj_to_jj_dist, p.lead_width,
                           0, -p.fake_diel_patch_dist - p.lead_width/2),
            draw.rectangle(p.jj_to_jj_dist, p.lead_width,
                                         0, p.fake_diel_patch_dist + p.lead_width/2)
            )
        
        pad1 = round_polygon(
            draw.subtract(
                draw.rectangle(wire_length, p.lead_width, -p.jj_to_jj_dist/2 + wire_length/2),
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
                draw.rectangle(wire_length, p.lead_width, p.jj_to_jj_dist/2 - wire_length/2),
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
            [p.jj_bridge_width/2 + p.small_aperture_dist, -p.jj_lead_width/2],
            [p.jj_bridge_width/2 + p.small_aperture_dist, p.jj_lead_width/2],
            [p.jj_bridge_width/2 + p.jj_to_bridge_length + p.al_patch_dist, p.jj_lead_width/2],
            [p.jj_bridge_width/2 + p.jj_to_bridge_length + p.al_patch_dist, p.lead_width/2],
            [p.jj_to_jj_dist/2, p.lead_width/2],
            [p.jj_to_jj_dist/2, -p.lead_width/2],
            [p.jj_bridge_width/2 + p.jj_to_bridge_length + p.al_patch_dist, -p.lead_width/2],
            [p.jj_bridge_width/2 + p.jj_to_bridge_length + p.al_patch_dist, -p.jj_lead_width/2]
        ])
        
        lead2 = draw.Polygon([
            [-p.jj_bridge_width/2 - p.small_aperture_dist, -p.jj_lead_width/2],
            [-p.jj_bridge_width/2 - p.small_aperture_dist, p.jj_lead_width/2],
            [-p.jj_bridge_width/2 - p.jj_to_bridge_length - p.al_patch_dist, p.jj_lead_width/2],
            [-p.jj_bridge_width/2 - p.jj_to_bridge_length - p.al_patch_dist, p.lead_width/2],
            [-p.jj_to_jj_dist/2, p.lead_width/2],
            [-p.jj_to_jj_dist/2, -p.lead_width/2],
            [-p.jj_bridge_width/2 - p.jj_to_bridge_length - p.al_patch_dist, -p.lead_width/2],
            [-p.jj_bridge_width/2 - p.jj_to_bridge_length - p.al_patch_dist, -p.jj_lead_width/2]
        ])
       
        jj_left = draw.Polygon([
            [-p.jj_bridge_width/2 - p.small_aperture_dist - p.alignment_tol, -p.jj_lead_width/2],
            [-p.jj_bridge_width/2 - p.small_aperture_dist - p.alignment_tol, p.jj_lead_width/2],
            [-p.jj_bridge_width/2 - p.jj_left_width - p.jj_fine_length, p.jj_lead_width/2],
            [-p.jj_bridge_width/2 - p.jj_left_width - p.jj_fine_length, -p.jj_lead_width/2 + p.jj_left_wire_width],
            [-p.jj_bridge_width/2 - p.jj_left_width, -p.jj_lead_width/2 + p.jj_left_wire_width],
            [-p.jj_bridge_width/2 - p.jj_left_width, p.jj_lead_width/2],
            [-p.jj_bridge_width/2, p.jj_lead_width/2],
            [-p.jj_bridge_width/2, -p.jj_lead_width/2]      
        ])
        
        jj_right = draw.Polygon([
            [p.jj_bridge_width/2 + p.small_aperture_dist + p.alignment_tol, -p.jj_lead_width/2],
            [p.jj_bridge_width/2 + p.jj_right_width + p.jj_fine_length, -p.jj_lead_width/2],
            [p.jj_bridge_width/2 + p.jj_right_width + p.jj_fine_length, p.jj_left_wire_width/2 - p.jj_right_width/2],
            [p.jj_bridge_width/2, p.jj_left_wire_width/2 - p.jj_right_width/2],
            [p.jj_bridge_width/2, p.jj_left_wire_width/2 + p.jj_right_width/2],
            [p.jj_bridge_width/2 + p.jj_right_width + p.jj_fine_length, p.jj_left_wire_width/2 + p.jj_right_width/2],
            [p.jj_bridge_width/2 + p.jj_right_width + p.jj_fine_length, p.jj_lead_width/2],
            [p.jj_bridge_width/2 + p.small_aperture_dist + p.alignment_tol, p.jj_lead_width/2]
        ])
        
        underetch = draw.Polygon([
            [-p.undercut_width/2, -p.undercut_height/2 + p.jj_left_wire_width/2],
            [-p.undercut_width/2, -p.jj_lead_width/2 - p.under_spacing],
            [-p.jj_bridge_width/2 + p.under_spacing, -p.jj_lead_width/2 - p.under_spacing],
            [-p.jj_bridge_width/2 + p.under_spacing, p.jj_lead_width/2 + p.under_spacing],
            [-p.jj_bridge_width/2 - p.jj_left_width - p.under_spacing, p.jj_lead_width/2 + p.under_spacing],
            [-p.jj_bridge_width/2 - p.jj_left_width - p.under_spacing, -p.jj_lead_width/2 + p.jj_left_wire_width + p.under_spacing],
            [-p.undercut_width/2, -p.jj_lead_width/2 + p.jj_left_wire_width + p.under_spacing],
            [-p.undercut_width/2, p.undercut_height/2],
            [p.undercut_width/2, p.undercut_height/2],
            [p.undercut_width/2, p.jj_left_wire_width/2 + p.jj_right_width/2 + p.under_spacing],
            [p.jj_bridge_width/2 - p.under_spacing, p.jj_left_wire_width/2 + p.jj_right_width/2 + p.under_spacing],
            [p.jj_bridge_width/2 - p.under_spacing, p.jj_left_wire_width/2 - p.jj_right_width/2 - p.under_spacing],
            [p.undercut_width/2, p.jj_left_wire_width/2 - p.jj_right_width/2 - p.under_spacing],
            [p.undercut_width/2, -p.undercut_height/2 + p.jj_left_wire_width/2]
        ])
       
        polys = [fake_diel_patch, pad1, pad2, lead1, lead2, underetch, jj_left, jj_right]
        polys = draw.rotate(polys, p.orientation)
        polys = draw.translate(polys, p.pos_x + offset_x, p.pos_y + offset_y)
        [fake_diel_patch, pad1, pad2, lead1, lead2, underetch, jj_left, jj_right] = polys
        
        pocket = draw.union(
            draw.union(pad1, pad2).buffer(p.buffer_size),
            draw.rectangle(p.jj_to_jj_dist, 2*p.lead_width + 2*p.fake_diel_patch_dist, p.pos_x, p.pos_y)
        )
        ##############################################
        # add qgeometry
        
        self.add_qgeometry('poly', {f"jj_L": jj_left},
                            subtract=False,
                            helper=p.helper,
                            layer=p.layer[2],
                            chip=p.chip)
        self.add_qgeometry('poly', {f"jj_cut_R_bulk": jj_right},
                            subtract=False,
                            helper=p.helper,
                            layer=p.layer[2],
                            chip=p.chip)
        
        self.add_qgeometry('poly', {'fake_diel': fake_diel_patch},
                           subtract=False,
                           helper=p.helper,
                           layer=p.layer[4],
                           chip=p.chip)
        self.add_qgeometry('poly', {'pocket': pocket},
                           subtract=True,
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
                           layer=p.layer[3],
                           chip=p.chip)
        
        
    def make_lead(self, offset_x, offset_y, rotation, affix):
        p = self.p
        
        pos_x = p.pos_x + offset_x
        pos_y = p.pos_y + offset_y
        
        lead = draw.rectangle(p.side_lead_width, p.pads_dist,
                              0, -p.pads_dist/2)
        pad = draw.rectangle(p.pads_size, p.pads_size,
                             0, - p.pads_dist - p.pads_size/2)
        pocket = draw.union(pad, lead).buffer(p.buffer_size)
        
        polys = [lead, pad, pocket]
        polys = draw.rotate(polys, rotation, origin=(0, 0))
        polys = draw.translate(polys, pos_x, pos_y)
        [lead, pad, pocket] = polys
        
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
        self.add_qgeometry('poly', {'pocket' + affix: pocket},
                           subtract=True,
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
                           -p.lead_width/2, 0, str(i_side))