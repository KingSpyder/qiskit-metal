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
""""""

from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.core import QComponent
import numpy as np


class LineTeeMultiMat(QComponent):
    """Generates a three pin (+) structure comprised of a primary two pin CPW
    transmission line, and a secondary one pin neighboring CPW transmission
    line that is capacitively coupled to the primary. Such a structure can be
    used, as an example, for generating CPW resonator hangars off of a
    transmission line. (0,0) represents the center position of the component.

    Inherits QComponent class.

    ::

                  (0,0)
        +--------------------------+
                    |
                    |
                    |
                    |
                    |
                    +

    .. image::
        LineTee.png

    .. meta::
        Line Tee

    Options:
        * prime_width: '10um' -- The width of the trace of the two pin CPW transmission line
        * prime_gap: '6um' -- The dielectric gap of the two pin CPW transmission line
        * second_width: '10um' -- The width of the trace of the one pin CPW transmission line
        * second_gap: '6um' -- The dielectric gap of the one pin CPW transmission line (also for the capacitor)
        * t_length: '50um' -- The length for the t branches
    """
    component_metadata = Dict(short_name='cpw', _qgeometry_table_path='True')
    """Component metadata"""

    #Currently setting the primary CPW length based on the coupling_length
    #May want it to be it's own value that the user can control?
    default_options = Dict(prime_width='10um',
                           prime_gap='6um',
                           second_width='10um',
                           second_gap='6um',
                           t_length='50um',
                           coupling_space='10um',
                           coupling_length='5um',
                           down_length='500um',
                           second_end_overlap='5um',
                           open_termination=False,
                           impedance=False)
    """Default connector options"""

    TOOLTIP = """Generates a three pin (+) structure comprised of a primary two pin CPW
    transmission line, and a secondary one pin neighboring CPW transmission
    line that is capacitively coupled to the primary."""

    def make(self):
        """Build the component."""
        p = self.p
        
        if not isinstance(p.layer, list):
            p.layer = [p.layer]
        if len(p.layer)==1:
            p.layer = [p.layer[0]]*3
        if len(p.layer)==2:
            p.layer = [p.layer[0], p.layer[0], p.layer[1]]
        if not isinstance(p.impedance, list):
            p.impedance = [p.impedance]
        if len(p.impedance)==1:
            p.impedance = [p.impedance[0]]*2
            
        prime_cpw_length = p.t_length * 2

        #Primary CPW
        prime_cpw = draw.LineString([[-prime_cpw_length/2, 0],
                                     [prime_cpw_length/2, 0]])

        #Secondary CPW
        second_cpw = draw.LineString([[0, -p.prime_width / 2 - p.coupling_space],
                                      [0, -p.down_length -p.prime_width/2 
                                       - p.coupling_space -p.second_end_overlap]])
        if p.open_termination:
            second_cpw_sub = draw.LineString([[0, -p.prime_width / 2 - p.coupling_space],
                                      [0, -p.down_length -p.prime_width/2 - p.coupling_space
                                       -2*p.second_gap]])
        else:
            second_cpw_sub = draw.LineString([[0, -p.prime_width / 2 - p.coupling_space],
                                      [0, -p.down_length -p.prime_width/2 
                                       - p.coupling_space]])
            
        #padT
        pad_T = draw.rectangle(p.coupling_length, p.second_width,
                               0, -p.prime_width / 2 - p.coupling_space- p.second_width/2)
        pocket = draw.rectangle(p.coupling_length + 4*p.second_gap,
                                p.coupling_space-p.prime_gap+p.second_width+p.second_gap,
                                0,
                                -p.coupling_space/2 - p.prime_gap/2 
                                - p.prime_width/2-p.second_width/2-p.second_gap/2,
                                )
        
        #Rotate and Translate
        c_items = [prime_cpw, second_cpw, second_cpw_sub, pad_T, pocket]
        c_items = draw.rotate(c_items, p.orientation, origin=(0, 0))
        c_items = draw.translate(c_items, p.pos_x, p.pos_y)
        [prime_cpw, second_cpw, second_cpw_sub, pad_T, pocket] = c_items

        #Add to qgeometry tables
        self.add_qgeometry('path', {'prime_cpw': prime_cpw},
                           width=p.prime_width,
                           layer=p.layer[1],
                           impedance=p.impedance[1])
        self.add_qgeometry('path', {'prime_cpw_sub': prime_cpw},
                           width=p.prime_width + 2 * p.prime_gap,
                           subtract=True,
                           layer=p.layer[0])
        self.add_qgeometry('path', {'second_cpw': second_cpw},
                           width=p.second_width,
                           layer=p.layer[2],
                           impedance=p.impedance[2])
        self.add_qgeometry('poly', {'pad_T': pad_T},
                           width=p.second_width,
                           layer=p.layer[2],
                           impedance=p.impedance[2])
        self.add_qgeometry('path', {'second_cpw_sub': second_cpw_sub},
                           width=p.second_width + 2 * p.second_gap,
                           subtract=True,
                           layer=p.layer[0])
        self.add_qgeometry('poly', {'pocket': pocket},
                           subtract=True,
                           layer=p.layer[0])

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
                     points=np.array(second_pin_list),
                     width=p.second_width,
                     input_as_norm=True)
