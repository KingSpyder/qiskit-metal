from qiskit_metal.qlibrary.couplers.coupled_line_tee import CoupledLineTee
from qiskit_metal import draw, Dict
import numpy as np

class CoupledTeeBuffered(CoupledLineTee):
    
    default_options = Dict(layer=['2', '2', '1'],
                           last_trace_added_gap="50um",
                           buffer_width="50um")
    
    def make(self):
        """Build the component."""
        p = self.p

        prime_cpw_length = p.coupling_length * 2
        
        second_flip = 1
        if p.mirror:
            second_flip = -1

        #Primary CPW
        prime_offset = p.prime_width/2 + p.prime_gap + p.buffer_width/2
        
        prime_cpw = draw.LineString([[-prime_cpw_length / 2, 0],
                                     [prime_cpw_length / 2, 0]])
        prime_cpw_up_buffer = draw.LineString([[-prime_cpw_length / 2, prime_offset],
                                     [prime_cpw_length / 2, prime_offset]])
        prime_cpw_down_buffer = draw.LineString([[-prime_cpw_length / 2, -prime_offset],
                                     [prime_cpw_length / 2, -prime_offset]])
        
        
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

        #short always created, but not always added to qgeometry tables
        short_height = 2*p.buffer_width + 2*p.second_gap + p.second_width
        short_termination = draw.rectangle(p.buffer_width, short_height,
            second_flip * (-p.coupling_length/2 - p.buffer_width/2), second_y)
        
        second_cpw_inner_buff = draw.LineString(
            [[
                second_flip * (-p.coupling_length / 2 - second_termination),
                second_y - p.second_width/2 - p.second_gap - p.buffer_width/2
            ], [second_flip * (p.coupling_length/2 - p.second_width/2 - p.second_gap - p.buffer_width/2),
                second_y - p.second_width/2 - p.second_gap - p.buffer_width/2],
             [
                 second_flip * (p.coupling_length/2 - p.second_width/2 - p.second_gap - p.buffer_width/2),
                 second_y - second_down_length
             ]])
        second_cpw_outer_buff = draw.LineString(
            [[
                second_flip * (-p.coupling_length / 2 - second_termination),
                second_y + p.second_width/2 + p.second_gap + p.buffer_width/2
            ], [second_flip * (p.coupling_length/2 + p.second_width/2 + p.second_gap + p.buffer_width/2),
                second_y + p.second_width/2 + p.second_gap + p.buffer_width/2],
             [
                 second_flip * (p.coupling_length/2 + p.second_width/2 + p.second_gap + p.buffer_width/2),
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
        c_items = [prime_cpw, prime_cpw_up_buffer, prime_cpw_down_buffer,
                   second_cpw, second_cpw_inner_buff,
                   second_cpw_outer_buff, short_termination, second_cpw_ter]
        c_items = draw.rotate(c_items, p.rotation, origin=(0, 0))
        c_items = draw.translate(c_items, p.pos_x, p.pos_y)
        [prime_cpw, prime_cpw_up_buffer, prime_cpw_down_buffer, 
         second_cpw, second_cpw_inner_buff, 
         second_cpw_outer_buff, short_termination, second_cpw_ter] = c_items

        #Add to qgeometry tables
        self.add_qgeometry('path', {'prime_cpw': prime_cpw},
                           width=p.prime_width,
                           layer=p.layer[0])
        self.add_qgeometry('path', {'prime_cpw_up_buffer': prime_cpw_up_buffer},
                           width=p.buffer_width,
                           layer=p.layer[1])
        self.add_qgeometry('path', {'prime_cpw_down_buffer': prime_cpw_down_buffer},
                           width=p.buffer_width,
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
        self.add_qgeometry('path', {'second_cpw_inner_buffer': second_cpw_inner_buff},
                           width=p.buffer_width,
                           fillet=p.fillet - p.second_width/2 - p.second_gap - p.buffer_width/2,
                           layer=p.layer[1])
        self.add_qgeometry('path', {'second_cpw_outer_buffer': second_cpw_outer_buff},
                           width=p.buffer_width,
                           fillet=p.fillet + p.second_width/2 + p.second_gap + p.buffer_width/2,
                           layer=p.layer[1])
        self.add_qgeometry('path', {'second_cpw_ter': second_cpw_ter},
                           width=p.second_width + 2 * p.second_gap\
                                    + 2 * p.last_trace_added_gap,
                           subtract=True,
                           fillet=p.fillet,
                           layer=p.layer[2])
        if not(p.open_termination):
            self.add_qgeometry("poly", {'second_short':short_termination},
                               layer=p.layer[1])   
             
             
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