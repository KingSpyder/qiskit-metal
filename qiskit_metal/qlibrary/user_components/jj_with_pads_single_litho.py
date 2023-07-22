"""File contains dictionary for JJ_with_pads and the make()."""

from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent


class JJ_with_pads(QComponent):
    """Josephson junction with pads.

    Inherits QComponent class.

    The class will add default_options class Dict to QComponent class before calling make.
    """

    default_options = Dict(pads_size='75um',
                           pads_distance="50um",
                           jj_lead_width="4um",
                           jj_bridge_length="2um",
                           jj_overlength_left='0.5um',
                           jj_bridge_width="2um",
                           jj_to_bridge_length="4um",
                           undersize="2um",
                           under_spacing="50nm",
                           alignment_tol="500nm",
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
        wire_length = p.pads_distance/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length
        pad1 = draw.union(draw.rectangle(p.pads_size, p.pads_size, -p.pads_size/2 - p.pads_distance/2),
                          draw.rectangle(wire_length, p.jj_lead_width, -p.pads_distance/2 + wire_length/2))
        pad2 = draw.union(draw.rectangle(p.pads_size, p.pads_size, p.pads_size/2+p.pads_distance/2),
                          draw.rectangle(wire_length, p.jj_lead_width, p.pads_distance/2 - wire_length/2))
       
       
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