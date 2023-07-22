from re import T
import numpy as np
from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent

def draw_rectangle_corner_offset(w, h, xoff=0, yoff=0):
    return draw.rectangle(w, h, xoff+w/2, yoff+h/2)

class circuLiteDoubleCell(QComponent):
    default_options = Dict(
        bottom_plane_width="40um",
        bottom_diel_width="25um",
        jj_lead_width='2um',
        jj_bridge_length='2um',
        jj_bridge_width='2um',
        jj_to_bridge_length='4um',
        cell_length='50um',
        central_width="4um",
        jj_wire_to_line_gap='30um',
        lines_distance='2um',
        central_cell_to_cell_dist='5um',
        layers=[1, 2, 3, 4, 5]
    )
    """Default drawing options"""

    component_metadata = Dict(short_name='Pocket',
                              _qgeometry_table_path='True',
                              _qgeometry_table_poly='True',
                              _qgeometry_table_junction='True')
    """Component metadata"""

    TOOLTIP = """CircuLite double cell."""
    
    def make_cell(self, offset_x=0, offset_y=0, affix=None):

        # self.p allows us to directly access parsed values (string -> numbers) form the user option
        p = self.p

        # extract chip name
        chip = p.chip

        # since we will reuse these options, parse them once and define them as variables
        pos_x = p.pos_x + offset_x
        pos_y = p.pos_y + offset_y

        #Bottom ground        
        bot_ground = draw_rectangle_corner_offset(2*p.cell_length, p.bottom_plane_width, 0, -p.bottom_plane_width/2)
        bot_diel = draw_rectangle_corner_offset(2*p.cell_length, p.bottom_diel_width, 0, -p.bottom_diel_width/2)

        #layer des lignes
        top_left_pts = np.array([
                        [0, p.lines_distance/2],
                        [0, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width],
                        [p.jj_lead_width/2, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width],
                        [p.jj_lead_width/2, p.lines_distance/2 + p.central_width],
                        [p.cell_length/2 - p.central_cell_to_cell_dist/2, p.lines_distance/2 + p.central_width],
                        [p.cell_length/2 - p.central_cell_to_cell_dist/2, p.lines_distance/2],
                        [0, p.lines_distance/2]
                        ])
        
        top_central_pts = np.array([
                        [p.cell_length/2 + p.central_cell_to_cell_dist/2, p.lines_distance/2],
                        [p.cell_length/2 + p.central_cell_to_cell_dist/2, p.lines_distance/2 + p.central_width],
                        [p.cell_length-p.jj_lead_width/2, p.lines_distance/2 + p.central_width],
                        [p.cell_length-p.jj_lead_width/2, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width],
                        [p.cell_length+p.jj_lead_width/2, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width],
                        [p.cell_length+p.jj_lead_width/2, p.lines_distance/2 + p.central_width],
                        [p.cell_length*3/2 - p.central_cell_to_cell_dist/2, p.lines_distance/2 + p.central_width],
                        [p.cell_length*3/2 - p.central_cell_to_cell_dist/2, p.lines_distance/2],
                        [p.cell_length/2 + p.central_cell_to_cell_dist/2, p.lines_distance/2]
                        ])
        
        top_right_pts = np.array([
                        [p.cell_length*3/2 + p.central_cell_to_cell_dist/2, p.lines_distance/2],
                        [p.cell_length*3/2 + p.central_cell_to_cell_dist/2, p.lines_distance/2+p.central_width],
                        [p.cell_length*2 - p.jj_lead_width/2, p.lines_distance/2 + p.central_width],
                        [p.cell_length*2 - p.jj_lead_width/2, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width],
                        [p.cell_length*2, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width],
                        [p.cell_length*2, p.lines_distance/2],
                        [p.cell_length*3/2 + p.central_cell_to_cell_dist/2, p.lines_distance/2]
                        ])
        
        top_left = draw.Polygon(top_left_pts)
        top_central = draw.Polygon(top_central_pts)
        top_right = draw.Polygon(top_right_pts)
        bottom_left = draw.Polygon(top_left_pts.dot([[1,0],[0,-1]]))
        bottom_central = draw.Polygon(top_central_pts.dot([[1,0],[0,-1]]))
        bottom_right = draw.Polygon(top_right_pts.dot([[1,0],[0,-1]]))
        
        #Dieletric second layer
        second_diel = draw.Polygon([
                        [0, 0],
                        [p.cell_length/2 - p.central_cell_to_cell_dist/2, 0],
                        [p.cell_length/2, p.lines_distance/2],
                        [p.cell_length/2, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap/2],
                        [p.cell_length*3/2, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap/2],
                        [p.cell_length*3/2, p.lines_distance/2],
                        [p.cell_length*3/2 + p.central_cell_to_cell_dist/2, 0],
                        [p.cell_length*2, 0],
                        [p.cell_length*2, -(p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap/2)],
                        [p.cell_length*3/2, -(p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap/2)],
                        [p.cell_length*3/2, -p.lines_distance/2],
                        [p.cell_length*3/2 - p.central_cell_to_cell_dist/2, 0],
                        [p.cell_length/2 + p.central_cell_to_cell_dist/2, 0],
                        [p.cell_length/2, -p.lines_distance/2],
                        [p.cell_length/2, -(p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap/2)],
                        [0, -(p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap/2)],
                        [0, 0]
                        ])
        
        #Wires second layer 
        second_top_left_pts = np.array([
                        [0, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width],
                        [p.cell_length/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width],
                        [p.cell_length/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width/2 + p.jj_bridge_length/2],
                        [p.cell_length/2 - p.jj_bridge_width/2, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width/2 + p.jj_bridge_length/2],
                        [p.cell_length/2 - p.jj_bridge_width/2, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width/2 - p.jj_bridge_length/2],
                        [p.cell_length/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width/2 - p.jj_bridge_length/2],
                        [p.cell_length/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap],
                        [0, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap],
                        [0, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width]                        
                        ])
        
        
        second_top_central_pts = np.array([
                        [p.cell_length/2 + p.jj_bridge_width/2, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width/2 - p.jj_bridge_length/2],
                        [p.cell_length/2 + p.jj_bridge_width/2, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width/2 + p.jj_bridge_length/2],
                        [p.cell_length/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width/2 + p.jj_bridge_length/2],
                        [p.cell_length/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width],
                        [p.cell_length*3/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width],
                        [p.cell_length*3/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width/2 + p.jj_bridge_width/2],
                        [p.cell_length*3/2 - p.jj_bridge_width/2, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width/2 + p.jj_bridge_width/2],
                        [p.cell_length*3/2 - p.jj_bridge_width/2, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width/2 - p.jj_bridge_width/2],
                        [p.cell_length*3/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width/2 - p.jj_bridge_width/2],
                        [p.cell_length*3/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap],
                        [p.cell_length/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap],
                        [p.cell_length/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width/2 - p.jj_bridge_length/2],
                        [p.cell_length/2 + p.jj_bridge_width/2, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width/2 - p.jj_bridge_length/2]
                        ])
        
        second_top_right_pts = np.array([
                        [p.cell_length*3/2 + p.jj_bridge_width/2, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width/2 - p.jj_bridge_length/2],
                        [p.cell_length*3/2 + p.jj_bridge_width/2, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width/2 + p.jj_bridge_length/2],
                        [p.cell_length*3/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width/2 + p.jj_bridge_length/2],
                        [p.cell_length*3/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width],
                        [p.cell_length*2, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width],
                        [p.cell_length*2, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap],
                        [p.cell_length*3/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap],
                        [p.cell_length*3/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width/2 - p.jj_bridge_length/2],
                        [p.cell_length*3/2 + p.jj_bridge_width/2, p.lines_distance/2 + p.central_width + p.jj_wire_to_line_gap + p.jj_lead_width/2 - p.jj_bridge_length/2]
                        ])
        
        second_top_left = draw.Polygon(second_top_left_pts)
        second_top_central = draw.Polygon(second_top_central_pts)
        second_top_right = draw.Polygon(second_top_right_pts)
        second_bottom_left = draw.Polygon(second_top_left_pts.dot([[1,0],[0,-1]]))
        second_bottom_central = draw.Polygon(second_top_central_pts.dot([[1,0],[0,-1]]))
        second_bottom_right = draw.Polygon(second_top_right_pts.dot([[1,0],[0,-1]]))
        
        capa_left =draw_rectangle_corner_offset(p.cell_length/2-p.central_cell_to_cell_dist/2, p.lines_distance+p.central_width*2,
                                   0, -p.lines_distance/2 - p.central_width)
        capa_central = draw_rectangle_corner_offset(p.cell_length-p.central_cell_to_cell_dist, p.lines_distance+p.central_width*2,
                                   p.cell_length/2 + p.central_cell_to_cell_dist/2, -p.lines_distance/2 - p.central_width)
        capa_right = draw_rectangle_corner_offset(p.cell_length/2-p.central_cell_to_cell_dist/2, p.lines_distance+p.central_width*2,
                                   p.cell_length*3/2 + p.central_cell_to_cell_dist/2, -p.lines_distance/2 - p.central_width)
        
        # Rotate and translate all qgeometry as needed.
        # Done with utility functions in Metal 'draw_utility' for easy rotation/translation
        polys = [bot_ground, bot_diel, 
                 top_left, top_central, top_right, 
                 bottom_left, bottom_central, bottom_right,
                 second_diel,
                 second_top_left, second_top_central, second_top_right, 
                 second_bottom_left, second_bottom_central, second_bottom_right,
                 capa_left, capa_central, capa_right]
        
        polys = draw.rotate(polys, p.orientation, origin=(0,0))
        polys = draw.translate(polys, pos_x, pos_y)
        
        [bot_ground, bot_diel, 
        top_left, top_central, top_right, 
        bottom_left, bottom_central, bottom_right,
        second_diel,
        second_top_left, second_top_central, second_top_right, 
        second_bottom_left, second_bottom_central, second_bottom_right,
        capa_left, capa_central, capa_right] = polys

        # Use the geometry to create Metal qgeometryx
        bot_ground_name = "lower_cell"
        bot_diel_name = "bottom_diel"
        top_left_name = "top_left"
        top_central_name = "top_central"
        top_right_name = "top_right"
        bottom_left_name = "bottom_left"
        bottom_central_name = "bottom_central"
        bottom_right_name = "bottom_right"
        second_diel_name = "second_diel"
        second_top_left_name = "second_top_left"
        second_top_central_name = "second_top_central"
        second_top_right_name = "second_top_right"
        second_bottom_left_name = "second_bottom_left"
        second_bottom_central_name = "second_bottom_central"
        second_bottom_right_name = "second_bottom_right"
        capa_left_name = "capa_left"
        capa_central_name = "capa_central"
        capa_right_name = "capa_right"
        
        if affix is not None:
            bot_ground_name += affix
            bot_diel_name += affix
            top_left_name += affix
            top_central_name += affix
            top_right_name += affix
            bottom_left_name += affix
            bottom_central_name += affix
            bottom_right_name += affix
            second_diel_name += affix
            second_top_left_name += affix
            second_top_central_name += affix
            second_top_right_name += affix
            second_bottom_left_name += affix
            second_bottom_central_name += affix
            second_bottom_right_name += affix
            capa_left_name += affix
            capa_central_name += affix
            capa_right_name += affix
            
        self.add_qgeometry('poly',{bot_ground_name: bot_ground},
                           chip=chip, layer=p.layers[0])
        self.add_qgeometry('poly',
                           {bot_diel_name: bot_diel},
                           chip=chip, layer=p.layers[1])
        self.add_qgeometry('poly',
                           {top_left_name: top_left},
                           chip=chip, layer=p.layers[2])
        self.add_qgeometry('poly',
                           {top_central_name: top_central},
                           chip=chip, layer=p.layers[2])
        self.add_qgeometry('poly',
                           {top_right_name: top_right},
                           chip=chip, layer=p.layers[2])
        self.add_qgeometry('poly',
                           {bottom_left_name: bottom_left},
                           chip=chip, layer=p.layers[2])
        self.add_qgeometry('poly',
                           {bottom_central_name: bottom_central},
                           chip=chip, layer=p.layers[2])
        self.add_qgeometry('poly',
                           {bottom_right_name: bottom_right},
                           chip=chip, layer=p.layers[2])
        self.add_qgeometry('poly',
                           {second_diel_name: second_diel},
                           chip=chip, layer=p.layers[3])
        self.add_qgeometry('poly',
                           {second_top_left_name: second_top_left},
                           chip=chip, layer=p.layers[4])
        self.add_qgeometry('poly',
                           {second_top_central_name: second_top_central},
                           chip=chip, layer=p.layers[4])
        self.add_qgeometry('poly',
                           {second_top_right_name: second_top_right},
                           chip=chip, layer=p.layers[4])
        self.add_qgeometry('poly',
                           {second_bottom_left_name: second_bottom_left},
                           chip=chip, layer=p.layers[4])
        self.add_qgeometry('poly',
                           {second_bottom_central_name: second_bottom_central},
                           chip=chip, layer=p.layers[4])
        self.add_qgeometry('poly',
                           {second_bottom_right_name: second_bottom_right},
                           chip=chip, layer=p.layers[4])
        self.add_qgeometry('poly',
                           {capa_left_name: capa_left},
                           chip=chip, layer=p.layers[4])
        self.add_qgeometry('poly',
                           {capa_central_name: capa_central},
                           chip=chip, layer=p.layers[4])
        self.add_qgeometry('poly',
                           {capa_right_name: capa_right},
                           chip=chip, layer=p.layers[4])
        
    def make(self):
        self.make_cell()
        

class circuLiteLine(circuLiteDoubleCell):
    
    default_options = Dict(
        n_cells=10
    )
    """Default drawing options"""

    component_metadata = Dict(short_name='circuLiteLine',
                              _qgeometry_table_path='True',
                              _qgeometry_table_poly='True',
                              _qgeometry_table_junction='True')
    """Component metadata"""

    TOOLTIP = """CircuLite line."""
    
    def make(self):
        p = self.p
        chip = p.chip
        
        tot_cell_length = 2*p.cell_length
        
        for idx in range(p.n_cells):
            offset_x = tot_cell_length*np.cos(p.orientation*np.pi/180)
            offset_y = tot_cell_length*np.sin(p.orientation*np.pi/180)
            self.make_cell(idx*offset_x, idx*offset_y, affix=self.name+f"_c_{idx}")
            
        ############################################################

        # add pins
        input_top = draw.LineString([(tot_cell_length, p.lines_distance/2 + p.central_width/2),
                                     (0, p.lines_distance/2 + p.central_width/2)])
        input_bot = draw.LineString([(tot_cell_length, -p.lines_distance/2 - p.central_width/2),
                                     (0, -p.lines_distance/2 - p.central_width/2)])
        output_top = draw.LineString([((p.n_cells-1)*tot_cell_length, p.lines_distance/2 + p.central_width/2),
                                  (p.n_cells*tot_cell_length, p.lines_distance/2 + p.central_width/2)])
        output_bot = draw.LineString([((p.n_cells-1)*tot_cell_length, -p.lines_distance/2 - p.central_width/2),
                                  (p.n_cells*tot_cell_length, -p.lines_distance/2 - p.central_width/2)])
        polys = [input_top, input_bot, output_top, output_bot]
        polys = draw.rotate(polys, p.orientation, origin=(0,0))
        polys = draw.translate(polys, p.pos_x, p.pos_y)
        [input_top, input_bot, output_top, output_bot] = polys
                
        self.add_pin("in_top",
                     points=input_top.coords,
                     width=p.central_width,
                     input_as_norm=True,
                     chip=chip)
        self.add_pin("in_bottom",
                     points=input_bot.coords,
                     width=p.central_width,
                     input_as_norm=True,
                     chip=chip)
        self.add_pin("out_top",
                     points=output_top.coords,
                     width=p.central_width,
                     input_as_norm=True,
                     chip=chip)
        self.add_pin("out_bottom",
                     points=output_bot.coords,
                     width=p.central_width,
                     input_as_norm=True,
                     chip=chip)