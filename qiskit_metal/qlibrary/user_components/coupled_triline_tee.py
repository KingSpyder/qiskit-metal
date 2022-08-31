from qiskit_metal.qlibrary.couplers.coupled_line_tee import CoupledLineTee
from qiskit_metal import draw, Dict
import numpy as np

class CoupledTriLineTee(CoupledLineTee):
    '''TODO: This is not really good as it requires rework in a gds editor to fill the gaps
    and remove excess material due to buffer...
    Maybe something with polygons and subtract operations.
    '''
    default_options = Dict(layer=['2', '2', '1'],
                           last_trace_added_gap="50um")
    
    def make(self):
        """Build the component."""
        p = self.p

        prime_cpw_length = p.coupling_length * 2
        second_flip = 1
        if p.mirror:
            second_flip = -1

        #Primary CPW
        prime_cpw = draw.LineString([[-prime_cpw_length / 2, 0],
                                     [prime_cpw_length / 2, 0]])

        #Secondary CPW
        second_down_length = p.down_length
        second_y = -p.prime_width / 2 - p.prime_gap - p.coupling_space - p.second_gap - p.second_width / 2
        second_cpw = draw.LineString(
            [[second_flip * (-p.coupling_length / 2), second_y],
             [second_flip * (p.coupling_length / 2), second_y],
             [
                 second_flip * (p.coupling_length / 2),
                 second_y - second_down_length
             ]])

        second_termination = 0
        if p.open_termination:
            second_termination = p.second_gap

        second_cpw_etch = draw.LineString(
            [[
                second_flip * (-p.coupling_length / 2 - second_termination),
                second_y
            ], [second_flip * (p.coupling_length / 2), second_y],
             [
                 second_flip * (p.coupling_length / 2),
                 second_y - second_down_length
             ]])

        second_cpw_ter = draw.LineString(
            [[
                second_flip * (-p.coupling_length / 2 - second_termination
                               - p.last_trace_added_gap),
                second_y
            ], [second_flip * (p.coupling_length / 2), second_y],
             [
                 second_flip * (p.coupling_length / 2),
                 second_y - second_down_length
             ]])
        
        #Rotate and Translate
        c_items = [prime_cpw, second_cpw, second_cpw_etch, second_cpw_ter]
        c_items = draw.rotate(c_items, p.rotation, origin=(0, 0))
        c_items = draw.translate(c_items, p.pos_x, p.pos_y)
        [prime_cpw, second_cpw, second_cpw_etch, second_cpw_ter] = c_items

        #Add to qgeometry tables
        self.add_qgeometry('path', {'prime_cpw': prime_cpw},
                           width=p.prime_width,
                           layer=p.layer[0])
        self.add_qgeometry('path', {'prime_cpw_sub': prime_cpw},
                           width=p.prime_width + 2 * p.prime_gap,
                           subtract=True,
                           layer=p.layer[1])
        self.add_qgeometry('path', {'prime_cpw_ter': prime_cpw},
                           width=p.prime_width + 2 * p.prime_gap\
                                    + 2 * p.last_trace_added_gap,
                           subtract=True,
                           layer=p.layer[2])
        self.add_qgeometry('path', {'second_cpw': second_cpw},
                           width=p.second_width,
                           fillet=p.fillet,
                           layer=p.layer[0])
        self.add_qgeometry('path', {'second_cpw_sub': second_cpw_etch},
                           width=p.second_width + 2 * p.second_gap,
                           subtract=True,
                           fillet=p.fillet,
                           layer=p.layer[1])
        self.add_qgeometry('path', {'second_cpw_ter': second_cpw_ter},
                           width=p.second_width + 2 * p.second_gap\
                                    + 2 * p.last_trace_added_gap,
                           subtract=True,
                           fillet=p.fillet,
                           layer=p.layer[2])
             
        #Add pins
        prime_pin_list = prime_cpw.coords
        second_pin_list = second_cpw.coords

        self.add_pin('prime_start',
                     points=np.array(prime_pin_list[::-1]),
                     width=p.prime_width,
                     input_as_norm=True)
        self.add_pin('prime_end',
                     points=np.array(prime_pin_list),
                     width=p.prime_width,
                     input_as_norm=True)
        self.add_pin('second_end',
                     points=np.array(second_pin_list[1:]),
                     width=p.second_width,
                     input_as_norm=True)