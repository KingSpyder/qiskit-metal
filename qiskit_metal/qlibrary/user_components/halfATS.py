from re import T
import numpy as np
from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent

def draw_rectangle_corner_offset(w, h, xoff=0, yoff=0):
    return draw.rectangle(w, h, xoff+w/2, yoff+h/2)

class HalfATS(QComponent):
    default_options = Dict(
        inductor_width='5um',
        pad_width='5um',
        cell_length='50um',
        jj_wire_width='3um',
        bridge_width='350nm',
        jj_width='0.4um',
        jj_wire_spacing='30um',
        jj_lead_width='1um',
        jj_lead_length='5um',
        gap_inner='5um',
        gap_outer='30um',
        layers=[1,2],
        # 0 has dipole aligned along the +X axis,
        # while 90 has dipole aligned along the +Y axis
    )
    """Default drawing options"""

    component_metadata = Dict(short_name='Pocket',
                              _qgeometry_table_path='True',
                              _qgeometry_table_poly='True',
                              _qgeometry_table_junction='True')
    """Component metadata"""

    TOOLTIP = """HalfATS."""
    
    def make_cell(self, offset_x=0, offset_y=0, alternate=False, affix=None):

        # self.p allows us to directly access parsed values (string -> numbers) form the user option
        p = self.p

        # extract chip name
        chip = p.chip

        # since we will reuse these options, parse them once and define them as variables
        pad_height = p.jj_wire_width + p.gap_inner + p.inductor_width
        pos_x = p.pos_x + offset_x
        pos_y = p.pos_y + offset_y

        # make the pads as rectangles (shapely polygons)
        pad_left = draw_rectangle_corner_offset(p.pad_width, pad_height, 0, -p.inductor_width/2)
        pad_right = draw.translate(pad_left, p.cell_length+p.pad_width, 0)
        inductor = draw_rectangle_corner_offset(p.cell_length, p.inductor_width,
                                                p.pad_width, -p.inductor_width/2)
        
        jj_wire_raw = draw_rectangle_corner_offset(p.cell_length, -p.jj_wire_width,
                                                   p.pad_width, pad_height-p.inductor_width/2)
        wire_sub_pos = p.pad_width + p.cell_length/2 - p.jj_wire_spacing/2
        jj_wire_sub = draw_rectangle_corner_offset(p.jj_wire_spacing, -p.jj_wire_width,
                                                   wire_sub_pos, pad_height-p.inductor_width/2)
        jj_wire = draw.subtract(jj_wire_raw, jj_wire_sub)
        
        jj_lead_y_off = pad_height-p.jj_wire_width/2-p.jj_lead_width/2-p.inductor_width/2
        jj_lead_raw = draw_rectangle_corner_offset(p.jj_wire_spacing, p.jj_lead_width, 
                                                   wire_sub_pos, jj_lead_y_off)
        jj_lead_sub_pos = p.pad_width + p.cell_length/2 - p.jj_lead_length/2
        jj_lead_sub = draw_rectangle_corner_offset(p.jj_lead_length, p.jj_lead_width,
                                                   jj_lead_sub_pos, jj_lead_y_off)
        jj_lead = draw.subtract(jj_lead_raw, jj_lead_sub)
        
        jj_pos = p.pad_width + p.cell_length/2 - p.jj_lead_length/2
        jj_y_off = pad_height-p.jj_wire_width/2-p.jj_width/2-p.inductor_width/2
        jj_rect_raw = draw_rectangle_corner_offset(p.jj_lead_length, p.jj_width, 
                                                   jj_pos, jj_y_off)
        jj_sub_pos = p.pad_width + p.cell_length/2 - p.bridge_width/2
        jj_rect_sub = draw_rectangle_corner_offset(p.bridge_width, p.jj_width,
                                                   jj_sub_pos, jj_y_off)
        jj_rect = draw.subtract(jj_rect_raw, jj_rect_sub)
        
        pocket_rect = draw_rectangle_corner_offset(p.pad_width*2+p.cell_length, p.inductor_width+2*p.gap_outer,
                                                   0, -p.gap_outer-p.inductor_width/2)
        
        # for hfss only
        fake_junction_y = pad_height-p.jj_wire_width/2-p.inductor_width/2
        fake_junction = draw.LineString([(jj_sub_pos, fake_junction_y),
                                         (jj_sub_pos+p.bridge_width, fake_junction_y)])
        
        lower_cell = draw.union([pad_left, pad_right, inductor])
        upper_cell = draw.union([pad_left, pad_right, jj_wire, jj_lead, jj_rect])
        # Rotate and translate all qgeometry as needed.
        # Done with utility functions in Metal 'draw_utility' for easy rotation/translation
        polys = [fake_junction, lower_cell, upper_cell, pocket_rect]
        if alternate:
            polys = draw.rotate(polys, 180,
                                origin = (p.pad_width+p.cell_length/2, 0))
        polys = draw.rotate(polys, p.orientation, origin=(0,0))
        polys = draw.translate(polys, pos_x, pos_y)
        [fake_junction, lower_cell, upper_cell, pocket_rect] = polys

        # Use the geometry to create Metal qgeometryx
        lower_cell_name = "lower_cell"
        upper_cell_name = "upper_cell"
        pocket_rect_name = "pocket_rect"
        fake_junction_name = "fake_junction"
        if affix is not None:
            lower_cell_name += affix
            upper_cell_name += affix
            pocket_rect_name += affix
            fake_junction_name += affix
            
        self.add_qgeometry('poly',{lower_cell_name: lower_cell},
                           chip=chip, layer=p.layers[0],
                           impedance=True)
        self.add_qgeometry('poly',
                           {upper_cell_name: upper_cell},
                           chip=chip, layer=p.layers[1])
        self.add_qgeometry('poly',
                           {pocket_rect_name: pocket_rect},
                           chip=chip, layer=p.layers[1],
                           subtract=True)
        self.add_qgeometry('junction',
                           {fake_junction_name: fake_junction},
                           width=p.jj_width,
                           chip=chip)
        
    def make(self):
        self.make_cell()
        

class HalfATSLine(HalfATS):
    
    default_options = Dict(
        n_cells=10,
        alternate=False
    )
    """Default drawing options"""

    component_metadata = Dict(short_name='HalfATSLine',
                              _qgeometry_table_path='True',
                              _qgeometry_table_poly='True',
                              _qgeometry_table_junction='True')
    """Component metadata"""

    TOOLTIP = """Half ATS line."""
    
    def make(self):
        p = self.p
        chip = p.chip
        
        tot_cell_length = (2*p.pad_width+p.cell_length)
        if p.alternate:
            tot_cell_length -= p.pad_width
        # pad_heigth = p.jj_wire_width + p.gap_inner + p.inductor_width
        # diag_length = np.sqrt((2*p.pad_width+p.cell_length)**2+pad_heigth**2)
        # diag_angle = np.arctan2(pad_heigth, (2*p.pad_width+p.cell_length))
        # diag_off_x = diag_length*np.cos(diag_angle*np.pi/180)
        # diag_off_y = diag_length*np.sin(diag_angle*np.pi/180)
        for idx in range(p.n_cells):
            offset_x = tot_cell_length*np.cos(p.orientation*np.pi/180)
            offset_y = tot_cell_length*np.sin(p.orientation*np.pi/180)
            if p.alternate and idx%2==1:
                self.make_cell(idx*offset_x, idx*offset_y, alternate=True, affix=self.name+f"_c_{idx}")
            else:
                self.make_cell(idx*offset_x, idx*offset_y, affix=self.name+f"_c_{idx}")
            
        ############################################################

        # add pins
        input = draw.LineString([(tot_cell_length, 0), (0, 0)])
        output = draw.LineString([((p.n_cells-1)*tot_cell_length, 0),
                                  (p.n_cells*tot_cell_length, 0)])
        polys = [input, output]
        polys = draw.rotate(polys, p.orientation, origin=(0,0))
        polys = draw.translate(polys, p.pos_x, p.pos_y)
        [input, output] = polys
                
        self.add_pin("in",
                     points=input.coords,
                     width=p.inductor_width,
                     input_as_norm=True,
                     chip=chip)
        
        self.add_pin("out",
                     points=output.coords,
                     width=p.inductor_width,
                     input_as_norm=True,
                     chip=chip)
