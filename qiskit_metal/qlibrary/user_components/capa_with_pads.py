"""File contains dictionary for JJ_with_pads and the make()."""

from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent


def round_polygon(polygon, radius):
    return polygon.buffer(radius).buffer(-2*radius).buffer(radius)


class capaJanis(QComponent):
    """Layered capacitor with pads for Janis.

    Inherits QComponent class.

    The class will add default_options class Dict to QComponent class before calling make.
    """

    default_options = Dict(pad_gap='23.5um',
                           pad_width="50um",
                           pad_length="100um",
                           capa_height="15um",
                           capa_width="15um",
                           top_cap_reduction="1.7um",
                           capa_lead_width="8um",
                           top_cap_gnd_overlap="15um",
                           top_cap_gnd_overlap_height="15um",
                           alignment_tol="1um",
                           corner_rounding="200nm",
                           diel_overlap="5um",
                           layer=[1, 2, 3],
                           helper='False')
    """Default drawing options"""

    TOOLTIP = """A single configurable capacitor with pads for Janis setup"""

    def make(self):
        """The make function implements the logic that creates the geoemtry
        (poly, path, etc.) from the qcomponent.options dictionary of
        parameters, and the adds them to the design, using
        qcomponent.add_qgeometry(...), adding in extra needed information, such
        as layer, subtract, etc."""
        p = self.p  # p for parsed parameters. Access to the parsed options.

        # create the geometry
        
        pocket = round_polygon(draw.Polygon([
            [-2*p.pad_gap, -p.pad_width/2 - p.pad_gap],
            [-2*p.pad_gap, p.pad_width/2 + p.pad_gap],
            [p.pad_length - p.pad_gap, p.pad_width/2 + p.pad_gap],
            [p.pad_length - p.pad_gap, p.capa_height/2 + p.pad_gap],
            [p.pad_length + p.capa_width + p.pad_gap/2, p.capa_height/2 + p.pad_gap],
            [p.pad_length + p.capa_width + p.pad_gap/2, -p.capa_height/2 - p.pad_gap],
            [p.pad_length - p.pad_gap, -p.capa_height/2 - p.pad_gap],
            [p.pad_length - p.pad_gap, -p.pad_width/2 - p.pad_gap]
        ]), p.corner_rounding)
        
        bottom_conduc = round_polygon(draw.Polygon([
            [0, -p.pad_width/2],
            [0, p.pad_width/2],
            [p.pad_length - p.capa_lead_width, p.pad_width/2],
            [p.pad_length - p.capa_lead_width, p.capa_lead_width/2],
            [p.pad_length, p.capa_lead_width/2],
            [p.pad_length, p.capa_height/2],
            [p.pad_length + p.capa_width, p.capa_height/2],
            [p.pad_length + p.capa_width, -p.capa_height/2],
            [p.pad_length, -p.capa_height/2],
            [p.pad_length, -p.capa_lead_width/2],
            [p.pad_length - p.capa_lead_width, -p.capa_lead_width/2],
            [p.pad_length - p.capa_lead_width, -p.pad_width/2]
        ]), p.corner_rounding)
        
        top_conduc = round_polygon(draw.Polygon([
            [p.pad_length + p.alignment_tol, -p.capa_height/2 + p.top_cap_reduction],
            [p.pad_length + p.alignment_tol, p.capa_height/2 - p.top_cap_reduction],
            [p.pad_length + p.capa_width - p.alignment_tol, p.capa_height/2 - p.top_cap_reduction],
            [p.pad_length + p.capa_width - p.alignment_tol, p.capa_lead_width/2],
            [p.pad_length + p.capa_width + p.pad_gap/2 + p.diel_overlap + p.alignment_tol, p.capa_lead_width/2],
            [p.pad_length + p.capa_width + p.pad_gap/2 + p.diel_overlap + p.alignment_tol, p.capa_lead_width/2],
            [p.pad_length + p.capa_width + p.pad_gap/2 + p.diel_overlap + p.alignment_tol, p.top_cap_gnd_overlap_height/2],
            [p.pad_length + p.capa_width + p.pad_gap/2 + p.diel_overlap + p.alignment_tol + p.top_cap_gnd_overlap, p.top_cap_gnd_overlap_height/2],
            [p.pad_length + p.capa_width + p.pad_gap/2 + p.diel_overlap + p.alignment_tol + p.top_cap_gnd_overlap, -p.top_cap_gnd_overlap_height/2],
            [p.pad_length + p.capa_width + p.pad_gap/2 + p.diel_overlap + p.alignment_tol, -p.top_cap_gnd_overlap_height/2],
            [p.pad_length + p.capa_width + p.pad_gap/2 + p.diel_overlap + p.alignment_tol, -p.capa_lead_width/2],
            [p.pad_length + p.capa_width - p.alignment_tol, -p.capa_lead_width/2],
            [p.pad_length + p.capa_width - p.alignment_tol, -p.capa_height/2 + p.top_cap_reduction]
        ]), p.corner_rounding)
        
        diel = round_polygon(draw.rectangle(2*p.diel_overlap + p.capa_width + p.pad_gap, p.capa_height + 2*p.diel_overlap + 2*p.pad_gap,
                             p.pad_length + p.capa_width/2, 0), p.corner_rounding)
        
        polys = [pocket, bottom_conduc, top_conduc, diel]
        polys = draw.rotate(polys, p.orientation)
        polys = draw.translate(polys, p.pos_x, p.pos_y)
        [pocket, bottom_conduc, top_conduc, diel] = polys
        ##############################################
        # add qgeometry
        self.add_qgeometry('poly', {'pocket': pocket},
                           subtract=True,
                           helper=p.helper,
                           layer=p.layer[0],
                           chip=p.chip)
        self.add_qgeometry('poly', {'bottom_conduc': bottom_conduc},
                           subtract=False,
                           helper=p.helper,
                           layer=p.layer[0],
                           chip=p.chip)
        self.add_qgeometry('poly', {'top_conduc': top_conduc},
                           subtract=False,
                           helper=p.helper,
                           layer=p.layer[2],
                           chip=p.chip)
        self.add_qgeometry('poly', {'diel': diel},
                           subtract=False,
                           helper=p.helper,
                           layer=p.layer[1],
                           chip=p.chip)