# -*- coding: utf-8 -*-
"""
All Mixture object builders.

"""
from ..base import PhaseMixtureProperty
from .ideal_mixture_model import IdealMixtureModel
from .mixture import Mixture

__all__ = ('ideal_mixture',)

# %% Functions

def group_properties_by_phase(phase_properties):
    hasfield = hasattr
    getfield = getattr
    iscallable = callable
    properties_by_phase = {'s': [],
                           'l': [],
                           'g': []}
    for phase, properties in properties_by_phase.items():
        for phase_property in phase_properties:
            if iscallable(phase_property) and hasfield(phase_property, phase):
                prop = getfield(phase_property, phase)
            else:
                prop = phase_property
            properties.append(prop)
    return properties_by_phase
    
def build_ideal_PhaseMixtureProperty(chemicals, var):
    setfield = setattr
    getfield = getattr
    phase_properties = [getfield(i, var) for i in chemicals]
    new = PhaseMixtureProperty.__new__(PhaseMixtureProperty)
    for phase, properties in group_properties_by_phase(phase_properties).items():
        setfield(new, phase, IdealMixtureModel(properties, var))
    new.var = var
    return new

# %% Ideal mixture model builder 

def ideal_mixture(chemicals,
                  rigorous_energy_balance=True,
                  include_excess_energies=False):
    """
    Create a Mixture object that computes mixture properties using ideal mixing rules.
    
    Parameters
    ----------
    chemicals : Chemicals
        For retrieving pure component chemical data.
    rigorous_energy_balance=True : bool
        Whether to rigorously solve for temperature in energy balance or simply approximate.
    include_excess_energies=False : bool
        Whether to include excess energies in enthalpy and entropy calculations.

    See also
    --------
    :class:`~.mixture.Mixture`
    :class:`~.IdealMixtureModel`

    Examples
    --------
    >>> from thermosteam import Chemicals
    >>> from thermosteam.mixture import ideal_mixture
    >>> chemicals = Chemicals(['Water', 'Ethanol'])
    >>> ideal_mixture_model = ideal_mixture(chemicals)
    >>> ideal_mixture_model.Hvap([0.2, 0.8], 350)
    39601.089191849824


    """
    chemicals = tuple(chemicals)
    getfield = getattr
    Cn =  build_ideal_PhaseMixtureProperty(chemicals, 'Cn')
    H =  build_ideal_PhaseMixtureProperty(chemicals, 'H')
    S = build_ideal_PhaseMixtureProperty(chemicals, 'S')
    H_excess = build_ideal_PhaseMixtureProperty(chemicals, 'H_excess')
    S_excess = build_ideal_PhaseMixtureProperty(chemicals, 'S_excess')
    mu = build_ideal_PhaseMixtureProperty(chemicals, 'mu')
    V = build_ideal_PhaseMixtureProperty(chemicals, 'V')
    kappa = build_ideal_PhaseMixtureProperty(chemicals, 'kappa')
    Hvap = IdealMixtureModel([getfield(i, 'Hvap') for i in chemicals], 'Hvap')
    sigma = IdealMixtureModel([getfield(i, 'sigma') for i in chemicals], 'sigma')
    epsilon = IdealMixtureModel([getfield(i, 'epsilon') for i in chemicals], 'epsilon')
    return Mixture('ideal mixing', Cn, H, S, H_excess, S_excess,
                   mu, V, kappa, Hvap, sigma, epsilon,
                   rigorous_energy_balance, include_excess_energies)