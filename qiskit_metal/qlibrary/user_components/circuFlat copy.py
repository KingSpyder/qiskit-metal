from re import T
import numpy as np
from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent

def draw_rectangle_corner_offset(w, h, xoff=0, yoff=0):
    return draw.rectangle(w, h, xoff+w/2, yoff+h/2)

def round_polygon(polygon, radius):
    return polygon.buffer(radius).buffer(-2*radius).buffer(radius)

class circuFlatDoubleCell(QComponent):
    default_options = Dict(
        jj_lead_width='2um',
        jj_bridge_length='1um',
        jj_bridge_width='0.33um',
        jj_to_bridge_length='4um',
        cell_length='50um',
        central_width="5um",
        ground_cap_width="3um",
        jj_wire_to_cap_gap='10um',
        jj_wire_to_ground_gap='10um',
        cap_to_cap_dist='5um',
        top_cap_reduction="1um",
        top_cap_overlap_pad="5um",
        alignment_tol='500nm',
        corner_rounding="200nm",
        layers=[1, 2, 3, 4] #Nb, Al2O3, Al, Al_underdose
    )
    """Default drawing options"""

    component_metadata = Dict(short_name='CircuFlatCell',
                              _qgeometry_table_path='True',
                              _qgeometry_table_poly='True',
                              _qgeometry_table_junction='False')
    """Component metadata"""

    TOOLTIP = """CircuFlat double cell."""
    
    def make_cell(self, offset_x=0, offset_y=0, affix=None):

        # self.p allows us to directly access parsed values (string -> numbers) form the user option
        p = self.p

        # extract chip name
        chip = p.chip

        # since we will reuse these options, parse them once and define them as variables
        pos_x = p.pos_x + offset_x
        pos_y = p.pos_y + offset_y

        #Bottom ground
        ground_pocket = draw.rectangle(2*p.cell_length,
                                       p.jj_wire_to_ground_gap*2 + p.jj_lead_width*2 + p.jj_wire_to_cap_gap*2 + p.central_width,
                                       p.cell_length, 0)
        #lignes layer 1
        
        double_cell_rectangle = draw.rectangle(2*p.cell_length,
                                       p.jj_wire_to_ground_gap*2 + p.jj_lead_width*2 + p.jj_wire_to_cap_gap*2 + p.central_width + 2*p.alignment_tol + 2*p.ground_cap_width,
                                       p.cell_length, 0)
        
        wire_center = p.central_width/2 + p.jj_wire_to_cap_gap + p.jj_lead_width/2
        
        top_central_pts = np.array([
            [p.cell_length/2 + p.cap_to_cap_dist/2, -p.central_width/2],
            [p.cell_length/2 + p.cap_to_cap_dist/2, p.central_width/2],
            [p.cell_length - p.jj_lead_width/2, p.central_width/2],
            [p.cell_length - p.jj_lead_width/2, wire_center - p.jj_lead_width/2],
            [p.cell_length/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length, wire_center - p.jj_lead_width/2],
            [p.cell_length/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length, wire_center - p.jj_bridge_length/2],
            [p.cell_length/2 + p.jj_bridge_width/2, wire_center - p.jj_bridge_length/2],
            [p.cell_length/2 + p.jj_bridge_width/2, wire_center + p.jj_bridge_length/2],
            [p.cell_length/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length, wire_center + p.jj_bridge_length/2],
            [p.cell_length/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length, wire_center + p.jj_lead_width/2],
            [p.cell_length*3/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length, wire_center + p.jj_lead_width/2],
            [p.cell_length*3/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length, wire_center + p.jj_bridge_length/2],
            [p.cell_length*3/2 - p.jj_bridge_width/2, wire_center + p.jj_bridge_length/2],
            [p.cell_length*3/2 - p.jj_bridge_width/2, wire_center - p.jj_bridge_length/2],
            [p.cell_length*3/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length, wire_center - p.jj_bridge_length/2],
            [p.cell_length*3/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length, wire_center - p.jj_lead_width/2],
            [p.cell_length + p.jj_lead_width/2, wire_center - p.jj_lead_width/2],
            [p.cell_length + p.jj_lead_width/2, p.central_width/2],
            [p.cell_length*3/2 - p.cap_to_cap_dist/2, p.central_width/2],
            [p.cell_length*3/2 - p.cap_to_cap_dist/2, -p.central_width/2],
            [p.cell_length/2 + p.cap_to_cap_dist/2, -p.central_width/2]            
        ])
        top_central_sharp_1_pts = np.array([
            top_central_pts[6],
            top_central_pts[7],
            top_central_pts[7] + [p.corner_rounding, 0],
            top_central_pts[6] + [p.corner_rounding, 0],
            top_central_pts[6]
        ])
        top_central_sharp_2_pts = np.array([
            top_central_pts[12],
            top_central_pts[13],
            top_central_pts[13] - [p.corner_rounding, 0],
            top_central_pts[12] - [p.corner_rounding, 0],
            top_central_pts[12]
        ])
        
        #bottom central copy relevant points then offset        
        offset_top_bottom = p.jj_lead_width + 2*p.jj_wire_to_cap_gap + p.central_width
        bottom_central_pts = np.concatenate((top_central_pts[4:16], [top_central_pts[4]])) - [0, offset_top_bottom]
        bottom_central_sharp_1_pts = top_central_sharp_1_pts - [0, offset_top_bottom]
        bottom_central_sharp_2_pts = top_central_sharp_2_pts - [0, offset_top_bottom]
        
        #round and keep some sharp pieces
        top_central_rnd = round_polygon(draw.Polygon(top_central_pts), p.corner_rounding)
        top_central_sharp_1 = draw.Polygon(top_central_sharp_1_pts)
        top_central_sharp_2 = draw.Polygon(top_central_sharp_2_pts)
        top_central = draw.union((top_central_rnd, top_central_sharp_1, top_central_sharp_2))
        
        bottom_central_rnd = round_polygon(draw.Polygon(bottom_central_pts), p.corner_rounding)
        bottom_central_sharp_1 = draw.Polygon(bottom_central_sharp_1_pts)
        bottom_central_sharp_2 = draw.Polygon(bottom_central_sharp_2_pts)
        bottom_central = draw.union((bottom_central_rnd, bottom_central_sharp_1, bottom_central_sharp_2))
        
        #copy second part of the cell by rotation
        #remove part going into adjacent cell
        top_left, bottom_left = draw.intersection(
            draw.rotate((bottom_central, top_central), 180, (p.cell_length/2, 0)),
            double_cell_rectangle)
        top_right, bottom_right = draw.intersection(
            draw.rotate((bottom_central, top_central), 180, (p.cell_length*3/2, 0)),
            double_cell_rectangle)
        
        #Dieletric layer
        top_diel = draw_rectangle_corner_offset(p.cell_length*2, p.jj_wire_to_ground_gap + 2*p.alignment_tol + p.ground_cap_width,
                                                0, wire_center + p.jj_lead_width/2 + p.jj_wire_to_ground_gap/2)
        bottom_diel = draw_rectangle_corner_offset(p.cell_length*2, -(p.jj_wire_to_ground_gap + 2*p.alignment_tol + p.ground_cap_width),
                                                0, -(wire_center + p.jj_lead_width/2 + p.jj_wire_to_ground_gap/2))
        central_diel = draw.rectangle(p.cell_length*2, p.central_width + p.jj_wire_to_cap_gap, p.cell_length, 0)
        
        #Wires second layer, same idea than first layer
        second_bottom_central_pts = np.array([
            [p.cell_length/2 + p.cap_to_cap_dist/2 + p.top_cap_reduction, -p.central_width/2 + p.alignment_tol],
            [p.cell_length/2 + p.cap_to_cap_dist/2 + p.top_cap_reduction, p.central_width/2 - p.alignment_tol],
            [p.cell_length*3/2 - p.cap_to_cap_dist/2 - p.top_cap_reduction, p.central_width/2 - p.alignment_tol],
            [p.cell_length*3/2 - p.cap_to_cap_dist/2 - p.top_cap_reduction, -p.central_width/2 + p.alignment_tol],
            [p.cell_length + p.jj_lead_width/2, -p.central_width/2 + p.alignment_tol],
            [p.cell_length + p.jj_lead_width/2, -wire_center + p.jj_lead_width/2 - p.alignment_tol],
            [p.cell_length + p.top_cap_overlap_pad/2, -wire_center + p.jj_lead_width/2 - p.alignment_tol],
            [p.cell_length + p.top_cap_overlap_pad/2, -wire_center - p.jj_lead_width/2 + p.alignment_tol],
            [p.cell_length + p.jj_lead_width/2, -wire_center - p.jj_lead_width/2 + p.alignment_tol],
            [p.cell_length + p.jj_lead_width/2, -wire_center - p.jj_lead_width/2 - p.jj_wire_to_ground_gap - p.alignment_tol],
            [p.cell_length*3/2 - p.cap_to_cap_dist/2 - p.top_cap_reduction, -wire_center - p.jj_lead_width/2 - p.jj_wire_to_ground_gap - p.alignment_tol],
            [p.cell_length*3/2 - p.cap_to_cap_dist/2 - p.top_cap_reduction, -wire_center - p.jj_lead_width/2 - p.jj_wire_to_ground_gap - p.alignment_tol - p.ground_cap_width],
            [p.cell_length/2 + p.cap_to_cap_dist/2 + p.top_cap_reduction, -wire_center - p.jj_lead_width/2 - p.jj_wire_to_ground_gap - p.alignment_tol - p.ground_cap_width],
            [p.cell_length/2 + p.cap_to_cap_dist/2 + p.top_cap_reduction, -wire_center - p.jj_lead_width/2 - p.jj_wire_to_ground_gap - p.alignment_tol],
            [p.cell_length - p.jj_lead_width/2, -wire_center - p.jj_lead_width/2 - p.jj_wire_to_ground_gap - p.alignment_tol],
            [p.cell_length - p.jj_lead_width/2, -wire_center - p.jj_lead_width/2 + p.alignment_tol],
            [p.cell_length - p.top_cap_overlap_pad/2, -wire_center - p.jj_lead_width/2 + p.alignment_tol],
            [p.cell_length - p.top_cap_overlap_pad/2, -wire_center + p.jj_lead_width/2 - p.alignment_tol],
            [p.cell_length - p.jj_lead_width/2, -wire_center + p.jj_lead_width/2 - p.alignment_tol],
            [p.cell_length - p.jj_lead_width/2, -p.central_width/2 + p.alignment_tol],
            [p.cell_length/2 + p.cap_to_cap_dist/2 + p.top_cap_reduction, -p.central_width/2 + p.alignment_tol]
        ])
        second_top_central_pts_unrot = np.concatenate((second_bottom_central_pts[6:18], [second_bottom_central_pts[6]]))
        
        second_bottom_central = round_polygon(draw.Polygon(second_bottom_central_pts), p.corner_rounding)
        second_top_central = draw.rotate(
            round_polygon(
                draw.Polygon(second_top_central_pts_unrot), 
                p.corner_rounding), 
            180, (p.cell_length, 0))
        
        #copy left and right and rotate
        #remove part going into adjacent cell
        second_top_left, second_bottom_left = draw.intersection(
            draw.rotate((second_bottom_central, second_top_central), 180, (p.cell_length/2, 0)),
            double_cell_rectangle)
        second_top_right, second_bottom_right = draw.intersection(
            draw.rotate((second_bottom_central, second_top_central), 180, (p.cell_length*3/2, 0)),
            double_cell_rectangle)
               
        # Rotate and translate all qgeometry as needed.
        # Done with utility functions in Metal 'draw_utility' for easy rotation/translation
        polys = [ground_pocket, 
                top_left, top_central, top_right, 
                bottom_left, bottom_central, bottom_right,
                top_diel, bottom_diel, central_diel,
                second_top_left, second_top_central, second_top_right, 
                second_bottom_left, second_bottom_central, second_bottom_right]
        
        polys = draw.rotate(polys, p.orientation, origin=(0,0))
        polys = draw.translate(polys, pos_x, pos_y)
        
        [ground_pocket, 
        top_left, top_central, top_right, 
        bottom_left, bottom_central, bottom_right,
        top_diel, bottom_diel, central_diel,
        second_top_left, second_top_central, second_top_right, 
        second_bottom_left, second_bottom_central, second_bottom_right] = polys

        # Use the geometry to create Metal qgeometryx
        ground_pocket_name = "pocket_cell"
        top_left_name = "top_left"
        top_central_name = "top_central"
        top_right_name = "top_right"
        bottom_left_name = "bottom_left"
        bottom_central_name = "bottom_central"
        bottom_right_name = "bottom_right"
        top_diel_name = "top_diel"
        central_diel_name = "center_diel"
        bottom_diel_name = "bottom_diel"
        second_top_left_name = "second_top_left"
        second_top_central_name = "second_top_central"
        second_top_right_name = "second_top_right"
        second_bottom_left_name = "second_bottom_left"
        second_bottom_central_name = "second_bottom_central"
        second_bottom_right_name = "second_bottom_right"
        
        if affix is not None:
            ground_pocket_name += affix
            top_left_name += affix
            top_central_name += affix
            top_right_name += affix
            bottom_left_name += affix
            bottom_central_name += affix
            bottom_right_name += affix
            top_diel_name += affix
            central_diel_name += affix
            bottom_diel_name += affix
            second_top_left_name += affix
            second_top_central_name += affix
            second_top_right_name += affix
            second_bottom_left_name += affix
            second_bottom_central_name += affix
            second_bottom_right_name += affix
            
        self.add_qgeometry('poly',{ground_pocket_name: ground_pocket},
                           chip=chip, layer=p.layers[0], subtract=True)
        self.add_qgeometry('poly',
                           {top_left_name: top_left},
                           chip=chip, layer=p.layers[0])
        self.add_qgeometry('poly',
                           {top_central_name: top_central},
                           chip=chip, layer=p.layers[0])
        self.add_qgeometry('poly',
                           {top_right_name: top_right},
                           chip=chip, layer=p.layers[0])
        self.add_qgeometry('poly',
                           {bottom_left_name: bottom_left},
                           chip=chip, layer=p.layers[0])
        self.add_qgeometry('poly',
                           {bottom_central_name: bottom_central},
                           chip=chip, layer=p.layers[0])
        self.add_qgeometry('poly',
                           {bottom_right_name: bottom_right},
                           chip=chip, layer=p.layers[0])
        self.add_qgeometry('poly',
                           {top_diel_name: top_diel},
                           chip=chip, layer=p.layers[1])
        self.add_qgeometry('poly',
                           {central_diel_name: central_diel},
                           chip=chip, layer=p.layers[1])
        self.add_qgeometry('poly',
                           {bottom_diel_name: bottom_diel},
                           chip=chip, layer=p.layers[1])
        self.add_qgeometry('poly',
                           {second_top_left_name: second_top_left},
                           chip=chip, layer=p.layers[2])
        self.add_qgeometry('poly',
                           {second_top_central_name: second_top_central},
                           chip=chip, layer=p.layers[2])
        self.add_qgeometry('poly',
                           {second_top_right_name: second_top_right},
                           chip=chip, layer=p.layers[2])
        self.add_qgeometry('poly',
                           {second_bottom_left_name: second_bottom_left},
                           chip=chip, layer=p.layers[2])
        self.add_qgeometry('poly',
                           {second_bottom_central_name: second_bottom_central},
                           chip=chip, layer=p.layers[2])
        self.add_qgeometry('poly',
                           {second_bottom_right_name: second_bottom_right},
                           chip=chip, layer=p.layers[2])
        
    def make(self):
        self.make_cell()
        

class circuFlatLine(circuFlatDoubleCell):
    
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
        input_top = draw.LineString([(tot_cell_length, p.central_width/2 + p.jj_wire_to_cap_gap + p.jj_lead_width/2),
                                     (0, p.central_width/2 + p.jj_wire_to_cap_gap + p.jj_lead_width/2)])
        input_bot = draw.LineString([(tot_cell_length, -(p.central_width/2 + p.jj_wire_to_cap_gap + p.jj_lead_width/2)),
                                     (0, -(p.central_width/2 + p.jj_wire_to_cap_gap + p.jj_lead_width/2))])
        output_top = draw.LineString([((p.n_cells-1)*tot_cell_length, p.central_width/2 + p.jj_wire_to_cap_gap + p.jj_lead_width/2),
                                  (p.n_cells*tot_cell_length, p.central_width/2 + p.jj_wire_to_cap_gap + p.jj_lead_width/2)])
        output_bot = draw.LineString([((p.n_cells-1)*tot_cell_length, -(p.central_width/2 + p.jj_wire_to_cap_gap + p.jj_lead_width/2)),
                                  (p.n_cells*tot_cell_length, -(p.central_width/2 + p.jj_wire_to_cap_gap + p.jj_lead_width/2))])
        polys = [input_top, input_bot, output_top, output_bot]
        polys = draw.rotate(polys, p.orientation, origin=(0,0))
        polys = draw.translate(polys, p.pos_x, p.pos_y)
        [input_top, input_bot, output_top, output_bot] = polys
                
        self.add_pin("in_top",
                     points=input_top.coords,
                     width=p.jj_lead_width,
                     input_as_norm=True,
                     chip=chip)
        self.add_pin("in_bottom",
                     points=input_bot.coords,
                     width=p.jj_lead_width,
                     input_as_norm=True,
                     chip=chip)
        self.add_pin("out_top",
                     points=output_top.coords,
                     width=p.jj_lead_width,
                     input_as_norm=True,
                     chip=chip)
        self.add_pin("out_bottom",
                     points=output_bot.coords,
                     width=p.jj_lead_width,
                     input_as_norm=True,
                     chip=chip)