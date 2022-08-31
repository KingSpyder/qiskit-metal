# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# ALTERED CODE


from re import sub
from tracemalloc import start
from typing import TYPE_CHECKING
from shapely.geometry.polygon import Polygon
from qiskit_metal.qlibrary.core.qroute import QRouteLead
import numpy as np
from qiskit_metal import draw, Dict
from numpy.linalg import norm
from qiskit_metal.qlibrary.core import QRoute
import math

from qiskit_metal import logger
from qiskit_metal.toolbox_python.utility_functions import bad_fillet_idxs
    
def turn_direction(pts: np.ndarray):
    """Characterize the middle point as left or right turn.

    Args:
        pts (np.ndarray): (3,2) array of points coordinates

    Returns:
        String: "L" or "R"
    """
    v_1 = pts[1]-pts[0]
    v_2 = pts[2]-pts[1]
    if np.cross(v_1, v_2)>0:
        return "L"
    else:
        return "R"

class QRouteMod(QRoute):
    """DOC TO MODIFY
    Super-class implementing routing methods that are valid irrespective of
    the number of pins (>=1). The route is stored in a n array of planar points
    (x,y coordinates) and one direction, which is that of the last point in the
    array. Values are stored as np.ndarray of parsed floats or np.array float
    pair.

    Inherits `QComponent` class

    Default Options:
        * pin_inputs: Dict
            * start_pin: Dict -- Component and pin string pair. Define which pin to start from
                * component: '' -- Name of component to start from, which has a pin
                * pin: '' -- Name of pin used for pin_start
            * end_pin=Dict -- Component and pin string pair. Define which pin to start from
                * component: '' -- Name of component to end on, which has a pin
                * pin: '' -- Name of pin used for pin_end
        * lead: Dict
            * start_straight: '0mm' -- Lead-in, defined as the straight segment extension from start_pin.  Defaults to 0.1um.
            * end_straight: '0mm' -- Lead-out, defined as the straight segment extension from end_pin.  Defaults to 0.1um.
            * start_jogged_extension: '' -- Lead-in, jogged extension of lead-in. Described as list of tuples
            * end_jogged_extension: '' -- Lead-out, jogged extension of lead-out. Described as list of tuples
        * fillet: '0'
        * total_length: '7mm'
        * chip: 'main' -- Which chip is this component attached to.  Defaults to 'main'.
        * layer: '1' -- Which layer this component should be rendered on.  Defaults to '1'.
        * trace_width: 'cpw_width' -- Defines the width of the line.  Defaults to 'cpw_width'.

    How to specify \*_jogged_extensions for the QRouteLeads:
        \*_jogged_extensions have to be specified in an OrderedDict with incremental keys.
        the value of each key specifies the direction of the jog and the extension past the jog.
        For example:

        .. code-block:: python
            :linenos:

            jogs = OrderedDict()
            jogs[0] = ["R", '200um']
            jogs[1] = ["R", '200um']
            jogs[2] = ["L", '200um']
            jogs[3] = ["L", '500um']
            jogs[4] = ["R", '200um']
            jogs_other = ....

            options = {'lead': {
                'start_straight': '0.3mm',
                'end_straight': '0.3mm',
                'start_jogged_extension': jogs,
                'end_jogged_extension': jogs_other
            }}

        The jog direction can be specified in several ways. Feel free to pick the one more
        convenient for your coding style:

        >> "L", "L#", "R", "R#", #, "#", "A,#", "left", "left#", "right", "right#"

        where # is any signed or unsigned integer or floating point value.
        For example the following will all lead to the same turn:

        >> "L", "L90", "R-90", 90, "90", "A,90", "left", "left90", "right-90"
    """

    component_metadata = Dict(short_name='route', _qgeometry_table_path='True')
    """Component metadata"""

    default_options = Dict(
        pin_inputs=Dict(
            start_pin=Dict(  # QRoute also supports single pin routes
                component='',  # Name of component to start from, which has a pin
                pin=''),  # Name of pin used for pin_start
            end_pin=Dict(
                component='',  # Name of component to end on, which has a pin
                pin='')  # Name of pin used for pin_end
        ),
        fillet='0',
        lead=Dict(start_straight='0mm',
                  end_straight='0mm',
                  start_jogged_extension='',
                  end_jogged_extension=''),
        total_length='7mm',
        chip='main',
        layer='1',
        param_width=lambda t:1e-3,
        step=1e-3,
        overlap="0um")
    """Default options"""

    TOOLTIP = """QRoute"""

    def __init__(self,
                 design,
                 name: str = None,
                 options: Dict = None,
                 type: str = "CPW",
                 **kwargs):
        """Initializes all Routes.

        Calls the QComponent __init__() to create a new Metal component.
        Before that, it adds the variables that are needed to support routing.

        Args:
            design (QDesign): The parent design.
            name (str): Name of the component. Auto-named if possible.
            options (dict): User options that will override the defaults.  Defaults to None.
            type (string or list of strings): Supports Route (single layer trace), gap, CPW.
            In CPW, first function is a route, and second is a gap.
                Defaults to "CPW".
            NEW: gnd_buffer_inner and gnd_buffer_outer so that a ground buffer is created between
            the width function corresponding to gnd_buffer_outer and the one of gnd_buffer_inner.
        """
        # Class key Attributes:
        #     * head (QRouteLead()): Stores sequential points to start the route.
        #     * tail (QRouteLead()): (optional) Stores sequential points to terminate the route.
        #     * intermediate_pts: (list or numpy Nx2 or dict) Sequence of points between and other
        #         than head and tail.  Defaults to None. Type could be either list or numpy Nx2,
        #         or dict/OrderedDict nesting lists or numpy Nx2.
        #     * start_pin_name (string): Head pin name.  Defaults to "start".
        #     * end_pin_name (string): Tail pin name.  Defaults to "end".

        self.head = QRouteLead()
        self.tail = QRouteLead()

        # keep track of all points so far in the route from both ends
        self.intermediate_pts = np.empty((0, 2), float)  # will be numpy Nx2

        # supported pin names (constants)
        self.start_pin_name = "start"
        self.end_pin_name = "end"

        self.type = type
        
        # regular QComponent boot, including the run of make()
        super(QRoute, self).__init__(design, name, options, **kwargs)
        
    def fillet_path_and_draw(self, pts, w_func):
        """Output the filleted path.
        Args:
            row (DataFrame): Row to fillet.
        Returns:
            Polygon of the new filleted path.
        """
        fillet = self.p.fillet
        coord = 0
        polys = []
        if fillet == 0:  # zero radius, no need to fillet
            for seg_pts in zip(pts, pts[1:]):
                poly = self.straight_segment(seg_pts, coord, w_func)
                polys.append(poly)
                coord += norm(seg_pts[1]-seg_pts[0])
            return draw.union(polys), pts
        if len(pts) <= 2:  # only start and end points, no need to fillet
            poly = self.straight_segment(pts, coord, w_func)
            return poly, pts
        newpath = np.array([pts[0]])

        # Get list of vertices that can't be filleted
        no_fillet = bad_fillet_idxs(pts, fillet,
                                    self.design.template_options.PRECISION)

        # Iterate through every three-vertex corner
        for (i, (start, corner, end)) in enumerate(zip(pts, pts[1:],
                                                       pts[2:])):
            if i + 1 in no_fillet:  # don't fillet this corner
                poly = self.straight_segment([newpath[-1], corner], coord, w_func)
                coord += norm(corner-newpath[-1])
                newpath = np.concatenate((newpath, np.array([corner])))
                polys.append(poly)
            else:
                curve_poly, fillet_pts, end_coord = self._calc_fillet(np.array(start), np.array(corner),
                                           np.array(end),fillet, w_func, newpath[-1], coord,
                                           int(np.pi/2*fillet/self.p.step))
                if fillet_pts is not False:
                    poly = self.straight_segment([newpath[-1], fillet_pts[0]], coord, w_func)
                    coord = end_coord
                    if poly is not None:
                        polys += [poly, curve_poly]
                    else:
                        polys.append(curve_poly)
                    newpath = np.concatenate((newpath, fillet_pts))
                else:
                    poly = self.straight_segment([newpath[-1], corner], coord, w_func)
                    coord += norm(corner-newpath[-1])
                    polys.append(poly)
                    newpath = np.concatenate((newpath, np.array([corner])))
        poly = self.straight_segment([newpath[-1], end], coord, w_func)
        polys.append(poly)
        fillet_poly = draw.union(polys)
        newpath = np.concatenate((newpath, np.array([end])))
        return fillet_poly, newpath

    def _calc_fillet(self,
                     vertex_start,
                     vertex_corner,
                     vertex_end,
                     radius,
                     w_func,
                     last_point,
                     start_coord,
                     points=16):
        """Returns the filleted path based on the start, corner, and end
        vertices and the fillet radius.
        Args:
            vertex_start (np.ndarray): x-y coordinates of starting vertex.
            vertex_corner (np.ndarray): x-y coordinates of corner vertex.
            vertex_end (np.ndarray): x-y coordinates of end vertex.
            radius (float): Fillet radius.
            points (int): Number of points to draw in the fillet corner.
        """
        # Start, corner, and end vertices must be distinct
        if np.array_equal(vertex_start, vertex_corner) or np.array_equal(
                vertex_end, vertex_corner):
            return False

        # Vectors pointing from corner to start and end vertices, respectively
        # Also calculate their lengths and unit vectors
        sc_vec = vertex_start - vertex_corner
        ec_vec = vertex_end - vertex_corner
        sc_norm = np.linalg.norm(sc_vec)
        ec_norm = np.linalg.norm(ec_vec)
        sc_uvec = sc_vec / sc_norm
        ec_uvec = ec_vec / ec_norm

        # Angle between previous unit vectors
        end_angle = np.arccos(np.dot(sc_uvec, ec_uvec))

        # Start, corner, and end vertices can't be collinear
        if (end_angle == 0) or (end_angle == np.pi):
            return False

        # Fillet circle must be small enough to fit inside corner
        if radius / np.tan(end_angle / 2) > min(sc_norm, ec_norm):
            return False

        # Unit vector pointing from corner vertex to center of fillet circle
        net_uvec = (sc_uvec + ec_uvec) / np.linalg.norm(sc_uvec + ec_uvec)

        # Coordinates of center of fillet circle
        circle_center = vertex_corner + net_uvec * radius / np.sin(
            end_angle / 2)

        # Deltas represent displacement from corner vertex to circle center
        # Midpoint angle from circle center to corner, wrt to horizontal extending from former
        # Note: arctan is fine for angles in range (-pi / 2, pi / 2] but needs extra pi factor otherwise
        delta_x = vertex_corner[0] - circle_center[0]
        delta_y = vertex_corner[1] - circle_center[1]
        if delta_x:
            theta_mid = np.arctan(delta_y / delta_x) + np.pi * int(delta_x < 0)
        else:
            theta_mid = np.pi * ((1 - 2 * int(delta_y < 0)) + int(delta_y < 0))

        # Start and end sweep angles determined relative to midpoint angle
        # Swap them as needed to resolve ambiguity in arctan
        theta_start = theta_mid - (np.pi - end_angle) / 2
        theta_end = theta_mid + (np.pi - end_angle) / 2
        p1 = circle_center + radius * np.array(
            [np.cos(theta_start), np.sin(theta_start)])
        p2 = circle_center + radius * np.array(
            [np.cos(theta_end), np.sin(theta_end)])
        if np.linalg.norm(vertex_start - p2) < np.linalg.norm(vertex_start -
                                                              p1):
            theta_start, theta_end = theta_end, theta_start

        # Populate the fillet corner, skipping the start point since it's already added
        path_pt = circle_center + radius\
            *np.array([np.cos(theta_start), np.sin(theta_start)])
        path = np.array([path_pt])
        cur_coord = start_coord + norm(path[0]-last_point)
        theta_step = np.abs(theta_end-theta_start)/(points-1)
        direction_factor = 1 - 2*(theta_end>theta_start)
        v_ortho_left = direction_factor*np.array([
                                    np.cos(theta_start), np.sin(theta_start)])
        leftside_points = [path_pt + w_func(cur_coord)/2 * v_ortho_left]
        rightside_points = [path_pt - w_func(cur_coord)/2 * v_ortho_left]
        # 1 if clockwise, -1 if other way
        for theta in np.linspace(theta_start, theta_end, points)[1:]:
            path_pt = circle_center + radius\
                    *np.array([np.cos(theta), np.sin(theta)])
            v_ortho_left = direction_factor*np.array([
                                        np.cos(theta), np.sin(theta)])
            cur_coord += radius*theta_step
            p_left = path_pt + w_func(cur_coord)/2 * v_ortho_left
            p_right = path_pt - w_func(cur_coord)/2 * v_ortho_left
            leftside_points.append(p_left)
            rightside_points.append(p_right)
            path = np.concatenate(
                (path, np.array([path_pt])))
        rightside_points.reverse()
        totlist = leftside_points + rightside_points
        curve_poly = draw.Polygon(totlist)
        return curve_poly, path, cur_coord

    def straight_segment(self, segment_pts, beg_coord, width_func) -> Polygon:
        """Draws the polygon for a straight segment. 

        Args:
            segment_pts (list): list of the two extremities of the segment
            beg_coord (float): the line coordinate of the beginning point
            step (float): max step size

        Returns:
            Polygon: 
        """
        step = self.p.step
        seg_length = np.linalg.norm(segment_pts[1]-segment_pts[0])
        if seg_length>1e-9: #for rounding error tolerance
            num_points = int(np.ceil(seg_length/step))+1
            actual_step = seg_length/(num_points-1)

            leftside_points = []
            rightside_points = []
            x0, y0 = segment_pts[0]
            x1, y1 = segment_pts[1]
            orthog_vec = np.array([y0 - y1, x1 - x0])/seg_length
            for i in range(num_points):
                p_left = np.array([x0+(x1-x0)*i/(num_points-1), 
                                y0+(y1-y0)*i/(num_points-1)])\
                    + width_func(beg_coord+i*actual_step)/2 * orthog_vec
                p_right = np.array([x0+(x1-x0)*i/(num_points-1), 
                                y0+(y1-y0)*i/(num_points-1)])\
                    - width_func(beg_coord+i*actual_step)/2 * orthog_vec
                leftside_points.append(p_left)
                rightside_points.append(p_right)
            rightside_points.reverse()
            totlist = leftside_points + rightside_points
            polygon = draw.Polygon(totlist)

            return polygon

    def make_elements(self, pts: np.ndarray):
        """Turns the CPW points into design elements, and add them to the
        design object.

        Args:
            pts (np.ndarray): Array of points
        """

        # prepare the routing track
        line = draw.LineString(pts)

        # compute actual final length
        p = self.p
        self.options._actual_length = str(
            line.length - self.length_excess_corner_rounding(line.coords)
        ) + ' ' + self.design.get_units()
        actual_length = self.parse_value(self.options._actual_length)
        
        if "meander" in p:
         if round(actual_length, 4) != p.total_length:
            logger.warning(f"ModRoute line {self.name} length is different than expected."
                           f"Change routing jogs or such.") 
        # BIG ass function to make polygon
        
        #if the parametric width is a single function, put it in a list to
        #cover all cases in a single piece of code:
        if callable(p.param_width):
            p.param_width = [p.param_width]
        
        for w_func_id, w_func in enumerate(p.param_width):
            modline_poly,_ = self.fillet_path_and_draw(pts, w_func)
            #check if all widths are to be drawn on the same layer or not
            if type(p.layer)==list or type(p.layer)==list:
                layer = p.layer[w_func_id]
            else:
                layer = p.layer 
            #again to see if a gap is drawn or a line
            if type(self.type)==list or type(p.layer)==list:
                cur_type = self.type[w_func_id].upper().strip()
            else:
                cur_type = self.type.upper().strip()
            add_qgeo = True
            if cur_type=="ROUTE":
                subtract = False
                #Code for the overlap pad
                pin_start = self.pins["start"]
                height = self.design.parse_value(p.overlap)
                if height!=0:
                    xpad = pin_start["middle"][0] + height/2*pin_start["normal"][0]
                    ypad = pin_start["middle"][1] + height/2*pin_start["normal"][1]
                    if pin_start["normal"][0]==0:
                        overlap_pad = draw.rectangle(w_func(0), height, xpad, ypad)
                    else:
                        overlap_pad = draw.rectangle(height, w_func(0), xpad, ypad)
                    modline_poly = draw.union([modline_poly, overlap_pad])
            elif cur_type=="GAP":
                subtract = True
            elif cur_type=="CPW":
                if w_func_id==0:
                    subtract = False
                elif w_func_id==1:
                    subtract = True
                else:
                    raise Exception("Can't pass \"CPW\" route type to a ModRoute with\
                        more than two parametric functions.")
            elif cur_type=="GND_BUFFER_INNER":
                inner_buffer_to_sub = modline_poly
                add_qgeo = False
            elif cur_type=="GND_BUFFER_OUTER":
                try:
                    modline_poly = draw.subtract(modline_poly, inner_buffer_to_sub)
                except NameError:
                    raise Exception(f"ModRoute error: can't find the inner limit of the ground buffer."
                                    f"self.type should be [*, 'gnd_buffer_inner', 'gnd_buffer_outer', *] "
                                    f"with the corresponding width functions at the corresponding indices.")
                subtract = False
            else:
                raise Exception("Unknown route type " + self.type + 
                                " The only supported types are cpw, gap, and route.\
                                  Beware this is specific to modroute.")
            if add_qgeo:
                self.add_qgeometry('poly', {'modline': modline_poly},
                                    layer=layer, subtract=subtract)
