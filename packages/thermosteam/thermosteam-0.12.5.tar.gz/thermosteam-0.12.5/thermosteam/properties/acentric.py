# -*- coding: utf-8 -*-
'''
All data and methods related to estimating a chemical's accentric factor.
'''

__all__ = ('omega', 'LK_omega', 'StielPolar',
           'omega_methods', 'Stiel_polar_methods')

import numpy as np
from math import log, log10
from .critical import Tc, Pc
from .critical import _crit_PSRKR4, _crit_PassutDanner, _crit_Yaws
from .phase_change import Tb


omega_methods = ['PSRK', 'PD', 'YAWS', 'LK', 'DEFINITION']


def omega(CASRN, AvailableMethods=False, Method=None,
          IgnoreMethods=['LK', 'DEFINITION'], *, P_at_Tr_seventenths=None):
    r'''This function handles the retrieval of a chemical's acentric factor,
    `omega`, or its calculation from correlations or directly through the
    definition of acentric factor if possible. Requires a known boiling point,
    critical temperature and pressure for use of the correlations. Requires
    accurate vapor pressure data for direct calculation.

    Will automatically select a method to use if no Method is provided;
    returns None if the data is not available and cannot be calculated.

    .. math::
        \omega \equiv -\log_{10}\left[\lim_{T/T_c=0.7}(P^{sat}/P_c)\right]-1.0

    Examples
    --------
    >>> omega(CASRN='64-17-5')
    0.635

    Parameters
    ----------
    CASRN : string
        CASRN [-]

    Returns
    -------
    omega : float
        Acentric factor of compound
    methods : list, only returned if AvailableMethods == True
        List of methods which can be used to obtain omega with the given inputs

    Other Parameters
    ----------------
    Method : string, optional
        The method name to use. Accepted methods are 'PSRK', 'PD', 'YAWS', 
        'LK', and 'DEFINITION'. All valid values are also held in the list
        omega_methods.
    AvailableMethods : bool, optional
        If True, function will determine which methods can be used to obtain
        omega for the desired chemical, and will return methods instead of
        omega
    IgnoreMethods : list, optional
        A list of methods to ignore in obtaining the full list of methods,
        useful for for performance reasons and ignoring inaccurate methods

    Notes
    -----
    A total of five sources are available for this function. They are:

        * 'PSRK', a compillation of experimental and estimated data published 
          in the Appendix of [2]_, the fourth revision of the PSRK model.
        * 'PD', an older compillation of
          data published in (Passut & Danner, 1973) [3]_.
        * 'YAWS', a large compillation of data from a
          variety of sources; no data points are sourced in the work of [4]_.
        * 'LK', a estimation method for hydrocarbons.
        * 'DEFINITION', based on the definition of omega as
          presented in [1]_, using vapor pressure data.

    References
    ----------
    .. [1] Pitzer, K. S., D. Z. Lippmann, R. F. Curl, C. M. Huggins, and
       D. E. Petersen: The Volumetric and Thermodynamic Properties of Fluids.
       II. Compressibility Factor, Vapor Pressure and Entropy of Vaporization.
       J. Am. Chem. Soc., 77: 3433 (1955).
    .. [2] Horstmann, Sven, Anna Jabłoniec, Jörg Krafczyk, Kai Fischer, and
       Jürgen Gmehling. "PSRK Group Contribution Equation of State:
       Comprehensive Revision and Extension IV, Including Critical Constants
       and Α-Function Parameters for 1000 Components." Fluid Phase Equilibria
       227, no. 2 (January 25, 2005): 157-64. doi:10.1016/j.fluid.2004.11.002.
    .. [3] Passut, Charles A., and Ronald P. Danner. "Acentric Factor. A
       Valuable Correlating Parameter for the Properties of Hydrocarbons."
       Industrial & Engineering Chemistry Process Design and Development 12,
       no. 3 (July 1, 1973): 365-68. doi:10.1021/i260047a026.
    .. [4] Yaws, Carl L. Thermophysical Properties of Chemicals and
       Hydrocarbons, Second Edition. Amsterdam Boston: Gulf Professional
       Publishing, 2014.
    '''
    def list_methods():
        methods = []
        if CASRN in _crit_PSRKR4.index and not np.isnan(_crit_PSRKR4.at[CASRN, 'omega']):
            methods.append('PSRK')
        if CASRN in _crit_PassutDanner.index and not np.isnan(_crit_PassutDanner.at[CASRN, 'omega']):
            methods.append('PD')
        if CASRN in _crit_Yaws.index and not np.isnan(_crit_Yaws.at[CASRN, 'omega']):
            methods.append('YAWS')
        Tcrit, Pcrit = Tc(CASRN), Pc(CASRN)
        if Tcrit and Pcrit:
            if Tb(CASRN):
                methods.append('LK')
            if P_at_Tr_seventenths:
                methods.append('DEFINITION')  # TODO: better integration
        if IgnoreMethods:
            for Method in IgnoreMethods:
                if Method in methods:
                    methods.remove(Method)
        methods.append('NONE')
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]
    # This is the calculate, given the method section
    if Method == 'PSRK':
        _omega = float(_crit_PSRKR4.at[CASRN, 'omega'])
    elif Method == 'PD':
        _omega = float(_crit_PassutDanner.at[CASRN, 'omega'])
    elif Method == 'YAWS':
        _omega = float(_crit_Yaws.at[CASRN, 'omega'])
    elif Method == 'LK':
        _omega = LK_omega(Tb(CASRN), Tc(CASRN), Pc(CASRN))
    elif Method == 'DEFINITION':
        _omega = -log10(P_at_Tr_seventenths/Pc(CASRN)) - 1.0
    elif Method == 'NONE':
        _omega = None
    else:
        raise Exception('Failure in in function')
    return _omega


def LK_omega(Tb, Tc, Pc):
    r'''Estimates the acentric factor of a fluid using a correlation in [1]_.

    .. math::
        \omega = \frac{\ln P_{br}^{sat} - 5.92714 + 6.09648/T_{br} + 1.28862
        \ln T_{br} -0.169347T_{br}^6}
        {15.2518 - 15.6875/T_{br} - 13.4721 \ln T_{br} + 0.43577 T_{br}^6}

    Parameters
    ----------
    Tb : float
        Boiling temperature of the fluid [K]
    Tc : float
        Critical temperature of the fluid [K]
    Pc : float
        Critical pressure of the fluid [Pa]

    Returns
    -------
    omega : float
        Acentric factor of the fluid [-]

    Notes
    -----
    Internal units are atmosphere and Kelvin.
    Example value from Reid (1987). Using ASPEN V8.4, LK method gives 0.325595.

    Examples
    --------
    Isopropylbenzene

    >>> LK_omega(425.6, 631.1, 32.1E5)
    0.32544249926397856

    References
    ----------
    .. [1] Lee, Byung Ik, and Michael G. Kesler. "A Generalized Thermodynamic
       Correlation Based on Three-Parameter Corresponding States." AIChE Journal
       21, no. 3 (1975): 510-527. doi:10.1002/aic.690210313.
    '''
    T_br = Tb/Tc
    omega = (log(101325.0/Pc) - 5.92714 + 6.09648/T_br + 1.28862*log(T_br) -
             0.169347*T_br**6)/(15.2518 - 15.6875/T_br - 13.4721*log(T_br) +
             0.43577*T_br**6)
    return omega


Stiel_polar_methods = ['DEFINITION']


def StielPolar(Tc=None, Pc=None, omega=None, CASRN='', Method=None,
               AvailableMethods=False, *, P_at_Tr_sixtenths=None):
    r'''This function handles the calculation of a chemical's Stiel Polar
    factor, directly through the definition of Stiel-polar factor if possible.
    Requires Tc, Pc, acentric factor, and a vapor pressure datum at Tr=0.6.

    Will automatically select a method to use if no Method is provided;
    returns None if the data is not available and cannot be calculated.

    .. math::
        x = \log P_r|_{T_r=0.6} + 1.70 \omega + 1.552

    Parameters
    ----------
    Tc : float
        Critical temperature of fluid [K]
    Pc : float
        Critical pressure of fluid [Pa]
    omega : float
        Acentric factor of the fluid [-]
    CASRN : string
    P_at_Tr_sixtenths : float
        Pressure at Tr=0.6

    Returns
    -------
    factor : float
        Stiel polar factor of compound
    methods : list, only returned if AvailableMethods == True
        List of methods which can be used to obtain Stiel polar factor with the
        given inputs

    Other Parameters
    ----------------
    Method : string, optional
        The method name to use. Only 'DEFINITION' is accepted so far.
        All valid values are also held in the list Stiel_polar_methods.
    AvailableMethods : bool, optional
        If True, function will determine which methods can be used to obtain
        Stiel-polar factor for the desired chemical, and will return methods
        instead of stiel-polar factor

    Notes
    -----
    Only one source is available for this function. It is:

        * 'DEFINITION', based on the definition of
          Stiel Polar Factor presented in [1]_, using vapor pressure data.

    A few points have also been published in [2]_, which may be used for
    comparison. Currently this is only used for a surface tension correlation.

    Examples
    --------
    >>> StielPolar(647.3, 22048321.0, 0.344, CASRN='7732-18-5')
    0.024581140348734376

    References
    ----------
    .. [1] Halm, Roland L., and Leonard I. Stiel. "A Fourth Parameter for the
       Vapor Pressure and Entropy of Vaporization of Polar Fluids." AIChE
       Journal 13, no. 2 (1967): 351-355. doi:10.1002/aic.690130228.
    .. [2] D, Kukoljac Miloš, and Grozdanić Dušan K. "New Values of the
       Polarity Factor." Journal of the Serbian Chemical Society 65, no. 12
       (January 1, 2000). http://www.shd.org.rs/JSCS/Vol65/No12-Pdf/JSCS12-07.pdf
    '''
    def list_methods():
        methods = []
        if Tc and Pc and omega:
            methods.append('DEFINITION')
        methods.append('NONE')
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]
    if Method == 'DEFINITION':
        if not P_at_Tr_sixtenths:
            factor = None
        else:
            Pr = P_at_Tr_sixtenths/Pc
            factor = log10(Pr) + 1.70*omega + 1.552
    elif Method == 'NONE':
        factor = None
    else:
        raise Exception('Failure in in function')
    return factor


