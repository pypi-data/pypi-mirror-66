# -*- coding: utf-8 -*-

__all__ = ('Chemical',)

import thermosteam as tmo
from flexsolve import IQ_interpolation
from .utils import copy_maybe, to_searchable_format
from .properties.identifiers import CAS_from_any, pubchem_db
from .properties.vapor_pressure import VaporPressure
from .properties.phase_change import Tb, Tm, Hfus, Hsub, EnthalpyVaporization
from .properties.critical import Tc, Pc, Vc
from .properties.acentric import omega, StielPolar
from .properties.triple import Tt, Pt
from .properties.volume import Volume
from .properties.heat_capacity import HeatCapacity
from .properties.reaction import Hf
from .properties.combustion import CombustionData
from .properties.elements import compute_similarity_variable, parse_simple_formula
from .properties.eos import GCEOS_DUMMY, PR
from .properties.viscosity import Viscosity
from .properties.thermal_conductivity import ThermalConductivity
from .properties.free_energy import \
    EnthalpyRefSolid, EnthalpyRefLiquid, EnthalpyRefGas, \
    EntropyRefSolid, EntropyRefLiquid, EntropyRefGas, \
    ExcessEnthalpyRefSolid, ExcessEnthalpyRefLiquid, ExcessEnthalpyRefGas, \
    ExcessEntropyRefSolid, ExcessEntropyRefLiquid, ExcessEntropyRefGas
from .base import PhaseProperty, PhaseTProperty, PhaseTPProperty, \
                  ThermoModelHandle, TDependentModelHandle, TPDependentModelHandle, \
                  display_asfunctor
from .base.units_of_measure import chemical_units_of_measure
from .properties.dipole import dipole_moment as dipole
from . import functional as fn 
from .properties.permittivity import Permittivity
from .properties.interface import SurfaceTension
from .equilibrium.unifac_data import \
    DDBST_UNIFAC_assignments, DDBST_MODIFIED_UNIFAC_assignments, DDBST_PSRK_assignments, \
    UNIFACGroupCounts, DortmundGroupCounts, PSRKGroupCounts
# from .solubility import SolubilityParameter
# from .safety import Tflash, Tautoignition, LFL, UFL, TWA, STEL, Ceiling, Skin, Carcinogen
# from .lennard_jones import Stockmayer, MolecularDiameter
# from .environment import GWP, ODP, logP
# from .refractivity import refractive_index
# from .electrochem import conductivity


# %% Filling missing properties

def fill_from_dict(chemical, dict, slots=None):
    if not slots: slots = chemical.get_missing_slots(slots)
    missing = []
    setfield = setattr
    for i in slots :
        if i in dict:
            setfield(chemical, i, dict[i])
        else:
            missing.append(i)
    return missing

def fill_from_obj(chemical, obj, slots=None):
    if not slots: slots = chemical.get_missing_slots(slots)
    missing = []
    setfield = setattr
    getfield = getattr
    for i in slots:
        field = getfield(obj, i)
        if field:
            setfield(chemical, i, field)
        else:
            missing.append(i)
    return missing

def fill(chemical, other, slots=None):
    fill = fill_from_dict if isinstance(other, dict) else fill_from_obj
    return fill(chemical, other, slots)

def get_chemical_data(chemical):
    getfield = getattr
    return {i:getfield(chemical, i) for i in chemical.__slots__}

def unpickle_chemical(chemical_data):
    cache = Chemical._cache
    CAS = chemical_data['_CAS']
    if CAS in cache:
        chemical = cache[CAS]
    else:
        chemical = object.__new__(Chemical)
        setfield = setattr
        for field, value in chemical_data.items():
            setfield(chemical, field, value)
    return chemical

# %% Representation
    
def chemical_identity(chemical, pretty=False):
    typeheader = f"{type(chemical).__name__}:"
    full_ID = f"{typeheader} {chemical.ID} (phase_ref={repr(chemical.phase_ref)})"
    phase = chemical.locked_state
    state = ' at ' + f"phase={repr(phase)}" if phase else ""
    return full_ID + state


# %% Initialize EOS
                         
def create_eos(eos, Tc, Pc, omega):
    try: return eos(T=298.15, P=101325., Tc=Tc, Pc=Pc, omega=omega)
    except: return GCEOS_DUMMY(T=298.15, P=101325.)


# %% Chemical fields

_names = ('_CAS', 'InChI', 'InChI_key',
         'common_name', 'iupac_name',
         'pubchemid', 'smiles', 'formula')

_groups = ('Dortmund', 'UNIFAC', 'PSRK')

_reactions = ('combustion',)

_thermo = ('S_excess', 'H_excess', 'mu', 'kappa', 'V', 'S', 'H', 'Cn',
           'Psat', 'Hvap', 'sigma', 'epsilon')
    
_phase_properties = ('kappa', 'V', 'Cn', 'mu')

_free_energies = ('S_excess', 'H_excess', 'S', 'H')

_liquid_only_properties = ('sigma', 'epsilon')

_equilibrium_properties = ('Psat', 'Hvap')

_data = ('MW', 'Tm', 'Tb', 'Tt', 'Tc', 'Pt', 'Pc', 'Vc', 'Zc',
         'Hf', 'LHV', 'HHV', 'Hfus', 'Hsub', 'omega', 'dipole',
         'StielPolar', 'similarity_variable', 'iscyclic_aliphatic')

_checked_slots = ('phase_ref', 'eos', 'eos_1atm',
                  *_names[1:], *_groups, *_reactions,
                  *_thermo, *_data)

_chemical_fields = {'\n[Names]  ': _names,
                    '\n[Groups] ': _groups,
                    '\n[Thermo] ': _thermo,
                    '\n[Data]   ': _data}


# %% Chemical

class Chemical:
    """
    Creates a Chemical object which contains constant chemical properties,
    as well as thermodynamic and transport properties as a function of 
    temperature and pressure.
    
    Parameters
    ----------
    ID : str
        One of the following [-]:
            * Name, in IUPAC form or common form or a synonym registered in PubChem
            * InChI name, prefixed by 'InChI=1S/' or 'InChI=1/'
            * InChI key, prefixed by 'InChIKey='
            * PubChem CID, prefixed by 'PubChem='
            * SMILES (prefix with 'SMILES=' to ensure smiles parsing)
            * CAS number
    
    Examples
    --------
    Chemical objects contain pure component properties:
    
    >>> import thermosteam as tmo
    >>> # Initialize with an identifier
    >>> # (e.g. by name, CAS, InChI...)
    >>> Water = tmo.Chemical('Water') 
    >>> Water.show()
    Chemical: Water (phase_ref='l')
    [Names]  CAS: 7732-18-5
             InChI: H2O/h1H2
             InChI_key: XLYOFNOQVPJJNP-U...
             common_name: water
             iupac_name: oxidane
             pubchemid: 962
             smiles: O
             formula: H2O
    [Groups] Dortmund: <1H2O>
             UNIFAC: <1H2O>
             PSRK: <1H2O>
    [Thermo] S_excess(phase, T, P) -> J/mol
             H_excess(phase, T, P) -> J/mol
             mu(phase, T, P) -> Pa*s
             kappa(phase, T, P) -> W/m/K
             V(phase, T, P) -> m^3/mol
             S(phase, T, P) -> J/mol
             H(phase, T, P=None) -> J/mol
             Cn(phase, T, P=None) -> J/mol/K
             Psat(T, P=None) -> Pa
             Hvap(T, P=None) -> J/mol
             sigma(T, P=None) -> N/m
             epsilon(T, P=None)
    [Data]   MW: 18.015 g/mol
             Tm: 273.15 K
             Tb: 373.12 K
             Tt: 273.15 K
             Tc: 647.14 K
             Pt: None
             Pc: 2.2048e+07 Pa
             Vc: 5.6e-05 m^3/mol
             Zc: 0.22947
             Hf: -2.4182e+05 J/mol
             LHV: 0
             HHV: 0
             Hfus: 6010 J/mol
             Hsub: None
             omega: 0.344
             dipole: 1.85 Debye
             StielPolar: None
             similarity_variable: 0.16653
             iscyclic_aliphatic: 0

    All fields shown are accessible:
    
    >>> Water.CAS
    '7732-18-5'

    Functional group identifiers (e.g. `Dortmund`, `UNIFAC`, `PSRK`) allow for the estimation of activity coefficients through group contribution methods. In other words, these attributes define the functional groups for thermodynamic equilibrium calculations:
        
    >>> Water.Dortmund
    <DortmundGroupCounts: 1H2O>
    
    Temperature (in Kelvin) and pressure (in Pascal) dependent properties can be computed:
        
    >>> # Vapor pressure (Pa)
    >>> Water.Psat(T=373.15)
    101284.55179999319
    >>> # Surface tension (N/m)
    >>> Water.sigma(T=298.15)
    0.07205503890847455
    >>> # Molar volume (m^3/mol)
    >>> Water.V(phase='l', T=298.15, P=101325)
    1.802828527066713e-05
    
    Note that the reference state of all chemicals is 25 degC and 1 atm:
    
    >>> (Water.T_ref, Water.P_ref)
    (298.15, 101325.0)
    >>> # Enthalpy at reference conditions (J/mol; without excess energies)
    >>> Water.H(T=298.15, phase='l')
    0.0
    
    Constant pure component properties are also available:
    
    >>> # Molecular weight (g/mol)
    >>> Water.MW
    18.01528
    >>> # Boiling point (K)
    >>> Water.Tb
    373.124
    
    Temperature dependent properties are managed by model handles:
    
    >>> Water.Psat.show()
    TDependentModelHandle(T, P=None) -> Psat [Pa]
    [0] Wagner_McGraw
    [1] Antoine
    [2] DIPPR_EQ101
    [3] Wagner
    [4] Boiling_Critical_Relation
    [5] Lee_Kesler
    [6] Ambrose_Walton
    [7] Sanjari
    [8] Edalat

    Phase dependent properties have attributes with model handles for each phase:

    >>> Water.V
    <PhaseTPProperty(phase, T, P) -> V [m^3/mol]>
    >>> (Water.V.l, Water.V.g)
    (<TPDependentModelHandle(T, P) -> V.l [m^3/mol]>, <TPDependentModelHandle(T, P) -> V.g [m^3/mol]>)

    A model handle contains a series of models applicable to a certain domain:
    
    >>> Water.Psat[0].show()
    TDependentModel: Wagner_McGraw
     evaluate: Wagner_McGraw(T, P=None) -> Psat [Pa]
     Tmin: 275 K
     Tmax: 647.35 K

    When called, the model handle searches through each model until it finds one with an applicable domain. If none are applicable, a value error is raised:
        
    >>> Water.Psat(373.15)
    101284.55179999319
    >>> # Water.Psat(1000.0) ->
    >>> # ValueError: Water has no valid saturated vapor pressure model at T=1000.00 K
    
    Model handles as well as the models themselves have tabulation and plotting methods to help visualize how properties depend on temperature and pressure.
    
    >>> # Water.Psat.plot_vs_T([Water.Tm, Water.Tb], 'degC', 'atm', label="Water")
    
    .. figure:: ./images/Water_Psat_vs_T.png
    
    >>> # Plot all models
    >>> # Water.Psat.plot_models_vs_T([Water.Tm, Water.Tb], 'degC', 'atm')
    
    .. figure:: ./images/Water_all_models_Psat_vs_T.png
    
    Each model may contain either a function or a functor (a function with stored data) to compute the property:
        
    >>> functor = Water.Psat[0].evaluate
    >>> functor.show()
    Functor: Wagner_McGraw(T, P=None) -> Psat [Pa]
     Tc: 647.35 K
     Pc: 2.2122e+07 Pa
     a: -7.7645
     b: 1.4584
     c: -2.7758
     d: -1.233
    
    .. Note::
       All chemical property functors are available in the thermosteam.properties subpackage. You can also use help(<functor>) for further information on the math and equations used in the functor.
    
    A new model can be added easily to a model handle through the `add_model` method, for example:
        
    >>> # Set top_priority=True to place model in postion [0]
    >>> @Water.Psat.add_model(Tmin=273.20, Tmax=473.20, top_priority=True)
    ... def User_antoine_model(T):
    ...     return 10.0**(10.116 -  1687.537 / (T - 42.98))
    >>> Water.Psat.show()
    TDependentModelHandle(T, P=None) -> Psat [Pa]
    [0] User_antoine_model
    [1] Wagner_McGraw
    [2] Antoine
    [3] DIPPR_EQ101
    [4] Wagner
    [5] Boiling_Critical_Relation
    [6] Lee_Kesler
    [7] Ambrose_Walton
    [8] Sanjari
    [9] Edalat

    The `add_model` method is a high level interface that even lets you create a constant model:
        
    >>> value = Water.V.l.add_model(1.687e-05)
    ... # Model is appended at the end by default
    >>> added_model = Water.V.l[-1]
    >>> added_model.show()
    ConstantThermoModel: Constant
     value (V.l): 1.687e-05 m^3/mol
     Tmin: 0 K
     Tmax: inf K
     Pmin: 0 Pa
     Pmax: inf Pa

    .. Note::
       Because no bounds were given, the model assumes it is valid across all temperatures and pressures.

    Manage the model order with the `set_model_priority` and `move_up_model_priority` methods:
    
    >>> # Note: In this case, we pass the model name, but its
    >>> # also possible to pass the current index, or the model itself.
    >>> Water.Psat.move_up_model_priority('Wagner_McGraw')
    >>> Water.Psat.show()
    TDependentModelHandle(T, P=None) -> Psat [Pa]
    [0] Wagner_McGraw
    [1] Antoine
    [2] DIPPR_EQ101
    [3] Wagner
    [4] Boiling_Critical_Relation
    [5] Lee_Kesler
    [6] Ambrose_Walton
    [7] Sanjari
    [8] Edalat
    [9] User_antoine_model
    
    >>> Water.Psat.set_model_priority('Antoine')
    >>> Water.Psat.show()
    TDependentModelHandle(T, P=None) -> Psat [Pa]
    [0] Antoine
    [1] Wagner_McGraw
    [2] DIPPR_EQ101
    [3] Wagner
    [4] Boiling_Critical_Relation
    [5] Lee_Kesler
    [6] Ambrose_Walton
    [7] Sanjari
    [8] Edalat
    [9] User_antoine_model
    
    The default priority is `0` (or top priority), but you can choose any priority:
    
    >>> Water.Psat.set_model_priority('Antoine', 1)
    >>> Water.Psat.show()
    TDependentModelHandle(T, P=None) -> Psat [Pa]
    [0] Wagner_McGraw
    [1] Antoine
    [2] DIPPR_EQ101
    [3] Wagner
    [4] Boiling_Critical_Relation
    [5] Lee_Kesler
    [6] Ambrose_Walton
    [7] Sanjari
    [8] Edalat
    [9] User_antoine_model
    
    .. note::
    
        All models are stored as a `deque <https://docs.python.org/3.8/library/collections.html#collections.deque>`_ in the `models` attribute (e.g. Water.Psat.models).
    
    Attributes
    ----------
    InChI : str
        IUPAC International Chemical Identifier.
    InChI_key : str
        IUPAC International Chemical Identifier shorthand.
    common_name : str
        Common name identifier.
    iupac_name : str
        Standard name as defined by IUPAC.
    pubchemid : str
        Chemical identifier as defined by PubMed.
    smiles : str
        Chemical SMILES formula.
    Dortmund : DortmundGroupCounts
        Dictionary-like object with functional group numerical
        identifiers as keys and the number of groups as values.
    UNIFAC : UNIFACGroupCounts
        Dictionary-like object with functional group numerical
        identifiers as keys and the number of groups as values.
    PSRK : PSRKGroupCounts
        Dictionary-like object with functional group numerical
        identifiers as keys and the number of groups as values.
    mu(phase, T, P) : 
        Dynamic viscosity [Pa*s].
    kappa(phase, T, P): 
        Thermal conductivity [W/m/K].
    V(phase, T, P): 
        Molar volume [m^3/mol].
    Cn(phase, T) : 
        Molar heat capacity [J/mol/K].
    Psat(T) : 
        Vapor pressure [Pa].
    Hvap(T) : 
        Heat of vaporization [J/mol]
    sigma(T) : 
        Surface tension [N/m].
    epsilon : 
        Relative permitivity [-]
    S(phase, T, P) : 
        Entropy [J/mol].
    H(phase, T) : 
        Enthalpy [J/mol].
    S_excess(T, P) : 
        Excess entropy [J/mol].
    H_excess(T, P) : 
        Excess enthalpy [J/mol].
    phase_ref : {'s', 'l', 'g'}
        Phase at 298 K and 101325 Pa.
    MW : float
        Molecular weight [g/mol].
    Tm : float
        Normal melting temperature [K].
    Tb : float
        Normal boiling temperature [K].
    Tt : float
        Triple point temperature [K].
    Tc : float
        Critical point temperature [K].
    Pt : float
        Triple point pressure [Pa].
    Pc : float
        Critical point pressure [Pa].
    Vc : float
        Critical point molar volume [m^3/mol].
    Zc : float
        Critical point molar volume [m^3/mol].
    Hf : float
        Heat of formation [J/mol].
    LHV : float
        Lower heating value [J/mol].
    HHV : float
        Higher heating value [J/mol].
    Hfus : float
        Heat of fusion [J/mol].
    Hsub : float
        Heat of sublimation [J/mol].
    omega :
        Accentric factor [-].
    dipole : float
        Dipole moment [Debye].
    StielPolar : float
        Stiel Polar factor [-].
    similarity_variable : float
        Similarity variable [-].
    iscyclic_aliphatic : bool
        Whether the chemical is cyclic-aliphatic.
    eos : object
        Instance for solving equations of state.
    eos_1atm : object
        Instance for solving equations of state at 1 atm.
    
    """
    __slots__ = ('_ID', '_locked_state', 
                 'phase_ref', 'eos', 'eos_1atm',
                 *_names, *_groups, *_reactions,
                 *_thermo, *_data)
    
    #: [float] Reference temperature in Kelvin
    T_ref = 298.15
    #: [float] Reference pressure in Pascal
    P_ref = 101325.
    #: [float] Reference enthalpy in J/mol
    H_ref = 0.
    #: [float] Reference entropy in J/mol
    S_ref = 0.
    
    _cache = {}
    
    def __new__(cls, ID, *, search_ID=None, eos=PR, phase_ref=None):
        cache = cls._cache
        search_ID = search_ID or ID
        try:
            CAS = CAS_from_any(search_ID)
        except Exception as Error:
            search_ID = to_searchable_format(search_ID)
            try: CAS = CAS_from_any(search_ID)
            except: raise Error
            
        if CAS in cache:
            self = cache[CAS]
            if ID != self.ID:
                if ID in cache:
                    self = cache[ID]
                else:
                    cache[ID] = self = self.copy(ID=ID, CAS=self.CAS)                    
        else:
            self = super().__new__(cls)
            self._ID = ID
            self.load_chemical(CAS, eos, phase_ref)
            cache[CAS] = self
        return self

    def load_chemical(self, CAS, eos=PR, phase_ref=None):
        """
        Load all chemical properties.

        Parameters
        ----------
        CAS : str
            CAS number of chemical to load.
        eos : optional
            Equation of state. The default is Peng Robinson.
        phase_ref : str, optional
            Phase reference. Defaults to the phase at 298.15 K and 101325 Pa.

        """
        info = pubchem_db.search_CAS(CAS)
        self._locked_state = None
        self._init_names(CAS, info.smiles, info.InChI, info.InChI_key, 
                         info.pubchemid, info.iupac_name, info.common_name,
                         info.formula)
        self._init_groups(info.InChI_key)
        if CAS == '56-81-5': # TODO: Make this part of data
            self.Dortmund = DortmundGroupCounts({2: 2, 3: 1, 14: 2, 81: 1})
        self._init_data(CAS, self.get_atoms(), info.MW)
        self._init_eos(eos, self.Tc, self.Pc, self.omega)
        has_hydroxyl = False
        for dct in (self.Dortmund, self.UNIFAC, self.PSRK):
            for n in (14, 15, 16, 81):
                if n in dct:
                   has_hydroxyl = True
                   break
            if has_hydroxyl: break
        self._init_properties(CAS, self.MW, self.Tm, self.Tb, self.Tc,
                              self.Pc, self.Zc, self.Vc, self.Hfus,
                              self.omega, self.dipole, self.similarity_variable,
                              self.iscyclic_aliphatic, self.eos, has_hydroxyl)
        self._init_energies(self.Cn, self.Hvap, self.Psat, self.Hfus,
                            self.Tm, self.Tb, self.eos, self.eos_1atm,
                            phase_ref)
        
    def get_key_property_names(self):
        """Return the attribute names of key properties required to model a process."""
        if not self.locked_state and self.phase_ref != 's':
            return ('V', 'S', 'H', 'Cn', 'Psat', 'Tb')
        else:
            return ('V', 'S', 'H', 'Cn',)
        
    def get_combustion_reaction(self, chemicals):
        """Return a Reaction object defining the combustion of this chemical."""
        ID = self.ID
        combustion = self.combustion.copy()
        combustion[ID] = -1
        return tmo.reaction.Reaction(combustion, ID, 1.0, chemicals)
        
    def load_combustion_data(self, method="Stoichiometry"):
        """Load combustion data (LHV, HHV, and combution attributes)
        based on the molecular formula and the heat of formation."""
        CD = CombustionData.from_chemical_data(self.get_atoms(), self.CAS,
                                               self.MW, self.Hf, method)
        self.LHV = CD.LHV
        self.HHV = CD.HHV
        self.combustion = CD.stoichiometry

    def __reduce__(self):
        return unpickle_chemical, (get_chemical_data(self),)

    def __setattr__(self, name, value):
        isa = isinstance
        if isa(value, ThermoModelHandle):
            value.chemical = self
        elif isa(value, PhaseProperty):
            for phase in (value.s, value.l, value.g):
                if isa(phase, ThermoModelHandle): phase.chemical = self
        super().__setattr__(name, value)

    @property
    def ID(self):
        """[str] Identification of chemical."""
        return self._ID
    @property
    def CAS(self):
        """[str] CAS number of chemical."""
        return self._CAS
    
    def get_atoms(self):
        """dict[str: int] Atom-count pairs."""
        return parse_simple_formula(self.formula)

    def Tsat(self, P, Tguess=None, Tmin=None, Tmax=None):
        """Return the saturated temperature (in Kelvin) given the pressure (in Pascal)."""
        Tb = self.Tb
        Psat = self.Psat
        if not Tmin: Tmin = Psat.Tmin 
        if not Tmax: Tmax = Psat.Tmax
        if Tb:
            if P == 101325:
                return Tb
            elif not Tguess:
                Tguess = Tb * (P / 101325)
        elif not Tguess:
            Tguess = (Tmin + Tmax)/2
        return IQ_interpolation(Psat, Tmin, Tmax, 0, Psat(Tmax-1e-4), Tguess, P, 1e-2, 1e-1)

    def copy(self, ID, CAS=None):
        """Return a copy of the chemical with a new ID."""
        cache = self._cache
        CAS = CAS or ID
        new = super().__new__(self.__class__)
        getfield = getattr
        setfield = setattr
        for field in self.__slots__: 
            value = getfield(self, field)
            setfield(new, field, copy_maybe(value))
        new._ID = ID
        new._CAS = CAS
        new._locked_state = new._locked_state
        new._init_energies(new.Cn, new.Hvap, new.Psat, new.Hfus, new.Tm,
                           new.Tb, new.eos, new.eos_1atm, new.phase_ref,
                           new._locked_state)
        cache[CAS] = new
        return new
    __copy__ = copy
    
    def _init_names(self, CAS, smiles, InChI, InChI_key,
                    pubchemid, iupac_name, common_name, formula):
        self._CAS = CAS
        self.smiles = smiles
        self.InChI = InChI
        self.InChI_key = InChI_key
        self.pubchemid = pubchemid
        self.iupac_name = iupac_name
        self.common_name = common_name
        self.formula = formula
        
    def _init_groups(self, InChI_key):
        if InChI_key in DDBST_UNIFAC_assignments:
            self.UNIFAC = DDBST_UNIFAC_assignments[InChI_key]
        else:
            self.UNIFAC = UNIFACGroupCounts()
        if InChI_key in DDBST_MODIFIED_UNIFAC_assignments:
            self.Dortmund = DDBST_MODIFIED_UNIFAC_assignments[InChI_key]
        else:
            self.Dortmund = DortmundGroupCounts()
        if InChI_key in DDBST_PSRK_assignments:
            self.PSRK = DDBST_PSRK_assignments[InChI_key]
        else:
            self.PSRK = PSRKGroupCounts()

    def _init_data(self, CAS, atoms, MW):
        self.MW = MW
        self.Tm = Tm(CAS)
        self.Tb = Tb(CAS)

        # Critical Point
        self.Tc = Tc(CAS)
        self.Pc = Pc(CAS)
        self.Vc = Vc(CAS)
        self.omega = omega(CAS)
        self.Zc = fn.Z(self.Tc, self.Pc, self.Vc) if all((self.Tc, self.Pc, self.Vc)) else None

        # Triple point
        self.Pt = Pt(CAS)
        self.Tt = Tt(CAS)

        # Energy
        self.Hfus = Hfus(CASRN=CAS, MW=MW)
        self.Hsub = Hsub(CASRN=CAS)

        # Chemistry
        self.Hf = Hf(CAS) or None
        try:
            CD = CombustionData.from_chemical_data(atoms, self.CAS, MW, self.Hf)
        except:
            self.LHV = self.HHV = self.combustion = None
        else:
            self.LHV = CD.LHV
            self.HHV = CD.HHV
            self.combustion = CD.stoichiometry
        
        # Critical Point
        self.StielPolar = StielPolar(CAS, Tc, Pc, omega)
        
        # Other
        self.dipole = dipole(CAS)
        self.similarity_variable = compute_similarity_variable(atoms, MW)
        self.iscyclic_aliphatic = False

    def _init_eos(self, eos, Tc, Pc, omega):
        self.eos = create_eos(eos, Tc, Pc, omega)
        self.eos_1atm = self.eos.to_TP(298.15, 101325)

    def _init_properties(self, CAS, MW, Tm, Tb, Tc, Pc, Zc, Vc, Hfus, omega,
                         dipole, similarity_variable, iscyclic_aliphatic, eos,
                         has_hydroxyl):
        # Vapor pressure
        self.Psat = Psat = VaporPressure((CAS, Tb, Tc, Pc, omega))
        
        # Volume
        sdata = (CAS,)
        ldata = (CAS, MW, Tb, Tc, Pc, Vc, Zc, omega, Psat, eos, dipole, has_hydroxyl)
        gdata = (CAS, Tc, Pc, omega, eos)
        self.V = V = Volume(sdata, ldata, gdata)
        
        # Heat capacity
        Cn = PhaseTProperty('Cn')
        sdata = (CAS, similarity_variable, MW)
        ldata = (CAS, Tb, Tc, omega, MW, similarity_variable, Cn)
        gdata = (CAS, MW, similarity_variable, iscyclic_aliphatic)
        self.Cn = Cn = HeatCapacity(sdata, ldata, gdata, Cn)
        
        # Heat of vaporization
        data = (CAS, Tb, Tc, Pc, omega, similarity_variable, Psat, V)
        self.Hvap = Hvap = EnthalpyVaporization(data)
        
        # Viscosity
        ldata = (CAS, MW, Tm, Tc, Pc, Vc, omega, Psat, V.l)
        gdata = (CAS, MW, Tc, Pc, Zc, dipole)
        self.mu = mu = Viscosity(None, ldata, gdata)
        
        # Conductivity
        ldata = (CAS, MW, Tm, Tb, Tc, Pc, omega, Hfus)
        gdata = (CAS, MW, Tb, Tc, Pc, Vc, Zc, omega, dipole, V.g, Cn.g, mu.g)
        self.kappa = ThermalConductivity(None, ldata, gdata)
        
        # Surface tension
        if Tb:
            try:    Hvap_Tb = Hvap(Tb)
            except: Hvap_Tb = None
            try:    Cnl_Tb = Cn.l(Tb)
            except: Cnl_Tb = None
            try:    rhol = 1/V.l(Tb, 101325.) * MW
            except: rhol = None
        else:
            Hvap_Tb = Cnl_Tb = rhol = None
        data = (CAS, MW, Tb, Tc, Pc, Vc, Zc,
                omega, StielPolar, Hvap_Tb, rhol, Cnl_Tb)
        self.sigma = SurfaceTension(data)
        
        # Other
        self.epsilon = Permittivity((CAS, V.l,))
        # self.delta = SolubilityParameter(self)
        # self.molecular_diameter = MolecularDiameter(self)

    def _init_energies(self, Cn, Hvap, Psat, Hfus, Tm, Tb, eos, eos_1atm,
                       phase_ref=None, single_phase=False):        
        # Reference
        P_ref = self.P_ref
        T_ref = self.T_ref
        H_ref = self.H_ref
        S_ref = self.S_ref
        Sfus = Hfus / Tm if Hfus and Tm else None
        
        if isinstance(Cn, PhaseProperty):
            Cn_s = Cn.s
            Cn_l = Cn.l
            Cn_g = Cn.g
            has_Cns = bool(Cn_s)
            has_Cnl = bool(Cn_l)
            has_Cng = bool(Cn_g)
        elif Cn and single_phase:
            has_Cns = single_phase == 's'
            has_Cnl = single_phase == 'l'
            has_Cng = single_phase == 'g'
            Cn_s = Cn_l = Cn_g = Cn
        else:
            has_Cns = has_Cnl = has_Cng = False
        
        if any((has_Cns, has_Cnl, has_Cng)):
            if phase_ref:
                self.phase_ref = phase_ref
            else:
                if Tm and T_ref <= Tm:
                    self.phase_ref = phase_ref = 's'
                elif Tb and T_ref >= Tb:
                    self.phase_ref = phase_ref = 'g'
                else:
                    self.phase_ref = phase_ref = 'l'

            if Hvap:
                Hvap_Tb = Hvap(Tb) if Tb else None
                Svap_Tb = Hvap_Tb / Tb if Tb else None
            else:
                Hvap_Tb = Svap_Tb = None
            
            # Enthalpy and entropy integrals
            if phase_ref != 'l' and has_Cnl and (Tm and Tb):
                H_int_Tm_to_Tb_l = Cn_l.integrate_by_T(Tm, Tb)
                S_int_Tm_to_Tb_l = Cn_l.integrate_by_T_over_T(Tm, Tb)
            else:
                H_int_Tm_to_Tb_l = S_int_Tm_to_Tb_l = None
            if phase_ref == 's' and has_Cns and Tm:
                H_int_T_ref_to_Tm_s = Cn_s.integrate_by_T(T_ref, Tm)
                S_int_T_ref_to_Tm_s = Cn_s.integrate_by_T_over_T(T_ref, Tm)
            else:
                H_int_T_ref_to_Tm_s = S_int_T_ref_to_Tm_s = None
            if phase_ref == 'g' and has_Cng and Tb:
                H_int_Tb_to_T_ref_g = Cn_g.integrate_by_T(Tb, T_ref)
                S_int_Tb_to_T_ref_g = Cn_g.integrate_by_T_over_T(Tb, T_ref)
            else:
                H_int_Tb_to_T_ref_g = S_int_Tb_to_T_ref_g = None
            if phase_ref == 'l':
                if has_Cnl:
                    if Tb:
                        H_int_T_ref_to_Tb_l = Cn_l.integrate_by_T(T_ref, Tb)
                        S_int_T_ref_to_Tb_l = Cn_l.integrate_by_T_over_T(T_ref, Tb)
                    else:
                        H_int_T_ref_to_Tb_l = S_int_T_ref_to_Tb_l = None
                    if Tm:
                        H_int_Tm_to_T_ref_l = Cn_l.integrate_by_T(Tm, T_ref)
                        S_int_Tm_to_T_ref_l = Cn_l.integrate_by_T_over_T(Tm, T_ref)
                    else:
                        H_int_Tm_to_T_ref_l = S_int_Tm_to_T_ref_l = None
    
            # Excess data
            if isinstance(eos, GCEOS_DUMMY):
                H_dep_ref_g = S_dep_ref_g = H_dep_ref_l = S_dep_ref_l = \
                H_dep_T_ref_Pb = S_dep_T_ref_Pb = H_dep_Tb_Pb_g = H_dep_Tb_P_ref_g = \
                S_dep_Tb_P_ref_g = S_dep_Tb_Pb_g = 0
            else:
                if phase_ref == 'g':
                    eos_phase_ref = eos.to_TP(T_ref, P_ref)
                    H_dep_ref_g = eos_phase_ref.H_dep_g
                    S_dep_ref_g = eos_phase_ref.S_dep_g
                elif phase_ref == 'l':
                    eos_phase_ref = eos.to_TP(T_ref, P_ref)
                    H_dep_ref_l = eos_phase_ref.H_dep_l
                    S_dep_ref_l = eos_phase_ref.S_dep_l
                    eos_T_ref_Pb = eos.to_TP(T_ref, 101325)
                    H_dep_T_ref_Pb = eos_T_ref_Pb.H_dep_l
                    S_dep_T_ref_Pb = eos_T_ref_Pb.S_dep_l
                if Tb:
                    eos_Tb = eos.to_TP(Tb, 101325)
                    eos_Tb_P_ref = eos.to_TP(Tb, P_ref)
                    H_dep_Tb_Pb_g = eos_Tb.H_dep_g
                    H_dep_Tb_P_ref_g = eos_Tb_P_ref.H_dep_g
                    S_dep_Tb_P_ref_g = eos_Tb_P_ref.S_dep_g
                    S_dep_Tb_Pb_g = eos_Tb.S_dep_g
                else:
                    S_dep_Tb_Pb_g = S_dep_Tb_P_ref_g = H_dep_Tb_P_ref_g = \
                    H_dep_Tb_Pb_g = 0.
            
            # Enthalpy and Entropy
            if phase_ref == 's':
                sdata = (Cn_s, T_ref, H_ref)
                ldata = (Cn_l, H_int_T_ref_to_Tm_s, Hfus, Tm, H_ref)
                gdata = (Cn_g, H_int_T_ref_to_Tm_s, Hfus, H_int_Tm_to_Tb_l, Hvap_Tb, Tb, H_ref)
                self.H = EnthalpyRefSolid(sdata, ldata, gdata)
                sdata = (Cn_s, T_ref, S_ref)
                ldata = (Cn_l, S_int_T_ref_to_Tm_s, Sfus, Tm, S_ref)
                gdata = (Cn_g, S_int_T_ref_to_Tm_s, Sfus, S_int_Tm_to_Tb_l, Svap_Tb, Tb, P_ref, S_ref)
                self.S = EntropyRefSolid(sdata, ldata, gdata)
            elif phase_ref == 'l':
                sdata = (Cn_s, H_int_Tm_to_T_ref_l, Hfus, Tm, H_ref)
                ldata = (Cn_l, T_ref, H_ref)
                gdata = (Cn_g, H_int_T_ref_to_Tb_l, Hvap_Tb, T_ref, H_ref)
                self.H = EnthalpyRefLiquid(sdata, ldata, gdata)
                sdata = (Cn_s, S_int_Tm_to_T_ref_l, Sfus, Tm, S_ref)
                ldata = (Cn_l, T_ref, S_ref)
                gdata = (Cn_g, S_int_T_ref_to_Tb_l, Svap_Tb, T_ref, P_ref, S_ref)
                self.S = EntropyRefLiquid(sdata, ldata, gdata)
            elif phase_ref == 'g':
                sdata = (Cn_s, H_int_Tb_to_T_ref_g, Hvap_Tb, H_int_Tm_to_Tb_l, Hfus, Tm, H_ref)
                ldata = (Cn_l, H_int_Tb_to_T_ref_g, Hvap_Tb, Tb, H_ref)
                gdata = (Cn_g, T_ref, H_ref)
                self.H = EnthalpyRefGas(sdata, ldata, gdata)
                sdata = (Cn_s, S_int_Tb_to_T_ref_g, Svap_Tb, S_int_Tm_to_Tb_l, Sfus, Tm, S_ref)
                ldata = (Cn_l, S_int_Tb_to_T_ref_g, Svap_Tb, Tb, S_ref)
                gdata = (Cn_g, T_ref, P_ref, S_ref)
                self.S = EntropyRefGas(sdata, ldata, gdata)
            
            # Excess energies
            if phase_ref == 's':
                self.H_excess = ExcessEnthalpyRefSolid((), (), ())
                self.S_excess = ExcessEntropyRefSolid((), (), ())
            elif phase_ref == 'l':
                gdata = (eos, H_dep_T_ref_Pb, H_dep_ref_l, H_dep_Tb_Pb_g)
                self.H_excess = ExcessEnthalpyRefLiquid((), (), gdata)
                gdata = (eos, S_dep_T_ref_Pb, S_dep_ref_l, S_dep_Tb_Pb_g)
                self.S_excess = ExcessEntropyRefLiquid((), (), gdata)
            elif phase_ref == 'g':
                ldata = (eos, H_dep_Tb_Pb_g, H_dep_Tb_P_ref_g, eos_1atm)
                gdata = (eos, H_dep_ref_g)
                self.H_excess = ExcessEnthalpyRefGas((), ldata, gdata)
                ldata = (eos, S_dep_Tb_Pb_g, S_dep_Tb_P_ref_g, eos_1atm)
                gdata = (eos, S_dep_ref_g)
                self.S_excess = ExcessEntropyRefGas((), ldata, gdata)
                
            if single_phase:
                getfield = getattr
                self.H = getfield(self.H, single_phase)
                self.S = getfield(self.S, single_phase)
                self.H_excess = getfield(self.H_excess, single_phase)
                self.S_excess = getfield(self.S_excess, single_phase)
        else:
            self.H = self.S = self.S_excess = self.H_excess = None

    def default(self, slots=None):
        """
        Default all `slots` with the chemical properties of water. If no
        `slots` given, all essential chemical properties that are missing
        are defaulted. `slots` which are still missing are returned as set.
        
        Parameters
        ----------
        slots : Iterable[str], optional
            Names of chemical properties to default.
        
        Returns
        -------
        missing_slots : list[str]
            Names of chemical properties that are still missing.
        
        Examples
        --------
        >>> from thermosteam import Chemical
        >>> Substance = Chemical.blank('Substance')
        >>> missing_slots = Substance.default()
        >>> sorted(missing_slots)
        ['Dortmund', 'Hfus', 'Hsub', 'Hvap', 'InChI', 'InChI_key', 'PSRK', 'Pc', 'Psat', 'Pt', 'StielPolar', 'Tb', 'Tc', 'Tm', 'Tt', 'UNIFAC', 'V', 'Vc', 'Zc', 'combustion', 'common_name', 'dipole', 'eos', 'eos_1atm', 'formula', 'iscyclic_aliphatic', 'iupac_name', 'omega', 'pubchemid', 'similarity_variable', 'smiles']
        
        Note that missing slots does not include essential properties volume, heat capacity, and conductivity.
        
        """
        if not slots:
            slots = self.get_missing_slots(slots)   
        hasfield = hasattr
        # Default to Water property values
        if 'MW' in slots:
            self.MW = MW = 1
        else:
            MW = self.MW
        if 'sigma' in slots:
            self.sigma.add_model(0.072055)
        if 'mu' in slots:
            mu = self.mu
            if hasfield(mu, 'l'):
                mu.l.add_model(0.00091272)
            elif not mu:
                mu.add_model(0.00091272)
        if 'V' in slots:
            V = self.V
            V_default = fn.rho_to_V(1050, MW)
            if hasfield(V, 'l'):
                V.l.add_model(V_default)
            elif not V:
                V.add_model(V_default)
        if 'kappa' in slots:
            kappa = self.kappa
            if hasfield(kappa, 'l'):
                kappa.l.add_model(0.5942)
            if not kappa:
                kappa.add_model(0.5942)
        if self.formula:
            if any([i in slots for i in ('HHV', 'LHV', 'combustion', 'Hf')]):
                if 'Hf' in slots:
                    method = 'Dulong'
                else:
                    method = 'Stoichiometry'
                CD = CombustionData.from_chemical_data(self.get_atoms(), self.CAS,
                                                       MW, self.Hf, method)
                if 'Hf' in slots:
                    self.Hf = CD.Hf
                if 'HHV' in slots:
                    self.HHV = CD.HHV
                if 'LHV' in slots:
                    self.LHV = CD.LHV
                if 'combustion' in slots:
                    self.combustion = CD.stoichiometry
        else:
            if 'LHV' in slots:
                self.LHV = 0
            if 'HHV' in slots:
                self.HHV = 0
            if 'combustion' in slots:
                self.combustion = ""
        if 'Hf' in slots:
            self.Hf = 0
        if 'epsilon' in slots:
            self.epsilon.add_model(0)
        if 'phase_ref' in slots:
            self.phase_ref = 'l'
        if 'eos' in slots:
            self.eos = GCEOS_DUMMY(T=298.15, P=101325.)
            self.eos_1atm = self.eos.to_TP(298.15, 101325)
        if 'Cn' in slots:
            MW = self.MW
            Cn = self.Cn
            phase_ref = self.phase_ref
            getfield = getattr
            single_phase = isinstance(Cn, TDependentModelHandle)
            if single_phase:
                Cn.add_model(4.18*MW)
                Cn_phase = Cn
            else:
                Cn_phase = getfield(Cn, phase_ref)
                Cn_phase.add_model(4.18*MW)
            self.load_free_energies()
        if not self.H:
            self.load_free_energies()
        missing = set(slots)
        missing.difference_update({'MW', 'CAS', 'Cn', 'Hf', 'sigma',
                                   'mu', 'kappa', 'LHV', 'HHV', 'epsilon', 'H',
                                   'S', 'H_excess', 'S_excess', 'phase_ref'})
        return missing
    
    def load_free_energies(self):
        """Load the `H`, `S`, `H_excess`, and `S_excess` functors."""
        Cn = self.Cn
        single_phase = isinstance(Cn, TDependentModelHandle)
        if not self.eos:
            self.eos = GCEOS_DUMMY(T=298.15, P=101325.)
            self.eos_1atm = self.eos.to_TP(298.15, 101325)
        self._init_energies(Cn, self.Hvap, self.Psat, self.Hfus, self.Tm,
                            self.Tb, self.eos, self.eos_1atm, self.phase_ref,
                            single_phase and self.phase_ref)
    
    def get_missing_slots(self, slots=None):
        """
        Return a list all missing thermodynamic properties.
        
        Examples
        --------
        >>> from thermosteam import Chemical
        >>> Substance = Chemical.blank('Substance', phase_ref='l')
        >>> Substance.get_missing_slots()
        ['eos', 'eos_1atm', 'InChI', 'InChI_key', 'common_name', 'iupac_name', 'pubchemid', 'smiles', 'formula', 'Dortmund', 'UNIFAC', 'PSRK', 'combustion', 'S_excess', 'H_excess', 'mu', 'kappa', 'V', 'S', 'H', 'Cn', 'Psat', 'Hvap', 'sigma', 'epsilon', 'MW', 'Tm', 'Tb', 'Tt', 'Tc', 'Pt', 'Pc', 'Vc', 'Zc', 'Hf', 'LHV', 'HHV', 'Hfus', 'Hsub', 'omega', 'dipole', 'StielPolar', 'similarity_variable', 'iscyclic_aliphatic']
        
        """
        getfield = getattr
        return [i for i in (slots or _checked_slots) if not getfield(self, i)]
    
    def copy_missing_slots_from(self, *sources, slots=None, default=True):
        """Copy the missing thermodynamic properties by copying from sources. Also return any names of thermodynamic properties that are still missing."""
        missing = slots if slots else self.get_missing_slots(slots)
        for source in sources:
            missing = fill(self, source, missing)
        if default:
            missing = self.default(missing)
        phase = self.locked_state
        if phase: lock_phase(self, phase)
        return missing
    
    @classmethod
    def blank(cls, ID, CAS=None, phase_ref=None, phase=None, **data):
        """
        Return a new Chemical object without any thermodynamic models or data (unless provided).

        Parameters
        ----------
        ID : str
            Chemical identifier.
        CAS : str, optional
            CAS number. If none provide, it defaults to the `ID`.
        phase_ref : str, optional
            Phase at the reference state (T=298.15, P=101325).
        phase : str, optional
            Phase to set state as a single phase chemical.
        **data : 
            Any data to fill chemical with.
        
        Examples
        --------
        >>> from thermosteam import Chemical
        >>> Substance = Chemical.blank('Substance')
        >>> Substance.show()
        Chemical: Substance (phase_ref=None)
        [Names]  CAS: Substance
                 InChI: None
                 InChI_key: None
                 common_name: None
                 iupac_name: None
                 pubchemid: None
                 smiles: None
                 formula: None
        [Groups] Dortmund: <Empty>
                 UNIFAC: <Empty>
                 PSRK: <Empty>
        [Thermo] S_excess: None
                 H_excess: None
                 mu(phase, T, P) -> Pa*s
                 kappa(phase, T, P) -> W/m/K
                 V(phase, T, P) -> m^3/mol
                 S: None
                 H: None
                 Cn(phase, T, P=None) -> J/mol/K
                 Psat(T, P=None) -> Pa
                 Hvap(T, P=None) -> J/mol
                 sigma(T, P=None) -> N/m
                 epsilon(T, P=None)
        [Data]   MW: None
                 Tm: None
                 Tb: None
                 Tt: None
                 Tc: None
                 Pt: None
                 Pc: None
                 Vc: None
                 Zc: None
                 Hf: None
                 LHV: None
                 HHV: None
                 Hfus: None
                 Hsub: None
                 omega: None
                 dipole: None
                 StielPolar: None
                 similarity_variable: None
                 iscyclic_aliphatic: None
        
        """
        self = super().__new__(cls)
        self.eos = self.eos_1atm = None
        setfield = setattr
        self.UNIFAC = UNIFACGroupCounts()
        self.Dortmund = DortmundGroupCounts()
        self.PSRK = PSRKGroupCounts()
        for i in _names: setfield(self, i, None)
        for i in _reactions: setfield(self, i, None)
        for i in _data: setfield(self, i, None)
        for i in _free_energies: setfield(self, i, None)
        if phase:
            for i in ('kappa', 'mu', 'V'):
                setfield(self, i, TPDependentModelHandle(i))
            self.Cn = TDependentModelHandle('Cn')
        else:
            for i in ('kappa', 'mu', 'V'):
                setfield(self, i, PhaseTPProperty(i))
            self.Cn = PhaseTProperty('Cn')
        for i in ('sigma', 'epsilon', 'Psat', 'Hvap'):
            setfield(self, i, TDependentModelHandle(i))
        self._locked_state = phase
        self._ID = ID
        self.phase_ref = phase_ref or phase
        self._CAS = CAS or ID
        for i,j in data.items(): setfield(self, i , j)
        return self
    
    def get_phase(self, T=298.15, P=101325.):
        """Return phase of chemical at given thermal condition.
        
        Examples
        --------
        >>> from thermosteam import Chemical
        >>> Water = Chemical('Water')
        >>> Water.get_phase(T=400, P=101325)
        'g'
        """
        if self._locked_state: return self._locked_state
        if self.Tm and T <= self.Tm: return 's'
        if self.Psat and P <= self.Psat(T): return 'g'
        else: return 'l'
    
    @property
    def locked_state(self):
        """[str] Constant phase of chemical."""
        return self._locked_state
    
    def at_state(self, phase=None, copy=False):
        """
        Set the state of chemical.
        
        Examples
        --------
        >>> from thermosteam import Chemical
        >>> N2 = Chemical('N2')
        >>> N2.at_state(phase='g')
        >>> N2.show() # Note how all models are not a function of phase anymore
        Chemical: N2 (phase_ref='g') at phase='g'
        [Names]  CAS: 7727-37-9
                 InChI: N2/c1-2
                 InChI_key: IJGRMHOSHXDMSA-U...
                 common_name: nitrogen
                 iupac_name: molecular nitro...
                 pubchemid: 947
                 smiles: N#N
                 formula: N2
        [Groups] Dortmund: <Empty>
                 UNIFAC: <Empty>
                 PSRK: <Empty>
        [Thermo] S_excess(T, P) -> J/mol
                 H_excess(T, P) -> J/mol
                 mu(T, P) -> Pa*s
                 kappa(T, P) -> W/m/K
                 V(T, P) -> m^3/mol
                 S(T, P) -> J/mol
                 H(T, P=None) -> J/mol
                 Cn(T, P=None) -> J/mol/K
                 Psat(T, P=None) -> Pa
                 Hvap(T, P=None) -> J/mol
                 sigma(T, P=None) -> N/m
                 epsilon(T, P=None)
        [Data]   MW: 28.013 g/mol
                 Tm: 63.15 K
                 Tb: 77.355 K
                 Tt: 63.15 K
                 Tc: 126.2 K
                 Pt: 12527 Pa
                 Pc: 3.3944e+06 Pa
                 Vc: 8.95e-05 m^3/mol
                 Zc: 0.28953
                 Hf: None
                 LHV: 0
                 HHV: 0
                 Hfus: 710 J/mol
                 Hsub: None
                 omega: 0.04
                 dipole: 0 Debye
                 StielPolar: None
                 similarity_variable: 0.071394
                 iscyclic_aliphatic: 0
        
        """
        if copy:
            new = self.copy(self.ID, self.CAS)
            new.at_state(phase)
            return new
        locked_state = self.locked_state
        if locked_state:
            if locked_state != phase:
                raise TypeError(f"{self}'s state is already locked")   
            else:
                return         
        elif phase:
            lock_phase(self, phase)
        else:
            raise ValueError(f"invalid phase {repr(phase)}")
    
    def show(self):
        """Print all specifications"""
        getfield = getattr
        info = chemical_identity(self, pretty=True)
        for header, fields in _chemical_fields.items():
            section = []
            for field in fields:
                value = getfield(self, field)
                field = field.lstrip('_')
                if value is None:
                    line = f"{field}: None"
                if callable(value):
                    line = f"{display_asfunctor(value, name=field, var=field, show_var=False)}"
                else:
                    if isinstance(value, (int, float)):
                        line = f"{field}: {value:.5g}"
                        units = chemical_units_of_measure.get(field, "")
                        if units: line += f' {units}'
                    else:
                        value = str(value)
                        line = f"{field}: {value}"
                        if len(line) > 27: line = line[:27] + '...'
                section.append(line)
            if section:
                info += header + ("\n" + 9*" ").join(section)
        print(info)
        
    _ipython_display_ = show
    
    def __str__(self):
        return self.ID
    
    def __repr__(self):
        return f"Chemical('{self}')"
    
def lock_phase(chemical, phase):
    getfield = getattr
    setfield = setattr
    hasfield = hasattr
    for field in _phase_properties:
        phase_property = getfield(chemical, field)
        if hasfield(phase_property, phase):
            model_handle = getfield(phase_property, phase)
            setfield(chemical, field, model_handle)
    for field in _free_energies:
        phase_property = getfield(chemical, field)
        if hasfield(phase_property, phase):
            functor = getfield(phase_property, phase)
            setfield(chemical, field, functor)
    chemical._locked_state = phase

# # Fire Safety Limits
# self.Tflash = Tflash(CAS)
# self.Tautoignition = Tautoignition(CAS)
# self.LFL = LFL(CASRN=CAS, atoms=self.atoms, Hc=self.Hc)
# self.UFL = UFL(CASRN=CAS, atoms=self.atoms, Hc=self.Hc)

# # Chemical Exposure Limits
# self.TWA = TWA(CASRN=CAS)
# self.STEL = STEL(CASRN=CAS)
# self.Ceiling = Ceiling(CASRN=CAS)
# self.Skin = Skin(CASRN=CAS)
# self.Carcinogen = Carcinogen(CASRN=CAS)

# # Misc
# self.dipole = dipole(CASRN=CAS) # Units of Debye
# self.Stockmayer = Stockmayer(CASRN=CAS, Tm=self.Tm, Tb=self.Tb, Tc=self.Tc,
#                               Zc=self.Zc, omega=self.omega)

# # Environmental
# self.GWP = GWP(CASRN=CAS)
# self.ODP = ODP(CASRN=CAS)
# self.logP = logP(CASRN=CAS)

# # Analytical
# self.RI, self.RIT = refractive_index(CASRN=CAS)
# self.conductivity, self.conductivityT = conductivity(CASRN=CAS)
    