'''This file is part of AeoLiS.
   
AeoLiS is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
   
AeoLiS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
   
You should have received a copy of the GNU General Public License
along with AeoLiS.  If not, see <http://www.gnu.org/licenses/>.
   
AeoLiS  Copyright (C) 2015 Bas Hoonhout

bas.hoonhout@deltares.nl         b.m.hoonhout@tudelft.nl
Deltares                         Delft University of Technology
Unit of Hydraulic Engineering    Faculty of Civil Engineering and Geosciences
Boussinesqweg 1                  Stevinweg 1
2629 HVDelft                     2628CN Delft
The Netherlands                  The Netherlands

'''


from __future__ import absolute_import, division

import logging
import numpy as np

# package modules
from aeolis.utils import *


# initialize logger
logger = logging.getLogger(__name__)


def equilibrium(s, p):
    '''Compute equilibrium sediment concentration following Bagnold (1937)

    Parameters
    ----------
    s : dict
        Spatial grids
    p : dict
        Model configuration parameters

    Returns
    -------
    dict
        Spatial grids

    '''

    if p['process_transport']:
        
        nf = p['nfractions']
        uw = s['uw'][:,:,np.newaxis].repeat(nf, axis=2)
        tau = s['tau'][:,:,np.newaxis].repeat(nf, axis=2)
        ix = tau != 0.
        
        s['Cu'] = np.zeros(uw.shape)
        s['Cuf'] = np.zeros(uw.shape)

        s['Cu'][ix] = _equilibrium(tau[ix], s['uth'][ix], uw[ix],
                                   Cb=p['Cb'], rhoa=p['rhoa'], g=p['g'], method=p['method_transport'])
        s['Cuf'][ix] = _equilibrium(tau[ix], s['uthf'][ix], uw[ix],
                                    Cb=p['Cb'], rhoa=p['rhoa'], g=p['g'], method=p['method_transport'])

    s['Cu'] *= p['accfac']
    s['Cuf'] *= p['accfac']

    return s


def _equilibrium(tau, uth, uw, Cb=1.5, rhoa=1.25, g=9.81, method='bagnold'):
    if method.lower() == 'bagnold':
        Cu = np.maximum(0., Cb * rhoa / g * (tau - uth)**3 / uw)
    elif method.lower() == 'kawamura':
        Cu = np.maximum(0., Cb * rhoa / g * (tau + uth)**2 * (tau - uth) / uw)
    elif method.lower() == 'lettau':
        Cu = np.maximum(0., Cb * rhoa / g * (tau - uth) * tau**2 / uw)
    else:
        logger.log_and_raise('Unknown transport formulation [%s]' % method, exc=ValueError)

    return Cu


def compute_weights(s, p):
    '''Compute weights for sediment fractions

    Multi-fraction sediment transport needs to weigh the transport of
    each sediment fraction to prevent the sediment transport to
    increase with an increasing number of sediment fractions. The
    weighing is not uniform over all sediment fractions, but depends
    on the sediment availibility in the air and the bed and the bed
    interaction parameter ``bi``.

    Parameters
    ----------
    s : dict
        Spatial grids
    p : dict
        Model configuration parameters

    Returns
    -------
    numpy.ndarray
        Array with weights for each sediment fraction

    '''

    w_air = normalize(s['Ct'], s['Cu'])
    w_bed = normalize(s['mass'][:,:,0,:], axis=2)

    w = (1. - p['bi']) * w_air \
        + (1. - np.minimum(1., (1. - p['bi']) * np.sum(w_air, axis=2, keepdims=True))) * w_bed
    w = normalize(w, axis=2)
    
    return w, w_air, w_bed


def renormalize_weights(w, ix):
    '''Renormalizes weights for sediment fractions

    Renormalizes weights for sediment fractions such that the sum of
    all weights is unity. To ensure that the erosion of specific
    fractions does not exceed the sediment availibility in the bed,
    the normalization only modifies the weights with index equal or
    larger than ``ix``.

    Parameters
    ----------
    w : numpy.ndarray
        Array with weights for each sediment fraction
    ix : int
        Minimum index to be modified

    Returns
    -------
    numpy.ndarray
        Array with weights for each sediment fraction

    '''
    
    f = np.sum(w[:,:,:ix], axis=2, keepdims=True)
    w[:,:,ix:] = normalize(w[:,:,ix:], axis=2) * (1. - f)

    # normalize in case of supply-limitation
    # use uniform distribution in case of no supply
    w = normalize(w, axis=2, fill=1./w.shape[2])

    return w
