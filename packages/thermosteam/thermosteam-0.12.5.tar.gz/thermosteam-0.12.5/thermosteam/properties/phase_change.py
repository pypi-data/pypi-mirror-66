# -*- coding: utf-8 -*-
"""
All data and methods related to the phase change of a chemical.

References
----------
.. [1] Haynes, W.M., Thomas J. Bruno, and David R. Lide. CRC Handbook of
       Chemistry and Physics, 95E. Boca Raton, FL: CRC press, 2014.
.. [2] Yaws, Carl L. Thermophysical Properties of Chemicals and
       Hydrocarbons, Second Edition. Amsterdam Boston: Gulf Professional
       Publishing, 2014.
.. [3] Bradley, Jean-Claude, Antony Williams, and Andrew Lang.
       "Jean-Claude Bradley Open Melting Point Dataset", May 20, 2014.
       https://figshare.com/articles/Jean_Claude_Bradley_Open_Melting_Point_Datset/1031637.
.. [4] Haynes, W.M., Thomas J. Bruno, and David R. Lide. CRC Handbook of
       Chemistry and Physics, 95E. Boca Raton, FL: CRC press, 2014.
.. [5] Poling, Bruce E. The Properties of Gases and Liquids. 5th edition.
       New York: McGraw-Hill Professional, 2000.
.. [6] Pitzer, Kenneth S. "The Volumetric and Thermodynamic Properties of
       Fluids. I. Theoretical Basis and Virial Coefficients."
       Journal of the American Chemical Society 77, no. 13 (July 1, 1955):
       3427-33. doi:10.1021/ja01618a001
.. [7] Green, Don, and Robert Perry. Perry's Chemical Engineers' Handbook,
       Eighth Edition. McGraw-Hill Professional, 2007.
.. [8] Sivaraman, Alwarappa, Joe W. Magee, and Riki Kobayashi. "Generalized
       Correlation of Latent Heats of Vaporization of Coal-Liquid Model Compounds
       between Their Freezing Points and Critical Points." Industrial &
       Engineering Chemistry Fundamentals 23, no. 1 (February 1, 1984): 97-100.
       doi:10.1021/i100013a017.
.. [9] Morgan, David L., and Riki Kobayashi. "Extension of Pitzer CSP
       Models for Vapor Pressures and Heats of Vaporization to Long-Chain
       Hydrocarbons." Fluid Phase Equilibria 94 (March 15, 1994): 51-87.
       doi:10.1016/0378-3812(94)87051-9.
.. [10] Velasco, S., M. J. Santos, and J. A. White. "Extended Corresponding
        States Expressions for the Changes in Enthalpy, Compressibility Factor
        and Constant-Volume Heat Capacity at Vaporization." The Journal of
        Chemical Thermodynamics 85 (June 2015): 68-76.
        doi:10.1016/j.jct.2015.01.011.
.. [11] Riedel, L. "Eine Neue Universelle Dampfdruckformel Untersuchungen
        Uber Eine Erweiterung Des Theorems Der Ubereinstimmenden Zustande. Teil
        I." Chemie Ingenieur Technik 26, no. 2 (February 1, 1954): 83-89.
        doi:10.1002/cite.330260206.
.. [12] Chen, N. H. "Generalized Correlation for Latent Heat of Vaporization."
        Journal of Chemical & Engineering Data 10, no. 2 (April 1, 1965): 207-10.
        doi:10.1021/je60025a047
.. [13] LIU, ZHI-YONG. "Estimation of Heat of Vaporization of Pure Liquid at
        Its Normal Boiling Temperature." Chemical Engineering Communications
        184, no. 1 (February 1, 2001): 221-28. doi:10.1080/00986440108912849.
.. [14] Vetere, Alessandro. "Methods to Predict the Vaporization Enthalpies
        at the Normal Boiling Temperature of Pure Compounds Revisited."
        Fluid Phase Equilibria 106, no. 1-2 (May 1, 1995): 1–10.
        doi:10.1016/0378-3812(94)02627-D.
"""


__all__ = ['EnthalpyVaporization',
           'Tb_methods', 'Tb', 'Tm_methods', 'Tm', 
           'Clapeyron', 'Pitzer', 'SMK', 'MK', 'Velasco', 'Riedel', 'Chen', 
           'Liu', 'Vetere', 'Watson',  'Hfus', 'Hsub']

import numpy as np
from ..base import InterpolatedTDependentModel, TDependentHandleBuilder, Hvap
from .._constants import R, N_A
from math import log, pi
from .utils import CASDataReader
from .miscdata import _CRC_organic, _CRC_inorganic
from .miscdata import _VDISaturationDict, VDI_tabular_data
from ..functional import Z
from .vapor_pressure import VaporPressure
from .coolprop import has_CoolProp, PropsSI, coolprop_dict, coolprop_fluids
from .dippr import DIPPR_EQ106

read = CASDataReader(__file__, 'Phase Change')


_Yaws = read('Yaws Boiling Points.tsv')
_Tm_ON = read('OpenNotebook Melting Points.tsv')
_GharagheiziHvap = read('Ghazerati Appendix Vaporization Enthalpy.tsv')
_CRCHvap = read('CRC Handbook Heat of Vaporization.tsv')
_CRCHfus = read('CRC Handbook Heat of Fusion.tsv')
_GharagheiziHsub = read('Ghazerati Appendix Sublimation Enthalpy.tsv')
_Perrys2_150 = read('Table 2-150 Heats of Vaporization of Inorganic and Organic Liquids.tsv')
_VDI_PPDS_4 = read('VDI PPDS Enthalpies of vaporization.tsv')
_Alibakhshi_Cs = read('Alibakhshi one-coefficient enthalpy of vaporization.tsv')

### Boiling Point at 1 atm

CRC_ORG = 'CRC_ORG'
CRC_INORG = 'CRC_INORG'
YAWS = 'YAWS'
PSAT_DEFINITION = 'PSAT_DEFINITION'
NONE = 'NONE'

Tb_methods = [CRC_INORG, CRC_ORG, YAWS, PSAT_DEFINITION]


def Tb(CASRN, AvailableMethods=False, Method=None, IgnoreMethods=[PSAT_DEFINITION]):
    r'''
    This function handles the retrieval of a chemical's boiling
    point as given by [1]_ [2]_. Lookup is based on CASRNs. Return None if the
    data is not available.

    Prefered sources are 'CRC Physical Constants, organic' for organic
    chemicals, and 'CRC Physical Constants, inorganic' for inorganic
    chemicals. This function has data for approximately 13000 chemicals.

    Parameters
    ----------
    CASRN : string
        CASRN [-]

    Returns
    -------
    Tb : float
        Boiling temperature, [K]
    methods : list, only returned if AvailableMethods == True
        List of methods which can be used to obtain Tb with the given inputs

    Other Parameters
    ----------------
    Method : string, optional
        A string for the method name to use, as defined by constants in
        Tb_methods
    AvailableMethods : bool, optional
        If True, function will determine which methods can be used to obtain
        Tb for the desired chemical, and will return methods instead of Tb
    IgnoreMethods : list, optional
        A list of methods to ignore in obtaining the full list of methods,
        useful for for performance reasons and ignoring inaccurate methods

    Notes
    -----
    A total of four methods are available for this function. They are:

        * 'CRC_ORG', a compillation of data on organics
          as published in [1]_.
        * 'CRC_INORG', a compillation of data on
          inorganic as published in [1]_.
        * 'YAWS', a large compillation of data from a
          variety of sources; no data points are sourced in the work of [2]_.
        * 'PSAT_DEFINITION', calculation of boiling point from a
          vapor pressure calculation. This is normally off by a fraction of a
          degree even in the best cases. Listed in IgnoreMethods by default
          for performance reasons.

    Examples
    --------
    >>> Tb('7732-18-5')
    373.124

    '''
    def list_methods():
        methods = []
        if CASRN in _CRC_inorganic and not np.isnan(_CRC_inorganic.at[CASRN, 'Tb']):
            methods.append(CRC_INORG)
        if CASRN in _CRC_organic and not np.isnan(_CRC_organic.at[CASRN, 'Tb']):
            methods.append(CRC_ORG)
        if CASRN in _Yaws:
            methods.append(YAWS)
        if PSAT_DEFINITION not in IgnoreMethods:
            try:
                # For some chemicals, vapor pressure range will exclude Tb
                VaporPressure(CASRN=CASRN).solve_prop(101325.)
                methods.append(PSAT_DEFINITION)
            except:  # pragma: no cover
                pass
        if IgnoreMethods:
            for Method in IgnoreMethods:
                if Method in methods:
                    methods.remove(Method)
        methods.append(NONE)
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]

    if Method == CRC_INORG:
        return float(_CRC_inorganic.at[CASRN, 'Tb'])
    elif Method == CRC_ORG:
        return float(_CRC_organic.at[CASRN, 'Tb'])
    elif Method == YAWS:
        return float(_Yaws.at[CASRN, 'Tb'])
    elif Method == PSAT_DEFINITION:
        return VaporPressure(CASRN=CASRN).solve_prop(101325.)
    elif Method == NONE:
        return None
    else:
        raise Exception('Failure in in function')


### Melting Point


OPEN_NTBKM = 'OPEN_NTBKM'

Tm_methods = [OPEN_NTBKM, CRC_INORG, CRC_ORG]


def Tm(CASRN, AvailableMethods=False, Method=None, IgnoreMethods=[]):
    r'''
    This function handles the retrieval of a chemical's melting
    point as given by [3]_ [4]_. Lookup is based on CASRNs. Return None if 
    the data is not available.

    Prefered sources are 'Open Notebook Melting Points', with backup sources
    'CRC Physical Constants, organic' for organic chemicals, and
    'CRC Physical Constants, inorganic' for inorganic chemicals. Function has
    data for approximately 14000 chemicals.

    Parameters
    ----------
    CASRN : string
        CASRN [-]

    Returns
    -------
    Tm : float
        Melting temperature, [K]
    methods : list, only returned if AvailableMethods == True
        List of methods which can be used to obtain Tm with the given inputs

    Other Parameters
    ----------------
    Method : string, optional
        A string for the method name to use, as defined by constants in
        Tm_methods
    AvailableMethods : bool, optional
        If True, function will determine which methods can be used to obtain
        Tm for the desired chemical, and will return methods instead of Tm
    IgnoreMethods : list, optional
        A list of methods to ignore in obtaining the full list of methods

    Notes
    -----
    A total of three sources are available for this function. They are:

        * 'OPEN_NTBKM, a compillation of data on organics
          as published in [1]_ as Open Notebook Melting Points; Averaged 
          (median) values were used when
          multiple points were available. For more information on this
          invaluable and excellent collection, see
          http://onswebservices.wikispaces.com/meltingpoint.
        * 'CRC_ORG', a compillation of data on organics
          as published in [2]_.
        * 'CRC_INORG', a compillation of data on
          inorganic as published in [2]_.

    Examples
    --------
    >>> Tm(CASRN='7732-18-5')
    273.15

    '''
    def list_methods():
        methods = []
        if CASRN in _Tm_ON.index:
            methods.append(OPEN_NTBKM)
        if CASRN in _CRC_inorganic and not np.isnan(_CRC_inorganic.at[CASRN, 'Tm']):
            methods.append(CRC_INORG)
        if CASRN in _CRC_organic and not np.isnan(_CRC_organic.at[CASRN, 'Tm']):
            methods.append(CRC_ORG)
        if IgnoreMethods:
            for Method in IgnoreMethods:
                if Method in methods:
                    methods.remove(Method)
        methods.append(NONE)
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]

    if Method == OPEN_NTBKM:
        return float(_Tm_ON.at[CASRN, 'Tm'])
    elif Method == CRC_INORG:
        return float(_CRC_inorganic.at[CASRN, 'Tm'])
    elif Method == CRC_ORG:
        return float(_CRC_organic.at[CASRN, 'Tm'])
    elif Method == NONE:
        return None
    else:
        raise Exception('Failure in in function')


### Enthalpy of Vaporization at T

@Hvap(ref="[5]_",
      types={'dZ': 'function(T)', 'Psat': 'function(T)'})
def Clapeyron(T, Tc, Pc, V, Psat):
    r"""
    Notes
    -----
    The enthalpy of vaporization (Hvap; in J/mol) is given by:
     
    .. math:: \Delta H_{vap} = RT \Delta Z \frac{\ln (P_c/Psat)}{(1-T_{r})}
    
    No original source is available for this equation.
    [1]_ claims this equation overpredicts enthalpy by several percent.
    Under Tr = 0.8, dZ = 1 is a reasonable assumption.
    This equation is most accurate at the normal boiling point.
    
    Internal units are bar.
    
    WARNING: It is possible that the adjustment for pressure may be incorrect
    
    Examples
    --------
    Problem from Perry's examples.
    
    >>> Clapeyron(T=294.0, Tc=466.0, Pc=5.55E6)
    26512.354585061985
    
    """
    Tr = T/Tc
    P = Psat(T)
    return R*T*Z(T, P, V.g(T, P))*log(Pc/P)/(1. - Tr)

@Hvap(ref="[5]_ [6]_")
def Pitzer(T, Tc, omega):
    r"""
    Notes
    -----
    
    .. math:: \frac{\Delta_{vap} H}{RT_c}=7.08(1-T_r)^{0.354}+10.95\omega(1-T_r)^{0.456}
    
    This equation is listed in [7]_, page 2-487 as method #2 for estimating
    Hvap. This cites [5]_.
    
    The recommended range is 0.6 to 1 Tr. Users should expect up to 5% error.
    T must be under Tc, or an exception is raised.
    
    The original article has been reviewed and found to have a set of tabulated
    values which could be used instead of the fit function to provide additional
    accuracy.
    
    Examples
    --------
    Example as in [7]_, p2-487; exp: 37.51 kJ/mol
    
    >>> Pitzer(452, 645.6, 0.35017)
    36696.736640106414
    
    """
    Tr = T/Tc
    return R*Tc * (7.08*(1. - Tr)**0.354 + 10.95*omega*(1. - Tr)**0.456)

@Hvap(ref="[8]_")
def SMK(T, Tc, omega):
    r"""
    Notes
    -----
    The enthalpy of vaporization (Hvap; in J/mol) is given by:
        
    .. math::
        \frac{\Delta H_{vap}} {RT_c} = 
        \left( \frac{\Delta H_{vap}} {RT_c} \right)^{(R1)} + \left(
        \frac{\omega - \omega^{(R1)}} {\omega^{(R2)} - \omega^{(R1)}} \right)
        \left[\left( \frac{\Delta H_{vap}} {RT_c} \right)^{(R2)} - \left(
        \frac{\Delta H_{vap}} {RT_c} \right)^{(R1)} \right]
        
        \left( \frac{\Delta H_{vap}} {RT_c} \right)^{(R1)}
        = 6.537 \tau^{1/3} - 2.467 \tau^{5/6} - 77.251 \tau^{1.208} +
        59.634 \tau + 36.009 \tau^2 - 14.606 \tau^3
        
        \tau = 1-T/T_c
    
    The original article has been reviewed and found to have coefficients with
    slightly more precision. Additionally, the form of the equation is slightly
    different, but numerically equivalent.

    The refence fluids are:
        
    :math:`\omega_0` = benzene = 0.212
    
    :math:`\omega_1` = carbazole = 0.461
    
    A sample problem in the article has been verified. The numerical result
    presented by the author requires high numerical accuracy to obtain.
    
    Examples
    --------
    Problem in [8]_:
    
    >>> SMK(553.15, 751.35, 0.302)
    39866.17647797959
    
    """
    omegaR1, omegaR2 = 0.212, 0.461
    A10 = 6.536924
    A20 = -2.466698
    A30 = -77.52141
    B10 = 59.63435
    B20 = 36.09887
    B30 = -14.60567

    A11 = -0.132584
    A21 = -28.21525
    A31 = -82.95820
    B11 = 99.00008
    B21 = 19.10458
    B31 = -2.795660

    tau = 1. - T/Tc
    L0 = A10*tau**(1/3.) + A20*tau**(5/6.) + A30*tau**(1-1/8. + 1/3.) + \
        B10*tau + B20*tau**2 + B30*tau**3

    L1 = A11*tau**(1/3.) + A21*tau**(5/6.0) + A31*tau**(1-1/8. + 1/3.) + \
        B11*tau + B21*tau**2 + B31*tau**3

    domega = (omega - omegaR1)/(omegaR2 - omegaR1)
    return R*Tc*(L0 + domega*L1)

@Hvap(ref="[9]_")
def MK(T, Tc, omega):
    r"""
    Notes
    -----
    The enthalpy of vaporization (Hvap; in J/mol) is given by:
    
    .. math::
        \Delta H_{vap} =  \Delta H_{vap}^{(0)} + \omega \Delta H_{vap}^{(1)} + \omega^2 \Delta H_{vap}^{(2)}
        
        \frac{\Delta H_{vap}^{(i)}}{RT_c} = b^{(j)} \tau^{1/3} + b_2^{(j)} \tau^{5/6} + b_3^{(j)} \tau^{1.2083} + b_4^{(j)}\tau + b_5^{(j)} \tau^2 + b_6^{(j)} \tau^3)
        
        \tau = 1-T/T_c
    
    The original article has been reviewed. A total of 18 coefficients are used:
    
    WARNING: The correlation has been implemented as described in the article,
    but its results seem different and with some error.
    Its results match with other functions however.
    
    Has poor behavior for low-temperature use.
    
    Examples
    --------
    Problem in article for SMK function.
    
    >>> f_mk = MK(751.35, 0.302)
    >>> f_mk
    Functor: MK(T, P=None)
     Tc: 751.35 K
     omega: 0.302
    
    >>> f_mk(553.15)
    38727.993546377205
    
    """
    bs = [[5.2804, 0.080022, 7.2543],
          [12.8650, 273.23, -346.45],
          [1.1710, 465.08, -610.48],
          [-13.1160, -638.51, 839.89],
          [0.4858, -145.12, 160.05],
          [-1.0880, 74.049, -50.711]]
    tau = 1. - T/Tc
    # TODO: Use numpy arrays
    H0 = (bs[0][0]*tau**(0.3333) + bs[1][0]*tau**(0.8333) + bs[2][0]*tau**(1.2083) +
    bs[3][0]*tau + bs[4][0]*tau**(2) + bs[5][0]*tau**(3))*R*Tc

    H1 = (bs[0][1]*tau**(0.3333) + bs[1][1]*tau**(0.8333) + bs[2][1]*tau**(1.2083) +
    bs[3][1]*tau + bs[4][1]*tau**(2) + bs[5][1]*tau**(3))*R*Tc

    H2 = (bs[0][2]*tau**(0.3333) + bs[1][2]*tau**(0.8333) + bs[2][2]*tau**(1.2083) +
    bs[3][2]*tau + bs[4][2]*tau**(2) + bs[5][2]*tau**(3))*R*Tc

    return H0 + omega*H1 + omega**2*H2

@Hvap(ref="[10]_")
def Velasco(T, Tc, omega):
    r"""
    Notes
    -----
    The enthalpy of vaporization (Hvap; in J/mol) is given by:
    
    .. math::
        \Delta_{vap} H = RT_c(7.2729 + 10.4962\omega + 0.6061\omega^2)(1-T_r)^{0.38}
    
    The original article has been reviewed. It is regressed from enthalpy of
    vaporization values at 0.7Tr, from 121 fluids in REFPROP 9.1.
    A value in the article was read to be similar, but slightly too low from
    that calculated here.
    
    Examples
    --------
    From graph, in [10]_ for perfluoro-n-heptane.
    
    >>> Velasco(333.2, 476.0, 0.5559)
    33299.41734936356
    
    """
    return (7.2729 + 10.4962*omega + 0.6061*omega**2)*(1-T/Tc)**0.38*R*Tc


### Enthalpy of Vaporization at Normal Boiling Point.

def Riedel(Tb, Tc, Pc):
    r'''
    Return the enthalpy of vaporization at the boiling point, using the
    Ridel [11]_ CSP method. Required information are critical temperature
    and pressure, and boiling point. Equation taken from [11]_ and [7]_.
    
    The enthalpy of vaporization (Hvap; in J/mol) is given by:
    
    .. math::
        \Delta_{vap} H=1.093 T_b R\frac{\ln P_c-1.013}{0.930-T_{br}}s
    
    Parameters
    ----------
    Tb : float
        Boiling temperature of fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    Pc : float
        Critical pressure of fluid [Pa]
        
    Returns
    -------
    Hvap : float
        Enthalpy of vaporization at the normal boiling point, [J/mol]
    
    Notes
    -----
    This equation has no example calculation in any source. The source has not
    been verified. It is equation 4-144 in Perry's. Perry's also claims that
    errors seldom surpass 5%.
    
    [5]_ is the source of example work here, showing a calculation at 0.0%
    error.
    
    Internal units of pressure are bar.
    
    Examples
    --------
    Pyridine, 0.0% err vs. exp: 35090 J/mol; from Poling [5]_.
    
    >>> Riedel(388.4, 620.0, 56.3E5)
    35089.78989646058
    
    '''
    Pc = Pc/1E5  # Pa to bar
    Tbr = Tb/Tc
    return 1.093*Tb*R*(log(Pc) - 1.013)/(0.93 - Tbr)

def Chen(Tb, Tc, Pc):
    r'''
    Return the enthalpy of vaporization using the Chen [12]_ correlation
    and a chemical's critical temperature, pressure and boiling point.
    
    The enthalpy of vaporization (Hvap; in J/mol) is given by:
        
    .. math::
        \Delta H_{vb} = RT_b \frac{3.978 T_r - 3.958 + 1.555 \ln P_c}{1.07 - T_r}
        
    Parameters
    ----------
    Tb : float
        Boiling temperature of the fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    Pc : float
        Critical pressure of fluid [Pa]
        
    Returns
    -------
    Hvap : float
        Enthalpy of vaporization, [J/mol]
    
    Notes
    -----
    The formulation presented in the original article is similar, but uses
    units of atm and calorie instead. The form in [5]_ has adjusted for this.
    A method for estimating enthalpy of vaporization at other conditions
    has also been developed, but the article is unclear on its implementation.
    Based on the Pitzer correlation.
    
    Internal units: bar and K
    
    Examples
    --------
    Same problem as in Perry's examples.
    
    >>> Chen(294.0, 466.0, 5.55E6)
    26705.893506174052
    
    '''
    Tbr = Tb/Tc
    Pc = Pc/1E5  # Pa to bar
    return R*Tb*(3.978*Tbr - 3.958 + 1.555*log(Pc))/(1.07 - Tbr)

def Liu(Tb, Tc, Pc):
    r'''
    Return the enthalpy of vaporization at the normal boiling point using
    the Liu [13]_ correlation, and a chemical's critical temperature, pressure
    and boiling point.

    The enthalpy of vaporization (Hvap; in J/mol) is given by:

    .. math::
        \Delta H_{vap} = RT_b \left[ \frac{T_b}{220}\right]^{0.0627} \frac{
        (1-T_{br})^{0.38} \ln(P_c/P_A)}{1-T_{br} + 0.38 T_{br} \ln T_{br}}

    Parameters
    ----------
    Tb : float
        Boiling temperature of the fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    Pc : float
        Critical pressure of fluid [Pa]

    Returns
    -------
    Hvap : float
        Enthalpy of vaporization, [J/mol]

    Notes
    -----
    This formulation can be adjusted for lower boiling points, due to the use
    of a rationalized pressure relationship. The formulation is taken from
    the original article.

    A correction for alcohols and organic acids based on carbon number,
    which only modifies the boiling point, is available but not implemented.

    No sample calculations are available in the article.

    Internal units: Pa and K

    Examples
    --------
    Same problem as in Perry's examples

    >>> Liu(294.0, 466.0, 5.55E6)
    26378.566319606754

    '''
    Tbr = Tb/Tc
    return R*Tb*(Tb/220.)**0.0627*(1. - Tbr)**0.38*log(Pc/101325.) \
        / (1 - Tbr + 0.38*Tbr*log(Tbr))

def Vetere(Tb, Tc, Pc, F=1):
    r'''
    Return the enthalpy of vaporization at the boiling point, using the
    Vetere [14]_ CSP method. Required information are critical temperature
    and pressure, and boiling point. Equation taken from [7]_.

    The enthalpy of vaporization (Hvap; in J/mol) is given by:

    .. math::
        \frac {\Delta H_{vap}}{RT_b} = \frac{\tau_b^{0.38}
        \left[ \ln P_c - 0.513 + \frac{0.5066}{P_cT_{br}^2}\right]}
        {\tau_b + F(1-\tau_b^{0.38})\ln T_{br}}

    Parameters
    ----------
    Tb : float
        Boiling temperature of fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    Pc : float
        Critical pressure of fluid [Pa]
    F : float, optional
        Constant for a fluid, [-]

    Returns
    -------
    Hvap : float
        Enthalpy of vaporization at the boiling point, [J/mol]

    Notes
    -----
    The equation cannot be found in the original source. It is believed that a
    second article is its source, or that DIPPR staff have altered the formulation.

    Internal units of pressure are bar.

    Examples
    --------
    Example as in [7]_, p2-487; exp: 25.73

    >>> Vetere(294.0, 466.0, 5.55E6)
    26363.430021286465

    '''
    Tbr = Tb/Tc
    taub = 1-Tb/Tc
    Pc = Pc/1E5
    term = taub**0.38*(log(Pc)-0.513 + 0.5066/Pc/Tbr**2) / (taub + F*(1-taub**0.38)*log(Tbr))
    return R*Tb*term


### Enthalpy of Vaporization at STP.


### Enthalpy of Vaporization adjusted for T
@Hvap
def Watson(T, Hvap_ref, T_ref, Tc, exponent=0.38):
    '''
    Adjusts enthalpy of vaporization of enthalpy for another temperature, for one temperature.
    '''
    Tr = T/Tc
    Trefr = T_ref/Tc
    H2 = Hvap_ref*((1-Tr)/(1-Trefr))**exponent
    return H2

@Hvap
def Alibakhshi(T, Tc, C):
    return (4.5*pi*N_A)**(1./3.)*4.2E-7*(Tc-6.) - R/2.*T*log(T) + C*T

@Hvap
def VDI_PPDS(T, Tc, A, B, C, D, E):
    tau = 1. - T/Tc
    return R*Tc*(A*tau**(1/3.) + B*tau**(2/3.) + C*tau + D*tau**2 + E*tau**6)

@TDependentHandleBuilder('Hvap')
def EnthalpyVaporization(handle, CAS, Tb, Tc, Pc, omega, similarity_variable, Psat, V):
    # if has_CoolProp and self.CASRN in coolprop_dict:
    #     methods.append(COOLPROP)
    #     self.CP_f = coolprop_fluids[self.CASRN]
    #     Tmins.append(self.CP_f.Tt); Tmaxs.append(self.CP_f.Tc)
    add_model = handle.add_model
    if CAS in _Perrys2_150:
        _, Tc, C1, C2, C3, C4, Tmin, Tmax = _Perrys2_150[CAS]
        data = (Tc, C1, C2, C3, C4)
        add_model(DIPPR_EQ106.from_args(data), Tmin, Tmax)
    if CAS in _VDI_PPDS_4:
        _,  MW, Tc, A, B, C, D, E = _VDI_PPDS_4[CAS]
        add_model(VDI_PPDS.from_args(data=(Tc, A, B, C, D, E)), 0, Tc)
    data = (Tb, Tc, Pc)
    if all(data):
        for f in (Riedel, Chen, Vetere, Liu):
            add_model(f(*data), 0, Tc)
    if all((Tc, Pc)):
        add_model(Clapeyron.from_args(data=(Tc, Pc, V, Psat)), 0, Tc)
    data = (Tc, omega)
    if all(data):
        for f in (MK, SMK, Velasco, Pitzer):
            add_model(f.from_args(data), 0, Tc)
    if CAS in _VDISaturationDict:
        Ts, Hvaps = VDI_tabular_data(CAS, 'Hvap')
        add_model(InterpolatedTDependentModel(Ts, Hvaps, Ts[0], Ts[-1]))
    if Tc:
        if CAS in _Alibakhshi_Cs:
            C = float(_Alibakhshi_Cs.at[CAS, 'C'])
            add_model(Alibakhshi.from_args(data=(Tc, C)), 0, Tc)
        if CAS in _CRCHvap and not np.isnan(_CRCHvap.at[CAS, 'HvapTb']):
            Tb = float(_CRCHvap.at[CAS, 'Tb'])
            Hvap = float(_CRCHvap.at[CAS, 'HvapTb'])
            data = dict(Hvap_ref=Hvap, T_ref=Tb, Tc=Tc, exponent=0.38)
            add_model(Watson.from_kwargs(data), 0, 10e6)
        if CAS in _CRCHvap and not np.isnan(_CRCHvap.at[CAS, 'Hvap298']):
            Hvap = float(_CRCHvap.at[CAS, 'Hvap298'])
            data = dict(Hvap_ref=Hvap, T_ref=298., Tc=Tc, exponent=0.38)
            add_model(Watson.from_kwargs(data), 0, 10e6)
        if CAS in _GharagheiziHvap.index:
            Hvap = float(_GharagheiziHvap.at[CAS, 'Hvap298'])
            data = dict(Hvap_ref=Hvap, T_ref=298., Tc=Tc, exponent=0.38)
            add_model(Watson.from_kwargs(data), 0, 10e6)


### Heat of Fusion


def Hfus(T=298.15, P=101325, MW=None, AvailableMethods=False, Method=None, CASRN=''):  # pragma: no cover
    '''This function handles the calculation of a chemical's enthalpy of fusion.
    Generally this, is used by the chemical class, as all parameters are passed.
    Calling the function directly works okay.

    Enthalpy of fusion is a weak function of pressure, and its effects are
    neglected.

    This API is considered experimental, and is expected to be removed in a
    future release in favor of a more complete object-oriented interface.

    '''
    def list_methods():
        methods = []
        if CASRN in _CRCHfus:
            methods.append('CRC, at melting point')
        methods.append('None')
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]
    # This is the calculate, given the method section
    if Method == 'CRC, at melting point':
        _Hfus = _CRCHfus.at[CASRN, 'Hfus']
    elif Method == 'None' or not MW:
        _Hfus = None
    else:
        raise Exception('Failure in in function')
    return _Hfus
#print Hfus(CASRN='75-07-0')
#['CRC, at melting point', 'None']


### Heat of Sublimation


def Hsub(T=298.15, P=101325, AvailableMethods=False, Method=None, CASRN=''):  # pragma: no cover
    '''This function handles the calculation of a chemical's enthalpy of sublimation.
    Generally this, is used by the chemical class, as all parameters are passed.


    This API is considered experimental, and is expected to be removed in a
    future release in favor of a more complete object-oriented interface.
    '''
    def list_methods():
        methods = []
#        if Hfus(T=T, P=P, MW=MW, CASRN=CASRN) and Hvap(T=T, P=P, MW=MW, CASRN=CASRN):
#            methods.append('Hfus + Hvap')
        if CASRN in _GharagheiziHsub:
            methods.append('Ghazerati Appendix, at 298K')
        methods.append('None')
        return methods
    if AvailableMethods:
        return list_methods()
    if not Method:
        Method = list_methods()[0]
    # This is the calculate, given the method section
#    if Method == 'Hfus + Hvap':
#        p1 = Hfus(T=T, P=P, MW=MW, CASRN=CASRN)
#        p2 = Hvap(T=T, P=P, MW=MW, CASRN=CASRN)
#        if p1 and p2:
#            _Hsub = p1 + p2
#        else:
#            _Hsub = None
    if Method == 'Ghazerati Appendix, at 298K':
        _Hsub = float(_GharagheiziHsub.at[CASRN, 'Hsub'])
    elif Method == 'None':
        return None
    else:
        raise Exception('Failure in in function')
    return _Hsub

