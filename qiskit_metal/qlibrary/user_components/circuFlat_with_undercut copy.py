import numpy as np
from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent

def draw_rectangle_corner_offset(w, h, xoff=0, yoff=0):
    return draw.rectangle(w, h, xoff+w/2, yoff+h/2)

def round_polygon(polygon, radius):
    return polygon.buffer(radius).buffer(-2*radius).buffer(radius)

class circuFlatDoubleCellWithUC(QComponent):
    default_options = Dict(
        jj_lead_width='2.5um',
        jj_bridge_length='1um',
        jj_overlength_left='0.5um',
        jj_bridge_width='330nm',
        jj_to_bridge_length='4um',
        cell_length='20um',
        central_width="5um",
        ground_cap_width="3um",
        jj_wire_to_cap_gap='10um',
        jj_wire_to_ground_gap='10um',
        cap_to_cap_dist='3.6um',
        jj_t_size="0.4um",
        top_cap_reduction="1.7um",
        top_cap_overlap_pad="15um",
        alignment_tol='500nm',
        corner_rounding="200nm",
        diel_rounding="500nm",
        undersize="1.0um",
        under_spacing="50nm",
        outer_groundcap_extra_l="0.0um",
        outer_intercap_extra_l="1um",
        extremity_gap="1.2um",
        adaptater_length="5um",
        adaptater_width="5um",
        adaptater_rounding="1um",
        layers=[1, 2, 3, 4, 5, 6] #Nb, Nb Ts, Al2O3, Al, Al_junctions, Al_underdose
    )
    """Default drawing options"""

    component_metadata = Dict(short_name='CircuFlatCell',
                              _qgeometry_table_path='True',
                              _qgeometry_table_poly='True',
                              _qgeometry_table_junction='False')
    """Component metadata"""

    TOOLTIP = """CircuFlat double cell."""
    
    def make_cell(self, offset_x=0, offset_y=0, affix=None, fully_round=None):

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
            #central cap
            [p.cell_length/2 + p.cap_to_cap_dist/2, -p.central_width/2],
            [p.cell_length/2 + p.cap_to_cap_dist/2, p.central_width/2],
            [p.cell_length - p.jj_lead_width/2, p.central_width/2],
            #up to top part
            [p.cell_length - p.jj_lead_width/2, wire_center - p.jj_lead_width/2],
            [p.cell_length/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length, wire_center - p.jj_lead_width/2],
            [p.cell_length/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length, wire_center + p.jj_lead_width/2],
            [p.cell_length*3/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length, wire_center + p.jj_lead_width/2],
            [p.cell_length*3/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length, wire_center - p.jj_lead_width/2],
            [p.cell_length + p.jj_lead_width/2, wire_center - p.jj_lead_width/2],
            #end of central capa
            [p.cell_length + p.jj_lead_width/2, p.central_width/2],
            [p.cell_length*3/2 - p.cap_to_cap_dist/2, p.central_width/2],
            [p.cell_length*3/2 - p.cap_to_cap_dist/2, -p.central_width/2],
            [p.cell_length/2 + p.cap_to_cap_dist/2, -p.central_width/2]            
        ])    
        top_little_t_left_pts = np.array([
            [p.cell_length/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length - p.alignment_tol, wire_center - p.jj_t_size/2],
            [p.cell_length/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length + 2*p.alignment_tol + p.jj_t_size, wire_center - p.jj_t_size/2],
            [p.cell_length/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length + 2*p.alignment_tol + p.jj_t_size, wire_center - p.jj_t_size],
            [p.cell_length/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length + 2*p.alignment_tol + 2*p.jj_t_size, wire_center - p.jj_t_size],
            [p.cell_length/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length + 2*p.alignment_tol + 2*p.jj_t_size, wire_center + p.jj_t_size],
            [p.cell_length/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length + 2*p.alignment_tol + p.jj_t_size, wire_center + p.jj_t_size],
            [p.cell_length/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length + 2*p.alignment_tol + p.jj_t_size, wire_center + p.jj_t_size/2],
            [p.cell_length/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length - p.alignment_tol, wire_center + p.jj_t_size/2],
            [p.cell_length/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length - p.alignment_tol, wire_center - p.jj_t_size/2]
        ])
        top_little_t_right_pts = np.array([
            [p.cell_length*3/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length + p.alignment_tol, wire_center + p.jj_t_size/2],
            [p.cell_length*3/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length - 2*p.alignment_tol - p.jj_t_size, wire_center + p.jj_t_size/2],
            [p.cell_length*3/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length - 2*p.alignment_tol - p.jj_t_size, wire_center + p.jj_t_size],
            [p.cell_length*3/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length - 2*p.alignment_tol - 2*p.jj_t_size, wire_center + p.jj_t_size],
            [p.cell_length*3/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length - 2*p.alignment_tol - 2*p.jj_t_size, wire_center - p.jj_t_size],
            [p.cell_length*3/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length - 2*p.alignment_tol - p.jj_t_size, wire_center - p.jj_t_size],
            [p.cell_length*3/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length - 2*p.alignment_tol - p.jj_t_size, wire_center - p.jj_t_size/2],
            [p.cell_length*3/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length + p.alignment_tol, wire_center - p.jj_t_size/2],
            [p.cell_length*3/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length + p.alignment_tol, wire_center + p.jj_t_size/2]
        ])
        
        offset_top_bottom = p.jj_lead_width + 2*p.jj_wire_to_cap_gap + p.central_width
        #little Ts
        bottom_little_t_left_pts = top_little_t_left_pts - [0, offset_top_bottom]
        bottom_little_t_right_pts = top_little_t_right_pts - [0, offset_top_bottom]
        top_little_t_left = draw.Polygon(top_little_t_left_pts)
        top_little_t_right = draw.Polygon(top_little_t_right_pts)
        bottom_little_t_left = draw.Polygon(bottom_little_t_left_pts)
        bottom_little_t_right = draw.Polygon(bottom_little_t_right_pts)
        
        #bottom central copy relevant points then offset        
        bottom_central_pts = np.concatenate((top_central_pts[4:8], [top_central_pts[4]])) - [0, offset_top_bottom]
        
        top_central = round_polygon(draw.Polygon(top_central_pts), p.corner_rounding)
        bottom_central = round_polygon(draw.Polygon(bottom_central_pts), p.corner_rounding)
        
        #copy second part of the cell by rotation
        #remove part going into adjacent cell
        top_left, bottom_left, top_left_little_t, bottom_left_little_t = draw.intersection(
            draw.rotate((bottom_central, top_central, bottom_little_t_left, top_little_t_left), 180, (p.cell_length/2, 0)),
            double_cell_rectangle)
        top_right, bottom_right, top_right_little_t, bottom_right_little_t = draw.intersection(
            draw.rotate((bottom_central, top_central, bottom_little_t_right, top_little_t_right), 180, (p.cell_length*3/2, 0)),
            double_cell_rectangle)
        
        #Dieletric layer
        top_diel = draw_rectangle_corner_offset(p.cell_length*2, p.jj_wire_to_ground_gap + 2*p.alignment_tol + p.ground_cap_width,
                                                0, wire_center + p.jj_lead_width/2 + p.jj_wire_to_ground_gap/2)
        bottom_diel = draw_rectangle_corner_offset(p.cell_length*2, -(p.jj_wire_to_ground_gap + 2*p.alignment_tol + p.ground_cap_width),
                                                0, -(wire_center + p.jj_lead_width/2 + p.jj_wire_to_ground_gap/2))
        central_diel = draw.rectangle(p.cell_length*2, p.central_width + p.jj_wire_to_cap_gap, p.cell_length, 0)
        
        #redo them rounded on end of lines
        #dirty overwrite
        if fully_round=="left":
            top_diel = round_polygon(top_diel, p.diel_rounding)
            unround_top_diel = draw_rectangle_corner_offset(-p.diel_rounding, p.jj_wire_to_ground_gap + 2*p.alignment_tol + p.ground_cap_width,
                                                2*p.cell_length, wire_center + p.jj_lead_width/2 + p.jj_wire_to_ground_gap/2)
            top_diel = draw.union(top_diel, unround_top_diel)
            
            central_diel = round_polygon(central_diel, p.diel_rounding)
            unround_central_diel = draw_rectangle_corner_offset(-p.diel_rounding, p.central_width + p.jj_wire_to_cap_gap, 2*p.cell_length, -(p.central_width + p.jj_wire_to_cap_gap)/2)
            central_diel = draw.union(central_diel, unround_central_diel)
            
            bottom_diel = round_polygon(bottom_diel, p.diel_rounding)
            unround_bottom_diel = draw_rectangle_corner_offset(-p.diel_rounding, -(p.jj_wire_to_ground_gap + 2*p.alignment_tol + p.ground_cap_width),
                                                2*p.cell_length, -(wire_center + p.jj_lead_width/2 + p.jj_wire_to_ground_gap/2))
            bottom_diel = draw.union(bottom_diel, unround_bottom_diel)
        
        if fully_round=="right":
            top_diel = round_polygon(top_diel, p.diel_rounding)
            unround_top_diel = draw_rectangle_corner_offset(p.diel_rounding, p.jj_wire_to_ground_gap + 2*p.alignment_tol + p.ground_cap_width,
                                                0, wire_center + p.jj_lead_width/2 + p.jj_wire_to_ground_gap/2)
            top_diel = draw.union(top_diel, unround_top_diel)
            
            central_diel = round_polygon(central_diel, p.diel_rounding)
            unround_central_diel = draw_rectangle_corner_offset(p.diel_rounding, p.central_width + p.jj_wire_to_cap_gap, 0, -(p.central_width + p.jj_wire_to_cap_gap)/2)
            central_diel = draw.union(central_diel, unround_central_diel)
            
            bottom_diel = round_polygon(bottom_diel, p.diel_rounding)
            unround_bottom_diel = draw_rectangle_corner_offset(p.diel_rounding, -(p.jj_wire_to_ground_gap + 2*p.alignment_tol + p.ground_cap_width),
                                                0, -(wire_center + p.jj_lead_width/2 + p.jj_wire_to_ground_gap/2))
            bottom_diel = draw.union(bottom_diel, unround_bottom_diel)
        
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
            
        #If first (left) or last (right) cell: modifier bottom left/right, second top right/left, et second bottom right/left
        #This is a DIRTY overwrite
        unround_height = p.central_width/2 + p.jj_wire_to_cap_gap + p.jj_lead_width - p.corner_rounding/2
        if fully_round=="right":
            bottom_right = round_polygon(draw.Polygon([
                [p.cell_length*3/2 + p.cap_to_cap_dist/2, p.central_width/2],
                [p.cell_length*2, p.central_width/2],
                [p.cell_length*2, -p.central_width/2],
                [p.cell_length*2, -p.central_width/2 - p.jj_wire_to_cap_gap - p.jj_lead_width],
                [p.cell_length*3/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length, -p.central_width/2 - p.jj_wire_to_cap_gap - p.jj_lead_width],
                [p.cell_length*3/2 + p.jj_bridge_width/2 + p.jj_to_bridge_length, -p.central_width/2 - p.jj_wire_to_cap_gap],
                [p.cell_length*2 - p.jj_lead_width, -p.central_width/2 - p.jj_wire_to_cap_gap],
                [p.cell_length*2 - p.jj_lead_width, -p.central_width/2],
                [p.cell_length*3/2 + p.cap_to_cap_dist/2, -p.central_width/2],
                [p.cell_length*3/2 + p.cap_to_cap_dist/2, p.central_width/2]
            ]), p.corner_rounding)
            unround_br = draw.rectangle(p.corner_rounding, p.corner_rounding,
                                        p.cell_length*2 - p.corner_rounding/2, -unround_height)
            bottom_right = draw.union(bottom_right, unround_br)
        
            sbr_middle = p.cell_length*2 - p.top_cap_overlap_pad/2 + (p.top_cap_overlap_pad/2 - p.extremity_gap)/2
            second_bottom_right = round_polygon(draw.Polygon([
                [p.cell_length*2 - p.top_cap_overlap_pad/2, -wire_center + p.jj_lead_width/2 - p.alignment_tol],
                [sbr_middle + p.jj_lead_width/2, -wire_center + p.jj_lead_width/2 - p.alignment_tol],
                [sbr_middle + p.jj_lead_width/2, -wire_center - p.jj_lead_width/2 - p.jj_wire_to_ground_gap - p.alignment_tol - p.ground_cap_width],
                [p.cell_length*3/2 + p.cap_to_cap_dist/2 + p.top_cap_reduction - p.outer_groundcap_extra_l, -wire_center - p.jj_lead_width/2 - p.jj_wire_to_ground_gap - p.alignment_tol - p.ground_cap_width],
                [p.cell_length*3/2 + p.cap_to_cap_dist/2 + p.top_cap_reduction - p.outer_groundcap_extra_l, -wire_center - p.jj_lead_width/2 - p.jj_wire_to_ground_gap - p.alignment_tol],
                [sbr_middle - p.jj_lead_width/2, -wire_center - p.jj_lead_width/2 - p.jj_wire_to_ground_gap - p.alignment_tol],
                [sbr_middle - p.jj_lead_width/2, -wire_center - p.jj_lead_width/2 + p.alignment_tol],
                [p.cell_length*2 - p.top_cap_overlap_pad/2, -wire_center - p.jj_lead_width/2 + p.alignment_tol],
                [p.cell_length*2 - p.top_cap_overlap_pad/2, -wire_center + p.jj_lead_width/2 - p.alignment_tol]                
            ]), p.corner_rounding)
            second_top_right = round_polygon(draw.Polygon([
                [p.cell_length*3/2 + p.cap_to_cap_dist/2 + p.top_cap_reduction - p.outer_intercap_extra_l, -p.central_width/2 + p.alignment_tol],
                [p.cell_length*3/2 + p.cap_to_cap_dist/2 + p.top_cap_reduction - p.outer_intercap_extra_l, +p.central_width/2 - p.alignment_tol],
                [sbr_middle - p.jj_lead_width/2, +p.central_width/2 - p.alignment_tol],
                [sbr_middle - p.jj_lead_width/2, +wire_center - p.jj_lead_width/2 + p.alignment_tol],
                [p.cell_length*2 - p.top_cap_overlap_pad/2, +wire_center - p.jj_lead_width/2 + p.alignment_tol],
                [p.cell_length*2 - p.top_cap_overlap_pad/2, +wire_center + p.jj_lead_width/2 - p.alignment_tol],
                [sbr_middle - p.jj_lead_width/2, +wire_center + p.jj_lead_width/2 - p.alignment_tol],
                [sbr_middle - p.jj_lead_width/2, +wire_center + p.jj_lead_width/2 + p.jj_wire_to_ground_gap + p.alignment_tol],
                [p.cell_length*3/2 + p.cap_to_cap_dist/2 + p.top_cap_reduction - p.outer_groundcap_extra_l, +wire_center + p.jj_lead_width/2 + p.jj_wire_to_ground_gap + p.alignment_tol],
                [p.cell_length*3/2 + p.cap_to_cap_dist/2 + p.top_cap_reduction - p.outer_groundcap_extra_l, +wire_center + p.jj_lead_width/2 + p.jj_wire_to_ground_gap + p.ground_cap_width + p.alignment_tol],
                [sbr_middle + p.jj_lead_width/2, +wire_center + p.jj_lead_width/2 + p.jj_wire_to_ground_gap + p.ground_cap_width + p.alignment_tol],
                [sbr_middle + p.jj_lead_width/2, -p.central_width/2 + p.alignment_tol]
            ]), p.corner_rounding)
            
        if fully_round=="left":
            bottom_left = round_polygon(draw.Polygon([
                [p.cell_length/2 - p.cap_to_cap_dist/2, p.central_width/2],
                [0, p.central_width/2],
                [0, -p.central_width/2],
                [0, -p.central_width/2 - p.jj_wire_to_cap_gap - p.jj_lead_width],
                [p.cell_length/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length, -p.central_width/2 - p.jj_wire_to_cap_gap - p.jj_lead_width],
                [p.cell_length/2 - p.jj_bridge_width/2 - p.jj_to_bridge_length, -p.central_width/2 - p.jj_wire_to_cap_gap],
                [p.jj_lead_width, -p.central_width/2 - p.jj_wire_to_cap_gap],
                [p.jj_lead_width, -p.central_width/2],
                [p.cell_length/2 - p.cap_to_cap_dist/2, -p.central_width/2],
                [p.cell_length/2 - p.cap_to_cap_dist/2, p.central_width/2]
            ]), p.corner_rounding)
            unround_bl = draw.rectangle(p.corner_rounding, p.corner_rounding,
                                        p.corner_rounding/2, -unround_height)
            bottom_left = draw.union(bottom_left, unround_bl)
        
            sbl_middle = p.top_cap_overlap_pad/2 - (p.top_cap_overlap_pad/2 - p.extremity_gap)/2
            second_bottom_left = round_polygon(draw.Polygon([
                [p.top_cap_overlap_pad/2, -wire_center + p.jj_lead_width/2 - p.alignment_tol],
                [sbl_middle - p.jj_lead_width/2, -wire_center + p.jj_lead_width/2 - p.alignment_tol],
                [sbl_middle - p.jj_lead_width/2, -wire_center - p.jj_lead_width/2 - p.jj_wire_to_ground_gap - p.alignment_tol],
                [sbl_middle - p.jj_lead_width/2, -wire_center - p.jj_lead_width/2 - p.jj_wire_to_ground_gap - p.alignment_tol - p.ground_cap_width],
                [p.cell_length/2 - p.cap_to_cap_dist/2 - p.top_cap_reduction + p.outer_groundcap_extra_l, -wire_center - p.jj_lead_width/2 - p.jj_wire_to_ground_gap - p.alignment_tol - p.ground_cap_width],
                [p.cell_length/2 - p.cap_to_cap_dist/2 - p.top_cap_reduction + p.outer_groundcap_extra_l, -wire_center - p.jj_lead_width/2 - p.jj_wire_to_ground_gap - p.alignment_tol],
                [sbl_middle + p.jj_lead_width/2, -wire_center - p.jj_lead_width/2 - p.jj_wire_to_ground_gap - p.alignment_tol],
                [sbl_middle + p.jj_lead_width/2, -wire_center - p.jj_lead_width/2 + p.alignment_tol],
                [p.top_cap_overlap_pad/2, -wire_center - p.jj_lead_width/2 + p.alignment_tol],
                [p.top_cap_overlap_pad/2, -wire_center + p.jj_lead_width/2 - p.alignment_tol]                
            ]), p.corner_rounding)
            second_top_left = round_polygon(draw.Polygon([
                [p.cell_length/2 - p.cap_to_cap_dist/2 - p.top_cap_reduction + p.outer_intercap_extra_l, -p.central_width/2 + p.alignment_tol],
                [p.cell_length/2 - p.cap_to_cap_dist/2 - p.top_cap_reduction + p.outer_intercap_extra_l, +p.central_width/2 - p.alignment_tol],
                [sbl_middle + p.jj_lead_width/2, +p.central_width/2 - p.alignment_tol],
                [sbl_middle + p.jj_lead_width/2, +wire_center - p.jj_lead_width/2 + p.alignment_tol],
                [p.top_cap_overlap_pad/2, +wire_center - p.jj_lead_width/2 + p.alignment_tol],
                [p.top_cap_overlap_pad/2, +wire_center + p.jj_lead_width/2 - p.alignment_tol],
                [sbl_middle + p.jj_lead_width/2, +wire_center + p.jj_lead_width/2 - p.alignment_tol],
                [sbl_middle + p.jj_lead_width/2, +wire_center + p.jj_lead_width/2 + p.jj_wire_to_ground_gap + p.alignment_tol],
                [p.cell_length/2 - p.cap_to_cap_dist/2 - p.top_cap_reduction + p.outer_groundcap_extra_l, +wire_center + p.jj_lead_width/2 + p.jj_wire_to_ground_gap + p.alignment_tol],
                [p.cell_length/2 - p.cap_to_cap_dist/2 - p.top_cap_reduction + p.outer_groundcap_extra_l, +wire_center + p.jj_lead_width/2 + p.jj_wire_to_ground_gap  + p.ground_cap_width + p.alignment_tol],
                [sbl_middle - p.jj_lead_width/2, +wire_center + p.jj_lead_width/2 + p.jj_wire_to_ground_gap  + p.ground_cap_width + p.alignment_tol],
                [sbl_middle - p.jj_lead_width/2, -p.central_width/2 + p.alignment_tol]
            ]), p.corner_rounding)
            
        #junctions, all manual
        
        jj_length = p.jj_to_bridge_length + 3.5*p.jj_t_size + 2*p.alignment_tol
        x_jj_off = p.jj_bridge_width/2 + jj_length/2
        overbridge_length = p.jj_bridge_length + 2*p.jj_overlength_left
        jj_TL = draw.rectangle(jj_length, overbridge_length, p.cell_length/2 - x_jj_off, wire_center)
        jj_BL = draw.rectangle(jj_length, overbridge_length, p.cell_length/2 - x_jj_off, -wire_center)
        jj_CTL = draw.rectangle(jj_length, p.jj_bridge_length, p.cell_length/2 + x_jj_off, wire_center)
        jj_CBL = draw.rectangle(jj_length, p.jj_bridge_length, p.cell_length/2 + x_jj_off, -wire_center)
        jj_CTR = draw.rectangle(jj_length, overbridge_length, p.cell_length*3/2 - x_jj_off, wire_center)
        jj_CBR = draw.rectangle(jj_length, overbridge_length, p.cell_length*3/2 - x_jj_off, -wire_center)
        jj_TR = draw.rectangle(jj_length, p.jj_bridge_length, p.cell_length*3/2 + x_jj_off, wire_center)
        jj_BR = draw.rectangle(jj_length, p.jj_bridge_length, p.cell_length*3/2 + x_jj_off, -wire_center)
               
        # underetch
        underetch_TL = draw.Polygon([
            [p.cell_length/2 - p.jj_bridge_width/2 - p.undersize, wire_center - overbridge_length/2 - p.under_spacing],
            [p.cell_length/2 - p.jj_bridge_width/2 + p.under_spacing, wire_center - overbridge_length/2 - p.under_spacing],
            [p.cell_length/2 - p.jj_bridge_width/2 + p.under_spacing, wire_center + overbridge_length/2 + p.under_spacing],
            [p.cell_length/2 - p.jj_bridge_width/2 - p.undersize, wire_center + overbridge_length/2 + p.under_spacing],
            [p.cell_length/2 - p.jj_bridge_width/2 - p.undersize, wire_center + p.jj_bridge_length/2 + p.undersize],
            [p.cell_length/2 + p.jj_bridge_width/2 + p.undersize, wire_center + p.jj_bridge_length/2 + p.undersize],
            [p.cell_length/2 + p.jj_bridge_width/2 + p.undersize, wire_center + p.jj_bridge_length/2 + p.under_spacing],
            [p.cell_length/2 + p.jj_bridge_width/2 - p.under_spacing, wire_center + p.jj_bridge_length/2 + p.under_spacing],
            [p.cell_length/2 + p.jj_bridge_width/2 - p.under_spacing, wire_center - p.jj_bridge_length/2 - p.under_spacing],
            [p.cell_length/2 + p.jj_bridge_width/2 + p.undersize, wire_center - p.jj_bridge_length/2 - p.under_spacing],
            [p.cell_length/2 + p.jj_bridge_width/2 + p.undersize, wire_center - p.jj_bridge_length/2 - p.undersize],
            [p.cell_length/2 - p.jj_bridge_width/2 - p.undersize, wire_center - p.jj_bridge_length/2 - p.undersize],
            [p.cell_length/2 - p.jj_bridge_width/2 - p.undersize, wire_center - overbridge_length/2 - p.under_spacing]            
        ])
        underetch_BL = draw.translate(underetch_TL, 0, -offset_top_bottom)
        underetch_TR, underetch_BR = draw.translate((underetch_TL, underetch_BL), p.cell_length)
            
        # Capas undercuts
        TL_uc = draw_rectangle_corner_offset(p.undersize, p.ground_cap_width,
            p.under_spacing + p.cell_length/2 - p.cap_to_cap_dist/2 - p.top_cap_reduction, 
            +wire_center + p.jj_lead_width/2 + p.jj_wire_to_ground_gap + p.alignment_tol)
        CL_uc = draw_rectangle_corner_offset(p.undersize, p.central_width - 2*p.alignment_tol,
            p.under_spacing + p.cell_length/2 - p.cap_to_cap_dist/2 - p.top_cap_reduction, 
            -p.central_width/2 + p.alignment_tol)
        BL_uc = draw_rectangle_corner_offset(p.undersize, p.ground_cap_width,
            p.under_spacing + p.cell_length/2 - p.cap_to_cap_dist/2 - p.top_cap_reduction, 
            -wire_center - p.jj_lead_width/2 - p.jj_wire_to_ground_gap -p.ground_cap_width - p.alignment_tol)
        
        TL_R_uc = draw_rectangle_corner_offset(-p.undersize, p.ground_cap_width,
            -p.under_spacing + p.cell_length/2 + p.cap_to_cap_dist/2 + p.top_cap_reduction, 
            +wire_center + p.jj_lead_width/2 + p.jj_wire_to_ground_gap + p.alignment_tol)
        CL_R_uc = draw_rectangle_corner_offset(-p.undersize, p.central_width - 2*p.alignment_tol,
            -p.under_spacing + p.cell_length/2 + p.cap_to_cap_dist/2 + p.top_cap_reduction, 
            -p.central_width/2 + p.alignment_tol)
        BL_R_uc = draw_rectangle_corner_offset(-p.undersize, p.ground_cap_width,
            -p.under_spacing + p.cell_length/2 + p.cap_to_cap_dist/2 + p.top_cap_reduction, 
            -wire_center - p.jj_lead_width/2 - p.jj_wire_to_ground_gap -p.ground_cap_width - p.alignment_tol)
        
        TR_uc, CR_uc, BR_uc, TR_R_uc, CR_R_uc, BR_R_uc = draw.translate((TL_uc, CL_uc, BL_uc, TL_R_uc, CL_R_uc, BL_R_uc), p.cell_length)
        
               
        # Rotate and translate all qgeometry as needed.
        # Done with utility functions in Metal 'draw_utility' for easy rotation/translation
        polys = [ground_pocket, 
                top_left, top_central, top_right, 
                bottom_left, bottom_central, bottom_right,
                top_diel, bottom_diel, central_diel,
                second_top_left, second_top_central, second_top_right, 
                second_bottom_left, second_bottom_central, second_bottom_right,
                top_little_t_left, top_little_t_right, bottom_little_t_left, bottom_little_t_right,
                top_left_little_t, bottom_left_little_t, top_right_little_t, bottom_right_little_t,
                jj_TL, jj_BL, jj_CTL, jj_CBL, jj_CTR, jj_CBR, jj_TR, jj_BR,
                underetch_TL, underetch_BL, underetch_TR, underetch_BR,
                TL_uc, CL_uc, BL_uc, TL_R_uc, CL_R_uc, BL_R_uc,
                TR_uc, CR_uc, BR_uc, TR_R_uc, CR_R_uc, BR_R_uc]
        
        polys = draw.rotate(polys, p.orientation, origin=(0,0))
        polys = draw.translate(polys, pos_x, pos_y)
        
        [ground_pocket, 
        top_left, top_central, top_right, 
        bottom_left, bottom_central, bottom_right,
        top_diel, bottom_diel, central_diel,
        second_top_left, second_top_central, second_top_right, 
        second_bottom_left, second_bottom_central, second_bottom_right,
        top_little_t_left, top_little_t_right, bottom_little_t_left, bottom_little_t_right,
        top_left_little_t, bottom_left_little_t, top_right_little_t, bottom_right_little_t,
        jj_TL, jj_BL, jj_CTL, jj_CBL, jj_CTR, jj_CBR, jj_TR, jj_BR,
        underetch_TL, underetch_BL, underetch_TR, underetch_BR,
        TL_uc, CL_uc, BL_uc, TL_R_uc, CL_R_uc, BL_R_uc,
        TR_uc, CR_uc, BR_uc, TR_R_uc, CR_R_uc, BR_R_uc] = polys

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
        #little Ts
        tee_CTL_name = "tee_CTL"
        tee_CTR_name = "tee_CTR"
        tee_CBL_name = "tee_CBL"
        tee_CBR_name = "tee_CBR"
        tee_TL_name = "tee_TL"
        tee_BL_name = "tee_BL"
        tee_TR_name = "tee_TR"
        tee_BR_name = "tee_BR"
        jj_TL_name = "jj_TL"
        jj_BL_name = "jj_BL"
        jj_CTL_name = "jj_CTL"
        jj_CBL_name = "jj_CBL"
        jj_CTR_name = "jj_CTR"
        jj_CBR_name = "jj_CBR"
        jj_TR_name = "jj_TR"
        jj_BR_name = "jj_BR"
        #underetches
        underetch_TL_name = "underetch_TL"
        underetch_BL_name = "underetch_BL"
        underetch_TR_name = "underetch_TR"
        underetch_BR_name = "underetch_BR"
        TL_uc_name = "TL_uc"
        CL_uc_name = "CL_uc"
        BL_uc_name = "BL_uc"
        TL_R_uc_name = "TL_R_uc"
        CL_R_uc_name = "CL_R_uc"
        BL_R_uc_name = "BL_R_uc"
        TR_uc_name = "TR_uc"
        CR_uc_name = "CR_uc"
        BR_uc_name = "BR_uc"
        TR_R_uc_name = "TR_R_uc"
        CR_R_uc_name = "CR_R_uc"
        BR_R_uc_name = "BR_R_uc"
        
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
            tee_CTL_name += affix
            tee_CTR_name += affix
            tee_CBL_name += affix
            tee_CBR_name += affix
            tee_TL_name += affix
            tee_BL_name += affix
            tee_TR_name += affix
            tee_BR_name += affix
            jj_TL_name += affix
            jj_BL_name += affix
            jj_CTL_name += affix
            jj_CBL_name += affix
            jj_CTR_name += affix
            jj_CBR_name += affix
            jj_TR_name += affix
            jj_BR_name += affix
            underetch_TL_name += affix
            underetch_BL_name += affix
            underetch_TR_name += affix
            underetch_BR_name += affix
            TL_uc_name += affix
            CL_uc_name += affix
            BL_uc_name += affix
            TL_R_uc_name += affix
            CL_R_uc_name += affix
            BL_R_uc_name += affix
            TR_uc_name += affix
            CR_uc_name += affix
            BR_uc_name += affix
            TR_R_uc_name += affix
            CR_R_uc_name += affix
            BR_R_uc_name += affix
            
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
                           {tee_CTL_name: top_little_t_left},
                           chip=chip, layer=p.layers[1])
        self.add_qgeometry('poly',
                           {tee_CTR_name: top_little_t_right},
                           chip=chip, layer=p.layers[1])
        self.add_qgeometry('poly',
                           {tee_CBL_name: bottom_little_t_left},
                           chip=chip, layer=p.layers[1])
        self.add_qgeometry('poly',
                           {tee_CBR_name: bottom_little_t_right},
                           chip=chip, layer=p.layers[1])
        self.add_qgeometry('poly',
                           {tee_TL_name: top_left_little_t},
                           chip=chip, layer=p.layers[1])
        self.add_qgeometry('poly',
                           {tee_BL_name: bottom_left_little_t},
                           chip=chip, layer=p.layers[1])
        self.add_qgeometry('poly',
                           {tee_TR_name: top_right_little_t},
                           chip=chip, layer=p.layers[1])
        self.add_qgeometry('poly',
                           {tee_BR_name: bottom_right_little_t},
                           chip=chip, layer=p.layers[1])
        
        self.add_qgeometry('poly',
                           {top_diel_name: top_diel},
                           chip=chip, layer=p.layers[2])
        self.add_qgeometry('poly',
                           {central_diel_name: central_diel},
                           chip=chip, layer=p.layers[2])
        self.add_qgeometry('poly',
                           {bottom_diel_name: bottom_diel},
                           chip=chip, layer=p.layers[2])
        self.add_qgeometry('poly',
                           {second_top_left_name: second_top_left},
                           chip=chip, layer=p.layers[3])
        self.add_qgeometry('poly',
                           {second_top_central_name: second_top_central},
                           chip=chip, layer=p.layers[3])
        self.add_qgeometry('poly',
                           {second_top_right_name: second_top_right},
                           chip=chip, layer=p.layers[3])
        self.add_qgeometry('poly',
                           {second_bottom_left_name: second_bottom_left},
                           chip=chip, layer=p.layers[3])
        self.add_qgeometry('poly',
                           {second_bottom_central_name: second_bottom_central},
                           chip=chip, layer=p.layers[3])
        self.add_qgeometry('poly',
                           {second_bottom_right_name: second_bottom_right},
                           chip=chip, layer=p.layers[3])
        
        self.add_qgeometry('poly',
                           {jj_TL_name: jj_TL},
                           chip=chip, layer=p.layers[4])
        self.add_qgeometry('poly',
                           {jj_BL_name: jj_BL},
                           chip=chip, layer=p.layers[4])
        self.add_qgeometry('poly',
                           {jj_CTL_name: jj_CTL},
                           chip=chip, layer=p.layers[4])
        self.add_qgeometry('poly',
                           {jj_CBL_name: jj_CBL},
                           chip=chip, layer=p.layers[4])
        self.add_qgeometry('poly',
                           {jj_CTR_name: jj_CTR},
                           chip=chip, layer=p.layers[4])
        self.add_qgeometry('poly',
                           {jj_CBR_name: jj_CBR},
                           chip=chip, layer=p.layers[4])
        self.add_qgeometry('poly',
                           {jj_TR_name: jj_TR},
                           chip=chip, layer=p.layers[4])
        self.add_qgeometry('poly',
                           {jj_BR_name: jj_BR},
                           chip=chip, layer=p.layers[4])
        
        self.add_qgeometry('poly',
                           {underetch_TL_name: underetch_TL},
                           chip=chip, layer=p.layers[5])
        self.add_qgeometry('poly',
                           {underetch_BL_name: underetch_BL},
                           chip=chip, layer=p.layers[5])
        self.add_qgeometry('poly',
                           {underetch_TR_name: underetch_TR},
                           chip=chip, layer=p.layers[5])
        self.add_qgeometry('poly',
                           {underetch_BR_name: underetch_BR},
                           chip=chip, layer=p.layers[5])
        
        
        self.add_qgeometry('poly',
                           {TL_uc_name: TL_uc},
                           chip=chip, layer=p.layers[5])
        self.add_qgeometry('poly',
                           {CL_uc_name: CL_uc},
                           chip=chip, layer=p.layers[5])
        self.add_qgeometry('poly',
                           {BL_uc_name: BL_uc},
                           chip=chip, layer=p.layers[5])
        self.add_qgeometry('poly',
                           {TL_R_uc_name: TL_R_uc},
                           chip=chip, layer=p.layers[5])
        self.add_qgeometry('poly',
                           {CL_R_uc_name: CL_R_uc},
                           chip=chip, layer=p.layers[5])
        self.add_qgeometry('poly',
                           {BL_R_uc_name: BL_R_uc},
                           chip=chip, layer=p.layers[5])
        self.add_qgeometry('poly',
                           {TR_uc_name: TR_uc},
                           chip=chip, layer=p.layers[5])
        self.add_qgeometry('poly',
                           {CR_uc_name: CR_uc},
                           chip=chip, layer=p.layers[5])
        self.add_qgeometry('poly',
                           {BR_uc_name: BR_uc},
                           chip=chip, layer=p.layers[5])
        self.add_qgeometry('poly',
                           {TR_R_uc_name: TR_R_uc},
                           chip=chip, layer=p.layers[5])
        self.add_qgeometry('poly',
                           {CR_R_uc_name: CR_R_uc},
                           chip=chip, layer=p.layers[5])
        self.add_qgeometry('poly',
                           {BR_R_uc_name: BR_R_uc},
                           chip=chip, layer=p.layers[5])
        
        if fully_round=="left":
            #additional area because of angle evaporation taken into account
            eps_0 = 8.854e-12
            eps_rel = 10.85
            evap_angle = 30 #degrees
            h_resist = 2e-3 #mm
            h_diel = 40e-9 #m
            print(f"Info given for eps_rel={eps_rel}, evap angle={evap_angle}°, h_resist={h_resist*1e3}µm and h_diel={h_diel*1e9}nm")
            evap_shadow = h_resist*np.tan(evap_angle*np.pi/180)
            print(f"Additionnal length from evap shadow = {evap_shadow*1e3:.2} µm")
            capa_ground_area = draw.subtract(second_top_central, ground_pocket).area
            capa_ground_area_left = draw.subtract(second_bottom_left, ground_pocket).area
            added_capa_ground_area = 2*(p.ground_cap_width+p.alignment_tol)*evap_shadow
            print(f"Added Capa to ground area : {added_capa_ground_area*1e6:.3} µm²")
            print(f"Total Capa to ground area : {(capa_ground_area + added_capa_ground_area)*1e6:.3} µm²")
            print(f"First cell area ratio: {(capa_ground_area_left + added_capa_ground_area)/(capa_ground_area + added_capa_ground_area):.3}")
            print(f"Capa to ground : {eps_0*eps_rel*(capa_ground_area+added_capa_ground_area)*1e-6/h_diel*1e12:.3} pF")
            capa_inter_area = second_bottom_central.intersection(top_central).area
            capa_inter_area_left = second_top_left.intersection(bottom_left).area
            added_capa_inter_area = 2*(p.central_width+p.alignment_tol)*evap_shadow
            print(f"Added Inter capa area : {added_capa_inter_area*1e6:.3} µm²")
            print(f"Inter capa area : {(capa_inter_area + added_capa_inter_area)*1e6:.3} µm²")
            print(f"First cell area ratio : {(capa_inter_area_left + added_capa_inter_area)/(capa_inter_area + added_capa_inter_area):.3}")
            print(f"Inter capa : {eps_0*eps_rel*(capa_inter_area+added_capa_inter_area)*1e-6/h_diel*1e12:.3} pF")
        
    def make(self):
        self.make_cell()
        

class circuFlatLineWithUC(circuFlatDoubleCellWithUC):
    
    default_options = Dict(
        n_cells=10
    )
    """Default drawing options"""

    component_metadata = Dict(short_name='circuLiteLine',
                              _qgeometry_table_path='True',
                              _qgeometry_table_poly='True',
                              _qgeometry_table_junction='False')
    """Component metadata"""

    TOOLTIP = """CircuLite line."""
    
    def make(self):
        p = self.p
        chip = p.chip
        
        tot_cell_length = 2*p.cell_length
        
        for idx in range(p.n_cells):
            if idx==0:
                fully_round = "left"
            elif idx==p.n_cells-1:
                fully_round = "right"
            else:
                fully_round = None
            offset_x = tot_cell_length*np.cos(p.orientation*np.pi/180)
            offset_y = tot_cell_length*np.sin(p.orientation*np.pi/180)
            self.make_cell(idx*offset_x, idx*offset_y, affix=self.name+f"_c_{idx}", fully_round=fully_round)
        
        #make the adapter things on extremities
        ground_pocket_left = draw.rectangle(p.adaptater_length,
                                       p.jj_wire_to_ground_gap*2 + p.jj_lead_width*2 + p.jj_wire_to_cap_gap*2 + p.central_width,
                                       -p.adaptater_length/2, 0)
        ground_pocket_right = draw.rectangle(p.adaptater_length,
                                       p.jj_wire_to_ground_gap*2 + p.jj_lead_width*2 + p.jj_wire_to_cap_gap*2 + p.central_width,
                                       p.n_cells*tot_cell_length + p.adaptater_length/2, 0)
        bottom_left_adaptater = round_polygon(draw.Polygon([
            [0, -p.central_width/2 - p.jj_wire_to_cap_gap - p.jj_lead_width],
            [-p.adaptater_length, -p.central_width/2 - p.jj_wire_to_cap_gap - p.jj_lead_width],
            [-p.adaptater_length, -p.central_width/2 - p.jj_wire_to_cap_gap - p.jj_lead_width + p.adaptater_width],
            [-p.adaptater_length + 2*p.adaptater_rounding, -p.central_width/2 - p.jj_wire_to_cap_gap - p.jj_lead_width + p.adaptater_width],
            [-2*p.adaptater_rounding, -p.central_width/2 - p.jj_wire_to_cap_gap],
            [0, -p.central_width/2 - p.jj_wire_to_cap_gap]
        ]), p.adaptater_rounding)
        unround_bl_adap_right = draw.rectangle(p.adaptater_rounding, p.jj_lead_width, 
                                               -p.adaptater_rounding/2, -p.central_width/2 - p.jj_wire_to_cap_gap - p.jj_lead_width/2)
        unround_bl_adap_left = draw_rectangle_corner_offset(p.adaptater_rounding, p.adaptater_width, 
                                               -p.adaptater_length, -p.central_width/2 - p.jj_wire_to_cap_gap - p.jj_lead_width)
        bottom_left_adaptater = draw.union(bottom_left_adaptater, unround_bl_adap_left, unround_bl_adap_right)
        
        top_left_adaptater = draw.scale(bottom_left_adaptater, yfact=-1, origin=(0, 0))
        bottom_right_adaptater, top_right_adaptater = draw.scale((bottom_left_adaptater, top_left_adaptater), 
                                                                 xfact=-1, origin=(p.n_cells/2*tot_cell_length, 0))
        
        polys = [bottom_left_adaptater, top_left_adaptater,
                 bottom_right_adaptater, top_right_adaptater,
                 ground_pocket_left, ground_pocket_right]
        polys = draw.rotate(polys, p.orientation, origin=(0,0))
        polys = draw.translate(polys, p.pos_x, p.pos_y)
        [bottom_left_adaptater, top_left_adaptater,
        bottom_right_adaptater, top_right_adaptater,
        ground_pocket_left, ground_pocket_right] = polys
        
        self.add_qgeometry('poly',
                           {"left_pocket_adap": ground_pocket_left},
                           chip=chip, layer=p.layers[0],
                           subtract=True)
        self.add_qgeometry('poly',
                           {"right_pocket_adap": ground_pocket_right},
                           chip=chip, layer=p.layers[0],
                           subtract=True)
        self.add_qgeometry('poly',
                           {"bot_left_adap": bottom_left_adaptater},
                           chip=chip, layer=p.layers[0])
        self.add_qgeometry('poly',
                           {"top_left_adap": top_left_adaptater},
                           chip=chip, layer=p.layers[0])
        self.add_qgeometry('poly',
                           {"bot_right_adap": bottom_right_adaptater},
                           chip=chip, layer=p.layers[0])
        self.add_qgeometry('poly',
                           {"top_right_adap": top_right_adaptater},
                           chip=chip, layer=p.layers[0])
        
        
        ############################################################

        # add pins
        pin_position = p.central_width/2 + p.jj_wire_to_cap_gap + p.jj_lead_width - p.adaptater_width/2
        pin_left_top = draw.LineString([(0, pin_position),
                                     (-p.adaptater_length, pin_position)])
        pin_left_bot = draw.LineString([(0, -pin_position),
                                     (-p.adaptater_length, -pin_position)])
        pin_right_top = draw.LineString([(p.n_cells*tot_cell_length, pin_position),
                                  (p.n_cells*tot_cell_length + p.adaptater_length, pin_position)])
        pin_right_bot = draw.LineString([(p.n_cells*tot_cell_length, -pin_position),
                                  (p.n_cells*tot_cell_length + p.adaptater_length, -pin_position)])
        pins = [pin_left_top, pin_left_bot, pin_right_top, pin_right_bot]
        pins = draw.rotate(pins, p.orientation, origin=(0,0))
        pins = draw.translate(pins, p.pos_x, p.pos_y)
        [pin_left_top, pin_left_bot, pin_right_top, pin_right_bot] = pins
                
        self.add_pin("left_top",
                     points=pin_left_top.coords,
                     width=p.jj_lead_width,
                     input_as_norm=True,
                     chip=chip)
        self.add_pin("left_bottom",
                     points=pin_left_bot.coords,
                     width=p.jj_lead_width,
                     input_as_norm=True,
                     chip=chip)
        self.add_pin("right_top",
                     points=pin_right_top.coords,
                     width=p.jj_lead_width,
                     input_as_norm=True,
                     chip=chip)
        self.add_pin("right_bottom",
                     points=pin_right_bot.coords,
                     width=p.jj_lead_width,
                     input_as_norm=True,
                     chip=chip)