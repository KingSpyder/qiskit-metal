# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.


'''
For basic utility functions involving Metal Objects
Updated 2019/09/25 - Thomas McConkey
@author: Zlatko
'''

from ...toolbox.addict import Dict

def is_metal_object(obj):
    '''
    Handle problem with isinstance when reloading modules
    '''
    if isinstance(obj, Dict):
        return False
    return hasattr(obj, '__i_am_metal__')


def is_metal_circuit(obj):
    '''
    Handle problem with isinstance when reloading modules
    '''
    if isinstance(obj, Dict):
        return False
    return hasattr(obj, '__i_am_metal_circuit__')