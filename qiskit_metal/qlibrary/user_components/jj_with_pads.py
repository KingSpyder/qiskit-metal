"""File contains dictionary for JJ_with_pads and the make()."""

from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent


class JJ_with_pads(QComponent):
    """Josephson junction with pads.

    Inherits QComponent class.

    The class will add default_options class Dict to QComponent class before calling make.
    """

    default_options = Dict(pads_size='100um',
                           pads_distance="50um",
                           jj_lead_width="2um",
                           jj_bridge_length="2um",
                           jj_bridge_width="2um",
                           jj_to_bridge_length="4um",
                           jj_pad_overlap="10um",
                           undersize="2um",
                           under_spacing="50nm",
                           t_size="2um",
                           layer=[1, 2, 3],
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
        pad1 = draw.subtract(draw.rectangle(p.pads_size, p.pads_size),
                             draw.Polygon([
                                 [p.pads_size/2, -p.t_size/2],
                                 [p.pads_size/2, p.t_size/2],
                                 [p.pads_size/2 - p.t_size*2, p.t_size/2],
                                 [p.pads_size/2 - p.t_size*2, p.t_size*3/2],
                                 [p.pads_size/2 - p.t_size*3, p.t_size*3/2],
                                 [p.pads_size/2 - p.t_size*3, -p.t_size*3/2],
                                 [p.pads_size/2 - p.t_size*2, -p.t_size*3/2],
                                 [p.pads_size/2 - p.t_size*2, -p.t_size/2],
                                 [p.pads_size/2, -p.t_size/2]
                             ]))
        pad2 = draw.subtract(draw.rectangle(p.pads_size, p.pads_size, p.pads_size+p.pads_distance),
                             draw.Polygon([
                                 [p.pads_size/2 + p.pads_distance, -p.t_size/2],
                                 [p.pads_size/2 + p.pads_distance, p.t_size/2],
                                 [p.pads_size/2  + p.pads_distance + p.t_size*2, p.t_size/2],
                                 [p.pads_size/2 + p.pads_distance + p.t_size*2, p.t_size*3/2],
                                 [p.pads_size/2 + p.pads_distance + p.t_size*3, p.t_size*3/2],
                                 [p.pads_size/2 + p.pads_distance + p.t_size*3, -p.t_size*3/2],
                                 [p.pads_size/2  + p.pads_distance + p.t_size*2, -p.t_size*3/2],
                                 [p.pads_size/2  + p.pads_distance + p.t_size*2, -p.t_size/2],
                                 [p.pads_size/2 + p.pads_distance, -p.t_size/2]
                             ]))
       
        underetch = draw.Polygon([
            [p.pads_size/2 + p.pads_distance/2 - p.jj_bridge_width/2 - p.undersize, -p.jj_bridge_length/2 - p.under_spacing],
            [p.pads_size/2 + p.pads_distance/2 - p.jj_bridge_width/2 + p.under_spacing, -p.jj_bridge_length/2 - p.under_spacing],
            [p.pads_size/2 + p.pads_distance/2 - p.jj_bridge_width/2 + p.under_spacing, p.jj_bridge_length/2 + p.under_spacing],
            [p.pads_size/2 + p.pads_distance/2 - p.jj_bridge_width/2 - p.undersize, p.jj_bridge_length/2 + p.under_spacing],
            [p.pads_size/2 + p.pads_distance/2 - p.jj_bridge_width/2 - p.undersize, p.jj_bridge_length/2 + p.undersize],
            [p.pads_size/2 + p.pads_distance/2 + p.jj_bridge_width/2 + p.undersize, p.jj_bridge_length/2 + p.undersize],
            [p.pads_size/2 + p.pads_distance/2 + p.jj_bridge_width/2 + p.undersize, p.jj_bridge_length/2 + p.under_spacing],
            [p.pads_size/2 + p.pads_distance/2 + p.jj_bridge_width/2 - p.under_spacing, p.jj_bridge_length/2 + p.under_spacing],
            [p.pads_size/2 + p.pads_distance/2 + p.jj_bridge_width/2 - p.under_spacing, -p.jj_bridge_length/2 - p.under_spacing],
            [p.pads_size/2 + p.pads_distance/2 + p.jj_bridge_width/2 + p.undersize, -p.jj_bridge_length/2 - p.under_spacing],
            [p.pads_size/2 + p.pads_distance/2 + p.jj_bridge_width/2 + p.undersize, -p.jj_bridge_length/2 - p.undersize],
            [p.pads_size/2 + p.pads_distance/2 - p.jj_bridge_width/2 - p.undersize, -p.jj_bridge_length/2 - p.undersize],
            [p.pads_size/2 + p.pads_distance/2 - p.jj_bridge_width/2 - p.undersize, -p.jj_bridge_length/2 - p.under_spacing]            
        ])
       
        jj1 = draw.Polygon([
            [p.pads_size/2 - p.jj_pad_overlap, -p.jj_lead_width/2],
            [p.pads_size/2 - p.jj_pad_overlap, p.jj_lead_width/2],
            [p.pads_size/2 + p.pads_distance/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length, p.jj_lead_width/2],
            [p.pads_size/2 + p.pads_distance/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length, p.jj_bridge_length/2],
            [p.pads_size/2 + p.pads_distance/2 - p.jj_bridge_width/2, p.jj_bridge_length/2],
            [p.pads_size/2 + p.pads_distance/2 - p.jj_bridge_width/2, -p.jj_bridge_length/2],
            [p.pads_size/2 + p.pads_distance/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length, -p.jj_bridge_length/2],
            [p.pads_size/2 + p.pads_distance/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length, -p.jj_lead_width/2],
            [p.pads_size/2 - p.jj_pad_overlap, -p.jj_lead_width/2]
        ])
        
        jj2 = draw.Polygon([
            [p.pads_size/2 + p.pads_distance + p.jj_pad_overlap, -p.jj_lead_width/2],
            [p.pads_size/2 + p.pads_distance + p.jj_pad_overlap, p.jj_lead_width/2],
            [p.pads_size/2 + p.pads_distance/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length, p.jj_lead_width/2],
            [p.pads_size/2 + p.pads_distance/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length, p.jj_bridge_length/2],
            [p.pads_size/2 + p.pads_distance/2 + p.jj_bridge_width/2, p.jj_bridge_length/2],
            [p.pads_size/2 + p.pads_distance/2 + p.jj_bridge_width/2, -p.jj_bridge_length/2],
            [p.pads_size/2 + p.pads_distance/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length, -p.jj_bridge_length/2],
            [p.pads_size/2 + p.pads_distance/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length, -p.jj_lead_width/2],
            [p.pads_size/2 + p.pads_distance + p.jj_pad_overlap, -p.jj_lead_width/2]
        ])
        
        polys = [pad1, pad2, jj1, jj2, underetch]
        polys = draw.rotate(polys, p.orientation)
        polys = draw.translate(polys, p.pos_x, p.pos_y)
        [pad1, pad2, jj1, jj2, underetch] = polys
        ##############################################
        # add qgeometry
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
        self.add_qgeometry('poly', {'jj1': jj1},
                           subtract=False,
                           helper=p.helper,
                           layer=p.layer[1],
                           chip=p.chip)
        self.add_qgeometry('poly', {'jj2': jj2},
                           subtract=False,
                           helper=p.helper,
                           layer=p.layer[1],
                           chip=p.chip)
        self.add_qgeometry('poly', {'underetch': underetch},
                           subtract=False,
                           helper=p.helper,
                           layer=p.layer[2],
                           chip=p.chip)