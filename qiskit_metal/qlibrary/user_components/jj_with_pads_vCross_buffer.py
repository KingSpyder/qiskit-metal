"""File contains dictionary for JJ_with_pads and the make()."""

from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent

def round_polygon(polygon, radius):
    return polygon.buffer(radius).buffer(-2*radius).buffer(radius)

class JJ_with_pads_and_buffer(QComponent):
    """Josephson junction with pads.

    Inherits QComponent class.

    The class will add default_options class Dict to QComponent class before calling make.
    """

    default_options = Dict(pads_size='75um',
                           pads_distance="50um",
                           lead_width="12um",
                           jj_lead_width="3um",
                           jj_left_width="0.4um",
                           jj_right_width="0.4um",
                           jj_bridge_width="0.25um",
                           jj_to_bridge_length="7um",
                           jj_left_wire_width="0.625um",
                           jj_fine_length="2um",
                           small_aperture_dist="4um",
                           undercut_height="4.1um",
                           undercut_width="2.5um",
                           under_spacing="60nm",
                           alignment_tol="1000nm",
                           jj_t_size="1um",
                           corner_rounding="200nm",
                           al_patch_dist="2.235um",
                           fake_diel_patch_dist="10.2um",
                           layer=[1, 2, 3, 4, 5],
                           buffer_size="10um",
                           helper='False')
    """Default drawing options"""

    TOOLTIP = """A single configurable JJ with pads"""

    def make(self):
        """The make function implements the logic that creates the geoemtry
        (poly, path, etc.) from the qcomponent.options dictionary of
        parameters, and the adds them to the design, using
        qcomponent.add_qgeometry(...), adding in extra needed information, such
        as layer, subtract, etc."""
        p = self.p  # p for parsed parameters. Access to the parsed options.

        # create the geometry
        wire_length = p.pads_distance/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length
        
        fake_diel_patch = draw.union(
            draw.rectangle(p.pads_distance - 10*p.alignment_tol, p.lead_width,
                           0, -p.fake_diel_patch_dist - p.lead_width/2),
            draw.rectangle(p.pads_distance - 10*p.alignment_tol, p.lead_width,
                                         0, p.fake_diel_patch_dist + p.lead_width/2)
            )
        
        pad1 = round_polygon(
            draw.union(
                draw.rectangle(p.pads_size, p.pads_size, -p.pads_size/2 - p.pads_distance/2),
                draw.subtract(
                    draw.rectangle(wire_length, p.lead_width, -p.pads_distance/2 + wire_length/2),
                    draw.Polygon([
                        [-p.pads_distance/2 + wire_length, p.jj_t_size/2],
                        [-p.pads_distance/2 + wire_length - p.jj_t_size, p.jj_t_size/2],
                        [-p.pads_distance/2 + wire_length - p.jj_t_size, 3/2*p.jj_t_size],
                        [-p.pads_distance/2 + wire_length - 2*p.jj_t_size, 3/2*p.jj_t_size],
                        [-p.pads_distance/2 + wire_length - 2*p.jj_t_size, -3/2*p.jj_t_size],
                        [-p.pads_distance/2 + wire_length - p.jj_t_size, -3/2*p.jj_t_size],
                        [-p.pads_distance/2 + wire_length - p.jj_t_size, -p.jj_t_size/2],
                        [-p.pads_distance/2 + wire_length, -p.jj_t_size/2],
                    ])
                )
            ),
            p.corner_rounding
        )
        pad2 = round_polygon(
            draw.union(
                draw.rectangle(p.pads_size, p.pads_size, p.pads_size/2+p.pads_distance/2),
                draw.subtract(
                    draw.rectangle(wire_length, p.lead_width, p.pads_distance/2 - wire_length/2),
                    draw.Polygon([
                        [p.pads_distance/2 - wire_length, p.jj_t_size/2],
                        [p.pads_distance/2 - wire_length + p.jj_t_size, p.jj_t_size/2],
                        [p.pads_distance/2 - wire_length + p.jj_t_size, 3/2*p.jj_t_size],
                        [p.pads_distance/2 - wire_length + 2*p.jj_t_size, 3/2*p.jj_t_size],
                        [p.pads_distance/2 - wire_length + 2*p.jj_t_size, -3/2*p.jj_t_size],
                        [p.pads_distance/2 - wire_length + p.jj_t_size, -3/2*p.jj_t_size],
                        [p.pads_distance/2 - wire_length + p.jj_t_size, -p.jj_t_size/2],
                        [p.pads_distance/2 - wire_length, -p.jj_t_size/2],
                    ])
                )
            ),
            p.corner_rounding
        )
        
        lead1 = draw.Polygon([
            [p.jj_bridge_width/2 + p.small_aperture_dist, -p.jj_lead_width/2],
            [p.jj_bridge_width/2 + p.small_aperture_dist, p.jj_lead_width/2],
            [p.jj_bridge_width/2 + p.jj_to_bridge_length + p.al_patch_dist, p.jj_lead_width/2],
            [p.jj_bridge_width/2 + p.jj_to_bridge_length + p.al_patch_dist, p.lead_width/2],
            [p.pads_distance/2, p.lead_width/2],
            [p.pads_distance/2, -p.lead_width/2],
            [p.jj_bridge_width/2 + p.jj_to_bridge_length + p.al_patch_dist, -p.lead_width/2],
            [p.jj_bridge_width/2 + p.jj_to_bridge_length + p.al_patch_dist, -p.jj_lead_width/2]
        ])
        
        lead2 = draw.Polygon([
            [-p.jj_bridge_width/2 - p.small_aperture_dist, -p.jj_lead_width/2],
            [-p.jj_bridge_width/2 - p.small_aperture_dist, p.jj_lead_width/2],
            [-p.jj_bridge_width/2 - p.jj_to_bridge_length - p.al_patch_dist, p.jj_lead_width/2],
            [-p.jj_bridge_width/2 - p.jj_to_bridge_length - p.al_patch_dist, p.lead_width/2],
            [-p.pads_distance/2, p.lead_width/2],
            [-p.pads_distance/2, -p.lead_width/2],
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
        polys = draw.translate(polys, p.pos_x, p.pos_y)
        [fake_diel_patch, pad1, pad2, lead1, lead2, underetch, jj_left, jj_right] = polys
        
        pocket = draw.union(
            draw.union(pad1, pad2).buffer(p.buffer_size),
            draw.rectangle(p.pads_distance, 2*p.lead_width + 2*p.fake_diel_patch_dist, p.pos_x, p.pos_y)
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